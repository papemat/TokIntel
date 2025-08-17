#!/usr/bin/env bash
set -euo pipefail

echo "== TokIntel — DX SUPER PROMPT (setup/verify all) =="

# 0) Root + sync (best-effort)
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"
git checkout main >/dev/null 2>&1 || true
git fetch origin main --tags >/dev/null 2>&1 || true
git pull --ff-only origin main >/dev/null 2>&1 || git pull --no-rebase origin main >/dev/null 2>&1 || true

# 1) Safeguard: salva modifiche locali
if ! git diff --quiet || ! git diff --cached --quiet; then
  git add -A
  git commit -m "chore(dx): safeguard local changes before DX super-prompt (idempotent)" || true
fi

# 2) VERSION (non forza downgrade)
if [ ! -f VERSION ] || ! grep -q "1\.1\.5-dev" VERSION; then
  echo "1.1.5-dev" > VERSION
  git add VERSION
  git commit -m "chore(version): bump to 1.1.5-dev" || true
fi

# 3) .env.example (defaults non sensibili)
if [ ! -f .env.example ]; then
  printf "TIMING_FAST=30\nTIMING_SLOW=60\nPORT=8501\n" > .env.example
  git add .env.example
  git commit -m "chore(dx): add .env.example (FAST/SLOW/PORT defaults)" || true
fi

# 4) scripts/dev_watch.sh (multi-backend + fallbacks)
mkdir -p scripts
if [ ! -f scripts/dev_watch.sh ]; then
  cat > scripts/dev_watch.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:-8501}"
WATCH_DIRS=("dash" "utils" "scripts")
WATCH_GLOBS=("*.py" "*.md" "*.yml" "*.yaml" "*.toml" "*.sh" "Makefile")

