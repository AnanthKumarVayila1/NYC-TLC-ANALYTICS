#!/usr/bin/env python3
"""
Comprehensive Backend Test Runner
Runs all backend tests and provides detailed reports
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_database import test_database_connection
import subprocess


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_section(text):
    """Print formatted section"""
    print("\n" + "-"*70)
    print(f"  {text}")
    print("-"*70 + "\n")


def main():
    """Main test runner"""
    print_header("🧪 NYC TLC ANALYTICS - BACKEND TEST SUITE")
    
    # Test 1: Database Connection
    print_section("TEST 1: DATABASE CONNECTION")
    db_success = test_database_connection()
    
    if not db_success:
        print("\n⚠️  WARNING: Database tests failed. API tests may also fail.")
        response = input("\nContinue with API tests anyway? (y/n): ")
        if response.lower() != 'y':
            print("\nTest suite aborted.")
            return
    
    # Test 2: API Endpoints
    print_section("TEST 2: API ENDPOINTS")
    print("Running pytest for API endpoint tests...")
    print()
    
    try:
        # Run pytest
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_api.py", "-v", "--tb=short"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=False
        )
        
        if result.returncode == 0:
            print("\n✅ API endpoint tests: PASSED")
        else:
            print("\n⚠️  Some API endpoint tests failed. Check output above.")
    except Exception as e:
        print(f"\n❌ Error running API tests: {str(e)}")
    
    # Summary
    print_header("📊 TEST SUMMARY")
    print("Database Connection:", "✅ PASSED" if db_success else "❌ FAILED")
    print("\nFor detailed API documentation, start the server and visit:")
    print("  http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    main()
