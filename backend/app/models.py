from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class ServiceType(str, Enum):
    YELLOW = "yellow"
    GREEN = "green"
    FHV = "fhv"
    FHVHV = "fhvhv"

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=100, ge=1, le=1000, description="Items per page")

class PaginationResponse(BaseModel):
    page: int
    page_size: int
    total_records: int
    total_pages: int

class DailyAggregate(BaseModel):
    metric_date: date
    service_type: str
    total_trips: int
    total_revenue: float
    avg_trip_distance: Optional[float]
    avg_trip_duration_sec: Optional[float]
    avg_fare_amount: Optional[float]

class DailyAggregatesResponse(BaseModel):
    data: List[DailyAggregate]
    pagination: PaginationResponse

class Trip(BaseModel):
    trip_id: int
    service_type: str
    pickup_datetime: datetime
    dropoff_datetime: datetime
    pickup_borough: Optional[str]
    pickup_zone: Optional[str]
    dropoff_borough: Optional[str]
    dropoff_zone: Optional[str]
    trip_distance: Optional[float]
    total_amount: Optional[float]
    trip_duration_sec: Optional[int]

class TripsResponse(BaseModel):
    data: List[Trip]
    pagination: PaginationResponse

class ServiceTypeStats(BaseModel):
    service_type: str
    total_trips: int
    valid_trips: int
    data_quality_pct: float
    total_revenue: float

class StatisticsResponse(BaseModel):
    total_trips: int
    total_revenue: float
    date_range: dict
    by_service_type: List[ServiceTypeStats]

class SummaryStats(BaseModel):
    total_trips: int
    total_revenue: float
    avg_distance: float
    avg_duration_minutes: float
    avg_fare: float
    by_service_type: List[dict]
    by_borough: List[dict]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str