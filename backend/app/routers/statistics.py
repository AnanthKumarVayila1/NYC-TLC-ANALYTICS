from fastapi import APIRouter, Depends
from typing import List
from app.database import db
from app.models import StatisticsResponse, ServiceTypeStats, User
from app.auth import get_current_active_user

router = APIRouter(
    prefix="/api/statistics",
    tags=["statistics"],
    dependencies=[Depends(get_current_active_user)]
)

@router.get("", response_model=StatisticsResponse)
async def get_statistics(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get overall statistics for all taxi trip data.
    """
    
    # Overall statistics
    overall_query = """
        SELECT 
            COUNT(*) as total_trips,
            COALESCE(SUM(total_amount), 0) as total_revenue,
            MIN(pickup_date) as start_date,
            MAX(pickup_date) as end_date
        FROM fact_trip
        WHERE is_valid = 1
    """
    overall_result = db.execute_query(overall_query)[0]
    
    # Statistics by service type
    by_service_query = """
        SELECT 
            service_type,
            COUNT(*) as total_trips,
            SUM(CASE WHEN is_valid = 1 THEN 1 ELSE 0 END) as valid_trips,
            CAST(SUM(CASE WHEN is_valid = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as data_quality_pct,
            COALESCE(SUM(CASE WHEN is_valid = 1 THEN total_amount ELSE 0 END), 0) as total_revenue
        FROM fact_trip
        GROUP BY service_type
        ORDER BY service_type
    """
    by_service_results = db.execute_query(by_service_query)
    
    service_stats = [ServiceTypeStats(**row) for row in by_service_results]
    
    return StatisticsResponse(
        total_trips=overall_result['total_trips'],
        total_revenue=float(overall_result['total_revenue']),
        date_range={
            "start": overall_result['start_date'].isoformat(),
            "end": overall_result['end_date'].isoformat()
        },
        by_service_type=service_stats
    )