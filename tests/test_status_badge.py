"""
Test for status badge system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dash.app import get_status_badge, norm_status, Status

def test_badge_contains_data_status():
    """Test that badges contain data-status attribute"""
    html = get_status_badge("ok")
    assert 'data-status="ok"' in html
    assert "✅" in html

def test_badge_contains_emoji():
    """Test that badges contain correct emojis"""
    html = get_status_badge("timeout")
    assert "🟡" in html
    
    html = get_status_badge("skipped")
    assert "🔵" in html
    
    html = get_status_badge("error")
    assert "🔴" in html

def test_norm_status():
    """Test status normalization"""
    assert norm_status("OK") == "ok"
    assert norm_status("  timeout  ") == "timeout"
    assert norm_status("") == "pending"
    assert norm_status(None) == "pending"
    assert norm_status("invalid") == "pending"

def test_small_badge():
    """Test small badge variant"""
    html = get_status_badge("ok", small=True)
    assert "2px 6px" in html  # smaller padding
    assert "11px" in html     # smaller font

def test_large_badge():
    """Test large badge variant"""
    html = get_status_badge("ok", small=False)
    assert "3px 8px" in html  # larger padding
    assert "12px" in html     # larger font

if __name__ == "__main__":
    # Run tests
    test_badge_contains_data_status()
    test_badge_contains_emoji()
    test_norm_status()
    test_small_badge()
    test_large_badge()
    print("✅ All status badge tests passed!")
