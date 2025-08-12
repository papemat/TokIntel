#!/usr/bin/env bash
set -euo pipefail
TI_PORT="${TI_PORT:-8510}"
echo "🧪 Dev smoke starting on port ${TI_PORT}..."
chmod +x scripts/kill_port.sh || true
python3 scripts/kill_port.py "${TI_PORT}" || true
make kill-port TI_PORT="${TI_PORT}" || true

echo "➡️  E2E headless"
TI_AUTO_EXPORT=1 TI_PORT="${TI_PORT}" make test-e2e-only

echo "➡️  Coverage Sprint 3"
make coverage-sprint3 || true

echo "➡️  Lint (non-blocking auto-fix)"
make lint-sprint3 || true

echo "➡️  Orchestrator CLI smoke"
.venv/bin/python -m analyzer.orchestrator --query "alpha beta" --topk 3 --export "exports/cli_smoke" || true

echo "✅ Dev smoke completed"
