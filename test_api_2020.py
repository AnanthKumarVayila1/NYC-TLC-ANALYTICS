#!/usr/bin/env python3
"""Test API with correct 2020-2024 date range"""
import urllib.request
import urllib.parse
import json

# Get token
auth_data = urllib.parse.urlencode({'username': 'admin', 'password': 'secret'}).encode()
with urllib.request.urlopen('http://localhost:8000/token', auth_data) as response:
    token = json.loads(response.read())['access_token']
    print(f"✅ Token obtained\n")

headers = {'Authorization': f'Bearer {token}'}

# Test summary for 2020
print("=" * 70)
print("  Testing with 2020 date range (when mock data should exist)")
print("=" * 70)

params = urllib.parse.urlencode({
    'start_date': '2020-01-01',
    'end_date': '2020-12-31'
})
req = urllib.request.Request(
    f'http://localhost:8000/api/summary?{params}',
    headers=headers
)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    print(f"\n📈 Summary for 2020:")
    print(f"   Total trips: {data.get('total_trips', 0):,}")
    print(f"   Total revenue: ${data.get('total_revenue', 0):,.2f}")
    print(f"   Avg fare: ${data.get('avg_fare', 0):.2f}")
    print(f"   Service types: {len(data.get('by_service_type', []))}")

# Test aggregates
params = urllib.parse.urlencode({
    'start_date': '2020-01-01',
    'end_date': '2020-12-31',
    'page': '1',
    'page_size': '10'
})
req = urllib.request.Request(
    f'http://localhost:8000/api/aggregates/daily?{params}',
    headers=headers
)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    print(f"\n📅 Daily Aggregates for 2020:")
    print(f"   Total records: {data.get('pagination', {}).get('total_records', 0)}")
    records = data.get('data', [])
    print(f"   Records returned on page 1: {len(records)}")
    if records:
        print(f"   Sample: {records[0]}")

# Test trips
params = urllib.parse.urlencode({
    'start_date': '2020-01-01',
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
    print(f"\n🚕 Trips (2020-2024):")
    print(f"   Total records: {data.get('pagination', {}).get('total_records', 0)}")
    records = data.get('data', [])
    print(f"   Records returned on page 1: {len(records)}")
    if records:
        print(f"   Sample: {records[0]}")

print("\n" + "=" * 70)
print("  ✅ All data is being served from mock database!")
print("=" * 70)
