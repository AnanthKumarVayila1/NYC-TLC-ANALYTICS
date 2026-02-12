#!/usr/bin/env python3
"""
Development Server - Lightweight backend without database dependency
For testing purposes when ODBC is not available
"""
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
import json

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class TripData(BaseModel):
    trip_id: int
    pickup_datetime: str
    dropoff_datetime: str
    pickup_location: str
    dropoff_location: str
    distance: float
    fare: float

class Summary(BaseModel):
    total_trips: int
    total_revenue: float
    average_fare: float
    date_range: str

# Create FastAPI app
app = FastAPI(
    title="NYC TLC Analytics API (Dev Mode)",
    version="1.0.0",
    description="Development mode - Mock data only, database not connected"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "mode": "development"}

# Authentication endpoint (mock)
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible token login (mock)"""
    if form_data.username == "admin" and form_data.password == "secret":
        return {
            "access_token": "dev-token-" + form_data.username,
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials (default: admin/secret)",
    )

# Mock endpoints
@app.get("/api/trips", response_model=List[TripData])
async def get_trips(skip: int = 0, limit: int = 10):
    """Get mock trip data"""
    mock_trips = [
        {
            "trip_id": i,
            "pickup_datetime": "2024-01-01T10:00:00",
            "dropoff_datetime": "2024-01-01T10:45:00",
            "pickup_location": "Manhattan",
            "dropoff_location": "Brooklyn",
            "distance": 5.2 + i * 0.1,
            "fare": 15.50 + i * 2
        }
        for i in range(skip, skip + limit)
    ]
    return mock_trips

@app.get("/api/summary", response_model=Summary)
async def get_summary():
    """Get mock summary data"""
    return {
        "total_trips": 2543,
        "total_revenue": 145230.50,
        "average_fare": 57.12,
        "date_range": "2024-01-01 to 2024-12-31"
    }

@app.get("/api/statistics")
async def get_statistics():
    """Get mock statistics"""
    return {
        "peak_hours": [8, 9, 17, 18, 19],
        "popular_routes": [
            {"from": "Manhattan", "to": "Brooklyn", "count": 456},
            {"from": "Manhattan", "to": "Queens", "count": 389},
            {"from": "Brooklyn", "to": "Manhattan", "count": 412}
        ],
        "average_trip_duration": 28.5,
        "average_distance": 4.8
    }

@app.get("/api/aggregates")
async def get_aggregates():
    """Get mock aggregated data"""
    return {
        "daily_average": {
            "trips": 234,
            "revenue": 1345.60
        },
        "hourly_distribution": {
            f"{h:02d}:00": 85 + (h % 12) * 5
            for h in range(24)
        }
    }

@app.get("/docs", include_in_schema=False)
async def custom_swagger():
    """Swagger UI"""
    return {"message": "API Documentation available at /docs"}

def main():
    """Start the server"""
    print("=" * 70)
    print("  🚀 NYC TLC ANALYTICS BACKEND (Development Mode)")
    print("=" * 70)
    print()
    print("Server will start on: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print()
    print("Note: Running in development mode with mock data")
    print("Database connection not available (ODBC not installed)")
    print()
    print("Default credentials:")
    print("  Username: admin")
    print("  Password: secret")
    print()
    print("Available endpoints:")
    print("  GET  /health - Health check")
    print("  POST /token - Get auth token")
    print("  GET  /api/trips - Mock trip data")
    print("  GET  /api/summary - Mock summary")
    print("  GET  /api/statistics - Mock statistics")
    print("  GET  /api/aggregates - Mock aggregates")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 70)
    print()
    
    uvicorn.run(
        "dev_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )

if __name__ == "__main__":
    main()
