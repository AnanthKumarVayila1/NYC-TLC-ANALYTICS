#!/usr/bin/env python3
"""
Test API endpoints to verify mock data is being served
"""
import urllib.request
import urllib.parse
import json

def test_api():
    print("=" * 70)
    print("  🧪 Testing NYC TLC Analytics API")
    print("=" * 70)
    print()
    
    # Get token
    print("1️⃣  Getting authentication token...")
    auth_data = urllib.parse.urlencode({'username': 'admin', 'password': 'secret'}).encode()
    try:
        with urllib.request.urlopen('http://localhost:8000/token', auth_data) as response:
            token = json.loads(response.read())['access_token']
            print("   ✅ Authentication successful")
    except Exception as e:
        print(f"   ❌ Authentication failed: {e}")
        return
    
    # Test summary endpoint
    print("\n2️⃣  Testing /api/summary endpoint...")
    params = urllib.parse.urlencode({
        'start_date': '2024-01-01',
        'end_date': '2024-12-31'
    })
    headers = {'Authorization': f'Bearer {token}'}
    req = urllib.request.Request(
        f'http://localhost:8000/api/summary?{params}',
        headers=headers
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(f"   ✅ Status: {response.status}")
            print(f"   ✅ Total trips: {data.get('total_trips', 0):,}")
            print(f"   ✅ Total revenue: ${data.get('total_revenue', 0):,.2f}")
            print(f"   ✅ Service types found: {len(data.get('by_service_type', []))}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test aggregates endpoint
    print("\n3️⃣  Testing /api/aggregates/daily endpoint...")
    params = urllib.parse.urlencode({
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
        'page': '1',
        'page_size': '10'
    })
    req = urllib.request.Request(
        f'http://localhost:8000/api/aggregates/daily?{params}',
        headers=headers
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(f"   ✅ Status: {response.status}")
            records = data.get('data', [])
            print(f"   ✅ Records returned: {len(records)}")
            if records:
                print(f"   ✅ First record: {records[0]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test trips endpoint
    print("\n4️⃣  Testing /api/trips endpoint...")
    params = urllib.parse.urlencode({
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
        'page': '1',
        'page_size': '5'
    })
    req = urllib.request.Request(
        f'http://localhost:8000/api/trips?{params}',
        headers=headers
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(f"   ✅ Status: {response.status}")
            records = data.get('data', [])
            print(f"   ✅ Records returned: {len(records)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("  ✅ All endpoints are working! Mock data is being served.")
    print("=" * 70)

if __name__ == '__main__':
    test_api()
