#!/usr/bin/env bash
set -euo pipefail

echo "🧪 Smoke test Docs Strict"
echo "=========================="

echo "1️⃣ Report duplicati (pre):"
python3 .github/scripts/report_qs_duplicates.py || echo "⚠️ Report duplicati fallito (normale se non ci sono duplicati)"

echo ""
echo "2️⃣ Docs CI All (autofix + linkcheck + lint + badges + idempotenza strict):"
make docs-ci-all

echo ""
echo "✅ Smoke test completato!"
echo ""
echo "💡 Prova anche:"
echo "   make docs-idem-strict    # Solo idempotenza strict"
echo "   make docs-doctor         # Docs Doctor completo"
echo "   bash cursor_strict.sh    # Cursore completo con PR"
