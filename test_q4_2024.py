#!/usr/bin/env python3
"""Test API with Q4 2024 dates"""
import urllib.request
import urllib.parse
import json

# Get token
auth_data = urllib.parse.urlencode({'username': 'admin', 'password': 'secret'}).encode()
with urllib.request.urlopen('http://localhost:8000/token', auth_data) as response:
    token = json.loads(response.read())['access_token']
    print(f"✅ Logged in\n")

headers = {'Authorization': f'Bearer {token}'}

print("=" * 70)
print("  Testing Q4 2024 date range (Oct 01 - Dec 31, 2024)")
print("=" * 70)

# Test summary for Q4 2024
params = urllib.parse.urlencode({
    'start_date': '2024-10-01',
    'end_date': '2024-12-31'
})
req = urllib.request.Request(
    f'http://localhost:8000/api/summary?{params}',
    headers=headers
)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    print(f"\n📈 Summary Statistics (Q4 2024):")
    print(f"   Total Trips: {data.get('total_trips', 0):,}")
    print(f"   Total Revenue: ${data.get('total_revenue', 0):,.2f}")
    print(f"   Avg Distance: {data.get('avg_distance', 0):.1f} mi")
    print(f"   Avg Duration: {data.get('avg_duration_minutes', 0):.0f} min")
    print(f"   Avg Fare: ${data.get('avg_fare', 0):.2f}")

# Test aggregates
params = urllib.parse.urlencode({
    'start_date': '2024-10-01',
    'end_date': '2024-12-31',
    'page': '1',
    'page_size': '20'
})
req = urllib.request.Request(
    f'http://localhost:8000/api/aggregates/daily?{params}',
    headers=headers
)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    records = data.get('data', [])
    pagination = data.get('pagination', {})
    print(f"\n📅 Daily Aggregates (Q4 2024):")
    print(f"   Total records: {pagination.get('total_records', 0)}")
    print(f"   Page 1 has: {len(records)} records")
    if records:
        print(f"   First record: {records[0].get('metric_date')} - {records[0].get('service_type')}: {records[0].get('total_trips', 0)} trips")
        print(f"   Last record: {records[-1].get('metric_date')} - {records[-1].get('service_type')}: {records[-1].get('total_trips', 0)} trips")

# Test trips
params = urllib.parse.urlencode({
    'start_date': '2024-10-01',
    'end_date': '2024-12-31',
    'page': '1',
    'page_size': '5'
})
req = urllib.request.Request(
    f'http://localhost:8000/api/trips?{params}',
    headers=headers
)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    records = data.get('data', [])
    pagination = data.get('pagination', {})
    print(f"\n🚕 Trip Records (Q4 2024):")
    print(f"   Total trips: {pagination.get('total_records', 0)}")
    print(f"   Page 1 has: {len(records)} records")
    if records:
        for trip in records[:3]:
            print(f"   - {trip.get('pickup_datetime')}: {trip.get('service_type')} - ${trip.get('total_amount', 0):.2f}")

print("\n" + "=" * 70)
print("  ✅ Expected results above! Data should now display on dashboard.")
print("=" * 70)
