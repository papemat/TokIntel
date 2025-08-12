from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable, List, Dict, Any, Optional, Tuple

# Tipi base
EmbeddingFn = Callable[[Iterable[Any]], List[List[float]]]
SingleEmbeddingFn = Callable[[Any], List[float]]

@dataclass
class OrchestratorConfig:
    k: int = 5
    weight_text: float = 0.6
    weight_visual: float = 0.4

def _sanitize_k(k: int, n: int) -> int:
    if n <= 0 or k <= 0:
        return 0
    return min(k, n)

def build_index(
    items: List[Dict[str, Any]],
    embedder_text: Optional[EmbeddingFn],
    embedder_image: Optional[EmbeddingFn],
    index_backend_factory: Callable[[int], Any],
    dim: int,
) -> Tuple[Any, List[Dict[str, Any]]]:
    """
    Crea backend di indice e ritorna (index_backend, items_enriched)
    Richiede: ogni item deve avere almeno 'id' e 'text' o 'image'
    """
    if not items:
        return index_backend_factory(dim), []

    # Calcolo embedding (deterministici in test)
    text_sources = [it.get("text") for it in items]
    img_sources = [it.get("image") for it in items]

    text_embs = embedder_text(text_sources) if embedder_text else None
    img_embs = embedder_image(img_sources) if embedder_image else None

    # Arricchisco gli item con embedding
    enriched = []
    for i, it in enumerate(items):
        e = dict(it)
        if text_embs is not None and text_embs[i] is not None:
            e["text_emb"] = text_embs[i]
        if img_embs is not None and img_embs[i] is not None:
            e["img_emb"] = img_embs[i]
        enriched.append(e)

    # Indicizzazione (usa solo le feature disponibili)
    backend = index_backend_factory(dim)
    vectors = []
    meta = []
    for ix, e in enumerate(enriched):
        vec = e.get("text_emb") or e.get("img_emb")
        if vec is None:
            continue
        vectors.append(vec)
        meta.append({"id": e["id"], "original_idx": ix})
    if vectors:
        backend.add(vectors, meta)
    return backend, enriched

def query_multimodal(
    backend: Any,
    items: List[Dict[str, Any]],
    text_query: Optional[Any],
    image_query: Optional[Any],
    text_embed_one: Optional[SingleEmbeddingFn],
    image_embed_one: Optional[SingleEmbeddingFn],
    cfg: OrchestratorConfig = OrchestratorConfig(),
) -> List[Dict[str, Any]]:
    """
    Esegue ricerca multimodale con pesi e merge stabile.
    Ritorna una lista di dict: {id, text_score, image_score, final_score, original_idx}
    """
    n = len(items)
    k = _sanitize_k(cfg.k, n)
    if k == 0 or n == 0:
        return []

    # Query embeddings
    text_qv = text_embed_one(text_query) if (text_query is not None and text_embed_one) else None
    img_qv = image_embed_one(image_query) if (image_query is not None and image_embed_one) else None

    # Se nessun canale disponibile → ritorna vuoto
    if text_qv is None and img_qv is None:
        return []

    # Query canali disponibili
    text_hits = backend.search(text_qv, k) if text_qv is not None else []
    img_hits = backend.search(img_qv, k) if img_qv is not None else []

    # Merge su id con max per canale
    merged: Dict[Any, Dict[str, Any]] = {}
    def _ingest(hits, kind):
        for rank, h in enumerate(hits):
            _id = h["id"]
            score = h["score"]
            orig = h.get("original_idx", -1)
            if _id not in merged:
                merged[_id] = {
                    "id": _id,
                    "text_score": 0.0,
                    "image_score": 0.0,
                    "original_idx": orig,
                }
            key = "text_score" if kind == "text" else "image_score"
            merged[_id][key] = max(merged[_id][key], float(score))

    _ingest(text_hits, "text")
    _ingest(img_hits, "image")

    # Final score
    results = []
    for v in merged.values():
        final_score = cfg.weight_text * v["text_score"] + cfg.weight_visual * v["image_score"]
        v["final_score"] = final_score
        results.append(v)

    # Ordinamento stabile: (-score, original_idx)
    results.sort(key=lambda r: (-r["final_score"], r.get("original_idx", 1_000_000)))
    return results[:k]


# Sprint 3: CLI interface
if __name__ == "__main__":
    import argparse
    import json
    import pandas as pd
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description="TokIntel Orchestrator CLI")
    parser.add_argument("--build", action="store_true", help="Build index from data")
    parser.add_argument("--query", type=str, help="Search query")
    parser.add_argument("--topk", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--export", type=str, help="Export path (without extension)")
    
    args = parser.parse_args()
    
    if args.query:
        # Simple mock search for CLI demo
        # In a real implementation, this would load actual indices and data
        mock_results = [
            {"id": f"result_{i}", "text_score": 0.9 - i*0.1, "image_score": 0.8 - i*0.1, 
             "final_score": 0.85 - i*0.1, "original_idx": i}
            for i in range(min(args.topk, 10))
        ]
        
        # Print results as JSON lines
        for result in mock_results:
            print(json.dumps(result))
        
        # Export if requested
        if args.export:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_path = f"{args.export}_{timestamp}.csv"
            json_path = f"{args.export}_{timestamp}.json"
            
            # CSV export
            df = pd.DataFrame(mock_results)
            df.to_csv(csv_path, index=False)
            
            # JSON export
            with open(json_path, "w") as f:
                json.dump(mock_results, f, indent=2)
            
            print(f"Export saved to {csv_path} and {json_path}")
    
    elif args.build:
        print("Building index... (mock implementation)")
        print("Index built successfully")
    
    else:
        parser.print_help()