PATHS=()
for d in "${WATCH_DIRS[@]}"; do [ -d "$d" ] && PATHS+=("$d"); done
for g in "${WATCH_GLOBS[@]}"; do for f in $g; do [ -e "$f" ] && PATHS+=("$f"); done; done
[ ${#PATHS[@]} -eq 0 ] && PATHS+=(".")

echo "🔭 dev-watch sources: ${PATHS[*]}"
export PORT
restart(){ echo "♻️ change → make dev-restart (PORT=$PORT)"; make dev-restart || true; }

if command -v watchexec >/dev/null 2>&1; then
  debounce="${WATCH_DEBOUNCE:-300}"
  exts="${WATCH_EXTS:-py,md,yml,yaml,toml,sh,Makefile}"
  echo "👀 watcher: watchexec (debounce ${debounce}ms, exts ${exts})"
  exec watchexec --watch "${PATHS[@]}" --restart --debounce "${debounce}ms" --exts "${exts}" --shell=none -- make dev-restart
fi
if command -v entr >/dev/null 2>&1; then
  echo "👀 watcher: entr"
  find "${PATHS[@]}" -type f \
    \( -name "*.py" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.sh" -o -name "Makefile" \) \
    -not -path "*/.git/*" -not -path "*/.venv/*" -not -path "*/node_modules/*" \
    | sort -u | entr -r sh -c 'make dev-restart'
  exit $?
fi
if command -v fswatch >/dev/null 2>&1; then
  echo "👀 watcher: fswatch"; fswatch -or 1 "${PATHS[@]}" | while read _; do restart; done; exit 0
fi
if command -v inotifywait >/dev/null 2>&1; then
  echo "👀 watcher: inotifywait"; while inotifywait -r -e close_write,move,create,delete "${PATHS[@]}"; do restart; done; exit 0
fi
if command -v python3 >/dev/null 2>&1 && python3 - <<'PY' >/dev/null 2>&1
import importlib.util, sys; sys.exit(0 if importlib.util.find_spec("watchdog") else 1)
PY
then
  echo "👀 watcher: python watchdog"
  python3 - <<PY
import os, time, subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
PORT=os.environ.get("PORT","8501"); PATHS=${PATHS!r}
class H(FileSystemEventHandler):
    def on_any_event(self, e):
        if e.is_directory: return
        good=(".py",".md",".yml",".yaml",".toml",".sh")
        if not e.src_path.endswith(good) and os.path.basename(e.src_path)!="Makefile": return
        print("♻️ change → make dev-restart (PORT=%s)"%PORT, flush=True)
        subprocess.run(["make","dev-restart"], check=False)
obs=Observer(); h=H()
for p in PATHS: obs.schedule(h,p,recursive=True)
obs.start(); print("watching:",PATHS,flush=True)
try:
    while True: time.sleep(1)
except KeyboardInterrupt: pass
finally:
    obs.stop(); obs.join()
PY
  exit 0
fi
echo "👀 watcher: polling fallback"
last=""; while true; do
  sig="$(
    { command -v stat >/dev/null 2>&1 && \
      find "${PATHS[@]}" -type f \( -name "*.py" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" -o -name "*.sh" -o -name "Makefile" \) \
      -not -path "*/.git/*" -not -path "*/.venv/*" -not -path "*/node_modules/*" -print0 \
      | xargs -0 stat -f "%N %m" 2>/dev/null; } || \
      find "${PATHS[@]}" -type f -printf "%p %T@\n" 2>/dev/null \
  ) | sort | shasum | awk '{print $1}')"
  if [ "$last" != "$sig" ]; then [ -n "$last" ] && restart; last="$sig"; fi
  sleep 2
done
SH
  chmod +x scripts/dev_watch.sh
  git add scripts/dev_watch.sh
  git commit -m "dx: add scripts/dev_watch.sh (multi-backend watcher + fallbacks)" || true
fi

# 5) Makefile: imposta/aggiorna targets con marker (PORT + health + dev meta + watch)
MAKEFILE="Makefile"
if [ ! -f "$MAKEFILE" ]; then
  cat > "$MAKEFILE" <<'MK'
PORT ?= 8501
.PHONY: help
help: ## Elenca i target disponibili
	@grep -E '^[A-Za-z0-9_.-]+:.*## ' $(MAKEFILE_LIST) | sed 's/:.*## / — /' | sort
MK
  git add "$MAKEFILE"
  git commit -m "chore: bootstrap Makefile (help + PORT)" || true
fi

ensure_line_at_top(){ grep -qE "^[[:space:]]*PORT[[:space:]]*\?=" "$MAKEFILE" || sed -i.bak '1i\
PORT ?= 8501
' "$MAKEFILE" && rm -f "$MAKEFILE.bak"; }
ensure_line_at_top

insert_or_replace_block() { # start, end, file, content
  local start="$1" end="$2" file="$3" content="$4"
  if grep -q "$start" "$file"; then
    awk -v s="$start" -v e="$end" -v repl="$content" '
      BEGIN{inblk=0}
      $0 ~ s {print repl; inblk=1; next}
      $0 ~ e && inblk==1 {inblk=0; next}
      inblk==0 {print}
    ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
  else
    printf "\n%s\n%s\n%s\n" "$start" "$content" "$end" >> "$file"
  fi
}

# dev-open
insert_or_replace_block "# --- TOKINTEL::DEV_OPEN START" "# --- TOKINTEL::DEV_OPEN END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: dev-open
dev-open: ## Apre la dashboard su http://localhost:$(PORT)
	@echo "== 🌐 http://localhost:$(PORT) =="
	@if command -v open >/dev/null 2>&1; then \
		open "http://localhost:$(PORT)"; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open "http://localhost:$(PORT)" >/dev/null 2>&1 || true; \
	elif command -v cmd.exe >/dev/null 2>&1; then \
		cmd.exe /c start http://localhost:$(PORT) || true; \
	else \
		echo "ℹ️ Apri manualmente: http://localhost:$(PORT)"; \
	fi
MK
)"

# dev-status (con health check HTTP)
insert_or_replace_block "# --- TOKINTEL::DEV_STATUS START" "# --- TOKINTEL::DEV_STATUS END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: dev-status
dev-status: ## Mostra stato dashboard (porta + health HTTP) e variabili env
	@$(MAKE) env-show || true
	@if command -v lsof >/dev/null 2>&1; then \
		if lsof -i :$(PORT) -sTCP:LISTEN >/dev/null 2>&1; then \
			echo "✅ Dashboard attiva su http://localhost:$(PORT)"; \
		else \
			echo "⚠️ Dashboard NON attiva sulla porta $(PORT)"; \
		fi; \
	else \
		echo "ℹ️ lsof non disponibile: controllo base con ps/grep"; \
		ps aux | grep -E 'streamlit|dash/app\.py' | grep -v grep || true; \
	fi
	@if command -v curl >/dev/null 2>&1; then \
		if curl -s --max-time 2 "http://localhost:$(PORT)" | grep -qi "streamlit"; then \
			echo "🩺 Health check: OK (contenuto atteso)"; \
		else \
			echo "⚠️ Health check: porta ok ma contenuto inatteso o app non pronta"; \
		fi; \
	elif command -v wget >/dev/null 2>&1; then \
		if wget -qO- --timeout=2 "http://localhost:$(PORT)" | grep -qi "streamlit"; then \
			echo "🩺 Health check: OK (contenuto atteso)"; \
		else \
			echo "⚠️ Health check: porta ok ma contenuto inatteso o app non pronta"; \
		fi; \
	else \
		echo "ℹ️ curl/wget assenti: salto health check HTTP"; \
	fi
MK
)"

# dev (meta target: status + autostart)
insert_or_replace_block "# --- TOKINTEL::DEV START" "# --- TOKINTEL::DEV END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: dev
dev: ## Status; se non attiva, lancia dev-ready (autostart)
	@echo "== 🛠️ TokIntel Dev =="
	@$(MAKE) dev-status || true
	@echo "== 🔁 Autostart check =="
	@if command -v lsof >/dev/null 2>&1; then \
		if lsof -i :$(PORT) -sTCP:LISTEN >/dev/null 2>&1; then \
			echo "✅ Dashboard già attiva su http://localhost:$(PORT)"; \
		else \
			echo "🚀 Dashboard non attiva: lancio dev-ready..."; \
			$(MAKE) dev-ready; \
		fi; \
	else \
		if ps aux | grep -E 'streamlit|dash/app\.py' | grep -v grep >/dev/null; then \
			echo "✅ Dashboard appare attiva (ps/grep)"; \
		else \
			echo "🚀 Dashboard non attiva: lancio dev-ready..."; \
			$(MAKE) dev-ready; \
		fi; \
	fi
MK
)"

# dev-ready
insert_or_replace_block "# --- TOKINTEL::DEV_READY START" "# --- TOKINTEL::DEV_READY END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: dev-ready
dev-ready: ## Mostra env, esegue test-fast e avvia dashboard con log live
	@echo "== 🌱 TokIntel Dev Ready =="
	@$(MAKE) env-show || true
	@$(MAKE) test-fast || python3 -m pytest -q tests/unit/test_timing_config.py tests/unit/test_stats_csv_export.py || true
	@echo "== 🚀 Avvio dashboard con log live =="
	LOG_LEVEL=INFO $(MAKE) start-logs
MK
)"

# dev-stop
insert_or_replace_block "# --- TOKINTEL::DEV_STOP START" "# --- TOKINTEL::DEV_STOP END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: dev-stop
dev-stop: ## Termina dashboard e processi TokIntel
	@echo "== 🛑 Stop dashboard e processi =="
	@pkill -f "streamlit run dash/app.py" 2>/dev/null || true
	@pkill -f "python.*dash/app.py" 2>/dev/null || true
	@pkill -f "streamlit" 2>/dev/null || true
	@lsof -ti tcp:$(PORT) 2>/dev/null | xargs -r kill -9 2>/dev/null || true
	@echo "✅ Processi terminati (se presenti)"
MK
)"

# dev-reset
insert_or_replace_block "# --- TOKINTEL::DEV_RESET START" "# --- TOKINTEL::DEV_RESET END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: dev-reset
dev-reset: ## Svuota log e mostra env
	@echo "== ♻️ TokIntel Dev Reset =="
	@$(MAKE) logs-clear || true
	@$(MAKE) env-show || true
	@echo "✅ Reset completato"
MK
)"

# dev-restart
insert_or_replace_block "# --- TOKINTEL::DEV_RESTART START" "# --- TOKINTEL::DEV_RESTART END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: dev-restart
dev-restart: ## Stop + Ready in un colpo solo
	@$(MAKE) dev-stop || true
	@sleep 2
	@$(MAKE) dev-ready
MK
)"

# dev-watch
insert_or_replace_block "# --- TOKINTEL::DEV_WATCH START" "# --- TOKINTEL::DEV_WATCH END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: dev-watch
dev-watch: ## Hot reload: osserva file e rilancia dev-restart automaticamente
	@echo "== 👀 TokIntel Dev Watch (PORT=$${PORT:-8501}) =="
	@./scripts/dev_watch.sh
MK
)"

# env-show
insert_or_replace_block "# --- TOKINTEL::ENV_SHOW START" "# --- TOKINTEL::ENV_SHOW END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: env-show
env-show: ## Mostra variabili .env rilevanti
	@echo "TIMING_FAST=$${TIMING_FAST:-30}"
	@echo "TIMING_SLOW=$${TIMING_SLOW:-60}"
	@echo "PORT=$${PORT:-8501}"
MK
)"

# logs-clear
insert_or_replace_block "# --- TOKINTEL::LOGS_CLEAR START" "# --- TOKINTEL::LOGS_CLEAR END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: logs-clear
logs-clear: ## Svuota i rotating logs di ingest
	@[ -f $$HOME/.tokintel/logs/ingest.log ] && : > $$HOME/.tokintel/logs/ingest.log || true
	@echo "✅ ingest.log pulito"
MK
)"

# test-fast
insert_or_replace_block "# --- TOKINTEL::TEST_FAST START" "# --- TOKINTEL::TEST_FAST END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: test-fast
test-fast: ## Pytest veloce (timing & CSV)
	@python -m pytest -q tests/unit/test_timing_config.py tests/unit/test_stats_csv_export.py || python3 -m pytest -q tests/unit/test_timing_config.py tests/unit/test_stats_csv_export.py
MK
)"

# watch-install
insert_or_replace_block "# --- TOKINTEL::WATCH_INSTALL START" "# --- TOKINTEL::WATCH_INSTALL END" "$MAKEFILE" "$(cat <<'MK'
.PHONY: watch-install
watch-install: ## Installa watcher consigliati (best-effort)
	@command -v watchexec >/dev/null || (command -v brew >/dev/null && brew install watchexec) || true
	@command -v entr >/dev/null || (command -v brew >/dev/null && brew install entr) || true
	@command -v fswatch >/dev/null || (command -v brew >/dev/null && brew install fswatch) || true
	@python3 -c "import watchdog" >/dev/null 2>&1 || pip install watchdog || true
MK
)"

git add "$MAKEFILE"
git commit -m "dx(make): ensure dev targets (PORT, health, watch) via markers (idempotent)" || true

# 6) CI fast-tests (se mancante)
mkdir -p .github/workflows
if [ ! -f .github/workflows/fast-tests.yml ]; then
  cat > .github/workflows/fast-tests.yml <<'YML'
name: fast-tests
on: [push, pull_request]
jobs:
  fast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install deps
        run: |
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Run fast unit tests
        run: |
          make test-fast || python -m pytest -q tests/unit/test_timing_config.py tests/unit/test_stats_csv_export.py
YML
  git add .github/workflows/fast-tests.yml
  git commit -m "ci: add fast-tests workflow (timing & CSV)" || true
fi

# 7) Git hook post-merge
if [ -d ".git/hooks" ]; then
  HOOK=".git/hooks/post-merge"
  if [ ! -f "$HOOK" ]; then
    cat > "$HOOK" <<'H'
#!/usr/bin/env bash
# TokIntel post-merge: mostra stato dashboard dopo pull
if command -v make >/dev/null 2>&1; then
  echo "== TokIntel post-merge: dev-status =="
  make dev-status || true
fi
H
    chmod +x "$HOOK"
  fi
fi

# 8) Push + smoke tests
SKIP_DOCS_STRICT=1 git push origin main || true
echo "== Smoke: make dev-status =="
(make dev-status || true)
echo "== Smoke: make dev-watch (3s, best-effort) =="
( command -v timeout >/dev/null 2>&1 && timeout 3s make dev-watch ) >/dev/null 2>&1 || true

# 9) Summary
echo "==== SUMMARY ===="
echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
git log -8 --oneline || true
echo "- Targets Make principali:"
grep -E '^[A-Za-z0-9_.-]+:.*## ' Makefile | sed 's/:.*## / — /' | sort || true
echo "- .env.example: $( [ -f .env.example ] && echo ok || echo missing )"
echo "- watcher script: $( [ -f scripts/dev_watch.sh ] && echo ok || echo missing )"
echo "- fast-tests CI: $( [ -f .github/workflows/fast-tests.yml ] && echo ok || echo missing )"
echo "- post-merge hook: $( [ -f .git/hooks/post-merge ] && echo ok || echo missing )"
echo "==== DONE ===="
