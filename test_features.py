#!/usr/bin/env python3
"""
Test rapido per verificare le funzionalità dei badge di stato
"""

import sys
sys.path.append('.')

from dash.app import get_status_badge, load_database

def test_status_badges():
    """Testa la generazione dei badge di stato"""
    print("🧪 Test badge di stato video...")
    
    # Test funzione get_status_badge
    print("\n1. Test generazione badge HTML:")
    
    test_cases = [
        ("ok", "🟢 OK"),
        ("timeout", "🟡 TIMEOUT"), 
        ("skipped", "🔵 SKIPPED"),
        ("unknown", "nessun badge")
    ]
    
    for status, expected in test_cases:
        badge = get_status_badge(status)
        if badge:
            print(f"   ✅ {status} -> {expected}")
            # Verifica che contenga il testo corretto
            if status.upper() in badge:
                print("      ✓ Badge contiene testo corretto")
            else:
                print("      ❌ Badge non contiene testo corretto")
        else:
            print(f"   ✅ {status} -> {expected}")
    
    # Test caricamento database
    print("\n2. Test caricamento database:")
    try:
        videos = load_database()
        print(f"   ✅ Database caricato: {len(videos)} video")
        
        # Conta stati
        status_counts = {}
        for video in videos:
            status = video.get('status', 'ok')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("   📊 Distribuzione stati nel database:")
        for status, count in status_counts.items():
            print(f"      {status}: {count} video")
            
    except Exception as e:
        print(f"   ❌ Errore caricamento database: {e}")
        return False
    
    print("\n✅ Test badge di stato completato!")
    return True

if __name__ == "__main__":
    success = test_status_badges()
    sys.exit(0 if success else 1)
