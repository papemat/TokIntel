from __future__ import annotations
import argparse, json, time, sqlite3, pathlib
from datetime import datetime

from playwright.sync_api import sync_playwright

def upsert_videos(urls: list[str]):
    pathlib.Path("data").mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect("data/db.sqlite")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS videos(
      id INTEGER PRIMARY KEY,
      collection_id TEXT,
      collection_name TEXT,
      url TEXT UNIQUE,
      title TEXT, author TEXT,
      duration_sec INTEGER,
      published_at TEXT,
      added_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    for u in urls:
        cur.execute("""INSERT OR IGNORE INTO videos(collection_id,collection_name,url,title,author,duration_sec,published_at)
                       VALUES (?,?,?,?,?,?,?)""",
                    ("public", "public-collection", u, None, None, None, None))
    con.commit(); con.close()

def collect_from_collection(collection_url: str, max_videos: int = 200, headless: bool = True) -> list[str]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=["--disable-blink-features=AutomationControlled"])
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = ctx.new_page()
        page.goto(collection_url, wait_until="domcontentloaded", timeout=60000)

        # Scroll progressivo per caricare la griglia
        last_height = 0
        urls = set()
        for _ in range(40):  # ~40 scroll -> più che sufficiente
            page.mouse.wheel(0, 2000)
            time.sleep(0.8)
            # Prendi tutti i link ai video visibili
            anchors = page.locator("a[href*='/video/']").all()
            for a in anchors:
                try:
                    href = a.get_attribute("href")
                    if href and "/video/" in href:
                        # normalizza
                        if href.startswith("//"): href = "https:" + href
                        if href.startswith("/"): href = "https://www.tiktok.com" + href
                        urls.add(href.split("?")[0])
                except Exception:
                    pass
            if len(urls) >= max_videos:
                break
            # stop se non scrolla più
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        browser.close()
        out = sorted(urls)[:max_videos]
        return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL raccolta pubblica TikTok")
    ap.add_argument("--max", type=int, default=200)
    ap.add_argument("--headless", action="store_true", default=True)
    args = ap.parse_args()

    urls = collect_from_collection(args.url, max_videos=args.max, headless=args.headless)
    print(f"[TokIntel] Trovati {len(urls)} video.")
    upsert_videos(urls)
    # salva anche file di appoggio
    pathlib.Path("data").mkdir(parents=True, exist_ok=True)
    pathlib.Path("data/collection_urls.json").write_text(json.dumps(urls, indent=2), encoding="utf-8")
    print("✓ URLs salvati in DB e data/collection_urls.json")

if __name__ == "__main__":
    main()
