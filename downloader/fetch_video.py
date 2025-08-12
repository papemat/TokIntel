from __future__ import annotations
import subprocess
import pathlib
import sys

def download_video(url: str, out_dir="data/media/video"):
    """Download video from URL using yt-dlp"""
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    # best mp4 compatibile
    cmd = ["yt-dlp", "-f", "mp4", "-o", f"{out}/%(id)s.%(ext)s", url]
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"[TokIntel] errore download video: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download video from URL")
    parser.add_argument("url", help="Video URL to download")
    parser.add_argument("--out-dir", default="data/media/video", help="Output directory")
    
    args = parser.parse_args()
    success = download_video(args.url, args.out_dir)
    if success:
        print(f"✓ Video scaricato in {args.out_dir}")
    else:
        print("✗ Errore nel download del video")
        sys.exit(1)
