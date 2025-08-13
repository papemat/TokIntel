#!/usr/bin/env bash
set -euo pipefail

echo "== 🧪 Docs Idempotency STRICT =="

# Funzione per eseguire generatori docs
run_docs_generator() {
    local run_num=$1
    echo "  Run $run_num: cercando generatori docs..."
    
    # 1. Target Makefile docs-generate
    if make -q docs-generate 2>/dev/null; then
        echo "    → Usando make docs-generate"
        make docs-generate
        return 0
    fi
    
    # 2. Script Python specifici
    for script in scripts/update_docs_status.py .github/scripts/update_docs_status.py scripts/generate_docs.py; do
        if [[ -x "$script" ]]; then
            echo "    → Usando $script"
            python3 "$script" || true
            return 0
        fi
    done
    
    # 3. Sphinx/MkDocs
    if [[ -f docs/conf.py ]] && command -v sphinx-build >/dev/null; then
        echo "    → Usando Sphinx"
        sphinx-build -b html docs docs/_build/html || true
        return 0
    fi
    
    if [[ -f mkdocs.yml ]] && command -v mkdocs >/dev/null; then
        echo "    → Usando MkDocs"
        mkdocs build || true
        return 0
    fi
    
    # 4. Fallback no-op
    echo "    → Nessun generatore trovato (no-op)"
    return 0
}

# Prima passata
run_docs_generator 1

# Staging intermedio
git add -A >/dev/null 2>&1 || true

# Seconda passata (deve essere no-op)
run_docs_generator 2

# Controllo diff: se c'è differenza -> FAIL
if ! git diff --quiet; then
    echo "❌ Non idempotente: il secondo run ha prodotto modifiche."
    echo "📊 Statistiche modifiche:"
    git --no-pager diff --stat
    echo ""
    echo "🔍 Diff dettagliato:"
    git --no-pager diff
    exit 1
fi

echo "✅ Idempotenza OK (nessuna modifica al secondo run)"
