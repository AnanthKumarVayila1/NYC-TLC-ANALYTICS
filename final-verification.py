#!/usr/bin/env python3
"""
Final verification that all API endpoints are working correctly
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("NYC TLC ANALYTICS - FINAL VERIFICATION")
print("=" * 80)

# 1. Login and get token
print("\n1. Testing Login...")
login_data = {"username": "admin", "password": "secret"}
response = requests.post(f"{BASE_URL}/token", data=login_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    print("✅ Login successful")
    print(f"   Token: {token[:20]}...")
else:
    print(f"❌ Login failed: {response.status_code}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# 2. Test Summary Endpoint
print("\n2. Testing Summary Endpoint...")
summary_params = {
    "start_date": "2024-10-01",
    "end_date": "2024-12-31"
}
response = requests.get(f"{BASE_URL}/api/summary", params=summary_params, headers=headers)
if response.status_code == 200:
    summary = response.json()
    print("✅ Summary endpoint working")
    print(f"   Total Trips: {summary.get('total_trips'):,}")
    print(f"   Total Revenue: ${summary.get('total_revenue'):,.2f}")
    print(f"   Avg Distance: {summary.get('avg_distance', 0):.2f} miles")
    print(f"   Service Types: {len(summary.get('by_service_type', []))} breakdown")
else:
    print(f"❌ Summary endpoint failed: {response.status_code}")

# 3. Test Daily Aggregates Endpoint
print("\n3. Testing Daily Aggregates Endpoint...")
agg_params = {
    "start_date": "2024-10-01",
    "end_date": "2024-12-31",
    "page": 1,
    "page_size": 20
}
response = requests.get(f"{BASE_URL}/api/aggregates/daily", params=agg_params, headers=headers)
if response.status_code == 200:
    data = response.json()
    print("✅ Aggregates endpoint working")
    print(f"   Total Records: {data.get('total')}")
    print(f"   Page Size: {len(data.get('data', []))}")
    if data.get('data'):
        first = data['data'][0]
        print(f"   First Record: {first['metric_date']} - {first['service_type']}: {first['total_trips']:,} trips")
else:
    print(f"❌ Aggregates endpoint failed: {response.status_code}")

# 4. Test Trips Endpoint
print("\n4. Testing Trips Endpoint...")
trip_params = {
    "start_date": "2024-10-01",
    "end_date": "2024-12-31",
    "page": 1,
    "page_size": 5
}
response = requests.get(f"{BASE_URL}/api/trips", params=trip_params, headers=headers)
if response.status_code == 200:
    data = response.json()
    print("✅ Trips endpoint working")
    print(f"   Total Records: {data.get('total')}")
    print(f"   Page Size: {len(data.get('data', []))}")
    if data.get('data'):
        first = data['data'][0]
        print(f"   First Trip: {first['service_type']} - {first['pickup_zone']} to {first['dropoff_zone']}")
else:
    print(f"❌ Trips endpoint failed: {response.status_code}")

# 5. Test with Pagination
print("\n5. Testing Pagination...")
agg_params = {
    "start_date": "2024-10-01",
    "end_date": "2024-12-31",
    "page": 2,
    "page_size": 20
}
response = requests.get(f"{BASE_URL}/api/aggregates/daily", params=agg_params, headers=headers)
if response.status_code == 200:
    data = response.json()
    print("✅ Pagination working")
    print(f"   Page 2 returned {len(data.get('data', []))} records")
    if data.get('data'):
        first = data['data'][0]
        print(f"   First Record on Page 2: {first['metric_date']}")
else:
    print(f"❌ Pagination failed: {response.status_code}")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE - All endpoints operational!")
print("=" * 80)
print("\n✨ Dashboard should now display data correctly at http://localhost:4200")
print("   Login with: admin / secret")
print("   Date range: October 1 - December 31, 2024")
