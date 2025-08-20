#!/usr/bin/env bash
set -euo pipefail

# Hotfix Express - Fix rapido con release automatica
# Uso: ./scripts/hotfix_express.sh "descrizione fix"

if [ $# -eq 0 ]; then
    echo "❌ Uso: ./scripts/hotfix_express.sh \"descrizione fix\""
    echo "Esempio: ./scripts/hotfix_express.sh \"fix: dashboard loading issue\""
    exit 1
fi

FIX_DESC="$1"
CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v1.0.0")
NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{print $1"."$2"."$3+1}')

echo "🚀 Hotfix Express"
echo "=================="
echo "📝 Descrizione: $FIX_DESC"
echo "🏷️  Versione attuale: $CURRENT_VERSION"
echo "🏷️  Nuova versione: $NEW_VERSION"

# 1) Crea branch hotfix
BRANCH_NAME="hotfix/$(date +%Y%m%d-%H%M%S)"
echo "🌿 Creo branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

echo ""
echo "🔧 Ora fai le tue modifiche, poi premi ENTER per continuare..."
read -r

# 2) Commit e push
echo "📝 Commit e push..."
git add .
git commit -m "fix: $FIX_DESC"
git push -u origin "$BRANCH_NAME"

echo ""
echo "✅ Hotfix branch creato: $BRANCH_NAME"
echo "📋 Prossimi step:"
echo "   1. Crea PR su GitHub"
echo "   2. Merge su main"
echo "   3. Esegui: make dx-release VER=$NEW_VERSION"
echo ""
echo "🎯 Per release automatica dopo merge:"
echo "   make dx-release VER=$NEW_VERSION"
