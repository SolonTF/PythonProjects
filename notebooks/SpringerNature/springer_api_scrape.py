import os
import requests
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------

# Load API key
API_KEY = os.getenv("SPRINGER_API_KEY")
if not API_KEY:
    raise ValueError("❌ No API key found. Set SPRINGER_API_KEY in your environment.")

# Set the search term here
QUERY = input("Enter a keyword to search Springer Open Access: ").strip()

# Base endpoint
URL = "https://api.springernature.com/openaccess/json"

params = {
    "q": QUERY,
    "api_key": API_KEY,
    "p": 50   # number of results
}

# ----------------------------------------------------------
# API REQUEST
# ----------------------------------------------------------

print(f"\n🔍 Searching Springer Open Access for: '{QUERY}'")
response = requests.get(URL, params=params)

if response.status_code != 200:
    print(f"❌ Error {response.status_code}: Could not contact Springer API.")
    print(response.text)
    exit()

data = response.json()

# If API indicates premium content, retry with openaccess/json
if "error_description" in data:
    print("⚠ Premium content detected — retrying request...")
    response = requests.get(URL, params=params)
    data = response.json()

records = data.get("records", [])

if not records:
    print(f"❌ No open-access results found for '{QUERY}'. Try another term.")
    exit()

print(f"✅ Found {len(records)} results.\n")


# ----------------------------------------------------------
# CONVERT TO DATAFRAME
# ----------------------------------------------------------

articles = []
for r in records:
    articles.append({
        "Title": r.get("title", ""),
        "Publication": r.get("journalTitle", ""),
        "Year": r.get("onlinePublicationDate", "")[:4] if r.get("onlinePublicationDate") else "",
        "Abstract": r.get("abstract", ""),
        "URL": r.get("url", "")
    })

df = pd.DataFrame(articles)

print("📄 Preview of results:")
print(df.head(), "\n")


# ----------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------

if len(df) > 0:
    most_common_year = df["Year"].value_counts().idxmax()
    top_journal = df["Publication"].value_counts().idxmax()

    print("📊 SUMMARY")
    print("--------------------------")
    print(f"Most common publication year: {most_common_year}")
    print(f"Most common journal: {top_journal}")
    print(f"Total records: {len(df)}")
    print("--------------------------\n")


# ----------------------------------------------------------
# SAVE TO CSV
# ----------------------------------------------------------

output_file = f"springer_{QUERY.replace(' ', '_')}.csv"
df.to_csv(output_file, index=False)

print(f"💾 Saved full results to: {output_file}\n")


# ----------------------------------------------------------
# PLOT RESULTS
# ----------------------------------------------------------

if len(df) > 0:
    year_counts = df["Year"].value_counts().sort_index()

    plt.figure(figsize=(10, 4))
    year_counts.plot(kind="bar", color="steelblue")
    plt.title(f"Publication Year Distribution for '{QUERY}'")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

print("🎉 Done!")
