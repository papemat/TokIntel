#!/usr/bin/env bash
set -euo pipefail
echo "== 🧪 Docs Idempotency STRICT =="

run_gen() {
  if [ -f Makefile ] && grep -qE '(^|:) *docs-generate' Makefile; then
    make -s docs-generate
  else
    bash scripts/docs_generate_auto.sh
  fi
}
run_gen
git add -A >/dev/null 2>&1 || true
# Scan anti‑timestamp/hash/uuid best‑effort
[ -x scripts/docs_output_scan.sh ] && bash scripts/docs_output_scan.sh || true
run_gen

if ! git diff --quiet; then
  echo "❌ Non idempotente: il secondo run ha prodotto modifiche."
  git --no-pager diff --stat || true
  git --no-pager diff > docs_idempotency.diff || true
  exit 1
fi
echo "✅ Idempotenza OK (nessuna modifica al secondo run)"
