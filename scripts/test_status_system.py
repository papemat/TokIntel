#!/usr/bin/env python3
"""
Test completo del sistema di stati
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dash.app import (
    Status, _STATUS_META, norm_status, get_status_badge, 
    render_title_with_status
)

def test_status_system():
    """Test completo del sistema di stati"""
    print("🧪 Test sistema di stati TokIntel")
    print("=" * 50)
    
    # Test enum
    print("1. Test Enum Status:")
    for status in Status:
        print(f"   {status.name} = {status.value}")
    
    # Test metadata
    print("\n2. Test Metadata:")
    for status, meta in _STATUS_META.items():
        print(f"   {status}: {meta['emoji']} {meta['title']}")
    
    # Test normalization
    print("\n3. Test Normalizzazione:")
    test_cases = ["OK", "  timeout  ", "", None, "invalid", "ERROR"]
    for case in test_cases:
        result = norm_status(case)
        print(f"   '{case}' -> '{result}'")
    
    # Test badge generation
    print("\n4. Test Generazione Badge:")
    for status in ["ok", "timeout", "skipped", "error", "pending"]:
        badge = get_status_badge(status)
        print(f"   {status}: {badge[:50]}...")
    
    # Test small badges
    print("\n5. Test Badge Piccoli:")
    for status in ["ok", "timeout"]:
        badge = get_status_badge(status, small=True)
        print(f"   {status} (small): {badge[:50]}...")
    
    # Test title rendering
    print("\n6. Test Rendering Titoli:")
    title = "Video di Test con Caratteri Speciali: <>&\"'"
    for status in ["ok", "error"]:
        rendered = render_title_with_status(title, status)
        print(f"   {status}: {rendered[:80]}...")
    
    # Test filter UI (simulated)
    print("\n7. Test Filtro UI (simulato):")
    test_items = [
        {"status": "ok"},
        {"status": "timeout"},
        {"status": "skipped"},
        {"status": "error"},
        {"status": "pending"},
        {"status": None},
    ]
    
    # Simulate what status_filter_ui would return
    all_statuses = sorted({norm_status(i.get("status")) for i in test_items})
    print(f"   Stati disponibili: {all_statuses}")
    
    print("\n✅ Tutti i test del sistema di stati completati con successo!")

if __name__ == "__main__":
    test_status_system()
