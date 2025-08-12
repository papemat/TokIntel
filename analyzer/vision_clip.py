from __future__ import annotations
import numpy as np
import pathlib
from PIL import Image
from sentence_transformers import SentenceTransformer
import torch

def device_from_pref(pref: str = "auto") -> str:
    """Determine device based on preference and availability"""
    p = (pref or "auto").lower()
    has = torch.cuda.is_available()
    
    if p == "on" and has:
        return "cuda"
    if p == "off":
        return "cpu"
    if p == "auto" and has:
        return "cuda"
    return "cpu"

def image_paths_to_embeddings(img_paths: list[str], model_name: str, device: str, 
                             batch_size: int = 32, normalize: bool = True) -> np.ndarray:
    """Generate embeddings for a list of image paths using CLIP model"""
    if not img_paths:
        return np.zeros((0, 512), dtype=np.float32)
    
    model = SentenceTransformer(model_name, device=device)
    
    # SentenceTransformer accetta direttamente path o PIL images
    embs = model.encode(
        img_paths, 
        batch_size=batch_size, 
        convert_to_numpy=True, 
        normalize_embeddings=normalize
    )
    
    return embs.astype(np.float32)

def pool_video_embedding(embs: np.ndarray) -> np.ndarray:
    """Pool multiple frame embeddings into a single video embedding"""
    if embs.size == 0:
        return np.zeros((1, embs.shape[1] if embs.ndim == 2 else 512), dtype=np.float32)
    
    return np.mean(embs, axis=0, keepdims=True).astype(np.float32)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate CLIP embeddings for images")
    parser.add_argument("images_dir", help="Directory containing images")
    parser.add_argument("--model", default="clip-ViT-B-32", help="CLIP model name")
    parser.add_argument("--device", default="auto", help="Device (auto/on/off)")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--normalize", action="store_true", help="Normalize embeddings")
    
    args = parser.parse_args()
    
    images_dir = pathlib.Path(args.images_dir)
    img_paths = sorted([str(p) for p in images_dir.glob("*.jpg")])
    
    device = device_from_pref(args.device)
    embs = image_paths_to_embeddings(
        img_paths, args.model, device, args.batch_size, args.normalize
    )
    
    print(f"✓ Embeddings generate: {embs.shape} su device {device}")
