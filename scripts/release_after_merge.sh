#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./scripts/release_after_merge.sh v1.1.0 [--dry-run]
# Do:
#   1) sync 'main' (or 'master') from origin (ff-only)
#   2) verify Quickstart files present
#   3) create & push annotated tag
#   4) optionally create GitHub release via gh CLI

VERSION="${1:-v1.1.0}"
DRY_RUN="${2:-}"
if [[ "${DRY_RUN:-}" == "--dry-run" ]]; then
  echo "[info] Dry-run mode: no tag creation/push, no GitHub release."
fi

# Remember current branch to restore on exit
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD || echo "")"
cleanup() {
  # best-effort: return to previous branch if it still exists
  if [[ -n "$CURRENT_BRANCH" ]]; then
    git checkout -q "$CURRENT_BRANCH" || true
  fi
}
trap cleanup EXIT

# Figure out default main branch
DEFAULT_MAIN="main"
git show-ref --verify --quiet refs/remotes/origin/master && DEFAULT_MAIN="master"

echo "[info] Fetching origin…"
git fetch origin

echo "[info] Switching to '$DEFAULT_MAIN' and fast-forward pulling…"
git checkout "$DEFAULT_MAIN"
git pull --ff-only origin "$DEFAULT_MAIN"

echo "[info] Verifying Quickstart files…"
need_files=(
  "scripts/run_tokintel.sh"
  "scripts/run_tokintel.bat"
  "README_QUICKSTART.md"
  "FAQ_TROUBLESHOOTING.md"
  "streamlit_config_example.toml"
  "CHANGELOG_QUICKSTART.md"
)
missing=0
for f in "${need_files[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "[error] Missing required file: $f"
    missing=1
  fi
done
if [[ $missing -ne 0 ]]; then
  cat <<'EOF'
[hint] Sembra che la PR non sia stata mergiata su '$DEFAULT_MAIN' oppure non hai pullato l'ultimo commit.
- Verifica su GitHub che la PR sia 'Merged' su '$DEFAULT_MAIN'
- Poi rilancia questo script
EOF
  exit 2
fi

# Ensure launcher is executable (no-op on Windows)
if [[ -f scripts/run_tokintel.sh ]]; then
  git update-index --chmod=+x scripts/run_tokintel.sh || true
fi

# Build tag message (include latest section from CHANGELOG if present)
TAG_MSG="Quickstart Bundle: cross-platform launchers + docs"
if [[ -f CHANGELOG_QUICKSTART.md ]]; then
  SECTION="$(awk 'f;/^## /{if(f)exit} /^## v/{f=1}1' CHANGELOG_QUICKSTART.md || true)"
  if [[ -n "${SECTION:-}" ]]; then
    TAG_MSG+=$'\n\n'"${SECTION}"
  fi
fi

if [[ "${DRY_RUN:-}" != "--dry-run" ]]; then
  # Remote-existence check first
  if git ls-remote --tags origin "refs/tags/$VERSION" | grep -q "$VERSION"; then
    echo "[warn] Tag $VERSION already exists on origin. Skipping tag creation/push."
  else
    # Local tag check
    if git rev-parse "$VERSION" >/dev/null 2>&1; then
      echo "[warn] Tag $VERSION already exists locally."
    else
      echo "[info] Creating annotated tag $VERSION"
      git tag -a "$VERSION" -m "$TAG_MSG"
    fi
    echo "[info] Pushing tag $VERSION to origin…"
    git push origin "$VERSION"
  fi
else
  echo "[dry-run] Would create annotated tag '$VERSION' with message:"
  echo "----------"
  echo "$TAG_MSG"
  echo "----------"
  echo "[dry-run] Would push tag '$VERSION' to origin."
fi

if [[ "${DRY_RUN:-}" != "--dry-run" ]] && command -v gh >/dev/null 2>&1; then
  echo "[info] Creating GitHub release via gh CLI (if not exists)…"
  if gh release view "$VERSION" >/dev/null 2>&1; then
    echo "[warn] Release $VERSION already exists on GitHub."
  else
    BODY_FILE="$(mktemp)"
    if [[ -f CHANGELOG_QUICKSTART.md ]]; then
      awk 'f;/^## /{if(f)exit} /^## v/{f=1}1' CHANGELOG_QUICKSTART.md >"$BODY_FILE"
    else
      echo "TokIntel Quickstart Bundle $VERSION" >"$BODY_FILE"
    fi
    gh release create "$VERSION" -F "$BODY_FILE" -t "$VERSION" --verify-tag || \
      echo "[warn] gh release failed. Create release manually."
    rm -f "$BODY_FILE"
  fi
else
  cat <<EOF
[info] 'gh' CLI non trovato ${DRY_RUN:+(o dry-run attivo)}. Release GitHub non creata automaticamente.
Crea la release manualmente: https://github.com/<OWNER>/<REPO>/releases/new?tag=$VERSION
Titolo: $VERSION – Quickstart Bundle
Body: incolla la sezione v1.1.0 da CHANGELOG_QUICKSTART.md
EOF
fi

echo "[done] Release workflow ${DRY_RUN:+(dry-run) }completed for $VERSION."
