from __future__ import annotations
import pathlib
import sqlite3
import subprocess
import sys
import time
from typing import Optional, Callable
from PIL import Image
import cv2

THUMB_DIR = pathlib.Path("data/thumbnails")

def make_thumb_from_file(path: pathlib.Path) -> None:
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    out = THUMB_DIR / (path.stem + ".jpg")
    if out.exists(): 
        return
    cmd = ["ffmpeg","-y","-ss","0.5","-i", str(path), "-frames:v","1","-q:v","3","-vf","scale=512:-2", str(out)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

MEDIA_DIR = pathlib.Path("data/media/video")

def already_downloaded(url: str) -> bool:
    vid = url.rstrip("/").split("/")[-1]
    return any(MEDIA_DIR.glob(f"{vid}.*"))

def extract_thumbnail(video_path: pathlib.Path) -> Optional[Image.Image]:
    """Extract first frame from video as PIL Image"""
    try:
        cap = cv2.VideoCapture(str(video_path))
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(rgb_frame)
    except Exception as e:
        print(f"[TokIntel] Errore estrazione thumbnail: {e}", file=sys.stderr)
    
    return None

def fetch_one(url: str, thumbnail_callback: Optional[Callable[[Image.Image], None]] = None) -> bool:
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    cmd = ["yt-dlp", "-f", "mp4", "-o", f"{MEDIA_DIR}/%(id)s.%(ext)s", url]
    try:
        subprocess.run(cmd, check=True)
        
        # Generate persistent thumbnail
        try:
            # Trova il file appena creato per mtime
            saved = max(MEDIA_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
            make_thumb_from_file(saved)
        except Exception:
            pass
        
        # Extract thumbnail if callback is provided
        if thumbnail_callback:
            vid = url.rstrip("/").split("/")[-1]
            video_path = next(MEDIA_DIR.glob(f"{vid}.*"), None)
            if video_path:
                thumbnail = extract_thumbnail(video_path)
                if thumbnail:
                    thumbnail_callback(thumbnail)
        
        return True
    except Exception as e:
        print(f"[TokIntel] download fallito: {url} -> {e}", file=sys.stderr)
        return False

def fetch_missing(limit: int | None = None):
    con = sqlite3.connect("data/db.sqlite"); cur = con.cursor()
    cur.execute("SELECT url FROM videos ORDER BY id DESC")
    urls = [r[0] for r in cur.fetchall()]
    con.close()
    cnt = 0
    for u in urls:
        if limit and cnt >= limit: break
        if already_downloaded(u): continue
        ok = fetch_one(u); cnt += 1 if ok else 0
        time.sleep(0.5)  # gentle
    print(f"✓ Scaricati {cnt} nuovi video.")

def fetch_missing_with_callbacks(
    limit: Optional[int] = None,
    thumbnail_callback: Optional[Callable[[Image.Image], None]] = None,
    status_callback: Optional[Callable[[str], None]] = None
):
    """Enhanced fetch function with callback support for live feedback"""
    con = sqlite3.connect("data/db.sqlite"); cur = con.cursor()
    cur.execute("SELECT url FROM videos ORDER BY id DESC")
    urls = [r[0] for r in cur.fetchall()]
    con.close()
    
    cnt = 0
    total_urls = len(urls)
    
    for i, url in enumerate(urls):
        if limit and cnt >= limit: 
            break
            
        if already_downloaded(url): 
            continue
            
        if status_callback:
            status_callback(f"Downloading video {i+1}/{total_urls}: {url.split('/')[-1]}")
        
        ok = fetch_one(url, thumbnail_callback)
        cnt += 1 if ok else 0
        time.sleep(0.5)  # gentle
    
    if status_callback:
        status_callback(f"✅ Scaricati {cnt} nuovi video")
    print(f"✓ Scaricati {cnt} nuovi video.")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    fetch_missing(args.limit)
