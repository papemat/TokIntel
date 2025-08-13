#!/usr/bin/env python3
"""
Aggiorna il badge Docs Ready nel README.md
Legge lo stato da docs/status.json e aggiorna il badge
"""
import json
import re
import sys
from pathlib import Path

def read_docs_status():
    """
    Legge lo stato dal file docs/status.json
    """
    status_file = Path('docs/status.json')
    
    if not status_file.exists():
        print("❌ File status.json non trovato")
        print("💡 Esegui prima: python scripts/update_docs_status.py passing")
        sys.exit(1)
    
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            status_data = json.load(f)
        return status_data.get('docs_ready', 'unknown')
    except Exception as e:
        print(f"❌ Errore nella lettura del file status: {e}")
        sys.exit(1)

def update_readme_badge(status):
    """
    Aggiorna il badge Docs Ready nel README.md
    """
    readme_file = Path('README.md')
    
    if not readme_file.exists():
        print("❌ README.md non trovato")
        sys.exit(1)
    
    # Leggi il contenuto del README
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Definisci i badge per ogni stato
    badges = {
        'passing': '[![Docs Ready](https://img.shields.io/badge/docs-ready-passing-brightgreen)](docs/status.json)',
        'failing': '[![Docs Ready](https://img.shields.io/badge/docs-ready-failing-red)](docs/status.json)',
        'unknown': '[![Docs Ready](https://img.shields.io/badge/docs-ready-unknown-gray)](docs/status.json)'
    }
    
    new_badge = badges.get(status, badges['unknown'])
    
    # Pattern per trovare il badge Docs Ready esistente
    badge_pattern = r'\[!\[Docs Ready\]\([^)]+\)\]\([^)]+\)'
    
    # Cerca se il badge esiste già
    if re.search(badge_pattern, content):
        # Sostituisci il badge esistente
        new_content = re.sub(badge_pattern, new_badge, content)
        print(f"✅ Badge Docs Ready aggiornato: {status}")
    else:
        # Aggiungi il badge dopo i badge esistenti (dopo la prima riga di badge)
        lines = content.split('\n')
        badge_inserted = False
        
        for i, line in enumerate(lines):
            if '![' in line and 'badge' in line and not badge_inserted:
                # Inserisci il badge dopo questa riga
                lines.insert(i + 1, new_badge)
                badge_inserted = True
                break
        
        if not badge_inserted:
            # Se non trova un posto adatto, aggiungi dopo il titolo
            for i, line in enumerate(lines):
                if line.startswith('# TokIntel'):
                    lines.insert(i + 2, new_badge)
                    break
        
        new_content = '\n'.join(lines)
        print(f"✅ Badge Docs Ready aggiunto: {status}")
    
    # Salva il README aggiornato
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"📄 README.md aggiornato")

def main():
    """
    Funzione principale
    """
    print("🔄 Aggiornamento badge Docs Ready...")
    
    # Leggi lo stato
    status = read_docs_status()
    print(f"📊 Status corrente: {status}")
    
    # Aggiorna il badge
    update_readme_badge(status)
    
    print("✅ Aggiornamento completato!")

if __name__ == "__main__":
    main()
