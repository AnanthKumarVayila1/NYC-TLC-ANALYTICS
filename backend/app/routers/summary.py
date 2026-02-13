from fastapi import APIRouter, Depends, HTTPException, Query, Response
from typing import Optional
from datetime import date
from app.database import db
from app.models import ServiceType, User, SummaryStats
from app.auth import get_current_active_user

router = APIRouter(
    prefix="/api/summary",
    tags=["summary"],
    dependencies=[Depends(get_current_active_user)]
)

# Simple cache
summary_cache = {}
MAX_CACHE_SIZE = 50

@router.get("", response_model=SummaryStats)
async def get_summary_stats(
    response: Response,
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    service_type: Optional[ServiceType] = Query(None, description="Filter by service type"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get summary statistics for the dashboard cards.
    Provides aggregated metrics across the selected date range.
    """
    print(f"DEBUG SUMMARY ROUTER: start_date={start_date}, end_date={end_date}, service_type={service_type}")
    
    # Validate date range
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    
    # Add cache headers (5 minutes)
    response.headers["Cache-Control"] = "private, max-age=300"
    
    # Check cache
    cache_key = f"summary:{start_date}:{end_date}:{service_type.value if service_type else None}"
    if cache_key in summary_cache:
        return summary_cache[cache_key]
    
    # Build query
    where_clauses = ["metric_date BETWEEN ? AND ?"]
    params = [start_date, end_date]
    
    if service_type:
        where_clauses.append("service_type = ?")
        params.append(service_type.value)
    
    where_sql = " AND ".join(where_clauses)
    
    print(f"DEBUG: where_sql = {where_sql}")
    print(f"DEBUG: params = {params}")
    
    # Get overall summary
    summary_query = f"""
        SELECT 
            SUM(total_trips) as total_trips,
            SUM(total_revenue) as total_revenue,
            AVG(avg_trip_distance) as avg_distance,
            AVG(avg_trip_duration_sec) as avg_duration_sec,
            AVG(avg_fare_amount) as avg_fare
        FROM agg_daily_metrics
        WHERE {where_sql}
    """
    
    print(f"DEBUG: About to execute summary_query")
    summary_result = db.execute_query(summary_query, tuple(params))
    print(f"DEBUG: summary_result = {summary_result}")
    summary = summary_result[0] if summary_result else {}
    
    print(f"DEBUG: summary dict keys = {summary.keys()}")
    print(f"DEBUG: avg_distance from summary = {summary.get('avg_distance')}")
    print(f"DEBUG: avg_duration_sec from summary = {summary.get('avg_duration_sec')}")
    print(f"DEBUG: avg_fare from summary = {summary.get('avg_fare')}")
    
    # Get by service type
    service_query = f"""
        SELECT 
            service_type,
            SUM(total_trips) as total_trips,
            SUM(total_revenue) as total_revenue
        FROM agg_daily_metrics
        WHERE {where_sql}
        GROUP BY service_type
        ORDER BY total_trips DESC
    """
    
    by_service = db.execute_query(service_query, tuple(params))
    
    # Skip borough query for performance - fact_trips table is too large (159.5M records)
    # This was causing timeouts
    
    avg_dist = round(float(summary.get('avg_distance', 0) or 0), 2)
    avg_dur_sec = float(summary.get('avg_duration_sec', 0) or 0)
    avg_dur_min = round(avg_dur_sec / 60, 1)
    avg_fa = round(float(summary.get('avg_fare', 0) or 0), 2)
    
    print(f"DEBUG: Calculated values: avg_dist={avg_dist}, avg_dur_min={avg_dur_min}, avg_fa={avg_fa}")
    
    result = SummaryStats(
        total_trips=int(summary.get('total_trips', 0) or 0),
        total_revenue=float(summary.get('total_revenue', 0) or 0),
        avg_distance=avg_dist,
        avg_duration_minutes=avg_dur_min,
        avg_fare=avg_fa,
        by_service_type=[dict(row) for row in by_service],
        by_borough=[]  # Empty for performance
    )
    
    # Cache result
    if len(summary_cache) >= MAX_CACHE_SIZE:
        summary_cache.pop(next(iter(summary_cache)))
    summary_cache[cache_key] = result
    
    return result
