from __future__ import annotations
import argparse
import json
import yaml
from sentence_transformers import SentenceTransformer
import faiss

def load_cfg():
    """Load configuration from settings.yaml"""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def search_text(query: str, index_path: str, map_path: str, model_name: str, device: str = "cpu", top_k: int = 5, 
                index_backend=None, text_encoder=None):
    """Search in text index"""
    # Load index and mapping
    if index_backend is None:
        index = faiss.read_index(index_path)
    else:
        index = index_backend
    
    if map_path is not None:
        with open(map_path, 'r', encoding='utf-8') as f:
            url_map = json.load(f)
    else:
        # For testing, create a simple mapping
        url_map = {str(i): f"test_url_{i}" for i in range(1000)}
    
    # Encode query
    if text_encoder is None:
        model = SentenceTransformer(model_name, device=device)
        query_emb = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    else:
        query_emb = text_encoder([query])
    
    # Search
    if hasattr(index, 'search'):
        # Use our IndexBackend interface
        indices, scores = index.search(query_emb[0], min(top_k, len(url_map)))
    else:
        # Use FAISS interface
        scores, indices = index.search(query_emb, min(top_k, index.ntotal))
        indices = indices[0]
        scores = scores[0]
    
    results = []
    for score, idx in zip(scores, indices):
        if idx != -1:  # Valid result
            results.append({
                "url": url_map[str(idx)],
                "score": float(score),
                "type": "text"
            })
    
    return results

def search_visual(query: str, index_path: str, map_path: str, model_name: str, device: str = "cpu", top_k: int = 5,
                 index_backend=None, text_encoder=None):
    """Search in visual index using text query"""
    # Load index and mapping
    if index_backend is None:
        index = faiss.read_index(index_path)
    else:
        index = index_backend
    
    if map_path is not None:
        with open(map_path, 'r', encoding='utf-8') as f:
            url_map = json.load(f)
    else:
        # For testing, create a simple mapping
        url_map = {str(i): f"test_url_{i}" for i in range(1000)}
    
    # Encode query (CLIP can encode text queries)
    if text_encoder is None:
        model = SentenceTransformer(model_name, device=device)
        query_emb = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    else:
        query_emb = text_encoder([query])
    
    # Search
    if hasattr(index, 'search'):
        # Use our IndexBackend interface
        indices, scores = index.search(query_emb[0], min(top_k, len(url_map)))
    else:
        # Use FAISS interface
        scores, indices = index.search(query_emb, min(top_k, index.ntotal))
        indices = indices[0]
        scores = scores[0]
    
    results = []
    for score, idx in zip(scores, indices):
        if idx != -1:  # Valid result
            results.append({
                "url": url_map[str(idx)],
                "score": float(score),
                "type": "visual"
            })
    
    return results

def combine_results(text_results: list, visual_results: list, weight_text: float = 0.6, weight_visual: float = 0.4):
    """Combine text and visual search results"""
    # Create URL to results mapping
    combined = {}
    
    # Add text results
    for result in text_results:
        url = result["url"]
        if url in combined:
            # Keep the higher text score for duplicates
            combined[url]["text_score"] = max(combined[url]["text_score"], result["score"])
            combined[url]["combined_score"] = combined[url]["text_score"] * weight_text + combined[url]["visual_score"] * weight_visual
        else:
            combined[url] = {
                "url": url,
                "text_score": result["score"],
                "visual_score": 0.0,
                "combined_score": result["score"] * weight_text
            }
    
    # Add visual results
    for result in visual_results:
        url = result["url"]
        if url in combined:
            # Keep the higher visual score for duplicates
            combined[url]["visual_score"] = max(combined[url]["visual_score"], result["score"])
            combined[url]["combined_score"] = combined[url]["text_score"] * weight_text + combined[url]["visual_score"] * weight_visual
        else:
            combined[url] = {
                "url": url,
                "text_score": 0.0,
                "visual_score": result["score"],
                "combined_score": result["score"] * weight_visual
            }
    
    # Sort by combined score
    sorted_results = sorted(combined.values(), key=lambda x: x["combined_score"], reverse=True)
    return sorted_results

def main():
    """Main search function"""
    parser = argparse.ArgumentParser(description="Multimodal search in TokIntel")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--gpu", default="auto", help="GPU preference (auto/on/off)")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--weight-text", type=float, default=0.6, help="Weight for text search")
    parser.add_argument("--weight-visual", type=float, default=0.4, help="Weight for visual search")
    
    args = parser.parse_args()
    
    cfg = load_cfg()
    
    # Determine device
    import torch
    if args.gpu == "auto" and torch.cuda.is_available():
        device = "cuda"
    elif args.gpu == "on" and torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    
    print(f"🔍 Ricerca multimodale per: '{args.query}'")
    print(f"📱 Device: {device}")
    print()
    
    # Text search
    print("📝 Ricerca testuale...")
    text_results = search_text(
        args.query,
        cfg["search"]["index_path"],
        cfg["search"]["map_path"],
        cfg["search"]["model"],
        device,
        args.top_k
    )
    
    # Visual search
    print("🎬 Ricerca visiva...")
    visual_results = search_visual(
        args.query,
        cfg["vision"]["image_index_path"],
        cfg["vision"]["image_map_path"],
        cfg["vision"]["clip_model"],
        device,
        args.top_k
    )
    
    # Combine results
    print("🔄 Combinazione risultati...")
    combined_results = combine_results(
        text_results, visual_results, 
        args.weight_text, args.weight_visual
    )
    
    # Display results
    print(f"\n📊 Risultati (top {args.top_k}):")
    print("-" * 80)
    
    for i, result in enumerate(combined_results[:args.top_k], 1):
        print(f"{i}. {result['url']}")
        print(f"   Score combinato: {result['combined_score']:.3f}")
        print(f"   Score testuale: {result['text_score']:.3f}")
        print(f"   Score visivo: {result['visual_score']:.3f}")
        print()

if __name__ == "__main__":
    main()
