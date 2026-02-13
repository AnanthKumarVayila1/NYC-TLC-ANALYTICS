#!/usr/bin/env python3
"""Test summary endpoint"""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Login
login_response = client.post(
    "/api/auth/login",
    json={"username": "admin", "password": "secret"}
)
print(f"Login response: {login_response.status_code}")
token = login_response.json()["access_token"]
print(f"Token: {token[:30]}...")

# Call summary endpoint
response = client.get(
    "/api/summary",
    params={
        "start_date": "2024-10-01",
        "end_date": "2024-12-31"
    },
    headers={"Authorization": f"Bearer {token}"}
)

print(f"\nSummary response status: {response.status_code}")
result = response.json()
print(f"\nSummary fields:")
print(f"  total_trips: {result.get('total_trips')}")
print(f"  total_revenue: {result.get('total_revenue')}")
print(f"  avg_distance: {result.get('avg_distance')}")
print(f"  avg_duration_minutes: {result.get('avg_duration_minutes')}")
print(f"  avg_fare: {result.get('avg_fare')}")
