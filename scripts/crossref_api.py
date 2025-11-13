import os
import requests
import pandas as pd
import matplotlib.pyplot as plt


def fetch_crossref_articles(query, rows=100):
    """Fetch articles from Crossref API based on query."""
    base_url = "https://api.crossref.org/works"
    params = {"query": query, "rows": rows}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("message", {}).get("items", [])


def create_dataframe(records):
    """Convert list of Crossref items to DataFrame with standard columns."""
    if not records:
        return pd.DataFrame()
    df = pd.json_normalize(records)
    # extract publication year
    if 'issued.date-parts' in df.columns:
        df['publicationDate'] = df['issued.date-parts'].apply(lambda x: x[0][0] if isinstance(x, list) and x else None)
    # extract journal title
    if 'container-title' in df.columns:
        df['journal'] = df['container-title'].apply(lambda x: x[0] if isinstance(x, list) and x else None)
    return df


def summarize(df):
    """Print summary of Crossref data."""
    if df.empty:
        print("No records found for your query.")
        return
    if 'publicationDate' in df.columns:
        years = df['publicationDate'].astype(str)
        year_counts = years.value_counts()
        top_year = year_counts.idxmax()
        print(f"Most common publication year: {top_year} ({year_counts[top_year]} articles)")
    if 'journal' in df.columns:
        journal_counts = df['journal'].value_counts()
        top_journal = journal_counts.idxmax()
        print(f"Most common journal: {top_journal} ({journal_counts[top_journal]} articles)")


def save_csv(df, query):
    """Save DataFrame to CSV with filename based on query."""
    filename = f"crossref_{query.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} records to {filename}")


def plot_year_distribution(df):
    """Plot a bar chart of publication years distribution."""
    if df.empty or 'publicationDate' not in df.columns:
        return
    year_counts = df['publicationDate'].astype(str).value_counts().sort_index()
    year_counts.plot(kind='bar')
    plt.title("Publication Year Distribution (Crossref)")
    plt.xlabel("Year")
    plt.ylabel("Number of articles")
    plt.tight_layout()
    plt.show()


def main():
    query = input("Enter query term for Crossref API: ").strip()
    try:
        records = fetch_crossref_articles(query)
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
