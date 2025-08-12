#!/usr/bin/env python3
"""
Script per verificare il setup di TokIntel
"""

import sys
import pathlib
import importlib

# Add current directory to Python path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

def check_python_version():
    """Verifica versione Python"""
    print("🐍 Verifica versione Python...")
    if sys.version_info >= (3, 8):
        print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True
    else:
        print(f"  ✗ Python {sys.version_info.major}.{sys.version_info.minor} - Richiesto 3.8+")
        return False

def check_directories():
    """Verifica struttura directory"""
    print("\n📁 Verifica struttura directory...")
    required_dirs = [
        "config",
        "analyzer", 
        "downloader",
        "scripts",
        "tests",
        "data/frames",
        "data/ocr", 
        "data/indexes",
        "data/media/video"
    ]
    
    all_good = True
    for dir_path in required_dirs:
        if pathlib.Path(dir_path).exists():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} - Mancante")
            all_good = False
    
    return all_good

def check_files():
    """Verifica file essenziali"""
    print("\n📄 Verifica file essenziali...")
    required_files = [
        "requirements.txt",
        "config/settings.yaml",
        "Makefile",
        "README.md",
        "analyzer/__init__.py",
        "downloader/__init__.py",
        "tests/__init__.py"
    ]
    
    all_good = True
    for file_path in required_files:
        if pathlib.Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - Mancante")
            all_good = False
    
    return all_good

def check_modules():
    """Verifica moduli Python"""
    print("\n🔧 Verifica moduli Python...")
    modules = [
        "analyzer.frame_sampler",
        "analyzer.ocr_extractor", 
        "analyzer.vision_clip",
        "analyzer.build_visual_index",
        "analyzer.index_faiss",
        "analyzer.run_multimodal",
        "downloader.fetch_video"
    ]
    
    all_good = True
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ✗ {module} - {e}")
            all_good = False
    
    return all_good

def check_requirements():
    """Verifica dipendenze"""
    print("\n📦 Verifica dipendenze...")
    try:
        import yaml
        print("  ✓ PyYAML")
    except ImportError:
        print("  ✗ PyYAML - Installa con: pip install pyyaml")
        return False
    
    try:
        import numpy
        print("  ✓ NumPy")
    except ImportError:
        print("  ✗ NumPy - Installa con: pip install numpy")
        return False
    
    try:
        import PIL
        print("  ✓ Pillow")
    except ImportError:
        print("  ✗ Pillow - Installa con: pip install Pillow")
        return False
    
    return True

def main():
    """Funzione principale"""
    print("🔍 Verifica Setup TokIntel Multimodale")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_directories(),
        check_files(),
        check_modules(),
        check_requirements()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("✅ Setup TokIntel verificato con successo!")
        print("\n🎯 Prossimi passi:")
        print("  1. make setup          # Crea virtual environment")
        print("  2. make multimodal-demo # Esegui demo")
        print("  3. make help           # Vedi tutti i comandi")
    else:
        print("❌ Setup incompleto. Risolvi i problemi sopra indicati.")
        sys.exit(1)

if __name__ == "__main__":
    main()
