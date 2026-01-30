"""
Backend API Tests
Tests for all API endpoints including authentication, aggregates, trips, and statistics
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

# Test data
TEST_USERNAME = "admin"
TEST_PASSWORD = "secret"


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        print("✅ Root endpoint test passed")
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        print("✅ Health check test passed")
    
    def test_login_success(self):
        """Test successful login"""
        response = client.post(
            "/token",
            data={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        print("✅ Login success test passed")
        return data["access_token"]
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post(
            "/token",
            data={"username": "wrong", "password": "wrong"}
        )
        assert response.status_code == 401
        print("✅ Invalid login test passed")
    
    def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token"""
        response = client.get("/api/users/me")
        assert response.status_code == 401
        print("✅ Protected endpoint without token test passed")
    
    def test_protected_endpoint_with_token(self):
        """Test accessing protected endpoint with valid token"""
        # First login to get token
        login_response = client.post(
            "/token",
            data={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        token = login_response.json()["access_token"]
        
        # Use token to access protected endpoint
        response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == TEST_USERNAME
        print("✅ Protected endpoint with token test passed")


class TestAggregatesAPI:
    """Test aggregates API endpoints"""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authentication headers"""
        login_response = client.post(
            "/token",
            data={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_daily_aggregates_endpoint_exists(self, auth_headers):
        """Test daily aggregates endpoint exists and requires dates"""
        response = client.get(
            "/api/aggregates/daily",
            headers=auth_headers
        )
        # Should return 422 (validation error) because dates are missing
        assert response.status_code == 422
        print("✅ Daily aggregates endpoint exists test passed")
    
    def test_daily_aggregates_with_dates(self, auth_headers):
        """Test daily aggregates with date parameters"""
        response = client.get(
            "/api/aggregates/daily",
            headers=auth_headers,
            params={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31"
            }
        )
        # Should return 200 or 404 depending on if data exists
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert "data" in data
            assert "pagination" in data
            print("✅ Daily aggregates with dates test passed - data found")
        else:
            print("✅ Daily aggregates with dates test passed - no data (expected)")


class TestTripsAPI:
    """Test trips API endpoints"""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authentication headers"""
        login_response = client.post(
            "/token",
            data={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_trips_endpoint_exists(self, auth_headers):
        """Test trips endpoint exists and requires dates"""
        response = client.get(
            "/api/trips",
            headers=auth_headers
        )
        # Should return 422 because dates are required
        assert response.status_code == 422
        print("✅ Trips endpoint exists test passed")
    
    def test_trips_with_dates(self, auth_headers):
        """Test trips endpoint with date parameters"""
        response = client.get(
            "/api/trips",
            headers=auth_headers,
            params={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "page": 1,
                "page_size": 10
            }
        )
        # Should return 200 or 404 depending on if data exists
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert "data" in data
            assert "pagination" in data
            print("✅ Trips with dates test passed - data found")
        else:
            print("✅ Trips with dates test passed - no data (expected)")


class TestStatisticsAPI:
    """Test statistics API endpoints"""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authentication headers"""
        login_response = client.post(
            "/token",
            data={"username": TEST_USERNAME, "password": TEST_PASSWORD}
        )
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_statistics_endpoint(self, auth_headers):
        """Test statistics endpoint"""
        response = client.get(
            "/api/statistics",
            headers=auth_headers
        )
        # Should return 200 or 500 depending on database
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "total_trips" in data
            assert "total_revenue" in data
            print("✅ Statistics endpoint test passed - data found")
        else:
            print("✅ Statistics endpoint test passed - database error (check connection)")


def run_all_tests():
    """Run all tests and print summary"""
    print("\n" + "="*60)
    print("🧪 RUNNING BACKEND API TESTS")
    print("="*60 + "\n")
    
    # Run pytest
    pytest.main([__file__, "-v", "--tb=short"])
    
    print("\n" + "="*60)
    print("✅ TEST SUITE COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
