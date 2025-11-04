import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://realpython.github.io/fake-jobs/"
HEADERS = {"User-Agent": "MyScraperBot/1.0 (+https://example.com/contact)"}

def scrape_page(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    rows = []
    for card in soup.find_all("div", class_="card-content"):
        title = card.find("h2", class_="title").get_text(strip=True)
        company = card.find("h3", class_="company").get_text(strip=True)
        location = card.find("p", class_="location").get_text(strip=True)
        link = card.find_parent("a")
        job_url = link["href"] if link and link.has_attr("href") else None
        rows.append({"title": title, "company": company, "location": location, "url": job_url})
    return rows

if __name__ == "__main__":
    print("Scraping single page:", URL)
    rows = scrape_page(URL)
    df = pd.DataFrame(rows)
    print(df.head())
    df.to_csv("jobs_single.csv", index=False)
    print("Saved jobs_single.csv - rows:", len(df))