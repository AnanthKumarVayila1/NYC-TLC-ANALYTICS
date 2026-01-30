"""
Database Connection Test
Tests database connectivity and basic queries
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import db
from app.config import settings


def test_database_connection():
    """Test database connection"""
    print("\n" + "="*60)
    print("🔌 TESTING DATABASE CONNECTION")
    print("="*60 + "\n")
    
    print(f"Server: {settings.DB_SERVER}")
    print(f"Database: {settings.DB_NAME}")
    print(f"User: {settings.DB_USER}")
    print(f"Driver: {settings.DB_DRIVER}")
    print()
    
    try:
        # Test basic query
        result = db.execute_scalar("SELECT 1 as test")
        assert result == 1
        print("✅ Basic query test: PASSED")
        
        # Test table existence - fact_trip
        try:
            count = db.execute_scalar("SELECT COUNT(*) FROM fact_trip")
            print(f"✅ fact_trip table exists: {count:,} rows")
        except Exception as e:
            print(f"⚠️  fact_trip table: {str(e)}")
        
        # Test table existence - agg_daily_metrics
        try:
            count = db.execute_scalar("SELECT COUNT(*) FROM agg_daily_metrics")
            print(f"✅ agg_daily_metrics table exists: {count:,} rows")
        except Exception as e:
            print(f"⚠️  agg_daily_metrics table: {str(e)}")
        
        # Test sample data from fact_trip
        try:
            sample = db.execute_query("""
                SELECT TOP 5 
                    trip_id, service_type, pickup_datetime, total_amount
                FROM fact_trip
                ORDER BY pickup_datetime DESC
            """)
            print(f"\n📊 Sample data from fact_trip (latest 5 trips):")
            for row in sample:
                print(f"   Trip {row['trip_id']}: {row['service_type']} - ${row['total_amount']:.2f}")
        except Exception as e:
            print(f"⚠️  Could not fetch sample data: {str(e)}")
        
        # Test date range
        try:
            date_range = db.execute_query("""
                SELECT 
                    MIN(pickup_date) as min_date,
                    MAX(pickup_date) as max_date,
                    COUNT(*) as total_trips
                FROM fact_trip
            """)[0]
            print(f"\n📅 Date Range:")
            print(f"   From: {date_range['min_date']}")
            print(f"   To: {date_range['max_date']}")
            print(f"   Total trips: {date_range['total_trips']:,}")
        except Exception as e:
            print(f"⚠️  Could not fetch date range: {str(e)}")
        
        print("\n" + "="*60)
        print("✅ DATABASE CONNECTION TEST: PASSED")
        print("="*60 + "\n")
        return True
        
    except Exception as e:
        print(f"\n❌ DATABASE CONNECTION TEST: FAILED")
        print(f"Error: {str(e)}")
        print("\nPlease check:")
        print("1. Azure SQL Database credentials in .env file")
        print("2. Database server firewall rules allow your IP")
        print("3. Database tables exist (fact_trip, agg_daily_metrics)")
        print("="*60 + "\n")
        return False


if __name__ == "__main__":
    test_database_connection()
