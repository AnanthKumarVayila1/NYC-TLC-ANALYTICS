#!/usr/bin/env python3
"""Debug mock data generation"""
import sys
sys.path.insert(0, '/Users/ananthkumarvayila/Desktop/Projects/NYC-TLC-ANALYTICS')

from backend.app.mock_data import generate_realistic_aggregates, generate_realistic_trips

print("Generating mock data...")
aggs = generate_realistic_aggregates()
trips = generate_realistic_trips(100)  

print(f"\n✅ Generated {len(aggs)} aggregate records")
print(f"✅ Generated {len(trips)} trip records")

# Show date ranges
print(f"\n📅 Aggregate date range:")
if aggs:
    print(f"   First: {aggs[0].get('metric_date')}")
    print(f"   Last: {aggs[-1].get('metric_date')}")

# Check Q4 2024
q4_aggs = [a for a in aggs if '2024-10' in a.get('metric_date', '') or '2024-11' in a.get('metric_date', '') or '2024-12' in a.get('metric_date', '')]
print(f"\n📊 Aggregates in Q4 2024: {len(q4_aggs)}")
if q4_aggs:
    print(f"   Dates: {[a.get('metric_date') for a in q4_aggs[:5]]}")

print(f"\n📅 Trip date range:")
trip_dates = sorted([t.get('pickup_date', '') for t in trips])  
if trip_dates:
    print(f"   First: {trip_dates[0]}")
    print(f"   Last: {trip_dates[-1]}")

q4_trips = [t for t in trips if '2024-10' in t.get('pickup_date', '') or '2024-11' in t.get('pickup_date', '') or '2024-12' in t.get('pickup_date', '')]
print(f"\n🚖 Trips in Q4 2024: {len(q4_trips)}")
if q4_trips:
    print(f"   Dates: {[t.get('pickup_date') for t in q4_trips[:5]]}")
