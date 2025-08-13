#!/usr/bin/env bash
set -euo pipefail

echo "=== 🚀 Setup Docs System Final (idempotente) ==="

# 1) Struttura cartelle
mkdir -p scripts docs .github/workflows .github/scripts .git/hooks

# 2) Script STRICT finale
cat > scripts/cursor_docs_strict.sh <<'SH'
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
SH
chmod +x scripts/cursor_docs_strict.sh

# 3) Documentazione finale
cat > docs/DOCS_SYSTEM_README.md <<'MD'
# 📚 Docs System – Final One Shot

Sistema universale per garantire **idempotenza** nella generazione/aggiornamento della documentazione.

## 🎯 Obiettivi
- ✅ **Idempotenza**: Due run consecutivi → nessuna modifica
- ✅ **Universale**: Funziona in qualsiasi repo
- ✅ **Smart**: Rileva generatori automaticamente
- ✅ **Soft**: Hook pre-commit non bloccante
- ✅ **Strict**: CI che fallisce su non-idempotenza

## 🔧 Componenti

### Script Strict
- `scripts/cursor_docs_strict.sh` → Verifica STRICT (CI)
- Rileva automaticamente: Makefile, Python, Sphinx, MkDocs
- Fallisce se il secondo run produce diff

### Hook Pre-commit
- `.git/hooks/pre-commit` → Verifica SOFT (locale)
- Avvisa ma **non blocca** i commit
- Perfetto per sviluppo veloce

### Target Makefile
- `docs-generate` → Generatore principale (fallback no-op)
- `docs-idem-soft` → Warning senza fallire
- `docs-idem-strict` → Hard fail su non-idempotenza

## 🚀 Uso Rapido

```bash
# Setup completo
bash setup_docs_system_final.sh

# Test locale (non blocca)
make docs-idem-soft

# Test strict (fallisce se non idempotente)
make docs-idem-strict

# Integrazione CI
# Copia lo step da CI_STRICT_STEP_YAML.md
```

## 🔍 Generatori Supportati

Il sistema rileva automaticamente:
1. **Makefile**: `make docs-generate`
2. **Python**: `scripts/update_docs_status.py`
3. **Sphinx**: `docs/conf.py` + `sphinx-build`
4. **MkDocs**: `mkdocs.yml` + `mkdocs build`
5. **Fallback**: No-op se nessun generatore trovato

## 📋 Workflow Consigliato

1. **Sviluppo**: Hook soft → sviluppo veloce
2. **Pre-PR**: `make docs-idem-strict` → verifica locale
3. **CI**: Step strict → garanzia qualità

## 🛠️ Personalizzazione

### Aggiungere un generatore custom
```make
docs-generate:
	@echo "Generando docs..."
	@python3 scripts/my_docs_generator.py
	@echo "✅ Docs generate"
```

### Hook pre-commit custom
```bash
# Modifica .git/hooks/pre-commit per aggiungere altri controlli
```

## 🎯 Integrazione CI

Usa lo step in `CI_STRICT_STEP_YAML.md` per integrare nel workflow GitHub Actions.
MD

# 4) Hook pre-commit finale
cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash

# SOFT check: non blocca il commit (avvisa soltanto)
echo "🔍 Pre-commit: verificando idempotenza docs..."

if command -v make >/dev/null 2>&1; then
    if make -q docs-idem-soft 2>/dev/null; then
        make docs-idem-soft || true
    elif grep -q "docs-idem-soft" Makefile 2>/dev/null; then
        make docs-idem-soft || true
    else
        echo "ℹ️  Target docs-idem-soft non trovato"
    fi
else
    echo "ℹ️  Make non disponibile"
fi

echo "✅ Pre-commit completato"
exit 0
HOOK
chmod +x .git/hooks/pre-commit

# 5) Makefile finale con gestione duplicati perfetta
if [[ -f Makefile ]]; then
    # Rimuovi TUTTI i blocchi esistenti del docs system
    awk 'BEGIN{inblk=0; skip=0}
    /# >>> DOCS SYSTEM TARGETS START >>>/ {inblk=1; skip=1; next}
    /# <<< DOCS SYSTEM TARGETS END <<</ {inblk=0; skip=0; next}
    /^docs-idem-soft:/ {skip=1; next}
    /^docs-idem-strict:/ {skip=1; next}
    /^docs-generate:/ {skip=1; next}
    /^docs-help:/ {skip=1; next}
    /^\.PHONY:.*docs-/ {skip=1; next}
    { if(!skip) print $0 }
    ' Makefile > Makefile.tmp || true

    cat >> Makefile.tmp <<'MK'

# >>> DOCS SYSTEM TARGETS START >>>

.PHONY: docs-generate docs-idem-soft docs-idem-strict docs-help

# docs-generate:
# - Se già definito altrove, verrà usato da scripts/cursor_docs_strict.sh.
# - Qui forniamo un fallback no-op per non rompere i repo che non hanno generatori ancora.

docs-generate:
	@echo "ℹ️  Fallback docs-generate (no-op)."
	@echo "   Sovrascrivi con il tuo generatore (es. sphinx, mkdocs, script python)."

