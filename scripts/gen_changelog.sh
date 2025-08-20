#!/usr/bin/env bash
set -euo pipefail
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
  RANGE="$(git rev-list --max-parents=0 HEAD)..HEAD"
else
  RANGE="$LAST_TAG..HEAD"
fi
{
  echo "## $(date +%Y-%m-%d) – Unreleased"
  git log --pretty="* %s (%h)" $RANGE
  echo
} | cat - CHANGELOG.md 2>/dev/null | awk '!seen[$0]++' > .CHANGELOG.tmp
mv .CHANGELOG.tmp CHANGELOG.md
echo "✅ CHANGELOG aggiornato"
