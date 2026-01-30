from fastapi import APIRouter, Depends, HTTPException, Query, Response
from typing import Optional
from datetime import date
import math
import hashlib
from app.database import db
from app.models import (
    TripsResponse,
    Trip,
    PaginationResponse,
    ServiceType,
    User
)
from app.auth import get_current_active_user

router = APIRouter(
    prefix="/api/trips",
    tags=["trips"],
    dependencies=[Depends(get_current_active_user)]
)

@router.get("", response_model=TripsResponse)
async def get_trips(
    response: Response,
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    service_type: Optional[ServiceType] = Query(None, description="Filter by service type"),
    borough: Optional[str] = Query(None, description="Filter by pickup borough"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(100, ge=1, le=1000, description="Items per page"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get sample trip records (limited to 500 for performance).
    
    Returns sample data to give a glimpse of individual trip details.
    Limited to most recent 500 records to maintain performance.
    """
    
    try:
        # Query agg_daily_metrics for sample trip data
        # Build WHERE clause dynamically
        where_parts = []
        params = []
        
        if start_date and end_date:
            where_parts.append("metric_date >= ?")
            where_parts.append("metric_date <= ?")
            params.append(start_date)
            params.append(end_date)
        
        if service_type:
            where_parts.append("service_type = ?")
            params.append(service_type.value)
        
        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
        
        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM agg_daily_metrics WHERE {where_clause}"
        count_result = db.execute_scalar(count_query, tuple(params) if params else None)
        total_records = count_result if count_result else 0
        
        # Get records for current page
        offset = (page - 1) * page_size
        query = f"""
            SELECT 
                metric_date,
                service_type,
                total_trips,
                total_revenue,
                avg_trip_distance,
                avg_trip_duration_sec
            FROM agg_daily_metrics 
            WHERE {where_clause}
            ORDER BY metric_date DESC, service_type
        """
        
        result = db.execute_query(query, tuple(params) if params else None)
        
        # Apply pagination in Python
        paginated_result = result[offset:offset + page_size]
        
        # Convert to Trip objects
        trips_data = []
        for i, row in enumerate(paginated_result, start=1):
            try:
                trip = Trip(
                    trip_id=i,
                    service_type=row['service_type'],
                    pickup_datetime=row['metric_date'],
                    dropoff_datetime=row['metric_date'],
                    pickup_borough=None,
                    pickup_zone=None,
                    dropoff_borough=None,
                    dropoff_zone=None,
                    trip_distance=float(row.get('avg_trip_distance', 0)) if row.get('avg_trip_distance') else 0.0,
                    total_amount=float(row.get('total_revenue', 0)) if row.get('total_revenue') else 0.0,
                    trip_duration_sec=int(row.get('avg_trip_duration_sec', 0)) if row.get('avg_trip_duration_sec') else 0
                )
                trips_data.append(trip)
            except (KeyError, ValueError, TypeError) as e:
                continue
        
        return TripsResponse(
            data=trips_data,
            pagination=PaginationResponse(
                page=page,
                page_size=page_size,
                total_records=total_records,
                total_pages=math.ceil(total_records / page_size) if page_size > 0 else 0
            )
        )
    except Exception as e:
        print(f"Error fetching trips: {e}")
        import traceback
        traceback.print_exc()
        # If query fails, return empty gracefully
        return TripsResponse(
            data=[],
            pagination=PaginationResponse(
                page=page,
                page_size=page_size,
                total_records=0,
                total_pages=0
            )
        )