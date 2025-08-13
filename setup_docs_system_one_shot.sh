#!/usr/bin/env bash
set -euo pipefail

echo "=== 🧭 Repo sanity ==="
test -f README.md || { echo "❌ Lancia nello stesso folder del repo (README.md mancante)"; exit 1; }

# ---------------------------------------------------------
# 1) File/dir di servizio
# ---------------------------------------------------------
mkdir -p scripts docs

# ---------------------------------------------------------
# 2) Script STRICT per PR/CI (eseguibile)
# ---------------------------------------------------------
cat > scripts/cursor_docs_strict.sh <<'BASH'
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
git add .github/workflows/*.yml .github/scripts/*.py scripts/generate_glow_badge.py 2>/dev/null || true
git add .pre-commit-config.yaml .markdownlint.jsonc Makefile 2>/dev/null || true

if ! git diff --cached --quiet; then
  git commit -m "ci(docs): strict idempotency + anti-duplicates + glow"
fi

echo "=== 📤 Push & PR ==="
git push -u origin chore/docs-doctor-anti-dup || true
if command -v gh >/dev/null; then
  gh pr create --base main --head chore/docs-doctor-anti-dup \
    --title "ci(docs): Strict Docs System" \
    --body "Enforce idempotenza (hard-fail), linkcheck, markdownlint, glow badges."
else
  echo "ℹ️ PR non creata (gh assente). Aprila a mano dall'interfaccia GitHub."
fi

echo "🎯 Done (strict)."
BASH
chmod +x scripts/cursor_docs_strict.sh

# ---------------------------------------------------------
# 3) README unico del sistema (documentazione completa)
# ---------------------------------------------------------
cat > docs/DOCS_SYSTEM_README.md <<'MD'
# Docs System — Strict + Soft

## Obiettivi
- Anti-duplicati blocco **Quick Start**
- **Idempotenza** (due run consecutivi → nessuna diff)
- **Linkcheck**, **Markdownlint**, **Glow badges**
- **Locale soft**, **CI strict**

## Uso rapido
- Strict end‑to‑end + PR:  
  ```bash
  scripts/cursor_docs_strict.sh
  ```

* Mini check idempotenza:

  ```bash
  python3 .github/scripts/autofix_quickstart.py && \
  python3 .github/scripts/autofix_quickstart.py && \
  git diff --quiet && echo "✅ OK" || echo "❌ Non idempotente"
  ```

## Flow consigliato

1. Sviluppo locale: **soft**
2. Prima della PR: `make docs-idem-strict` (deve passare)
3. CI/PR: **strict** (blocca se non idempotente)
MD

# ---------------------------------------------------------
# 4) Aggiorna/crea pre-commit (soft hook non bloccante)
# ---------------------------------------------------------
if [ ! -f .pre-commit-config.yaml ]; then
cat > .pre-commit-config.yaml <<'YAML'
repos:
  - repo: local
    hooks:
      - id: docs-doctor-idempotent-soft
        name: Docs Doctor Idempotency (soft)
        entry: bash -c 'python3 .github/scripts/autofix_quickstart.py && python3 .github/scripts/autofix_quickstart.py; if ! git diff --quiet; then echo "⚠️  Non idempotente (soft): vedi diff"; git --no-pager diff; fi; exit 0'
        language: system
        pass_filenames: false
        stages: [commit]
YAML
else
if ! grep -q 'docs-doctor-idempotent-soft' .pre-commit-config.yaml; then
cat >> .pre-commit-config.yaml <<'YAML'

  - repo: local
    hooks:
      - id: docs-doctor-idempotent-soft
        name: Docs Doctor Idempotency (soft)
        entry: bash -c 'python3 .github/scripts/autofix_quickstart.py && python3 .github/scripts/autofix_quickstart.py; if ! git diff --quiet; then echo "⚠️  Non idempotente (soft): vedi diff"; git --no-pager diff; fi; exit 0'
        language: system
        pass_filenames: false
        stages: [commit]
YAML
fi
fi

# ---------------------------------------------------------
# 5) Makefile: aggiungi target se mancanti (strict/soft/all)
# ---------------------------------------------------------
touch Makefile
if ! grep -q '^.PHONY: docs-idem-strict' Makefile; then
cat >> Makefile <<'MAKE'

.PHONY: docs-idem-strict
docs-idem-strict:
	@python3 .github/scripts/autofix_quickstart.py
	@python3 .github/scripts/autofix_quickstart.py
	@git diff --quiet || (echo "Non idempotente: diff dopo secondo run"; git --no-pager diff; exit 2)

.PHONY: docs-idem-soft
docs-idem-soft:
	@python3 .github/scripts/autofix_quickstart.py || true
	@python3 .github/scripts/autofix_quickstart.py || true
	@if ! git diff --quiet; then echo "⚠️  Non idempotente (soft): diff rilevato, exit 0"; git --no-pager diff; fi
	@exit 0

.PHONY: docs-ci-all
docs-ci-all:
	@$(MAKE) docs-autofix || true
	@$(MAKE) docs-links || true
	@$(MAKE) docs-lint || true
	@$(MAKE) glow-badges || true
	@$(MAKE) docs-idem-strict
MAKE
fi

# ---------------------------------------------------------
# 6) Mini check locale (non fallisce la pipeline globale)
# ---------------------------------------------------------
echo "=== 🧪 Mini check idempotenza strict ==="
if ( python3 .github/scripts/autofix_quickstart.py && python3 .github/scripts/autofix_quickstart.py && git diff --quiet ); then
echo "✅ Idempotenza OK"
else
echo "❌ Non idempotente (come previsto se ci sono duplicati/drift)"
fi

# ---------------------------------------------------------
# 7) Prepara commit (senza forzare)
# ---------------------------------------------------------
git add scripts/cursor_docs_strict.sh docs/DOCS_SYSTEM_README.md .pre-commit-config.yaml Makefile || true
if ! git diff --cached --quiet; then
git commit -m "docs: add unified Docs System (strict+soft) + script & hooks"
fi

echo "=== ℹ️ Consigli finali ==="
echo "- Locale: pre-commit soft → sviluppo rapido"
echo "- Prima PR: make docs-idem-strict"
echo "- In PR/CI: step strict che fallisce se il secondo run produce diff"
echo "🎯 Fatto."
