#!/usr/bin/env bash
# File: start_tokintel_auto.sh
# Uso:
#   ./start_tokintel_auto.sh [--mode auto|docker|venv] [--port N] [--no-open] [--stop] [--logs]
# Env:
#   MODE, PORT, OPEN_BROWSER

set -euo pipefail

# ========== Config ==========
PORT="${PORT:-8501}"
MODE="${MODE:-auto}"   # auto | docker | venv
OPEN_BROWSER="${OPEN_BROWSER:-1}"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ========== Helpers ==========
command_exists() { command -v "$1" >/dev/null 2>&1; }

wait_for_port() {
  local host="$1" port="$2" timeout="${3:-30}" elapsed=0
  while ! nc -z "$host" "$port" >/dev/null 2>&1; do
    sleep 1
    elapsed=$((elapsed+1))
    if [ "$elapsed" -ge "$timeout" ]; then
      echo "⏱️ Timeout: porta $host:$port non disponibile dopo ${timeout}s"
      return 1
    fi
  done
  return 0
}

docker_available() {
  command_exists docker || return 1
  docker info >/dev/null 2>&1 || return 1
  [ -f "$PROJECT_DIR/docker-compose.yml" ] || [ -f "$PROJECT_DIR/compose.yml" ] || return 1
  return 0
}

docker_cmd() {
  if command_exists docker-compose; then
    echo "docker-compose"
  else
    echo "docker compose"
  fi
}

open_url() {
  [ "$OPEN_BROWSER" = "1" ] && open "$1" >/dev/null 2>&1 || true
}

usage() {
  cat <<EOF
Usage: $0 [--mode auto|docker|venv] [--port N] [--no-open] [--stop] [--logs]
Env: MODE, PORT, OPEN_BROWSER
EOF
}

# ========== Args ==========
STOP=0
SHOW_LOGS=0
while [ $# -gt 0 ]; do
  case "$1" in
    --mode) MODE="$2"; shift 2;;
    --port) PORT="$2"; shift 2;;
    --no-open) OPEN_BROWSER=0; shift;;
    --stop) STOP=1; shift;;
    --logs) SHOW_LOGS=1; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Argomento sconosciuto: $1"; usage; exit 1;;
  esac
done

cd "$PROJECT_DIR"

# ========== Stop path ==========
if [ "$STOP" -eq 1 ]; then
  if docker_available; then
    echo "🛑 Stop Docker stack…"
    $(docker_cmd) down || true
  fi
  # Kill possible local Streamlit on the given port
  if lsof -i :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
    PID=$(lsof -i :"$PORT" -sTCP:LISTEN -t | head -n1)
    echo "🛑 Kill local process on :$PORT (pid $PID)…"
    kill "$PID" || true
  fi
  echo "✅ Stop completato."
  exit 0
fi

# ========== Choose mode ==========
CHOSEN="$MODE"
if [ "$MODE" = "auto" ]; then
  if docker_available; then CHOSEN="docker"; else CHOSEN="venv"; fi
fi
echo "🔧 Modalità: $CHOSEN  |  Porta: $PORT"

# ========== Start ==========
if [ "$CHOSEN" = "docker" ]; then
  DCMD="$(docker_cmd)"
  export STREAMLIT_SERVER_PORT="$PORT"
  echo "🐳 Avvio via Docker… ($DCMD)"
  $DCMD up --build -d

  echo "⏳ Attendo disponibilità su http://localhost:$PORT …"
  wait_for_port localhost "$PORT" 40

  URL="http://localhost:$PORT"
  echo "✅ TokIntel attivo su: $URL"
  open_url "$URL"

  if [ "$SHOW_LOGS" -eq 1 ]; then
    echo "📜 Logs (CTRL+C per uscire)…"
    $DCMD logs -f
  fi
  exit 0
fi

# ========== VENV mode ==========
echo "🐍 Avvio via Python venv…"

# Ensure venv
if [ ! -d ".venv" ]; then
  echo "📦 Creo virtualenv…"
  python3 -m venv .venv
fi
# Activate venv
# shellcheck disable=SC1091
source .venv/bin/activate

# Install deps (first time or if requirements changed)
if [ ! -f ".venv/.deps_ok" ] || [ "requirements.txt" -nt ".venv/.deps_ok" ]; then
  echo "📦 Installo dipendenze…"
  pip install --upgrade pip >/dev/null
  pip install -r requirements.txt
  touch .venv/.deps_ok
fi

# Kill any process on the port
if lsof -i :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
  PID=$(lsof -i :"$PORT" -sTCP:LISTEN -t | head -n1)
  echo "🧹 Porta $PORT occupata (pid $PID) → kill…"
  kill "$PID" || true
fi

echo "🚀 Avvio TokIntel (Streamlit)…"
# Respect custom port by passing --server.port
python3 -m streamlit run dash/app.py --server.port="$PORT" &

echo "⏳ Attendo disponibilità su http://localhost:$PORT …"
wait_for_port localhost "$PORT" 30

URL="http://localhost:$PORT"
echo "✅ TokIntel attivo su: $URL"
open_url "$URL"

if [ "$SHOW_LOGS" -eq 1 ]; then
  echo "📜 Logs (CTRL+C per uscire)…"
  LOGFILE="$(ls -1t ~/.streamlit/logs/*.log 2>/dev/null | head -n1 || true)"
  if [ -n "$LOGFILE" ]; then tail -f "$LOGFILE"; else tail -f /dev/null; fi
fi

# =====================
# Makefile targets (aggiungi nel tuo Makefile)
# ---------------------
# start: ## Avvia TokIntel in modalità smart (auto docker/venv)
# 	./start_tokintel_auto.sh
#
# start-docker: ## Forza Docker
# 	./start_tokintel_auto.sh --mode docker
#
# start-venv: ## Forza venv
# 	./start_tokintel_auto.sh --mode venv
#
# start-logs: ## Avvia e mostra i log
# 	./start_tokintel_auto.sh --logs
#
# start-port: ## Avvia su porta custom (es. 8600)
# 	PORT=8600 ./start_tokintel_auto.sh
#
# stop: ## Stop rapido (docker/down o kill porta)
# 	./start_tokintel_auto.sh --stop
