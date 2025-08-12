#!/usr/bin/env bash
set -euo pipefail

REPO_SLUG="${1:-papemat/TokIntel}"
DEFAULT_BRANCH="${2:-main}"

echo "🔧 Config repo: $REPO_SLUG"

# Assumi repo già creato; se serve crearla localmente, usare: gh repo create "$REPO_SLUG" --public -y

# Imposta default branch
gh api -X PATCH repos/$REPO_SLUG -f default_branch="$DEFAULT_BRANCH" >/dev/null || true

# Crea label se manca
gh label create "perf-regression" -R "$REPO_SLUG" --color FF006E --description "Performance regression tracking" 2>/dev/null || true

echo "✅ Setup base completato."
