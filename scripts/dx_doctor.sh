#!/usr/bin/env bash
set -euo pipefail
echo "🩺 DX Doctor"
command -v python3 >/dev/null || command -v python >/dev/null || { echo "Python non trovato"; exit 1; }
make dev-status || true
make env-show || true
make test-fast
echo "✅ Tutto OK"
