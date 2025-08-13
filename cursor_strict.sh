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

echo "=== 🧼 Autofix + linkcheck ==="
python3 .github/scripts/autofix_quickstart.py
python3 .github/scripts/docs_linkcheck.py || true
make docs-doctor || true

echo "=== 🔁 Idempotenza stretta ==="
# secondo run: se cambia qualcosa -> FAIL
python3 .github/scripts/autofix_quickstart.py
if ! git diff --quiet; then
  echo "❌ Non idempotente: ci sono diff dopo il secondo run!"
  git --no-pager diff
  exit 2
fi

echo "=== 🖼️ Badges ==="
make glow-badges || true

echo "=== 🧺 Staging selettivo ==="
git add README.md || true
git add docs/status.json docs/images/*.svg 2>/dev/null || true
git add .github/workflows/quickstart-guard.yml .github/workflows/markdownlint.yml .github/workflows/glow-badges.yml 2>/dev/null || true
git add .github/scripts/*.py scripts/generate_glow_badge.py 2>/dev/null || true
git add .pre-commit-config.yaml .markdownlint.jsonc Makefile 2>/dev/null || true

if git diff --cached --quiet; then
  echo "✅ Nessuna modifica da committare (repo già allineato)."
else
  git commit -m "ci(docs): strict idempotency for Docs Doctor + anti-duplicates + glow"
fi

git push -u origin chore/docs-doctor-anti-dup || true

if command -v gh >/dev/null; then
  gh pr create --base main --head chore/docs-doctor-anti-dup \
    --title "ci(docs): Strict Docs Doctor + Anti‑Duplicati + Glow" \
    --body "Enforce idempotenza: fallisce se il secondo run di autofix produce diff. Include linkcheck, markdownlint e glow badges."
else
  echo "ℹ️ Apri PR manualmente se non hai 'gh'."
fi

echo "🎯 Done (strict)."
