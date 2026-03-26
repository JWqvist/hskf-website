#!/usr/bin/env python3
"""Scrape all content from hskf.dk WordPress site (no posts — spam)."""

import json
import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://hskf.dk"
API_BASE = f"{BASE_URL}/wp-json/wp/v2"
SCRAPED_DIR = Path("/home/jewi/projects/hskf/scraped")
IMAGES_DIR = SCRAPED_DIR / "images"

AUTH = ("1986.jeppe@gmail.com", "jynl Y0kI h9KL 4TGc GWjJ 8kVH")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; HSKF-Scraper/1.0)"}

session = requests.Session()
session.headers.update(HEADERS)


def fetch_api(endpoint, params=None):
    url = f"{API_BASE}/{endpoint}"
    resp = session.get(url, params=params or {}, auth=AUTH, timeout=30)
    print(f"  GET {url} -> {resp.status_code}")
    resp.raise_for_status()
    return resp.json()


def fetch_all(endpoint, per_page=100):
    items, page = [], 1
    while True:
        data = fetch_api(endpoint, {"per_page": per_page, "page": page})
        if not data:
            break
        items.extend(data)
        if len(data) < per_page:
            break
        page += 1
    return items


# ── 1. Pages ─────────────────────────────────────────────────────────────────

def scrape_pages():
    print("\n=== Scraping Pages (WP REST API) ===")
    raw = fetch_all("pages", per_page=50)
    pages = [{
        "id":      p["id"],
        "slug":    p["slug"],
        "title":   p["title"]["rendered"],
        "content": p["content"]["rendered"],
        "link":    p.get("link", ""),
        "status":  p.get("status", ""),
        "date":    p.get("date", ""),
    } for p in raw]

    (SCRAPED_DIR / "pages.json").write_text(
        json.dumps(pages, ensure_ascii=False, indent=2))
    print(f"  Saved {len(pages)} pages")
    return pages


# ── 2. Media ─────────────────────────────────────────────────────────────────

def scrape_media():
    print("\n=== Scraping Media ===")
    raw = fetch_all("media", per_page=100)
    manifest = []
    downloaded = 0

    for item in raw:
        source_url = item.get("source_url", "")
        if not source_url:
            continue

        filename = os.path.basename(source_url.split("?")[0])
        dest = IMAGES_DIR / filename

        try:
            r = session.get(source_url, timeout=30, stream=True)
            if r.status_code == 200:
                dest.write_bytes(r.content)
                downloaded += 1
                print(f"  ✓ {filename}")
            else:
                print(f"  ✗ {filename} (HTTP {r.status_code})")
                filename = None
        except Exception as e:
            print(f"  ✗ {source_url}: {e}")
            filename = None

        manifest.append({
            "id":         item["id"],
            "filename":   filename,
            "source_url": source_url,
            "alt_text":   item.get("alt_text", ""),
            "title":      item["title"]["rendered"],
            "media_type": item.get("media_type", ""),
            "mime_type":  item.get("mime_type", ""),
            "date":       item.get("date", ""),
        })

    (SCRAPED_DIR / "images.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"  Downloaded {downloaded}/{len(raw)} media items")
    return manifest, downloaded


# ── 3. Static pages (rendered HTML) ──────────────────────────────────────────

# All known slugs from the WP pages API
KNOWN_SLUGS = [
    "hjem",
    "skytteforeningen",
    "bestyrelsen",
    "vedtaegter",
    "kontakt-os",
    "kontingent",
    "referater",
    "indendors-15m",
    "udendors-25m-og-50m",
    "pistolskytter",
    "traeningstider-riffelskytter",
    "skydekalender",
    "cookie-politik",
    # extra guesses in case of redirects / aliases
    "kontakt",
    "bliv-medlem",
    "om-klubben",
    "afdelinger",
    "events",
]

def scrape_static_pages():
    print("\n=== Scraping Static Pages (HTML) ===")
    results = {}

    for slug in KNOWN_SLUGS:
        url = f"{BASE_URL}/{slug}/"
        r = session.get(url, timeout=30, allow_redirects=True)
        print(f"  GET {url} -> {r.status_code}")
        if r.status_code != 200:
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        main = (soup.find("main") or
                soup.find("article") or
                soup.find("div", class_=re.compile(r"content|entry|post")))
        content_text = (main or soup).get_text(separator="\n", strip=True)
        title = soup.title.get_text(strip=True) if soup.title else slug

        # Save individual HTML
        (SCRAPED_DIR / f"page_{slug}.html").write_text(r.text, encoding="utf-8")

        results[slug] = {
            "url":          url,
            "final_url":    r.url,
            "title":        title,
            "content_text": content_text[:8000],
        }

    (SCRAPED_DIR / "static_pages.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2))
    print(f"  Saved {len(results)} static pages")
    return results


# ── 4. Homepage ───────────────────────────────────────────────────────────────

def scrape_homepage():
    print("\n=== Scraping Homepage ===")
    r = session.get(BASE_URL, timeout=30)
    print(f"  GET {BASE_URL} -> {r.status_code}")
    if r.status_code == 200:
        (SCRAPED_DIR / "homepage.html").write_text(r.text, encoding="utf-8")
        print(f"  Saved {len(r.text):,} bytes")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    SCRAPED_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Remove leftover posts.json if it exists
    stale = SCRAPED_DIR / "posts.json"
    if stale.exists():
        stale.unlink()
        print("Removed stale posts.json")

    pages          = scrape_pages()
    manifest, ndl  = scrape_media()
    static         = scrape_static_pages()
    scrape_homepage()

    print("\n" + "="*55)
    print("SCRAPE COMPLETE")
    print("="*55)
    print(f"  WP Pages (API):       {len(pages)}")
    print(f"  Media / images:       {len(manifest)} total, {ndl} downloaded")
    print(f"  Static pages (HTML):  {len(static)}")
    print()
    print("Static pages saved:")
    for slug, info in static.items():
        print(f"  /{slug}/  →  {info['title']}")
    print()
    print("Downloaded images:")
    for m in manifest:
        if m["filename"]:
            print(f"  {m['filename']}")

if __name__ == "__main__":
    main()
