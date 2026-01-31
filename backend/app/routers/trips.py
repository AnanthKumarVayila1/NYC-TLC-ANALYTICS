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
    Get trip records from fact_trip_sample table (sample data of 1 lakh records per service type).
    
    Returns individual trip details with all available fields.
    Supports filtering by date range, service type, and pickup borough.
    """
    
    try:
        # Query fact_trip_sample for individual trip records
        where_parts = []
        params = []
        
        if start_date and end_date:
            where_parts.append("CAST(pickup_date AS DATE) >= ?")
            where_parts.append("CAST(pickup_date AS DATE) <= ?")
            params.append(start_date)
            params.append(end_date)
        
        if service_type:
            where_parts.append("service_type = ?")
            params.append(service_type.value)
        
        if borough:
            where_parts.append("pickup_borough = ?")
            params.append(borough)
        
        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
        
        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM fact_trip_sample WHERE {where_clause}"
        count_result = db.execute_scalar(count_query, tuple(params) if params else None)
        total_records = count_result if count_result else 0
        
        # Get records for current page
        offset = (page - 1) * page_size
        query = f"""
            SELECT 
                trip_id,
                service_type,
                pickup_datetime,
                dropoff_datetime,
                pickup_location_id,
                dropoff_location_id,
                pickup_borough,
                pickup_zone,
                dropoff_borough,
                dropoff_zone,
                trip_distance,
                total_amount,
                trip_duration_sec,
                pickup_date,
                is_valid,
                created_at
            FROM fact_trip_sample 
            WHERE {where_clause}
            ORDER BY pickup_datetime DESC
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        """
        
        # Add pagination params
        params.append(offset)
        params.append(page_size)
        
        result = db.execute_query(query, tuple(params) if params else None)
        
        # Convert to Trip objects
        trips_data = []
        for row in result:
            try:
                trip = Trip(
                    trip_id=row['trip_id'],
                    service_type=row['service_type'],
                    pickup_datetime=row['pickup_datetime'],
                    dropoff_datetime=row['dropoff_datetime'],
                    pickup_borough=row.get('pickup_borough'),
                    pickup_zone=row.get('pickup_zone'),
                    dropoff_borough=row.get('dropoff_borough'),
                    dropoff_zone=row.get('dropoff_zone'),
                    trip_distance=float(row.get('trip_distance', 0)) if row.get('trip_distance') else 0.0,
                    total_amount=float(row.get('total_amount', 0)) if row.get('total_amount') else 0.0,
                    trip_duration_sec=int(row.get('trip_duration_sec', 0)) if row.get('trip_duration_sec') else 0
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