import os
import requests

API_KEY = os.getenv("SPRINGER_API_KEY")

if not API_KEY:
    print("❌ SPRINGER_API_KEY not set")
    exit(1)

print(f"✅ API Key found: {API_KEY[:20]}...")

query = "ai"
url = "https://api.springernature.com/openaccess/json"
params = {
    "q": query,
    "api_key": API_KEY,
    "p": 50,
    "s": 1
}

response = requests.get(url, params=params)
print(f"\nStatus Code: {response.status_code}")
print(f"Response:\n{response.json()}")
