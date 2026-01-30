#!/bin/bash
# Manual API Testing Script
# Tests all API endpoints with curl commands

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

API_BASE="http://localhost:8000"
USERNAME="admin"
PASSWORD="secret"

echo "======================================================================="
echo "  🧪 NYC TLC ANALYTICS - MANUAL API TESTING"
echo "======================================================================="
echo ""

# Test 1: Health Check
echo -e "${YELLOW}TEST 1: Health Check${NC}"
echo "GET $API_BASE/health"
curl -X GET "$API_BASE/health" -H "Content-Type: application/json" | jq .
echo ""
echo ""

# Test 2: Root Endpoint
echo -e "${YELLOW}TEST 2: Root Endpoint${NC}"
echo "GET $API_BASE/"
curl -X GET "$API_BASE/" -H "Content-Type: application/json" | jq .
echo ""
echo ""

# Test 3: Login and Get Token
echo -e "${YELLOW}TEST 3: Login (Get Access Token)${NC}"
echo "POST $API_BASE/token"
TOKEN_RESPONSE=$(curl -X POST "$API_BASE/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$USERNAME&password=$PASSWORD" 2>/dev/null)

echo "$TOKEN_RESPONSE" | jq .

# Extract token
TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo -e "${RED}❌ Failed to get access token${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Token received${NC}"
echo ""
echo ""

# Test 4: Get User Info
echo -e "${YELLOW}TEST 4: Get Current User Info${NC}"
echo "GET $API_BASE/api/users/me"
curl -X GET "$API_BASE/api/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq .
echo ""
echo ""

# Test 5: Get Daily Aggregates
echo -e "${YELLOW}TEST 5: Get Daily Aggregates${NC}"
echo "GET $API_BASE/api/aggregates/daily?start_date=2024-01-01&end_date=2024-01-31"
curl -X GET "$API_BASE/api/aggregates/daily?start_date=2024-01-01&end_date=2024-01-31&page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq .
echo ""
echo ""

# Test 6: Get Trips
echo -e "${YELLOW}TEST 6: Get Trip Records${NC}"
echo "GET $API_BASE/api/trips?start_date=2024-01-01&end_date=2024-01-31"
curl -X GET "$API_BASE/api/trips?start_date=2024-01-01&end_date=2024-01-31&page=1&page_size=5" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq .
echo ""
echo ""

# Test 7: Get Statistics
echo -e "${YELLOW}TEST 7: Get Overall Statistics${NC}"
echo "GET $API_BASE/api/statistics"
curl -X GET "$API_BASE/api/statistics" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq .
echo ""
echo ""

# Test 8: Filter by Service Type
echo -e "${YELLOW}TEST 8: Filter Aggregates by Service Type (Yellow Taxi)${NC}"
echo "GET $API_BASE/api/aggregates/daily?service_type=yellow"
curl -X GET "$API_BASE/api/aggregates/daily?start_date=2024-01-01&end_date=2024-01-31&service_type=yellow&page=1&page_size=5" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq .
echo ""
echo ""

# Test 9: Test Pagination
echo -e "${YELLOW}TEST 9: Test Pagination (Page 2)${NC}"
echo "GET $API_BASE/api/trips?page=2"
curl -X GET "$API_BASE/api/trips?start_date=2024-01-01&end_date=2024-01-31&page=2&page_size=5" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq .
echo ""
echo ""

echo "======================================================================="
echo -e "  ${GREEN}✅ MANUAL API TESTING COMPLETED${NC}"
echo "======================================================================="
echo ""
echo "To view interactive API documentation, visit:"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""
