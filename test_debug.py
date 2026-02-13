import requests
import json
from datetime import datetime, timedelta

# Get token
auth_response = requests.post(
    "http://localhost:8000/login",
    data={"username": "admin", "password": "secret"}
)
token = auth_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Test summary API
print("Testing /api/summary...")
response = requests.get(
    "http://localhost:8000/api/summary",
    params={},
    headers=headers
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Try with date range
print("\n\nTesting /api/summary with date range...")
response = requests.get(
    "http://localhost:8000/api/summary",
    params={
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    },
    headers=headers
)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
