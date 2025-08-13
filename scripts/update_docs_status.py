#!/usr/bin/env python3
"""
Aggiorna lo stato del sistema Docs Ready
Uso: python scripts/update_docs_status.py [passing|failing]
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

def update_docs_status(status):
    """
    Aggiorna lo stato del sistema Docs Ready
    """
    if status not in ['passing', 'failing']:
        print(f"❌ Status non valido: {status}")
        print("💡 Uso: python scripts/update_docs_status.py [passing|failing]")
        sys.exit(1)
    
    # Crea directory docs se non esiste
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Percorso del file status
    status_file = docs_dir / 'status.json'
    
    # Dati dello stato
    status_data = {
        'docs_ready': status,
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'updated_by': 'docs-ready-workflow'
    }
    
    # Salva il file
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Status Docs Ready aggiornato: {status}")
    print(f"📄 File salvato: {status_file}")
    
    return status_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Argomento mancante")
        print("💡 Uso: python scripts/update_docs_status.py [passing|failing]")
        sys.exit(1)
    
    status = sys.argv[1]
    update_docs_status(status)
