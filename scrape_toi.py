#!/usr/bin/env python3
"""
Generate stories.json by scraping a Times of India author page.
Usage:
    AUTHOR_URL="https://timesofindia.indiatimes.com/toireporter/author-Kanwardeep-Singh-479242302.cms" python scripts/scrape_toi.py
Output:
    stories.json in repo root.
"""
import os, re, sys, json, datetime
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

AUTHOR_URL = os.environ.get("AUTHOR_URL", "").strip()
if not AUTHOR_URL:
    print("ERROR: AUTHOR_URL env var is required", file=sys.stderr)
    sys.exit(1)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

def normalize_date(text):
    # Try to normalize dates like 'Nov 7, 2025' or 'Sep 13, 2019' or '7 Dec 2019'
    text = re.sub(r"\s+", " ", text.strip())
    for fmt in ["%b %d, %Y", "%d %b %Y", "%b %d %Y", "%d %B %Y", "%B %d, %Y"]:
        try:
            dt = datetime.datetime.strptime(text, fmt)
            return dt.strftime("%b %d, %Y")
        except Exception:
            pass
    return text

def extract_articles(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    # Strategy: Look for anchors that link to /articleshow/ and have meaningful text
    for a in soup.select("a"):
        href = a.get("href", "")
        title = a.get_text(strip=True)
        if not title or not href:
            continue
        if "/articleshow/" in href and len(title) > 30:
            url = urljoin(base_url, href)
            # Try to find a nearby date
            date_text = ""
            parent = a.find_parent()
            if parent:
                date_span = parent.find(lambda tag: tag.name in ["span", "time"] and ("time" in " ".join(tag.get("class", [])).lower() or "pub" in " ".join(tag.get("class", [])).lower() or "date" in " ".join(tag.get("class", [])).lower()))
                if date_span and date_span.get_text(strip=True):
                    date_text = normalize_date(date_span.get_text(strip=True))
            items.append({
                "title": title,
                "url": url,
                "date": date_text,
                "outlet": "The Times of India"
            })

    # Deduplicate by URL
    seen = set()
    uniq = []
    for it in items:
        if it["url"] in seen:
            continue
        seen.add(it["url"])
        uniq.append(it)

    return uniq[:20]

def main():
    r = requests.get(AUTHOR_URL, headers=headers, timeout=20)
    r.raise_for_status()
    articles = extract_articles(r.text, AUTHOR_URL)

    if not articles:
        print("WARNING: No articles extracted; check page structure.", file=sys.stderr)

    with open("stories.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(articles)} items to stories.json")

if __name__ == "__main__":
    main()
