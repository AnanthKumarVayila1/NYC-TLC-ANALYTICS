from fastapi import APIRouter, Depends, HTTPException, Query, Response
from typing import Optional
from datetime import date
import math
import hashlib
import json
from functools import lru_cache
from app.database import db
from app.models import (
    DailyAggregatesResponse, 
    DailyAggregate, 
    PaginationResponse,
    ServiceType,
    User,
    SummaryStats
)
from app.auth import get_current_active_user

router = APIRouter(
    prefix="/api/aggregates",
    tags=["aggregates"],
    dependencies=[Depends(get_current_active_user)]
)

# Simple in-memory cache for aggregate queries
aggregate_cache = {}
MAX_CACHE_SIZE = 100

def get_cache_key(start_date: date, end_date: date, service_type: Optional[str]) -> str:
    """Generate cache key for aggregate queries"""
    return hashlib.md5(f"{start_date}:{end_date}:{service_type}".encode()).hexdigest()

@router.get("/daily", response_model=DailyAggregatesResponse)
async def get_daily_aggregates(
    response: Response,
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    service_type: Optional[ServiceType] = Query(None, description="Filter by service type"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(100, ge=1, le=10000, description="Items per page"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get daily aggregated metrics for NYC taxi trips.
    
    Returns:
    - total_trips: Number of trips per day
    - total_revenue: Total revenue per day
    - avg_trip_distance: Average trip distance
    - avg_trip_duration_sec: Average trip duration in seconds
    - avg_fare_amount: Average fare amount
    """
    
    # Validate date range
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    
    # Add cache headers (5 minutes for aggregates)
    response.headers["Cache-Control"] = "private, max-age=300"
    
    # Check cache
    cache_key = get_cache_key(start_date, end_date, service_type.value if service_type else None)
    cache_entry_key = f"{cache_key}:{page}:{page_size}"
    
    if cache_entry_key in aggregate_cache:
        return aggregate_cache[cache_entry_key]
    
    # Build query
    where_clauses = ["metric_date BETWEEN ? AND ?"]
    params = [start_date, end_date]
    
    if service_type:
        where_clauses.append("service_type = ?")
        params.append(service_type.value)
    
    where_sql = " AND ".join(where_clauses)
    
    # Get total count
    count_query = f"""
        SELECT COUNT(*) 
        FROM agg_daily_metrics 
        WHERE {where_sql}
    """
    total_records = db.execute_scalar(count_query, tuple(params))
    
    if total_records == 0:
        return DailyAggregatesResponse(
            data=[],
            pagination=PaginationResponse(
                page=page,
                page_size=page_size,
                total_records=0,
                total_pages=0
            )
        )
    
    # Calculate pagination
    total_pages = math.ceil(total_records / page_size)
    offset = (page - 1) * page_size
    
    # Get paginated data
    data_query = f"""
        SELECT 
            metric_date,
            service_type,
            total_trips,
            total_revenue,
            avg_trip_distance,
            avg_trip_duration_sec,
            avg_fare_amount
        FROM agg_daily_metrics
        WHERE {where_sql}
        ORDER BY metric_date DESC, service_type
        OFFSET ? ROWS
        FETCH NEXT ? ROWS ONLY
    """
    
    results = db.execute_query(data_query, tuple(params + [offset, page_size]))
    
    # Convert to response model
    aggregates = [DailyAggregate(**row) for row in results]
    
    result = DailyAggregatesResponse(
        data=aggregates,
        pagination=PaginationResponse(
            page=page,
            page_size=page_size,
            total_records=total_records,
            total_pages=total_pages
        )
    )
    
    # Store in cache (limit cache size)
    if len(aggregate_cache) >= MAX_CACHE_SIZE:
        # Remove oldest entry
        aggregate_cache.pop(next(iter(aggregate_cache)))
    aggregate_cache[cache_entry_key] = result
    
    return result