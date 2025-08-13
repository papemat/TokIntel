#!/usr/bin/env python3
"""
Monitor continuo per l'ecosistema CI/Visual TokIntel
Rilancia docs-check e e2e-smoke quando vengono modificati file rilevanti
"""
import time
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime
import threading

class CIVisualMonitor:
    def __init__(self, check_interval=5):
        self.check_interval = check_interval
        self.last_modified = {}
        self.running = True
        
        # File e directory da monitorare
        self.watch_paths = [
            'README.md',
            'docs/status.json',
            'docs/images/',
            'Makefile',
            'scripts/',
            'exports/'
        ]
        
        # Target da eseguire quando rileva modifiche
        self.targets = ['docs-check', 'e2e-smoke']
        
    def get_file_mtime(self, path):
        """Ottiene il timestamp di modifica di un file/directory"""
        try:
            if os.path.isfile(path):
                return os.path.getmtime(path)
            elif os.path.isdir(path):
                # Per le directory, controlla il file più recente
                max_mtime = 0
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            mtime = os.path.getmtime(file_path)
                            max_mtime = max(max_mtime, mtime)
                        except:
                            continue
                return max_mtime
        except:
            return 0
        return 0
    
    def check_for_changes(self):
        """Controlla se ci sono modifiche nei file monitorati"""
        changes = []
        
        for path in self.watch_paths:
            if not os.path.exists(path):
                continue
                
            current_mtime = self.get_file_mtime(path)
            last_mtime = self.last_modified.get(path, 0)
            
            if current_mtime > last_mtime:
                changes.append(path)
                self.last_modified[path] = current_mtime
        
        return changes
    
    def run_make_target(self, target):
        """Esegue un target make"""
        try:
            print(f"🔄 Esecuzione: make {target}")
            result = subprocess.run(
                ['make', target], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ {target} completato con successo")
                if result.stdout.strip():
                    print(f"📄 Output: {result.stdout.strip()}")
            else:
                print(f"❌ {target} fallito")
                if result.stderr.strip():
                    print(f"🚨 Errore: {result.stderr.strip()}")
                    
        except subprocess.TimeoutExpired:
            print(f"⏰ {target} timeout (30s)")
        except Exception as e:
            print(f"💥 Errore eseguendo {target}: {e}")
    
    def run_targets(self):
        """Esegue tutti i target configurati"""
        print(f"\n🎯 Esecuzione target dopo modifiche rilevate...")
        for target in self.targets:
            self.run_make_target(target)
        print("✅ Target completati\n")
    
    def monitor_loop(self):
        """Loop principale di monitoraggio"""
        print("🚀 Avvio monitor CI/Visual continuo...")
        print("📁 File monitorati:")
        for path in self.watch_paths:
            print(f"   - {path}")
        print(f"🎯 Target: {', '.join(self.targets)}")
        print(f"⏱️  Intervallo controllo: {self.check_interval}s")
        print("🛑 Premi Ctrl+C per fermare\n")
        
        # Inizializza timestamp
        for path in self.watch_paths:
            if os.path.exists(path):
                self.last_modified[path] = self.get_file_mtime(path)
        
        try:
            while self.running:
                changes = self.check_for_changes()
                
                if changes:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] 🔍 Modifiche rilevate in:")
                    for change in changes:
                        print(f"   📝 {change}")
                    
                    self.run_targets()
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitor fermato dall'utente")
            self.running = False
    
    def start(self):
        """Avvia il monitor"""
        self.monitor_loop()

def main():
    """Funzione principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor continuo CI/Visual TokIntel')
    parser.add_argument('--interval', '-i', type=int, default=5, 
                       help='Intervallo di controllo in secondi (default: 5)')
    parser.add_argument('--targets', '-t', nargs='+', 
                       default=['docs-check', 'e2e-smoke'],
                       help='Target make da eseguire (default: docs-check e2e-smoke)')
    
    args = parser.parse_args()
    
    monitor = CIVisualMonitor(check_interval=args.interval)
    monitor.targets = args.targets
    monitor.start()

if __name__ == "__main__":
    main()
