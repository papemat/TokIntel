#!/usr/bin/env bash
set -euo pipefail
echo "=== ♻️  Rollback Docs Enterprise Add-ons ==="
rm -f .github/workflows/docs-idempotency-enterprise.yml
if [ -f README.md ]; then
  awk 'NR==1 && $0 ~ /Docs Idempotency/ {next} {print}' README.md > README.md.__tmp__ && mv README.md.__tmp__ README.md
fi
if [ -f .git/hooks/pre-push ]; then
  # rimuove se contiene firma di questo hook
  if grep -q "pre-push: running docs-idem-strict" .git/hooks/pre-push; then
    rm -f .git/hooks/pre-push
  fi
fi
echo "✅ Rollback completato."
