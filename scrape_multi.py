import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin


BASE = "https://realpython.github.io/fake-jobs/"
HEADERS = {"User-Agent": "MyScraperBot/1.0 (+https://example.com/contact)"}
DELAY = 1.0

def get_soup(url):
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            return BeautifulSoup(r.text, "html.parser")
        except requests.RequestException as e:
            print(f"Request error: {e} - retry {attempt+1}/3")
            time.sleep(1+attempt*2)
        raise RuntimeError("Failed to fetch page after 3 attempts")
    
def parse_jobs(soup, base_url):
    jobs = []
    for card in soup.find_all("div", class_="card-content"):
        title = card.find("h2", class_="title").get_text(strip=True)
        company = card.find("h3", class_="company").get_text(strip=True)
        location = card.find("p", class_="location").get_text(strip=True)
        link_tag = card.find_parent("a")
        job_url = urljoin(base_url, link_tag["href"]) if link_tag and link_tag.has_attr("href") else None
        jobs.append({"title": title, "company": company, "location": location, "url": job_url})
    return jobs

def find_next_link(soup, base_url):
    next_a = soup.find("a", string=lambda t: t and "next" in t.lower())
    return urljoin(base_url, next_a["href"]) if next_a and next_a.has_attr("href") else None


if __name__ == "__main__":
    url=BASE
    all_jobs = []
    page = 1
    while url:
        print(f"[Page {page}] Scraping: {url}")
        soup = get_soup(url)
        jobs = parse_jobs(soup, BASE)
        all_jobs.extend(jobs)
        url = find_next_link(soup, BASE)
        page += 1
        time.sleep(DELAY)

    df = pd.DataFrame(all_jobs)
    df.to_csv("jobs_multi.csv", index=False)
    print(f"Saved jobs_multi.csv - total rows: {len(df)}")