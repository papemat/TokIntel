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
