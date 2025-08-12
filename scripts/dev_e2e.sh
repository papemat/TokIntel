#!/usr/bin/env bash
set -euo pipefail

PORT="${TI_E2E_PORT:-8520}"
LOG="${TI_E2E_LOG:-streamlit_e2e.log}"

mkdir -p artifacts/e2e exports

echo "▶️  Avvio Streamlit su :$PORT (headless) con E2E mode..."
TI_E2E_MODE=1 TI_AUTO_EXPORT=1 \
python -m streamlit run dash/app.py --server.port "$PORT" --server.headless true >"$LOG" 2>&1 &

PID=$!
echo "🧠 PID streamlit: $PID (log: $LOG)"

echo "⏳ Health check con retry (max 60s)..."
START=$(date +%s)
until curl -fsS "http://localhost:${PORT}/?health=1" | grep -qi "OK"; do
  NOW=$(date +%s); ELAPSED=$((NOW-START))
  if [ "$ELAPSED" -gt 60 ]; then
    echo "❌ Health check timeout dopo 60s. Ultime righe log:"
    tail -n 120 "$LOG" || true
    kill "$PID" 2>/dev/null || true
    exit 1
  fi
  sleep 1
done

echo "✅ App pronta. Eseguo test E2E..."
if ! make ci-e2e-playwright; then
  echo "❌ E2E fallito. Tail log:"; tail -n 200 "$LOG" || true
  kill "$PID" 2>/dev/null || true
  exit 1
fi

echo "🧪 Export health:"
make export-health || true

echo "🧹 Stop Streamlit"
kill "$PID" 2>/dev/null || true

echo "🎉 Completato!"
