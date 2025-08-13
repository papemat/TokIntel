#!/usr/bin/env python3
"""
Monitor Python Matrix Summary
Analizza monitor_history.json per mostrare quale versione Python ha performato meglio.
"""

import json
import pathlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional

def analyze_python_matrix_performance() -> Optional[str]:
    """Analizza le ultime run per determinare quale Python ha performato meglio."""
    hist_path = pathlib.Path("docs/monitor_history.json")
    if not hist_path.exists():
        return None
    
    try:
        with open(hist_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return None
    
    runs = data.get('runs', [])
    if not runs:
        return None
    
    # Analizza le ultime 10 run per trovare matrix runs
    matrix_runs = []
    for run in runs[:10]:
        # Cerca run che sembrano essere parte di una matrix
        if 'run_url' in run and 'matrix' in run.get('run_url', '').lower():
            matrix_runs.append(run)
    
    if not matrix_runs:
        return None
    
    # Analizza performance (per ora semplificato)
    latest = matrix_runs[0]
    result = latest.get('result', 'unknown')
    targets = latest.get('targets', 'unknown')
    run_url = latest.get('run_url', '')
    
    # Determina emoji e messaggio
    if result.lower() == 'success':
        emoji = "🟢"
        status = "SUCCESS"
    elif result.lower() == 'neutral':
        emoji = "🟡"
        status = "NEUTRAL"
    else:
        emoji = "🔴"
        status = "FAILED"
    
    return f"{emoji} **Matrix Python 3.10/3.11**: {status} | `{targets}` | [run]({run_url})"

def update_readme_with_matrix_summary():
    """Aggiorna il README con il riassunto della matrix Python."""
    summary = analyze_python_matrix_performance()
    if not summary:
        print("ℹ️ Nessuna run matrix trovata")
        return
    
    readme_path = pathlib.Path("README.md")
    if not readme_path.exists():
        print("❌ README.md non trovato")
        return
    
    try:
        content = readme_path.read_text(encoding='utf-8')
    except:
        print("❌ Errore lettura README.md")
        return
    
    # Cerca la sezione monitor e aggiungi il riassunto matrix
    monitor_section = "## 📈 Ultimi esiti monitor"
    if monitor_section in content:
        # Inserisci dopo la sezione monitor
        lines = content.split('\n')
        new_lines = []
        matrix_added = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip() == monitor_section and not matrix_added:
                # Aggiungi il riassunto matrix dopo la sezione
                new_lines.append("")
                new_lines.append(f"> {summary}")
                new_lines.append("")
                matrix_added = True
        
        if matrix_added:
            readme_path.write_text('\n'.join(new_lines), encoding='utf-8')
            print(f"✅ README aggiornato con: {summary}")
        else:
            print("ℹ️ Sezione monitor non trovata per l'aggiornamento")
    else:
        print("ℹ️ Sezione monitor non trovata")

if __name__ == "__main__":
    update_readme_with_matrix_summary()
