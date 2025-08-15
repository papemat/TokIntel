#!/usr/bin/env bash
set -euo pipefail

# ---- Config ----
PORT="${PORT:-8501}"                     # ereditata dal Makefile/ambiente
WATCH_DIRS=("dash" "utils" "scripts")    # cartelle principali
WATCH_GLOBS=("*.py" "*.md" "*.yml" "*.yaml" "*.toml" "*.sh" "Makefile")

# Costruisci lista percorsi esistenti
PATHS=()
for d in "${WATCH_DIRS[@]}"; do
  [ -d "$d" ] && PATHS+=("$d")
done
# aggiungi file top-level comuni se presenti
for g in "${WATCH_GLOBS[@]}"; do
  for f in $g; do
    [ -e "$f" ] && PATHS+=("$f")
  done
done
# fallback: se nessun path trovato, osserva la root (meno efficiente)
[ ${#PATHS[@]} -eq 0 ] && PATHS+=(".")

echo "🔭 dev-watch sources: ${PATHS[*]}"
export PORT

# Helper: run restart
restart() {
  echo "♻️  change detected → make dev-restart (PORT=$PORT)"
  make dev-restart || true
}

# 1) watchexec (consigliato)
if command -v watchexec >/dev/null 2>&1; then
  echo "👀 watcher: watchexec"
  exec watchexec \
    --watch "${PATHS[@]}" \
    --restart \
    --exts py,md,yml,yaml,toml,sh,Makefile \
    --shell=none -- make dev-restart
fi

# 2) entr
if command -v entr >/dev/null 2>&1; then
  echo "👀 watcher: entr"
  # genera lista file
  find "${PATHS[@]}" -type f \
    \( -name "*.py" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.sh" -o -name "Makefile" \) \
    | sort -u \
    | entr -r sh -c 'make dev-restart'
  exit $?
fi

# 3) fswatch (macOS)
if command -v fswatch >/dev/null 2>&1; then
  echo "👀 watcher: fswatch"
  fswatch -or 1 "${PATHS[@]}" | while read _; do restart; done
  exit 0
fi

# 4) inotifywait (Linux)
if command -v inotifywait >/dev/null 2>&1; then
  echo "👀 watcher: inotifywait"
  while inotifywait -r -e close_write,move,create,delete "${PATHS[@]}"; do
    restart
  done
  exit 0
fi

# 5) Python watchdog (se disponibile)
if command -v python3 >/dev/null 2>&1 && python3 - <<'PY' >/dev/null 2>&1
import importlib.util
import sys
spec = importlib.util.find_spec("watchdog")
sys.exit(0 if spec else 1)
PY
then
  echo "👀 watcher: python watchdog"
  python3 - <<PY
import os, time, subprocess, sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PORT = os.environ.get("PORT", "8501")
PATHS = ${PATHS!r}

class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Filtra solo i file interessanti
        good = (".py",".md",".yml",".yaml",".toml",".sh")
        if event.is_directory:
            return
        if not event.src_path.endswith(good) and os.path.basename(event.src_path)!="Makefile":
            return
        print("♻️  change detected → make dev-restart (PORT=%s)" % PORT, flush=True)
        try:
            subprocess.run(["make","dev-restart"], check=False)
        except Exception as e:
            print("warn:", e, flush=True)

obs = Observer()
handler = Handler()
for p in PATHS:
    obs.schedule(handler, p, recursive=True)
obs.start()
print("watching:", PATHS, flush=True)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    obs.stop(); obs.join()
PY
  exit 0
fi

# 6) Fallback: polling (portabile)
echo "👀 watcher: polling fallback (no watchexec/entr/fswatch/inotifywait/watchdog)"
last=""
while true; do
  # calcola checksum dello snapshot filelist + mtime
  sig="$(/usr/bin/env bash -lc 'find ${PATHS[@]} -type f \( -name "*.py" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.sh" -o -name "Makefile" \) -print0 | xargs -0 stat -f "%N %m" 2>/dev/null || find ${PATHS[@]} -type f -printf "%p %T@\n" 2>/dev/null' | sort | shasum | awk "{print \$1}")"
  if [ "$last" != "$sig" ]; then
    [ -n "$last" ] && restart
    last="$sig"
  fi
  sleep 2
done
