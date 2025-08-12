import numpy as np

from tests.conftest import gen_embeds


D = 16
D_EMB = 16


def _fixed_img_encoder(paths):
    """Fixed image encoder for testing"""
    # return one embedding per path
    X = np.stack([np.full(D_EMB, 0.1 * (i+1), dtype=np.float32) for i, _ in enumerate(paths)], axis=0)
    # L2 normalize
    X /= np.clip(np.linalg.norm(X, axis=1, keepdims=True), 1e-12, None)
    return X


def _fixed_txt_encoder(text):
    """Fixed text encoder for testing"""
    v = np.full(D_EMB, 0.5, dtype=np.float32)
    v /= np.linalg.norm(v)
    return v[None, :]


def test_rank_and_topk(np_index_factory):
    """Test ranking and top-k functionality"""
    # Build index with deterministic items (as if from images)
    items = [f"img_{i}.jpg" for i in range(6)]
    X = _fixed_img_encoder(items)
    idx = np_index_factory(D_EMB)
    idx.add(X, ids=np.arange(len(items)))
    
    # Query from text
    q = _fixed_txt_encoder("query")[0]
    ids, scores = idx.search(q, top_k=3)
    assert ids.shape == (3,)
    assert (scores[:-1] >= scores[1:]).all()  # Scores should be decreasing


def test_threshold_filter(np_index_factory):
    """Test threshold filtering behavior"""
    items = [f"a{i}.jpg" for i in range(4)]
    X = _fixed_img_encoder(items)
    idx = np_index_factory(D_EMB)
    idx.add(X, ids=np.arange(len(items)))
    q = _fixed_txt_encoder("x")[0]
    ids, scores = idx.search(q, top_k=10)
    
    # simulate thresholding client-side to validate behavior
    mask = scores >= (scores.max() - 1e-6)
    ids = ids[mask]
    assert len(ids) >= 1


def test_search_text_with_di(np_index_factory):
    """Test search_text with dependency injection"""
    from analyzer.search_multimodal import search_text
    
    # Create test index
    X = gen_embeds(n=5, d=D_EMB, seed=42)
    idx = np_index_factory(D_EMB)
    idx.add(X, ids=np.arange(5))
    
    # Test with DI
    results = search_text(
        query="test query",
        index_path="",  # Not used with DI
        map_path=None,  # Use test mapping
        model_name="",  # Not used with DI
        device="cpu",
        top_k=3,
        index_backend=idx,
        text_encoder=_fixed_txt_encoder
    )
    
    assert len(results) == 3
    assert all(r["type"] == "text" for r in results)
    assert all("score" in r for r in results)
    assert all("url" in r for r in results)


def test_search_visual_with_di(np_index_factory):
    """Test search_visual with dependency injection"""
    from analyzer.search_multimodal import search_visual
    
    # Create test index
    X = gen_embeds(n=5, d=D_EMB, seed=42)
    idx = np_index_factory(D_EMB)
    idx.add(X, ids=np.arange(5))
    
    # Test with DI
    results = search_visual(
        query="test query",
        index_path="",  # Not used with DI
        map_path=None,  # Use test mapping
        model_name="",  # Not used with DI
        device="cpu",
        top_k=3,
        index_backend=idx,
        text_encoder=_fixed_txt_encoder
    )
    
    assert len(results) == 3
    assert all(r["type"] == "visual" for r in results)
    assert all("score" in r for r in results)
    assert all("url" in r for r in results)


def test_combine_results():
    """Test result combination logic"""
    from analyzer.search_multimodal import combine_results
    
    # Create test results
    text_results = [
        {"url": "url1", "score": 0.8, "type": "text"},
        {"url": "url2", "score": 0.6, "type": "text"}
    ]
    visual_results = [
        {"url": "url1", "score": 0.7, "type": "visual"},
        {"url": "url3", "score": 0.9, "type": "visual"}
    ]
    
    # Combine with default weights
    combined = combine_results(text_results, visual_results)
    
    assert len(combined) == 3  # url1, url2, url3
    
    # url1 should be first (highest combined score)
    assert combined[0]["url"] == "url1"
    assert combined[0]["text_score"] == 0.8
    assert combined[0]["visual_score"] == 0.7
    assert combined[0]["combined_score"] == 0.8 * 0.6 + 0.7 * 0.4
    
    # Check sorting
    scores = [r["combined_score"] for r in combined]
    assert scores == sorted(scores, reverse=True)


def test_combine_results_custom_weights():
    """Test result combination with custom weights"""
    from analyzer.search_multimodal import combine_results
    
    text_results = [{"url": "url1", "score": 0.5, "type": "text"}]
    visual_results = [{"url": "url1", "score": 0.5, "type": "visual"}]
    
    # Equal weights
    combined = combine_results(text_results, visual_results, 0.5, 0.5)
    assert combined[0]["combined_score"] == 0.5 * 0.5 + 0.5 * 0.5 == 0.5
    
    # Text only
    combined = combine_results(text_results, visual_results, 1.0, 0.0)
    assert combined[0]["combined_score"] == 0.5 * 1.0 + 0.5 * 0.0 == 0.5
    
    # Visual only
    combined = combine_results(text_results, visual_results, 0.0, 1.0)
    assert combined[0]["combined_score"] == 0.5 * 0.0 + 0.5 * 1.0 == 0.5


def test_empty_results_handling():
    """Test handling of empty result sets"""
    from analyzer.search_multimodal import combine_results
    
    # Empty text results
    combined = combine_results([], [{"url": "url1", "score": 0.5, "type": "visual"}])
    assert len(combined) == 1
    assert combined[0]["text_score"] == 0.0
    
    # Empty visual results
    combined = combine_results([{"url": "url1", "score": 0.5, "type": "text"}], [])
    assert len(combined) == 1
    assert combined[0]["visual_score"] == 0.0
    
    # Both empty
    combined = combine_results([], [])
    assert len(combined) == 0


def test_duplicate_url_handling():
    """Test handling of duplicate URLs in results"""
    from analyzer.search_multimodal import combine_results
    
    text_results = [
        {"url": "url1", "score": 0.8, "type": "text"},
        {"url": "url1", "score": 0.6, "type": "text"}  # Duplicate
    ]
    visual_results = [
        {"url": "url1", "score": 0.7, "type": "visual"}
    ]
    
    combined = combine_results(text_results, visual_results)
    
    # Should only have one entry for url1
    assert len(combined) == 1
    assert combined[0]["url"] == "url1"
    # Should use the higher text score
    assert combined[0]["text_score"] == 0.8
    assert combined[0]["visual_score"] == 0.7


def test_score_threshold_simulation(np_index_factory):
    """Test score threshold behavior simulation"""
    # Create index with varying similarity scores
    X = np.array([
        [1, 0, 0, 0],  # High similarity
        [0.5, 0.5, 0, 0],  # Medium similarity
        [0, 0, 1, 0],  # Low similarity
    ], dtype=np.float32)
    idx = np_index_factory(4)
    idx.add(X, ids=np.arange(3))
    
    # Query
    q = np.array([1, 0, 0, 0], dtype=np.float32)
    ids, scores = idx.search(q, top_k=3)
    
    # Apply threshold
    threshold = 0.7
    mask = scores >= threshold
    filtered_ids = ids[mask]
    filtered_scores = scores[mask]
    
    # Should only keep high similarity results
    assert len(filtered_ids) >= 1
    assert all(s >= threshold for s in filtered_scores)
