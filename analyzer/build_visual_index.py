from __future__ import annotations
import argparse
import json
import os
import pathlib
import sqlite3
import yaml
import numpy as np

from .vision_clip import device_from_pref, image_paths_to_embeddings, pool_video_embedding
from .frame_sampler import sample_frames_ffmpeg

def load_cfg():
    """Load configuration from settings.yaml"""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_dirs(cfg):
    """Ensure required directories exist"""
    pathlib.Path(cfg["visual"]["frames_dir"]).mkdir(parents=True, exist_ok=True)
    pathlib.Path(cfg["vision"]["image_index_path"]).parent.mkdir(parents=True, exist_ok=True)

def video_file_for_url(url: str, video_dir: str) -> str | None:
    """Find video file for a given URL"""
    # yt-dlp salva come <id>.mp4; qui assumiamo che la parte finale dell'URL sia l'ID.
    vid = url.rstrip("/").split("/")[-1]
    
    for p in pathlib.Path(video_dir).glob(f"{vid}.*"):
        return str(p)
    
    # fallback: prendi qualunque mp4 presente (solo demo)
    cand = sorted(pathlib.Path(video_dir).glob("*.mp4"))
    return str(cand[0]) if cand else None

def demo_frames_for_url(url: str, frames_dir: str) -> list[str] | None:
    """For demo: get existing frames for a URL"""
    # Map URLs to demo frame directories
    url_to_vid = {
        "https://tiktok.com/@yoga_master/video/123": "vid_00000",
        "https://tiktok.com/@pilates_pro/video/456": "vid_00001", 
        "https://tiktok.com/@marketing_guru/video/789": "vid_00002"
    }
    
    vid_id = url_to_vid.get(url)
    if vid_id:
        vid_dir = pathlib.Path(frames_dir) / vid_id
        if vid_dir.exists():
            frames = sorted([str(p) for p in vid_dir.glob("*.jpg")])
            return frames if frames else None
    
    return None

def fetch_urls_from_db(db="data/db.sqlite") -> list[str]:
    """Fetch video URLs from database"""
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("SELECT url FROM videos WHERE url IS NOT NULL")
    rows = [r[0] for r in cur.fetchall()]
    con.close()
    return rows

def build_index(urls: list[str], cfg: dict, gpu_pref: str | None = None):
    """Build visual index for video URLs"""
    import faiss
    
    dev = device_from_pref(gpu_pref or cfg["compute"].get("gpu_mode", "auto"))
    vcfg, icfg = cfg["visual"], cfg["vision"]
    frames_root = pathlib.Path(vcfg["frames_dir"])
    video_dir = vcfg["video_dir"]

    model_name = icfg["clip_model"]
    bs = icfg["batch_size"]
    norm = bool(icfg["normalize"])
    D = icfg["image_dim"]
    
    embs_all = []
    id_map = {}

    for idx, url in enumerate(urls):
        # Try to get existing demo frames first
        frames = demo_frames_for_url(url, str(frames_root))
        
        if not frames:
            # Fallback to video processing
            vid_path = video_file_for_url(url, video_dir)
            if not vid_path:
                print(f"Video non trovato per URL: {url}")
                continue
                
            out_dir = frames_root / f"vid_{idx:05d}"
            frames = sample_frames_ffmpeg(
                vid_path, str(out_dir), 
                mode=vcfg["sampling_mode"], 
                fps=vcfg["fps"], 
                scene_threshold=vcfg["scene_threshold"], 
                max_frames=vcfg["max_frames"], 
                resize_width=vcfg["resize_width"]
            )
            
            if not frames:
                print(f"Nessun frame estratto per: {url}")
                continue
        
        e = image_paths_to_embeddings(frames, model_name, dev, batch_size=bs, normalize=norm)
        pooled = pool_video_embedding(e)  # (1, D)
        
        if pooled.shape[1] != D:
            # adattamento se il modello ha dim diverso
            pooled = np.resize(pooled, (1, D)).astype(np.float32)
            
        embs_all.append(pooled)
        id_map[len(id_map)] = url
        print(f"✓ Processato {url}: {len(frames)} frame")

    if not embs_all:
        print("Nessuna embedding visiva generata.")
        return

    mat = np.vstack(embs_all).astype(np.float32)
    index = faiss.IndexFlatIP(mat.shape[1])
    index.add(mat)

    # salva
    if "Gpu" in str(type(index)):  # safety
        index = faiss.index_gpu_to_cpu(index)
        
    faiss.write_index(index, icfg["image_index_path"])
    pathlib.Path(icfg["image_map_path"]).write_text(
        json.dumps(id_map, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    
    print(f"✓ Visual index: {icfg['image_index_path']}  |  map: {icfg['image_map_path']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build visual index for videos")
    parser.add_argument("--gpu", default="auto", help="GPU preference (auto/on/off)")
    parser.add_argument("--urls", nargs="+", help="Specific URLs to process")
    
    args = parser.parse_args()
    
    cfg = load_cfg()
    ensure_dirs(cfg)
    
    if args.urls:
        urls = args.urls
    else:
        urls = fetch_urls_from_db()
    
    if not urls:
        print("Nessuna URL trovata nel database. Usa --urls per specificare URL manualmente.")
        exit(1)
    
    build_index(urls, cfg, args.gpu)
