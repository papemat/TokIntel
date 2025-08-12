#!/usr/bin/env python
"""
Test locale dei workflow prima del push GitHub
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    print(f"🧪 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def test_prod_check_workflow():
    """Test del workflow prod-check"""
    print("\n🔍 Test Workflow: Prod Check")
    
    # Test 1: Verifica file workflow
    workflow_file = Path(".github/workflows/prod-check.yml")
    if not workflow_file.exists():
        print("❌ File workflow prod-check.yml non trovato")
        return False
    
    # Test 2: Verifica script dipendenti
    scripts = [
        "scripts/prod_check_report.py",
        "scripts/export_sample.py",
        "scripts/add_db_indexes.py"
    ]
    
    for script in scripts:
        if not Path(script).exists():
            print(f"❌ Script {script} non trovato")
            return False
    
    print("✅ Workflow prod-check: file e script verificati")
    return True

def test_perf_nightly_workflow():
    """Test del workflow perf-nightly"""
    print("\n🔍 Test Workflow: Perf Nightly")
    
    # Test 1: Verifica file workflow
    workflow_file = Path(".github/workflows/perf-nightly.yml")
    if not workflow_file.exists():
        print("❌ File workflow perf-nightly.yml non trovato")
        return False
    
    # Test 2: Verifica script dipendenti
    scripts = [
        "scripts/perf_bench.py",
        "scripts/perf_aggregate.py",
        "scripts/create_sample_db.py"
    ]
    
    for script in scripts:
        if not Path(script).exists():
            print(f"❌ Script {script} non trovato")
            return False
    
    # Test 3: Verifica dashboard
    dashboard_file = Path("dash/perf_dashboard.py")
    if not dashboard_file.exists():
        print("❌ Dashboard perf_dashboard.py non trovata")
        return False
    
    print("✅ Workflow perf-nightly: file e script verificati")
    return True

def test_requirements():
    """Test delle dipendenze"""
    print("\n🔍 Test Dipendenze")
    
    deps = ["matplotlib", "pandas", "streamlit", "pytest"]
    missing = []
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - MANCANTE")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Dipendenze mancanti: {', '.join(missing)}")
        print("Installa con: pip install " + " ".join(missing))
        return False
    
    return True

def test_dashboard():
    """Test della dashboard"""
    print("\n🔍 Test Dashboard")
    
    # Test 1: Verifica dati CSV
    csv_file = Path("reports/perf_history.csv")
    if not csv_file.exists():
        print("❌ File CSV storico non trovato")
        return False
    
    # Test 2: Verifica che CSV contenga dati
    try:
        import pandas as pd
        df = pd.read_csv(csv_file)
        if df.empty:
            print("⚠️  CSV vuoto - aggiungi dati demo")
        else:
            print(f"✅ CSV contiene {len(df)} record")
    except Exception as e:
        print(f"❌ Errore lettura CSV: {e}")
        return False
    
    return True

def main():
    print("🚀 Test Workflow Locali - TokIntel")
    print("=" * 50)
    
    tests = [
        test_requirements,
        test_prod_check_workflow,
        test_perf_nightly_workflow,
        test_dashboard
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Risultati: {passed}/{total} test passati")
    
    if passed == total:
        print("🎉 Tutti i test passati! Pronto per il push GitHub.")
        print("\n📋 Prossimi passi:")
        print("1. Crea repo su GitHub.com")
        print("2. git remote add origin https://github.com/TUO_USERNAME/TokIntel.git")
        print("3. git push -u origin main")
        print("4. Abilita GitHub Actions")
        return 0
    else:
        print("⚠️  Alcuni test falliti. Risolvi prima del push.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
