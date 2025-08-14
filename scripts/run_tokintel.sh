#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

PORT="${PORT:-8501}"
HOST="localhost"
APP="dash/app.py"
HEADLESS=1
DEBUG=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --lan) HOST="0.0.0.0"; shift ;;
    --port) PORT="$2"; shift 2 ;;
    --app) APP="$2"; shift 2 ;;
    --no-headless) HEADLESS=0; shift ;;
    --debug) DEBUG=1; shift ;;
    -h|--help)
      cat <<EOF
TokIntel launcher (macOS/Linux)

Usage: ./scripts/run_tokintel.sh [options]
  --lan             Bind 0.0.0.0 (share on LAN)
  --port <num>      Server port (default 8501 or \$PORT)
  --app <path>      Streamlit app (default dash/app.py)
  --no-headless     Open browser automatically
  --debug           Verbose logs
  -h, --help        This help
EOF
      exit 0 ;;
    *) echo "[warn] Unknown option: $1" >&2; shift ;;
  esac
done

if [[ -x ".venv/bin/python" ]]; then
  PY=".venv/bin/python"
else
  PY="$(command -v python3 || true)"
fi
[[ -n "${PY}" ]] || { echo "[error] python3 not found"; exit 1; }

if ! "$PY" -c "import streamlit" >/dev/null 2>&1; then
  echo "[info] Installing streamlit/requirements..."
  "$PY" -m pip install --upgrade pip
  if [[ -f requirements.txt ]]; then
    "$PY" -m pip install -r requirements.txt
  else
    "$PY" -m pip install streamlit
  fi
fi

export STREAMLIT_SERVER_HEADLESS=$([[ $HEADLESS -eq 1 ]] && echo true || echo false)
[[ $DEBUG -eq 1 ]] && export STREAMLIT_LOG_LEVEL=debug

exec "$PY" -m streamlit run "$APP" --server.port="$PORT" --server.address="$HOST"
