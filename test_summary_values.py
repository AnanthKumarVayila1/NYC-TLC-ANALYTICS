#!/usr/bin/env python3
"""Test summary endpoint to debug avg_distance, avg_duration, avg_fare values"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Step 1: Login
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"username": "admin", "password": "secret"}
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.text}")
    exit(1)

token = login_response.json()["access_token"]
print(f"✅ Login successful, token: {token[:20]}...")

# Step 2: Call summary endpoint
headers = {"Authorization": f"Bearer {token}"}

summary_response = requests.get(
    f"{BASE_URL}/api/summary",
    params={
        "start_date": "2024-10-01",
        "end_date": "2024-12-31"
    },
    headers=headers
)

print(f"\n📊 Summary Response (Status: {summary_response.status_code}):")
summary = summary_response.json()
print(json.dumps(summary, indent=2))

print(f"\n🔍 Key Fields:")
print(f"   total_trips: {summary.get('total_trips')}")
print(f"   total_revenue: {summary.get('total_revenue')}")
print(f"   avg_distance: {summary.get('avg_distance')}")
print(f"   avg_duration_minutes: {summary.get('avg_duration_minutes')}")
print(f"   avg_fare: {summary.get('avg_fare')}")
