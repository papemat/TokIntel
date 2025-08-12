"""
Test script per verificare il funzionamento del dashboard
"""

import sys
import pathlib
import yaml

def test_imports():
    """Test che tutti i moduli necessari siano importabili"""
    print("🔍 Test import moduli...")
    
    try:
        import streamlit as st
        print("✅ Streamlit importato")
    except ImportError as e:
        print(f"❌ Errore import Streamlit: {e}")
        return False
    
    try:
        import faiss
        print("✅ FAISS importato")
    except ImportError as e:
        print(f"❌ Errore import FAISS: {e}")
        return False
    
    try:
        import torch
        print("✅ PyTorch importato")
    except ImportError as e:
        print(f"❌ Errore import PyTorch: {e}")
        return False
    
    return True

def test_config():
    """Test configurazione"""
    print("\n🔧 Test configurazione...")
    
    config_path = pathlib.Path("config/settings.yaml")
    if not config_path.exists():
        print("❌ config/settings.yaml non trovato")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
        print("✅ Configurazione caricata")
        
        # Verifica percorsi
        required_paths = [
            cfg["search"]["index_path"],
            cfg["search"]["map_path"],
            cfg["vision"]["image_index_path"],
            cfg["vision"]["image_map_path"]
        ]
        
        for path in required_paths:
            if pathlib.Path(path).exists():
                print(f"✅ {path} presente")
            else:
                print(f"⚠️  {path} mancante")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore configurazione: {e}")
        return False

def test_database():
    """Test database"""
    print("\n🗄️ Test database...")
    
    try:
        import sqlite3
        cfg = yaml.safe_load(open("config/settings.yaml", 'r', encoding='utf-8'))
        db_path = cfg["database"]["path"]
        
        if not pathlib.Path(db_path).exists():
            print("⚠️  Database non trovato")
            return True  # Non critico per il test
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT COUNT(*) FROM videos")
        count = cursor.fetchone()[0]
        print(f"✅ Database OK - {count} video trovati")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Errore database: {e}")
        return False

def test_dashboard_file():
    """Test file dashboard"""
    print("\n🎬 Test file dashboard...")
    
    dashboard_path = pathlib.Path("dash/app.py")
    if not dashboard_path.exists():
        print("❌ dash/app.py non trovato")
        return False
    
    try:
        # Test sintassi
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Compile test
        compile(code, 'dash/app.py', 'exec')
        print("✅ Sintassi dashboard OK")
        return True
        
    except Exception as e:
        print(f"❌ Errore sintassi dashboard: {e}")
        return False

def test_demo_images():
    """Test immagini demo"""
    print("\n🖼️ Test immagini demo...")
    
    demo_dir = pathlib.Path("demo_images")
    if not demo_dir.exists():
        print("⚠️  Directory demo_images non trovata")
        return True  # Non critico
    
    expected_images = ["yoga_breathing.jpg", "pilates_core.jpg", "marketing_conversion.jpg"]
    
    for img in expected_images:
        img_path = demo_dir / img
        if img_path.exists():
            print(f"✅ {img} presente")
        else:
            print(f"⚠️  {img} mancante")
    
    return True

def main():
    """Esegui tutti i test"""
    print("🎬 Test Dashboard TokIntel")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_database,
        test_dashboard_file,
        test_demo_images
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Errore durante test: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Risultati Test:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Test passati: {passed}/{total}")
    
    if passed == total:
        print("🎉 Tutti i test passati! Dashboard pronto.")
        print("\n🚀 Per avviare il dashboard:")
        print("   make dash")
        print("   # Poi apri http://localhost:8501")
    else:
        print("⚠️  Alcuni test falliti. Controlla la configurazione.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
