#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/reproducible_presets.sh" || true
python3 - <<'PY' || true
try:
    import runpy; runpy.run_module(".github.scripts.reproducible_preset", run_name="__main__")
except Exception:
    pass
PY

# Sphinx
if { [ -f "conf.py" ] || { [ -d docs ] && [ -f docs/conf.py ]; }; } && command -v sphinx-build >/dev/null 2>&1; then
  echo "➡️  Sphinx rilevato"
  OUT="${SPHINX_OUT:-docs/_build}"
  mkdir -p "$OUT"
  (sphinx-build -b html docs "$OUT" -q || sphinx-build -b html . "$OUT" -q) || true
  if [ -d "$OUT" ]; then
    find "$OUT" -type f -name "*.html" -print0 | xargs -0 -I{} bash -c 'repro_scrub_file "$@"' _ {} || true
  fi
  exit 0
fi

# MkDocs
if [ -f "mkdocs.yml" ] && command -v mkdocs >/dev/null 2>&1; then
  echo "➡️  MkDocs rilevato"
  DOCS_BUILD_DATE="${DOCS_BUILD_DATE:-2024-01-01}" mkdocs build --clean --strict || true
  if [ -d site ]; then
    find site -type f -name "*.html" -print0 | xargs -0 -I{} bash -c 'repro_scrub_file "$@"' _ {} || true
  fi
  exit 0
fi

# Script custom noti
if [ -x "scripts/update_docs_status.py" ]; then
  echo "➡️  scripts/update_docs_status.py"
  python3 scripts/update_docs_status.py || true
  exit 0
fi
if [ -x ".github/scripts/update_docs_status.py" ]; then
  echo "➡️  .github/scripts/update_docs_status.py"
  python3 .github/scripts/update_docs_status.py || true
  exit 0
fi

echo "ℹ️  Nessun generatore rilevato (no-op)."
exit 0
