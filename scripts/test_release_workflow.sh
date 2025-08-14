#!/usr/bin/env bash
set -euo pipefail

# Test script per verificare che il workflow di release sia configurato correttamente
# Usage: ./scripts/test_release_workflow.sh

echo "🧪 Testing TokIntel Release Workflow Configuration"
echo "=================================================="

# Test 1: Verifica che lo script di release esista e sia eseguibile
echo "1. Checking release script..."
if [[ -x scripts/release_after_merge.sh ]]; then
    echo "   ✅ scripts/release_after_merge.sh exists and is executable"
else
    echo "   ❌ scripts/release_after_merge.sh missing or not executable"
    exit 1
fi

# Test 2: Verifica che i file Quickstart richiesti esistano
echo "2. Checking Quickstart files..."
required_files=(
    "scripts/run_tokintel.sh"
    "scripts/run_tokintel.bat"
    "README_QUICKSTART.md"
    "FAQ_TROUBLESHOOTING.md"
    "streamlit_config_example.toml"
    "CHANGELOG_QUICKSTART.md"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -gt 0 ]]; then
    echo "   ⚠️  Missing files: ${missing_files[*]}"
    echo "   💡 Run 'make docs-generate' to create missing Quickstart files"
else
    echo "   ✅ All Quickstart files present"
fi

# Test 3: Verifica che il Makefile abbia i target di release
echo "3. Checking Makefile targets..."
if grep -q "release-dry:" Makefile; then
    echo "   ✅ make release-dry target found"
else
    echo "   ❌ make release-dry target missing"
fi

if grep -q "release:" Makefile; then
    echo "   ✅ make release target found"
else
    echo "   ❌ make release target missing"
fi

# Test 4: Verifica configurazione git
echo "4. Checking git configuration..."
if git remote get-url origin >/dev/null 2>&1; then
    echo "   ✅ Git remote 'origin' configured"
    echo "   📍 $(git remote get-url origin)"
else
    echo "   ❌ Git remote 'origin' not configured"
fi

# Test 5: Verifica gh CLI (opzionale)
echo "5. Checking GitHub CLI..."
if command -v gh >/dev/null 2>&1; then
    echo "   ✅ GitHub CLI (gh) available"
    if gh auth status >/dev/null 2>&1; then
        echo "   ✅ GitHub CLI authenticated"
    else
        echo "   ⚠️  GitHub CLI not authenticated (run 'gh auth login')"
    fi
else
    echo "   ℹ️  GitHub CLI not installed (optional for automatic releases)"
fi

echo ""
echo "🎯 Release Workflow Test Summary"
echo "================================"
echo ""
echo "Per eseguire un dry-run del release:"
echo "  make release-dry"
echo "  # oppure"
echo "  ./scripts/release_after_merge.sh v1.1.0 --dry-run"
echo ""
echo "Per eseguire il release completo:"
echo "  make release"
echo "  # oppure"
echo "  ./scripts/release_after_merge.sh v1.1.0"
echo ""
echo "📋 Pre-flight checklist:"
echo "  □ PR mergiata su main/master"
echo "  □ Tutti i file Quickstart presenti"
echo "  □ Branch locale sincronizzato con remoto"
echo "  □ Version tag corretto (v1.1.0)"
echo ""
echo "✅ Test completato!"
