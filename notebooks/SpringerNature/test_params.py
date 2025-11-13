import os
import requests

API_KEY = os.getenv("SPRINGER_API_KEY")

if not API_KEY:
    print("❌ SPRINGER_API_KEY not set")
    exit(1)

print(f"✅ API Key found: {API_KEY[:20]}...")

query = "ai"
url = "https://api.springernature.com/openaccess/json"

# Try different parameter combinations
test_params = [
    # Original attempt
    {"q": query, "api_key": API_KEY, "p": 50, "s": 1},
    # Using keyword instead of q
    {"keyword": query, "api_key": API_KEY, "p": 50, "s": 1},
    # Try with title parameter
    {"title": query, "api_key": API_KEY, "p": 50, "s": 1},
]

for i, params in enumerate(test_params, 1):
    print(f"\n--- Test {i}: {list(params.keys())} ---")
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Keys: {list(data.keys())}")
    if data.get("result"):
        print(f"Found {len(data['result'])} results!")
    else:
        print(f"Message: {data.get('message', 'No message')}")
