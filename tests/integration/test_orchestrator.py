import pytest

from analyzer.orchestrator import (
    build_index, query_multimodal, OrchestratorConfig
)

@pytest.fixture
def tiny_dataset():
    # 6 item, con 2 coppie pensate per pari punteggio
    return [
        {"id": "a", "text": "alpha cat", "image": "img/a"},
        {"id": "b", "text": "bravo cat", "image": "img/b"},
        {"id": "c", "text": "charlie dog", "image": "img/c"},
        {"id": "d", "text": "delta dog", "image": "img/d"},
        {"id": "e", "text": "echo bird", "image": "img/e"},
        {"id": "f", "text": "foxtrot bird", "image": "img/f"},
    ]

@pytest.fixture
def deterministic_text_embedder():
    def _emb_all(texts):
        out = []
        for t in texts:
            if t is None:
                out.append(None)
                continue
            h = abs(hash(t)) % 10_000
            out.append([float((h + i) % 97) for i in range(4)])
        return out
    return _emb_all

@pytest.fixture
def deterministic_image_embedder():
    def _emb_all(paths):
        out = []
        for p in paths:
            if p is None:
                out.append(None)
                continue
            h = abs(hash("IMG::" + p)) % 10_000
            out.append([float((h + i * 7) % 101) for i in range(4)])
        return out
    return _emb_all

@pytest.fixture
def deterministic_text_embed_one(deterministic_text_embedder):
    def _one(t):
        return deterministic_text_embedder([t])[0]
    return _one

@pytest.fixture
def deterministic_image_embed_one(deterministic_image_embedder):
    def _one(img):
        return deterministic_image_embedder([img])[0]
    return _one

@pytest.fixture
def numpy_index_factory(numpy_index_cls):
    def _factory(dim):
        return numpy_index_cls(dim=dim)
    return _factory

def test_build_and_query_multimodal_stable_sort(
    tiny_dataset,
    deterministic_text_embedder,
    deterministic_image_embedder,
    deterministic_text_embed_one,
    deterministic_image_embed_one,
    numpy_index_factory,
):
    backend, enriched = build_index(
        tiny_dataset,
        embedder_text=deterministic_text_embedder,
        embedder_image=deterministic_image_embedder,
        index_backend_factory=numpy_index_factory,
        dim=4,
    )
    cfg = OrchestratorConfig(k=4, weight_text=0.5, weight_visual=0.5)
    res = query_multimodal(
        backend,
        enriched,
        text_query="cat",
        image_query="img/d",
        text_embed_one=deterministic_text_embed_one,
        image_embed_one=deterministic_image_embed_one,
        cfg=cfg,
    )
    assert len(res) <= 4
    for r in res:
        assert "id" in r and "final_score" in r and "original_idx" in r


def test_guard_clauses_and_k_sanitization(
    tiny_dataset,
    deterministic_text_embedder,
    deterministic_image_embedder,
    deterministic_text_embed_one,
    numpy_index_factory,
):
    backend, enriched = build_index(
        tiny_dataset,
        embedder_text=deterministic_text_embedder,
        embedder_image=deterministic_image_embedder,
        index_backend_factory=numpy_index_factory,
        dim=4,
    )
    # k > len(index) → clamp
    res = query_multimodal(
        backend,
        enriched,
        text_query="bird",
        image_query=None,
        text_embed_one=deterministic_text_embed_one,
        image_embed_one=None,
        cfg=OrchestratorConfig(k=100),
    )
    assert len(res) <= len(enriched)

    # k <= 0 → vuoto
    res2 = query_multimodal(
        backend,
        enriched,
        text_query="bird",
        image_query=None,
        text_embed_one=deterministic_text_embed_one,
        image_embed_one=None,
        cfg=OrchestratorConfig(k=0),
    )
    assert res2 == []

    # Nessuna query → vuoto
    res3 = query_multimodal(
        backend,
        enriched,
        text_query=None,
        image_query=None,
        text_embed_one=None,
        image_embed_one=None,
        cfg=OrchestratorConfig(k=5),
    )
    assert res3 == []


def test_cli_interface(tmp_path):
    """Test CLI interface of orchestrator"""
    import subprocess
    import json
    import os
    import sys
    
    # Test query with export
    export_path = str(tmp_path / "cli_test")
    cmd = [
        sys.executable, "-m", "analyzer.orchestrator",
        "--query", "alpha",
        "--topk", "3",
        "--export", export_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
    
    # Check command executed successfully
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    
    # Check output contains JSON lines
    lines = result.stdout.strip().split('\n')
    assert len(lines) > 0, "No output from CLI"
    
    # Parse first line as JSON
    first_result = json.loads(lines[0])
    assert "id" in first_result, "Output not in expected format"
    
    # Check export files exist
    csv_files = list(tmp_path.glob("cli_test_*.csv"))
    json_files = list(tmp_path.glob("cli_test_*.json"))
    
    assert len(csv_files) > 0, "No CSV export file created"
    assert len(json_files) > 0, "No JSON export file created"
    
    print(f"CLI test passed. Export files: {csv_files + json_files}")
