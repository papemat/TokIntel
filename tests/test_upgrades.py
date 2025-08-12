"""
Test for all upgrade features
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dash.app import (
    sort_videos, get_state, _STATUS_RANK, _STATUS_META,
    norm_status, get_status_badge
)

def test_sort_videos():
    """Test intelligent video sorting"""
    videos = [
        {"title": "Video A", "status": "ok"},
        {"title": "Video B", "status": "error"},
        {"title": "Video C", "status": "pending"},
        {"title": "Video D", "status": "timeout"},
    ]
    
    sorted_videos = sort_videos(videos)
    
    # Should be sorted by status rank then by title
    expected_order = ["error", "pending", "timeout", "ok"]
    actual_order = [v["status"] for v in sorted_videos]
    
    assert actual_order == expected_order, f"Expected {expected_order}, got {actual_order}"
    
    # Test title sorting within same status
    videos_same_status = [
        {"title": "Zebra", "status": "ok"},
        {"title": "Alpha", "status": "ok"},
    ]
    sorted_same = sort_videos(videos_same_status)
    assert sorted_same[0]["title"] == "Alpha"
    assert sorted_same[1]["title"] == "Zebra"

def test_status_ranking():
    """Test status ranking system"""
    assert _STATUS_RANK["error"] == 0
    assert _STATUS_RANK["pending"] == 1
    assert _STATUS_RANK["timeout"] == 2
    assert _STATUS_RANK["skipped"] == 3
    assert _STATUS_RANK["ok"] == 4

def test_strong_validation():
    """Test strong validation in norm_status"""
    # Test various inputs
    assert norm_status("OK") == "ok"
    assert norm_status("  timeout  ") == "timeout"
    assert norm_status("") == "pending"
    assert norm_status(None) == "pending"
    assert norm_status("invalid") == "pending"
    assert norm_status("ERROR") == "error"

def test_badge_hover_attributes():
    """Test that badges have hover attributes"""
    badge = get_status_badge("ok")
    assert 'data-status="ok"' in badge
    assert 'transition:' in badge or 'transform' in badge

def test_metadata_completeness():
    """Test that all statuses have complete metadata"""
    for status, meta in _STATUS_META.items():
        assert "emoji" in meta
        assert "bg" in meta
        assert "fg" in meta
        assert "title" in meta
        assert len(meta["emoji"]) > 0
        assert meta["bg"].startswith("#")
        assert meta["fg"] in ["white", "black"]

def test_auto_layout_metrics():
    """Test that metrics can be auto-layout"""
    # This tests the logic for auto-layout metrics
    status_count = len(_STATUS_META)
    assert status_count == 5  # ok, timeout, skipped, error, pending
    
    # Test that all statuses have metadata for metrics
    for status in _STATUS_META.keys():
        meta = _STATUS_META[status]
        assert "emoji" in meta
        assert "title" in meta

def test_sort_stable():
    """Test stable sorting with tie-breaker"""
    videos = [
        {"id": 2, "title": "A", "status": "ok"},
        {"id": 1, "title": "A", "status": "ok"},
        {"id": 3, "title": "A", "status": "pending"},
    ]
    out = sort_videos(videos)
    # pending prima, poi OK per id crescente
    assert [v["id"] for v in out] == [3, 1, 2]

def test_status_normalization():
    """Test status normalization edge cases"""
    videos = [{"status": "  OK  "}, {"status": "Weird"}]
    # simula normalizzazione
    normed = [(v.get("status") or "").strip().lower() in _STATUS_META for v in videos]
    assert normed == [True, False]

def test_persistence_logic():
    """Test persistence logic (simulated)"""
    # Simulate session state
    session_state = {}
    
    def mock_get_state(key, default):
        if key not in session_state:
            session_state[key] = default
        return session_state[key]
    
    # Test initial state
    result = mock_get_state("test_key", "default_value")
    assert result == "default_value"
    assert session_state["test_key"] == "default_value"
    
    # Test persistence
    session_state["test_key"] = "new_value"
    result = mock_get_state("test_key", "default_value")
    assert result == "new_value"

def test_safe_status():
    """Test safe status function"""
    from dash.app import safe_status
    
    # Test various inputs
    assert safe_status({"status": "ok"}) == "ok"
    assert safe_status({"status": "  TIMEOUT  "}) == "timeout"
    assert safe_status({"status": None}) == "pending"
    assert safe_status({"status": "invalid"}) == "pending"
    assert safe_status({}) == "pending"

if __name__ == "__main__":
    print("🧪 Test upgrade features...")
    
    test_sort_videos()
    print("✅ Video sorting test passed")
    
    test_status_ranking()
    print("✅ Status ranking test passed")
    
    test_strong_validation()
    print("✅ Strong validation test passed")
    
    test_badge_hover_attributes()
    print("✅ Badge hover attributes test passed")
    
    test_metadata_completeness()
    print("✅ Metadata completeness test passed")
    
    test_auto_layout_metrics()
    print("✅ Auto-layout metrics test passed")
    
    test_sort_stable()
    print("✅ Stable sorting test passed")
    
    test_status_normalization()
    print("✅ Status normalization test passed")
    
    test_persistence_logic()
    print("✅ Persistence logic test passed")
    
    test_safe_status()
    print("✅ Safe status test passed")
    
    print("🎉 All upgrade tests passed!")