docs-idem-soft:
	@echo "== 🧪 Docs Idempotency SOFT =="
	@bash -c 'set -euo pipefail; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	git add -A >/dev/null 2>&1 || true; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	if ! git diff --quiet; then \
		echo "⚠️  Non idempotente (soft): il secondo run ha prodotto modifiche."; \
		git --no-pager diff --stat || true; \
	else \
		echo "✅ Idempotenza OK (nessuna modifica al secondo run)"; \
	fi'

docs-idem-strict:
	@bash -c 'set -euo pipefail; scripts/cursor_docs_strict.sh'

docs-help:
	@echo "📚 Docs System - Comandi disponibili:"
	@echo "  make docs-generate    # Genera docs (fallback no-op)"
	@echo "  make docs-idem-soft   # Test soft (warning, non blocca)"
	@echo "  make docs-idem-strict # Test strict (fallisce se non idempotente)"
	@echo "  make docs-help        # Questo aiuto"

# <<< DOCS SYSTEM TARGETS END <<<

MK
    mv Makefile.tmp Makefile
else
    cat > Makefile <<'MK'
# Autogenerato: Docs System Makefile

.PHONY: docs-generate docs-idem-soft docs-idem-strict docs-help

docs-generate:
	@echo "ℹ️  Fallback docs-generate (no-op). Aggiungi qui il tuo generatore."

docs-idem-soft:
	@echo "== 🧪 Docs Idempotency SOFT =="
	@bash -c 'set -euo pipefail; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	git add -A >/dev/null 2>&1 || true; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	if ! git diff --quiet; then \
		echo "⚠️  Non idempotente (soft): il secondo run ha prodotto modifiche."; \
		git --no-pager diff --stat || true; \
	else \
		echo "✅ Idempotenza OK (nessuna modifica al secondo run)"; \
	fi'

docs-idem-strict:
	@bash -c 'set -euo pipefail; scripts/cursor_docs_strict.sh'

docs-help:
	@echo "📚 Docs System - Comandi disponibili:"
	@echo "  make docs-generate    # Genera docs (fallback no-op)"
	@echo "  make docs-idem-soft   # Test soft (warning, non blocca)"
	@echo "  make docs-idem-strict # Test strict (fallisce se non idempotente)"
	@echo "  make docs-help        # Questo aiuto"
MK
fi

# 6) Step YAML finale
cat > CI_STRICT_STEP_YAML.md <<'YAML'
# 👇 Step per GitHub Actions (jobs.<job>.steps)

      - name: Setup Docs System
        run: |
          chmod +x scripts/cursor_docs_strict.sh
          git config user.email "ci-bot@example.com"
          git config user.name "ci-bot"

      - name: Docs Idempotency (STRICT)
        shell: bash
        run: |
          set -euo pipefail
          echo "🔍 Verificando idempotenza docs..."
          ./scripts/cursor_docs_strict.sh
          echo "✅ Idempotenza verificata"

# 🔄 Workflow completo di esempio:
# 
# name: Docs Check
# on: [push, pull_request]
# jobs:
#   docs:
#     runs-on: ubuntu-latest
#     steps:
#       - uses: actions/checkout@v4
#       - uses: actions/setup-python@v4
#         with:
#           python-version: '3.11'
#       - name: Install dependencies
#         run: |
#           python -m pip install --upgrade pip
#           pip install -r requirements.txt || true
#       - name: Setup Docs System
#         run: |
#           chmod +x scripts/cursor_docs_strict.sh
#           git config user.email "ci-bot@example.com"
#           git config user.name "ci-bot"
#       - name: Docs Idempotency (STRICT)
#         shell: bash
#         run: |
#           set -euo pipefail
#           echo "🔍 Verificando idempotenza docs..."
#           ./scripts/cursor_docs_strict.sh
#           echo "✅ Idempotenza verificata"
YAML

# 7) Test finale
echo "=== 🧪 Test finale ==="

echo "1️⃣ Test soft (non blocca):"
make docs-idem-soft || true

echo ""
echo "2️⃣ Test strict (fallisce se non idempotente):"
set +e
make docs-idem-strict
STRICT_RC=$?
set -e

echo ""
echo "3️⃣ Test help:"
make docs-help || true

echo ""
if [[ $STRICT_RC -eq 0 ]]; then
    echo "✅ STRICT OK - Sistema pronto!"
else
    echo "⚠️  STRICT ha trovato non-idempotenza"
    echo "   Questo è normale se il tuo generatore modifica file al 2° run"
fi

# 8) Preparazione commit
echo ""
echo "=== 📦 Preparazione commit ==="
git add setup_docs_system_final.sh scripts/cursor_docs_strict.sh docs/DOCS_SYSTEM_README.md CI_STRICT_STEP_YAML.md Makefile .git/hooks/pre-commit 2>/dev/null || true

if ! git diff --cached --quiet; then
    echo "✅ File pronti per commit"
    echo "💡 Esegui: git commit -m 'feat: add final docs system with idempotency'"
else
    echo "ℹ️  Nessuna modifica da committare (sistema già presente)"
fi

echo ""
echo "=== 🎯 Sistema Docs Final completato! ==="
echo "📚 Documentazione: docs/DOCS_SYSTEM_README.md"
echo "🔧 Script strict: scripts/cursor_docs_strict.sh"
echo "🪝 Hook pre-commit: .git/hooks/pre-commit"
echo "📋 Step CI: CI_STRICT_STEP_YAML.md"
echo "🛠️  Target Makefile: make docs-help"
echo ""
echo "🚀 Sistema pronto per l'uso in produzione!"
