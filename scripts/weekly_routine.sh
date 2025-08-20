#!/usr/bin/env bash
set -euo pipefail

echo "🧭 Routine Settimanale (2 minuti)"
echo "=================================="

# 1) Sync e aggiornamenti
echo "📥 Sync repository..."
git pull

# 2) Aggiorna changelog
echo "📝 Aggiorna changelog..."
make changelog

# 3) Doctor check
echo "🩺 Doctor check..."
./scripts/dx_doctor.sh

echo ""
echo "✅ Routine settimanale completata!"
echo ""
echo "📋 Prossimi step manuali:"
echo "   • Unisci PR Dependabot 'patch/minor' se verdi"
echo "   • Verifica badge CI nel README (Fast Tests)"
echo "   • Controlla stato dashboard: make dev-status"
