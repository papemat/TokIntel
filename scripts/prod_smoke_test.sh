#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Production Smoke Test (60s)"
echo "================================"

# 1) Sync e setup
echo "📥 Sync repository..."
git pull

echo "🔧 DX setup..."
./scripts/dx_super_setup.sh

# 2) Status check
echo "📊 Status dashboard..."
make dev-status

# 3) Fast tests
echo "🧪 Fast tests..."
make test-fast

echo "✅ Production smoke test completato!"
echo "🎯 Sistema pronto per produzione"
