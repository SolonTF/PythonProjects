import os
import requests
import pandas as pd
import matplotlib.pyplot as plt


def fetch_springer_articles(query, api_key=None, page_size=50, max_records=200):
    """Fetch open access articles from Springer Nature API for a given query, handling pagination."""
    key = api_key or os.getenv("SPRINGER_API_KEY")
    if not key:
        raise EnvironmentError("SPRINGER_API_KEY not set. Please set it in your environment or pass api_key.")
    base_url = "https://api.springernature.com/openaccess/json"
    all_records = []
    start_index = 1  # API uses 1-based indexing for 's' start
    while True:
        params = {
            "api_key": key,
            "q": query,
            "p": page_size,
            "s": start_index
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("records", [])
        if not records:
            break
        all_records.extend(records)
        if len(all_records) >= max_records:
            break
        start_index += page_size
    return all_records


def create_dataframe(records):
    """Convert a list of record dicts into a pandas DataFrame."""
    if not records:
        return pd.DataFrame()
    df = pd.json_normalize(records)
    # Rename journalTitle to journal for easier summarisation
    if 'journalTitle' in df.columns:
        df = df.rename(columns={'journalTitle': 'journal'})
    return df


def summarize(df):
    """Print summary statistics for the DataFrame, such as most common publication year and journal."""
    if df.empty:
        print("No records found for your query.")
        return
    if 'publicationDate' in df.columns:
        years = df['publicationDate'].astype(str).str[:4]
        year_counts = years.value_counts()
        top_year = year_counts.idxmax()
        top_year_count = year_counts.max()
        print(f"Most common publication year: {top_year} ({top_year_count} articles)")
    if 'journal' in df.columns:
        journal_counts = df['journal'].value_counts()
        top_journal = journal_counts.idxmax()
        top_journal_count = journal_counts.max()
        print(f"Most common journal: {top_journal} ({top_journal_count} articles)")


def save_csv(df, query):
    """Save DataFrame to CSV with filename based on query."""
    filename = f"springer_{query.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} records to {filename}")


def plot_year_distribution(df):
    """Plot a bar chart of publication years distribution."""
    if df.empty or 'publicationDate' not in df.columns:
        return
    year_counts = df['publicationDate'].astype(str).str[:4].value_counts().sort_index()
    year_counts.plot(kind='bar')
    plt.title("Publication Year Distribution")
    plt.xlabel("Year")
    plt.ylabel("Number of articles")
    plt.tight_layout()
    plt.show()


def main():
    query = input("Enter query term for Springer Nature Open Access API: ").strip()
    try:
        records = fetch_springer_articles(query)
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return
    df = create_dataframe(records)
    summarize(df)
    if not df.empty:
        save_csv(df, query)
        try:
            plot_year_distribution(df)
        except Exception as e:
            print(f"Error plotting results: {e}")


if __name__ == "__main__":
    main()
