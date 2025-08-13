#!/usr/bin/env bash
set -euo pipefail

echo "== 🧪 Docs Idempotency STRICT =="
# Prima passata (genera/aggiorna docs)
if make -q docs-generate 2>/dev/null; then
  make docs-generate
elif [[ -x scripts/update_docs_status.py ]]; then
  python3 scripts/update_docs_status.py || true
elif [[ -x .github/scripts/update_docs_status.py ]]; then
  python3 .github/scripts/update_docs_status.py || true
else
  echo "⚠️  Nessun generatore docs trovato: eseguo fallback no-op"
fi

# Seconda passata (deve essere no-op)
git add -A >/dev/null 2>&1 || true
if make -q docs-generate 2>/dev/null; then
  make docs-generate
elif [[ -x scripts/update_docs_status.py ]]; then
  python3 scripts/update_docs_status.py || true
elif [[ -x .github/scripts/update_docs_status.py ]]; then
  python3 .github/scripts/update_docs_status.py || true
fi

# Controllo diff: se c'è differenza -> FAIL
if ! git diff --quiet; then
  echo "❌ Non idempotente: il secondo run ha prodotto modifiche."
  git --no-pager diff --stat
  exit 1
fi

echo "✅ Idempotenza OK (nessuna modifica al secondo run)"
