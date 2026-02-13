"""
Enhanced mock data for NYC TLC Analytics - Interview Demo
Generates realistic NYC taxi trip data for demonstration purposes
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict

# NYC taxi zones organized by borough
NYCT_ZONES = {
    'Manhattan': [
        'Financial District', 'Tribeca', 'SoHo', 'East Village', 'Greenwich Village',
        'Chelsea', 'Midtown West', 'Times Square', 'Midtown East', 'Gramercy',
        'Upper East Side', 'Upper West Side', 'Central Park', 'Harlem',
        'Murray Hill', 'Kips Bay', 'Hell\'s Kitchen', 'Penn Station'
    ],
    'Queens': [
        'Long Island City', 'Astoria', 'Sunnyside', 'Jackson Heights', 'Corona',
        'Forest Hills', 'Flushing', 'Jamaica', 'Jamaica Estates', 'Saint Albans',
        'Bayside', 'Whitestone', 'College Point', 'Bowne Park'
    ],
    'Brooklyn': [
        'Downtown Brooklyn', 'DUMBO', 'Brooklyn Heights', 'Williamsburg', 'Greenpoint',
        'Bushwick', 'Bed-Stuy', 'Crown Heights', 'Prospect Heights', 'Park Slope',
        'Sunset Park', 'Flatbush', 'Coney Island', 'Brighton Beach', 'Bay Ridge'
    ],
    'Bronx': [
        'South Bronx', 'Mott Haven', 'Fordham', 'Pelham Parkway', 'Whitestone'
    ],
    'Staten Island': [
        'St. George', 'Tompkinsville', 'Great Kills', 'Fresh Kills'
    ]
}

SERVICE_TYPES = ['yellow', 'green', 'fhv', 'fhvhv']

# Realistic fare multipliers for different times
def get_time_multiplier(hour: int) -> float:
    """Get fare multiplier based on time of day"""
    if 7 <= hour < 10 or 17 <= hour < 20:  # Rush hours
        return 1.5
    elif 22 <= hour or hour < 5:  # Late night
        return 1.25
    else:
        return 1.0

def generate_realistic_trips(count: int = 5000) -> List[Dict]:
    """Generate realistic NYC taxi trip data from 2020-2024"""
    trips = []
    end_date = datetime(2024, 12, 31)  # End date: Dec 31, 2024
    start_date = datetime(2020, 1, 1)   # Start date: Jan 1, 2020
    random.seed(42)
    
    for i in range(count):
        # Create dates uniformly distributed across the 5-year range
        days_span = (end_date - start_date).days
        days_offset = random.randint(0, days_span)
        pickup_date = start_date + timedelta(days=days_offset)
        
        # More trips during business hours
        hour = random.choices(
            range(24),
            weights=[2, 1, 1, 1, 3, 5, 8, 12, 10, 8, 7, 6, 8, 9, 10, 11, 14, 15, 13, 10, 8, 6, 4, 3]
        )[0]
        minute = random.randint(0, 59)
        
        pickup_datetime = pickup_date.replace(hour=hour, minute=minute)
        
        # Trip duration between 5-120 minutes (realistic)
        trip_duration_min = random.choices(
            [random.randint(5, 15), random.randint(15, 45), random.randint(45, 120)],
            weights=[40, 45, 15]  # Most trips are short/medium
        )[0]
        
        trip_duration_sec = trip_duration_min * 60
        dropoff_datetime = pickup_datetime + timedelta(minutes=trip_duration_min)
        
        # Trip distance correlated with trip duration
        trip_distance = round(0.2 + (trip_duration_min * 0.15) + random.uniform(-1, 2), 2)
        trip_distance = max(0.5, min(trip_distance, 30))  # Clamp between 0.5 and 30 miles
        
        # Pickup location varies (more Manhattan than outer boroughs)
        pickup_borough = random.choices(
            ['Manhattan', 'Queens', 'Brooklyn', 'Bronx', 'Staten Island'],
            weights=[50, 20, 20, 5, 5]
        )[0]
        
        pickup_zone = random.choice(NYCT_ZONES[pickup_borough])
        
        # Dropoff location (some local trips)
        if random.random() < 0.3:  # 30% local trips
            dropoff_borough = pickup_borough
        else:
            dropoff_borough = random.choice(list(NYCT_ZONES.keys()))
        
        dropoff_zone = random.choice(NYCT_ZONES[dropoff_borough])
        
        # Service type (yellow more common)
        service_type = random.choices(
            SERVICE_TYPES,
            weights=[45, 30, 15, 10]
        )[0]
        
        # Calculate fare
        base_fare = 2.50
        per_mile = 2.50
        per_min = 0.50
        
        fare = base_fare + (trip_distance * per_mile) + (trip_duration_min * per_min)
        fare *= get_time_multiplier(hour)
        
        # Add tip and surcharges
        tip = round(fare * random.uniform(0.15, 0.25), 2)
        surcharge = 2.75 if service_type == 'yellow' else 2.50
        total_amount = round(fare + tip + surcharge, 2)
        
        trips.append({
            'trip_id': i + 1,
            'service_type': service_type,
            'pickup_datetime': pickup_datetime.isoformat(),
            'dropoff_datetime': dropoff_datetime.isoformat(),
            'pickup_location_id': random.randint(1, 263),
            'dropoff_location_id': random.randint(1, 263),
            'pickup_borough': pickup_borough,
            'pickup_zone': pickup_zone,
            'dropoff_borough': dropoff_borough,
            'dropoff_zone': dropoff_zone,
            'trip_distance': trip_distance,
            'fare_amount': round(fare, 2),
            'total_amount': total_amount,
            'trip_duration_sec': trip_duration_sec,
            'pickup_date': pickup_date.strftime('%Y-%m-%d'),
            'is_valid': 1,
            'payment_type': random.choice(['credit card', 'cash']),
            'passenger_count': random.choices([1, 2, 3, 4, 5, 6], weights=[50, 25, 15, 5, 3, 2])[0],
        })
    
    return trips

def generate_realistic_aggregates() -> List[Dict]:
    """Generate realistic daily aggregate data for 6+ years (2020-2026)"""
    aggregates = []
    base_date = datetime(2020, 1, 1)  # Start date: Jan 1, 2020
    
    # Generate data from 2020 to present (Feb 2026)
    # 2020(366) + 2021(365) + 2022(365) + 2023(365) + 2024(366) + 2025(365) + 2026(43 days until Feb 12) = 2195 days
    end_date = datetime(2026, 2, 12)  # Current date
    day_count = (end_date - base_date).days + 1
    
    for day_offset in range(day_count):
        date = base_date + timedelta(days=day_offset)
        
        for service_type in SERVICE_TYPES:
            # Yellow cabs have more trips overall
            if service_type == 'yellow':
                base_trips = random.randint(100000, 180000)
            elif service_type == 'green':
                base_trips = random.randint(60000, 110000)
            elif service_type == 'fhv':
                base_trips = random.randint(30000, 70000)
            else:  # fhvhv
                base_trips = random.randint(20000, 50000)
            
            # Weekday vs weekend variation
            if date.weekday() >= 5:  # Weekend
                total_trips = int(base_trips * 0.85)
            else:  # Weekday
                total_trips = base_trips
            
            # Add seasonal variation
            if date.month in [6, 7, 8]:  # Summer
                total_trips = int(total_trips * 1.1)
            elif date.month in [12, 1]:  # Winter
                total_trips = int(total_trips * 0.95)
            
            # Revenue calculation based on trips
            avg_fare = 15.50 if service_type == 'yellow' else 16.00
            total_revenue = round(total_trips * avg_fare * (0.9 + random.random() * 0.2), 2)
            
            aggregates.append({
                'metric_date': date.strftime('%Y-%m-%d'),
                'service_type': service_type,
                'total_trips': total_trips,
                'total_revenue': total_revenue,
                'avg_trip_distance': round(random.uniform(3.0, 8.5), 2),
                'avg_trip_duration_sec': random.randint(800, 1600),
                'avg_fare_amount': round(total_revenue / total_trips, 2),
            })
    
    return aggregates

def generate_statistics() -> Dict:
    """Generate system-wide statistics for 5 years (2020-2024)"""
    return {
        'total_trips': 8234567890,  # ~8.2 billion trips
        'total_revenue': 78567234567.50,  # ~$78.5 billion
        'average_trip_distance': 7.85,
        'average_trip_duration_sec': 1245,
        'data_quality_pct': 98.5,
        'service_types': {
            'yellow': 4234567890,
            'green': 2345678901,
            'fhv': 987654321,
            'fhvhv': 666666778
        },
        'boroughs': {
            'Manhattan': {
                'total_trips': 3567823456,
                'total_revenue': 42567234567.50
            },
            'Queens': {
                'total_trips': 1789456789,
                'total_revenue': 17892345678.25
            },
            'Brooklyn': {
                'total_trips': 1678923456,
                'total_revenue': 12345678901.50
            },
            'Bronx': {
                'total_trips': 223456789,
                'total_revenue': 3234567890.25
            },
            'Staten Island': {
                'total_trips': 28235400,
                'total_revenue': 2527407530.00
            }
        }
    }

if __name__ == '__main__':
    print("Generating 5 years of mock data for interview demo (2020-2024)...")
    trips = generate_realistic_trips(5000)
    aggregates = generate_realistic_aggregates()
    stats = generate_statistics()
    
    print(f"✅ Generated {len(trips)} trip records")
    print(f"✅ Generated {len(aggregates)} aggregate records (5 years of daily metrics)")
    print(f"✅ Generated statistics for {len(stats['service_types'])} service types")
    print("\nSample trip:", trips[0])
    print("Sample aggregate:", aggregates[0])
