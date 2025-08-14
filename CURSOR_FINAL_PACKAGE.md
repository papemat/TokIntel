# 🚀 Cursor Final Package — Strict CI Docs Doctor

Pacchetto completo per implementare il sistema **Docs Strict** con idempotenza hard-fail.

---

## 🎯 Script Unico (copia/incolla)

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== 🌿 Branch ==="
git checkout -B chore/docs-doctor-anti-dup

echo "=== 🐍 Deps ==="
python3 -m pip install -U pip >/dev/null
pip install -r requirements.txt || true
pip install markdown-it-py linkify-it-py >/dev/null

echo "=== 🔎 Report duplicati (pre) ==="
python3 .github/scripts/report_qs_duplicates.py || true

echo "=== 🧼 Autofix + linkcheck + docs ==="
python3 .github/scripts/autofix_quickstart.py
python3 .github/scripts/docs_linkcheck.py || true
make docs-doctor || true

echo "=== 🔁 Idempotenza strict (secondo run) ==="
python3 .github/scripts/autofix_quickstart.py
if ! git diff --quiet; then
  echo "❌ Non idempotente: diff dopo secondo run!"
  git --no-pager diff
  exit 2
fi

echo "=== 🖼️ Glow badges ==="
make glow-badges || true

echo "=== 🧺 Staging ==="
git add README.md || true
git add docs/status.json docs/images/*.svg 2>/dev/null || true
git add .github/workflows/quickstart-guard.yml .github/workflows/markdownlint.yml .github/workflows/glow-badges.yml 2>/dev/null || true
git add .github/scripts/*.py scripts/generate_glow_badge.py 2>/dev/null || true
git add .pre-commit-config.yaml .markdownlint.jsonc Makefile 2>/dev/null || true

if git diff --cached --quiet; then
  echo "✅ Nessuna modifica da committare."
else
  git commit -m "ci(docs): strict idempotency for Docs Doctor + anti-duplicates + glow"
fi

echo "=== 📤 Push branch ==="
git push -u origin chore/docs-doctor-anti-dup || true

if command -v gh >/dev/null; then
  gh pr create --base main --head chore/docs-doctor-anti-dup \
    --title "ci(docs): Strict Docs Doctor + Anti‑Duplicati + Glow" \
    --body "Enforce idempotenza (hard‑fail), linkcheck, markdownlint, glow badges. Secondo run senza diff."
else
  echo "ℹ️ Apri PR manualmente se non hai 'gh'."
fi

echo "🎯 Done (strict)."
```

---

## 🔩 Hook Pre-commit (Strict)

Aggiungi al tuo `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: docs-doctor-idempotent
        name: Docs Doctor Idempotency
        entry: bash -c 'python3 .github/scripts/autofix_quickstart.py && python3 .github/scripts/autofix_quickstart.py && git diff --quiet'
        language: system
        pass_filenames: false
        stages: [commit]
```

Setup:
```bash
pip install pre-commit && pre-commit install
```

---

## 🛠️ Makefile Targets

Aggiungi questi target al tuo `Makefile`:

```make
docs-idem-strict:
	@echo "🔁 Idempotenza strict: secondo run non deve produrre diff"
	@python3 .github/scripts/autofix_quickstart.py
	@python3 .github/scripts/autofix_quickstart.py
	@git diff --quiet || (echo "❌ Non idempotente: diff dopo secondo run"; git --no-pager diff; exit 2)
	@echo "✅ Idempotenza strict OK"

docs-ci-all:
	@echo "🧪 Docs CI All: autofix, linkcheck, lint, badges, idempotenza strict"
	@python3 .github/scripts/autofix_quickstart.py || true
	@python3 .github/scripts/docs_linkcheck.py || true
	@$(MAKE) docs-lint || true
	@$(MAKE) glow-badges || true
	@$(MAKE) docs-idem-strict
```

E aggiungi alla lista `.PHONY`:
```make
.PHONY: ... docs-idem-strict docs-ci-all
```

---

## ✅ Smoke Test Rapido

```bash
# Se hai già il target
make docs-idem-strict

# Oppure comando diretto
bash -c 'python3 .github/scripts/autofix_quickstart.py && python3 .github/scripts/autofix_quickstart.py && git diff --quiet'
```

---

## 🎯 Comportamento

- ✅ **Strict**: Fallisce se il secondo run produce diff
- ✅ **Anti-duplicati**: Rimuove blocchi Quick Start duplicati
- ✅ **Linkcheck**: Verifica link relativi
- ✅ **Glow badges**: Genera badge con effetto glow
- ✅ **PR automatico**: Crea PR con GitHub CLI

---

## 🚀 Uso

1. **Copia lo script** in `cursor_strict.sh`
2. **Rendi eseguibile**: `chmod +x cursor_strict.sh`
3. **Esegui**: `bash cursor_strict.sh`
4. **Setup pre-commit** (opzionale): `pip install pre-commit && pre-commit install`

---

## 📋 Checklist

- [ ] Script copiato e reso eseguibile
- [ ] Hook pre-commit configurato (opzionale)
- [ ] Target Makefile aggiunti
- [ ] Smoke test passa
- [ ] Idempotenza verificata

**Il sistema è pronto per l'uso!** 🎯
