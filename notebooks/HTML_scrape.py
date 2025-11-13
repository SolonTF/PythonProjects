import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://quotes.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

quotes = [q.text for q in soup.find_all("span", class_="text")]
authors = [a.text for a in soup.find_all("small", class_="author")]

df = pd.DataFrame({"Quote": quotes, "Author": authors})
print(df.head())
