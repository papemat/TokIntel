#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

# Defaults
PORT="${PORT:-8501}"
HOST="localhost"
APP="dash/app.py"
HEADLESS=1
DEBUG=0

# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --lan)
      HOST="0.0.0.0"; shift ;;
    --port)
      PORT="$2"; shift 2 ;;
    --app)
      APP="$2"; shift 2 ;;
    --no-headless)
      HEADLESS=0; shift ;;
    --debug)
      DEBUG=1; shift ;;
    -h|--help)
      cat <<EOF
TokIntel launcher (macOS/Linux)

Usage: ./scripts/run_tokintel.sh [options]

Options:
  --lan             Bind to 0.0.0.0 (share on LAN)
  --port <num>      Server port (default 8501 or $PORT)
  --app <path>      Streamlit app entry (default dash/app.py)
  --no-headless     Open browser automatically
  --debug           Verbose logs
  -h, --help        Show this help
EOF
      exit 0 ;;
    *)
      echo "[warn] Unknown option: $1" >&2; shift ;;
  esac
done

# Prefer repo venv if present
if [[ -x ".venv/bin/python" ]]; then
  PY=".venv/bin/python"
else
  PY="$(command -v python3 || true)"
fi

if [[ -z "${PY}" ]]; then
  echo "[error] python3 not found. Install Python 3.10+ and retry." >&2
  exit 1
fi

# Check streamlit availability
if ! "$PY" -c "import streamlit" >/dev/null 2>&1; then
  echo "[info] Streamlit not found. Installing dependencies from requirements.txt…"
  "$PY" -m pip install --upgrade pip
  if [[ -f requirements.txt ]]; then
    "$PY" -m pip install -r requirements.txt
  else
    "$PY" -m pip install streamlit
  fi
fi

# Environment toggles
if [[ $HEADLESS -eq 1 ]]; then
  export STREAMLIT_SERVER_HEADLESS=true
else
  export STREAMLIT_SERVER_HEADLESS=false
fi

if [[ $DEBUG -eq 1 ]]; then
  export STREAMLIT_LOG_LEVEL=debug
fi

# Launch
exec "$PY" -m streamlit run "$APP" \
  --server.port="$PORT" \
  --server.address="$HOST"
