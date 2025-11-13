import requests
import pandas as pd
import os

# Load your API key from environment
API_KEY = os.getenv("SPRINGER_API_KEY")
if not API_KEY:
    raise ValueError("❌ Springer API key not found. Please export SPRINGER_API_KEY first.")

# Correct Open Access API URL
url = "https://api.springernature.com/openaccess/json"

# Query parameters
params = {
    "q": "amyloidosis",
    "api_key": API_KEY,
    "p": 10
}

# Send request
response = requests.get(url, params=params)
print("Status code:", response.status_code)

# Parse JSON
data = response.json()
print("Response keys:", list(data.keys()))

# Check if records exist
if "records" not in data:
    print("❌ No 'records' field in response. Full response:")
    print(data)
else:
    # Prepare data
    records = [
        {
            "Title": r.get("title"),
            "Publication": r.get("publicationName"),
            "URL": r.get("url")[0]["value"] if r.get("url") else None,
            "Abstract": r.get("abstract"),
            "PublicationDate": r.get("publicationDate")
        }
        for r in data["records"]
    ]

    df = pd.DataFrame(records)

    # ✅ Automatically create the SpringerNature folder if missing
    save_dir = os.path.join(os.getcwd(), "notebooks", "SpringerNature")
    os.makedirs(save_dir, exist_ok=True)

    # Save CSV in that folder
    save_path = os.path.join(save_dir, "springer_open_amyloidosis.csv")
    df.to_csv(save_path, index=False)

    print(f"\n✅ Saved results to: {save_path}")
