#!/usr/bin/env bash
set -euo pipefail
# Usage: ./scripts/release_quickstart.sh v1.1.0

VERSION="${1:-}"
[[ -n "$VERSION" ]] || { echo "Usage: $0 vX.Y.Z"; exit 1; }

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "[error] not a git repo"; exit 1; }
git diff --quiet && git diff --cached --quiet || { echo "[error] working tree not clean"; exit 1; }

DEFAULT_MAIN="main"; git show-ref --verify --quiet refs/heads/master && DEFAULT_MAIN="master"
echo "[info] fetch + update $DEFAULT_MAIN"
git fetch origin
git checkout "$DEFAULT_MAIN"
git pull --ff-only origin "$DEFAULT_MAIN"

if git rev-parse "$VERSION" >/dev/null 2>&1; then
  echo "[warn] tag $VERSION already exists"
else
  TAG_MSG="Quickstart Bundle: cross-platform launchers + docs"
  if [[ -f CHANGELOG_QUICKSTART.md ]]; then
    TAG_MSG+=$'\n\n'"$(awk 'f;/^## /{if(f)exit} /^## v/{f=1}1' CHANGELOG_QUICKSTART.md)"
  fi
  git tag -a "$VERSION" -m "$TAG_MSG"
fi

git push origin "$VERSION"

if command -v gh >/dev/null 2>&1; then
  BODY_FILE="/tmp/ti_release_notes_$$.md"
  if [[ -f CHANGELOG_QUICKSTART.md ]]; then
    awk 'f;/^## /{if(f)exit} /^## v/{f=1}1' CHANGELOG_QUICKSTART.md >"$BODY_FILE"
  else
    echo "TokIntel Quickstart Bundle $VERSION" >"$BODY_FILE"
  fi
  gh release create "$VERSION" -F "$BODY_FILE" -t "$VERSION" --verify-tag || echo "[warn] gh release failed"
  rm -f "$BODY_FILE"
else
  cat <<EOF
[info] gh CLI non presente.
Crea la release manualmente con tag $VERSION.
EOF
fi

echo "[done] Release $VERSION completata."
