from __future__ import annotations
import pathlib
import subprocess
import sys

VIDEO_DIR = pathlib.Path("data/media/video")
THUMB_DIR = pathlib.Path("data/thumbnails")
THUMB_DIR.mkdir(parents=True, exist_ok=True)

def video_id_from_path(p: pathlib.Path) -> str:
    # usa nome file senza estensione come id
    return p.stem

def make_thumb(mp4: pathlib.Path, out_jpg: pathlib.Path) -> bool:
    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg","-y",
        "-ss","0.5","-i", str(mp4),
        "-frames:v","1","-q:v","3",
        "-vf","scale=512:-2",  # ridimensiona a 512px di larghezza
        str(out_jpg),
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return out_jpg.exists()
    except Exception as e:
        print("thumb fail:", mp4.name, e, file=sys.stderr)
        return False

def main():
    mp4s = sorted(VIDEO_DIR.glob("*.mp4"))
    ok = 0
    for mp4 in mp4s:
        vid = video_id_from_path(mp4)
        jpg = THUMB_DIR / f"{vid}.jpg"
        if jpg.exists(): 
            continue
        if make_thumb(mp4, jpg):
            ok += 1
    print(f"✓ Thumbnails generate: {ok}")

if __name__ == "__main__":
    main()
