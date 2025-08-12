import numpy as np
import pytest

from tests.conftest import gen_embeds


def test_add_search_basic(np_index_factory, small_dataset):
    """Test basic add and search functionality"""
    X, q = small_dataset
    idx = np_index_factory(X.shape[1])
    ids = np.arange(len(X))
    idx.add(X, ids=ids)
    got_ids, scores = idx.search(q, top_k=3)
    assert len(got_ids) == 3
    assert scores.shape == (3,)
    assert got_ids[0] == ids[0]  # nearest is itself


def test_dim_mismatch(np_index_factory):
    """Test dimension mismatch error"""
    idx = np_index_factory(8)
    with pytest.raises(ValueError):
        idx.add(np.zeros((2, 16), dtype=np.float32))


def test_empty_index(np_index_factory):
    """Test search on empty index"""
    idx = np_index_factory(4)
    ids, scores = idx.search(np.zeros(4, dtype=np.float32), top_k=5)
    assert ids.size == 0 and scores.size == 0


def test_save_load_roundtrip(tmp_path, np_index_factory):
    """Test save/load roundtrip"""
    X = gen_embeds(n=5, d=8, seed=7)
    idx = np_index_factory(8)
    idx.add(X, ids=np.arange(5))
    path = str(tmp_path / "idx")
    idx.save(path)
    ld = type(idx).load(path + ".npz")
    q = X[2]
    a_ids, a_s = idx.search(q, top_k=3)
    b_ids, b_s = ld.search(q, top_k=3)
    np.testing.assert_array_equal(a_ids, b_ids)
    np.testing.assert_allclose(a_s, b_s, rtol=1e-6, atol=1e-6)


def test_cosine_similarity_correctness(np_index_factory):
    """Test that cosine similarity is computed correctly"""
    # Create orthogonal vectors
    X = np.array([[1, 0], [0, 1], [0.707, 0.707]], dtype=np.float32)
    idx = np_index_factory(2)
    idx.add(X, ids=np.arange(3))
    
    # Query with first vector
    q = np.array([1, 0], dtype=np.float32)
    ids, scores = idx.search(q, top_k=3)
    
    # Should find exact match first
    assert ids[0] == 0
    assert np.isclose(scores[0], 1.0, atol=1e-6)
    
    # Third vector should have score ~0.707
    assert ids[1] == 2
    assert np.isclose(scores[1], 0.707, atol=1e-3)


def test_multiple_add_calls(np_index_factory):
    """Test adding data in multiple calls"""
    idx = np_index_factory(4)
    
    # First batch
    X1 = gen_embeds(n=3, d=4, seed=1)
    idx.add(X1, ids=np.arange(3))
    
    # Second batch
    X2 = gen_embeds(n=2, d=4, seed=2)
    idx.add(X2, ids=np.arange(3, 5))
    
    # Search
    q = X1[0]
    ids, scores = idx.search(q, top_k=5)
    assert len(ids) == 5
    assert ids[0] == 0  # Should find the query vector first


def test_top_k_limits(np_index_factory, small_dataset):
    """Test that top_k limits are respected"""
    X, q = small_dataset
    idx = np_index_factory(X.shape[1])
    idx.add(X, ids=np.arange(len(X)))
    
    # Request more than available
    ids, scores = idx.search(q, top_k=20)
    assert len(ids) == len(X)  # Should return all available
    
    # Request less than available
    ids, scores = idx.search(q, top_k=2)
    assert len(ids) == 2


def test_stable_sorting(np_index_factory):
    """Test that sorting is stable for equal scores"""
    # Create vectors with same similarity
    X = np.array([[1, 0], [1, 0], [1, 0]], dtype=np.float32)
    idx = np_index_factory(2)
    idx.add(X, ids=np.array([5, 3, 1]))  # Different order
    
    q = np.array([1, 0], dtype=np.float32)
    ids, scores = idx.search(q, top_k=3)
    
    # Should maintain original order for equal scores
    assert np.allclose(scores, 1.0, atol=1e-6)
    # IDs should be in original order: [5, 3, 1]
    np.testing.assert_array_equal(ids, np.array([5, 3, 1]))


def test_normalization_handling(np_index_factory):
    """Test that normalization is handled correctly"""
    # Create unnormalized vectors
    X = np.array([[2, 0], [0, 3], [4, 4]], dtype=np.float32)
    idx = np_index_factory(2)
    idx.add(X, ids=np.arange(3))
    
    # Query with unnormalized vector
    q = np.array([6, 0], dtype=np.float32)
    ids, scores = idx.search(q, top_k=3)
    
    # Should still work correctly (normalization happens internally)
    assert len(ids) == 3
    assert scores[0] > scores[1]  # [2,0] should be more similar than [0,3]
