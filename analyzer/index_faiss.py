from __future__ import annotations
import argparse
import json
import pathlib
import sqlite3
import yaml
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

# ===== SPRINT 2: FAISS Adapter with Dependency Injection =====

try:
    import faiss  # type: ignore
    _HAVE_FAISS = True
except Exception:
    _HAVE_FAISS = False


class IndexBackend:
    """Abstract interface for index backends"""
    def add(self, X: np.ndarray, ids=None): 
        raise NotImplementedError
    
    def search(self, q: np.ndarray, top_k: int = 5): 
        raise NotImplementedError
    
    def save(self, path: str): 
        raise NotImplementedError
    
    @classmethod
    def load(cls, path: str): 
        raise NotImplementedError


class FaissIndex(IndexBackend):
    """FAISS-based index backend"""
    def __init__(self, dim: int):
        if not _HAVE_FAISS:
            raise RuntimeError("FAISS not available")
        self.dim = dim
        self.idx = faiss.IndexFlatIP(dim)
        self.ids = None
    
    def add(self, X: np.ndarray, ids=None):
        # normalize for cosine via dot
        X = X.astype("float32")
        X /= np.clip(np.linalg.norm(X, axis=1, keepdims=True), 1e-12, None)
        self.idx.add(X)
        self.ids = ids if ids is not None else np.arange(X.shape[0])
    
    def search(self, q: np.ndarray, top_k: int = 5):
        if q.ndim == 1: 
            q = q[None, :]
        q = q.astype("float32")
        q /= np.clip(np.linalg.norm(q, axis=1, keepdims=True), 1e-12, None)
        D, I = self.idx.search(q, top_k)
        # map FAISS row ids back if provided
        if self.ids is not None:
            mapped = self.ids[I[0]]
        else:
            mapped = I[0]
        return mapped, D[0]
    
    def save(self, path: str):
        faiss.write_index(self.idx, path + ".faiss")
        # Save ids mapping if available
        if self.ids is not None:
            np.save(path + ".ids.npy", self.ids)
    
    @classmethod
    def load(cls, path: str):
        idx = faiss.read_index(path + ".faiss")
        obj = cls(idx.d)
        obj.idx = idx
        # Load ids mapping if available
        try:
            obj.ids = np.load(path + ".ids.npy")
        except FileNotFoundError:
            obj.ids = None
        return obj

def load_cfg():
    """Load configuration from settings.yaml"""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

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

def fetch_corpus_from_sqlite(db_path: str = "data/db.sqlite") -> list[tuple[str, str]]:
    """Fetch corpus from SQLite database with OCR text included"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Query modificata per includere OCR text
    cur.execute("""
        SELECT v.url,
               COALESCE(i.topic_micro || ' ' || i.hook || ' ' || IFNULL(i.ocr_text,''),
                        v.title)
        FROM videos v
        LEFT JOIN insights i ON i.video_url = v.url
        WHERE v.url IS NOT NULL
    """)
    
    rows = cur.fetchall()
    con.close()
    return rows

def build_text_index(corpus: list[tuple[str, str]], model_name: str, device: str, 
                    index_path: str, map_path: str, dimension: int = 384):
    """Build FAISS index for text corpus"""
    import faiss
    
    model = SentenceTransformer(model_name, device=device)
    
    # Generate embeddings
    texts = [row[1] for row in corpus]
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    embeddings = embeddings.astype(np.float32)
    
    # Create FAISS index
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    # Save index and mapping
    pathlib.Path(index_path).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, index_path)
    
    # Save URL mapping
    url_map = {i: row[0] for i, row in enumerate(corpus)}
    pathlib.Path(map_path).write_text(
        json.dumps(url_map, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    
    print(f"✓ Text index built: {len(corpus)} documents")
    print(f"  Index: {index_path}")
    print(f"  Map: {map_path}")

def main():
    """Main function for building text index"""
    parser = argparse.ArgumentParser(description="Build FAISS text index")
    parser.add_argument("--gpu", default="auto", help="GPU preference (auto/on/off)")
    parser.add_argument("--db", default="data/db.sqlite", help="Database path")
    
    args = parser.parse_args()
    
    cfg = load_cfg()
    device = device_from_pref(args.gpu)
    
    # Fetch corpus
    corpus = fetch_corpus_from_sqlite(args.db)
    if not corpus:
        print("Nessun documento trovato nel database")
        return
    
    # Build index
    build_text_index(
        corpus=corpus,
        model_name=cfg["search"]["model"],
        device=device,
        index_path=cfg["search"]["index_path"],
        map_path=cfg["search"]["map_path"],
        dimension=cfg["search"]["dimension"]
    )

if __name__ == "__main__":
    main()
