#!/usr/bin/env bash
set -euo pipefail
PORT="${1:-8510}"
echo "🔪 Killing processes on port ${PORT} (Unix)..."
if command -v lsof >/dev/null 2>&1; then
  PIDS=$(lsof -ti tcp:"${PORT}" || true)
  if [ -n "${PIDS}" ]; then echo "${PIDS}" | xargs -r kill -9 || true; fi
elif command -v fuser >/dev/null 2>&1; then
  fuser -k "${PORT}"/tcp || true
else
  echo "Neither lsof nor fuser found. Skipping."
fi
echo "✅ Done."
