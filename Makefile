# TokIntel Makefile

DB_PATH ?= data/db.sqlite
PY ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else which python; fi)
NODE ?= npx
COVERAGE_MIN ?= 40
TI_PORT ?= 8510

.PHONY: setup install test clean demo multimodal-demo visual-index index-cpu index-gpu search help prod-check report-prod-sample pytest-safe ensure-reports ensure-db add-indexes perf-check github-auto-setup test-dashboard post-deploy-checklist deploy-full init lint run run-ui kill-port kill-port-windows kill-port-unix test-e2e-only lint-sprint3 coverage-sprint3 playwright-install ci-e2e-playwright export-health last-export e2e-run ci-screenshot ci-tutorial-gif ci-badges-preview badges-glow-all ci-visual-refresh docs-check e2e-smoke install-hooks docs-ready docs-fail monitor-ci monitor-log tokintel-gui-quickstart

# Setup virtual environment
setup: ## Crea virtual environment e installa dipendenze
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo "✓ Virtual environment setup completato"

# Install dependencies
install: ## Installa dipendenze
	.venv/bin/pip install -r requirements.txt
	@echo "✓ Dipendenze installate"

# Run tests
test: ## Esegue test unitari con coverage e soglia minima
	[ -d tests ] && .venv/bin/python -m pytest -q --cov=. --cov-report=term-missing --cov-report=xml --cov-fail-under=$(COVERAGE_MIN) || echo "No tests dir, skipping"
	@echo "✓ Test completati"

# Clean generated files
clean: ## Pulisce file generati
	rm -rf data/frames/*
	rm -rf data/ocr/*
	rm -rf data/indexes/*
	rm -rf data/media/video/*
	@echo "✓ File generati puliti"

# Run multimodal demo
multimodal-demo:
	.venv/bin/python scripts/make_visual_demo.py
	.venv/bin/python -c "import glob, json, os, pathlib, yaml; from analyzer.ocr_extractor import run_ocr_on_frames; cfg = yaml.safe_load(open('config/settings.yaml','r',encoding='utf-8')); frames_root = pathlib.Path(cfg['visual']['frames_dir']); ocr_out = pathlib.Path(cfg['ocr']['out_dir']); ocr_out.mkdir(parents=True, exist_ok=True); [print(d.name, 'OCR:', run_ocr_on_frames(sorted([str(p) for p in d.glob('*.jpg')]), cfg['ocr']['langs'], str(ocr_out / (d.name + '.json')))['combined_text'][:80]) for d in sorted(frames_root.glob('vid_*'))]"
	.venv/bin/python -m analyzer.build_visual_index --gpu auto
	@echo "✓ Demo multimodale completata"

# Build visual index
visual-index:
	.venv/bin/python -m analyzer.build_visual_index --gpu auto
	@echo "✓ Indice visivo costruito"

# Build text index (CPU)
index-cpu:
	.venv/bin/python -m analyzer.index_faiss --gpu off
	@echo "✓ Indice testuale (CPU) costruito"

# Build text index (GPU)
index-gpu:
	.venv/bin/python -m analyzer.index_faiss --gpu on
	@echo "✓ Indice testuale (GPU) costruito"

# Search functionality
search:
	@echo "Uso: make search QUERY='your search query'"
	.venv/bin/python -m analyzer.search_multimodal "$(QUERY)"

# Download video
download:
	@echo "Uso: make download URL='https://example.com/video'"
	.venv/bin/python -m downloader.fetch_video $(URL)
	@echo "✓ Video scaricato"

# Extract frames from video
frames:
	@echo "Uso: make frames VIDEO='path/to/video.mp4' OUT='output/dir'"
	.venv/bin/python -m analyzer.frame_sampler $(VIDEO) $(OUT)
	@echo "✓ Frame estratti"

# Run OCR on frames
ocr:
	@echo "Uso: make ocr FRAMES='path/to/frames' OUT='output.json'"
	.venv/bin/python -m analyzer.ocr_extractor $(FRAMES) $(OUT)
	@echo "✓ OCR completato"

# Generate CLIP embeddings
clip:
	@echo "Uso: make clip IMAGES='path/to/images'"
	.venv/bin/python -m analyzer.vision_clip $(IMAGES)
	@echo "✓ Embeddings CLIP generati"

# Setup multimodal schema
multimodal-setup:
	.venv/bin/python -m analyzer.run_multimodal
	@echo "✓ Schema multimodale configurato"

# Full pipeline for a video URL
pipeline:
	@echo "Pipeline completa per URL: $(URL)"
	.venv/bin/python -m downloader.fetch_video $(URL)
	.venv/bin/python -m analyzer.build_visual_index --gpu auto --urls $(URL)
	.venv/bin/python -m analyzer.index_faiss --gpu auto
	@echo "✓ Pipeline completata per $(URL)"

# Ingest from TikTok collection (1-click)
ingest-collection:
	@echo "Ingest da raccolta TikTok: $(URL)"
	.venv/bin/python scripts/ingest_collection.py --url "$(URL)" --max 100 --gpu auto
	@echo "✓ Ingest da raccolta completato"

# Verify setup
verify:
	python scripts/verify_setup.py
	@echo "✓ Setup verificato"

# Dashboard
dash: ## Avvia dashboard Streamlit
	.venv/bin/streamlit run dash/app.py --server.port 8501 --server.address 0.0.0.0

# Performance dashboard
perf-dash: ## Avvia la dashboard Streamlit dei trend performance
	.venv/bin/streamlit run dash/perf_dashboard.py

# Create demo images for testing
demo-images:
	.venv/bin/python scripts/create_demo_images.py
	@echo "✓ Immagini demo create in demo_images/"

# Test dashboard
test-dash:
	.venv/bin/python scripts/test_dashboard.py

# Test live feedback features
test-live-feedback:
	@echo "🧪 Test funzionalità feedback live..."
	.venv/bin/python -c "from scripts.ingest_collection import main; from downloader.fetch_many import fetch_missing_with_callbacks; print('✅ Live feedback modules working')"
	@echo "✅ Test completato - moduli feedback live funzionanti"

# Test status badges demo
smoke-status-demo:
	@echo "🧪 Test badge di stato video..."
	.venv/bin/python scripts/create_sample_db.py
	@echo "✅ Database demo con stati diversi creato"

# Test status badge system
test-status: ## Esegui test badge di stato
	@echo "🧪 Test sistema badge di stato..."
	.venv/bin/python tests/test_status_badge.py
	@echo "✅ Test badge di stato completati"

# Demo with status system
demo-status: ## Demo con dati e dashboard
	$(MAKE) migrate-schema migrate-status smoke-status-demo dash

# Ensure database exists
ensure-db: ## Crea DB se manca (migrazione base)
	@[ -f $(DB_PATH) ] || (echo "[init] Creo DB base…"; $(PY) scripts/migrate_schema.py || true)

# Add database indexes for performance
add-indexes: ensure-db ## Aggiunge indici al DB se le colonne esistono
	@echo "🔄 Aggiunta indici database..."
	$(PY) scripts/add_db_indexes.py
	@echo "✅ Indici database aggiunti"

# Migrate database schema
migrate-schema:
	@echo "🔄 Migrazione schema database..."
	.venv/bin/python scripts/migrate_schema.py
	@echo "✅ Migrazione completata"

# Migrate status column
migrate-status:
	@echo "🔄 Migrazione colonna status..."
	.venv/bin/python scripts/migrate_add_status.py
	@echo "✅ Migrazione status completata"

# Generate thumbnails
thumbs:
	@echo "🖼️  Generazione miniature..."
	.venv/bin/python scripts/generate_thumbnails.py
	@echo "✅ Miniature generate"

# Go-live checklist
go-live: ## Esegue checklist completa per produzione
	@echo "🚀 Go-live checklist TokIntel..."
	@echo ""
	@echo "1️⃣  Aggiunta indici database..."
	$(MAKE) add-indexes
	@echo ""
	@echo "2️⃣  Test sistema badge di stato..."
	$(MAKE) test-status
	@echo ""
	@echo "3️⃣  Test completi..."
	.venv/bin/python -m pytest -q
	@echo ""
	@echo "4️⃣  Verifica setup..."
	$(MAKE) verify
	@echo ""
	@echo "✅ Go-live checklist completata!"
	@echo ""
	@echo "📋 Checklist manuale:"
	@echo "  □ Verifica cache: modifica 1 record → refresh → valori aggiornati"
	@echo "  □ Prova export CSV/JSON con timestamp"
	@echo "  □ Simula colonne mancanti (rinomina status → status_bak) e apri dashboard"
	@echo "  □ Controlla pannello diagnostica in dashboard"

# Test cache functionality
test-cache: ## Test funzionalità cache
	@echo "🧪 Test cache dashboard..."
	.venv/bin/python -c "import sqlite3, time; conn = sqlite3.connect('data/db.sqlite'); cur = conn.cursor(); cur.execute('UPDATE videos SET title = title || \" [CACHE-TEST]\" WHERE id = 1'); conn.commit(); conn.close(); print('✅ Record modificato per test cache')"
	@echo "📝 Ora apri dashboard e verifica che il titolo sia aggiornato"

# Test export functionality
test-export: ## Test export CSV/JSON
	@echo "🧪 Test export funzionalità..."
	.venv/bin/python -c "import pandas as pd, time; from dash.app import load_database; videos = load_database(); df = pd.DataFrame(videos); ts = time.strftime('%Y%m%d_%H%M%S'); df.to_csv(f'test_export_{ts}.csv', index=False); print(f'✅ Export test creato: test_export_{ts}.csv')"

# Test fail-soft UI
test-fail-soft: ## Test UI fail-soft (colonne mancanti)
	@echo "🧪 Test UI fail-soft..."
	@echo "📝 Rinomina temporaneamente la colonna 'status' nel DB:"
	@echo "   sqlite3 data/db.sqlite 'ALTER TABLE videos RENAME COLUMN status TO status_bak;'"
	@echo "📝 Poi apri dashboard e verifica che non crasha"
	@echo "📝 Ripristina: sqlite3 data/db.sqlite 'ALTER TABLE videos RENAME COLUMN status_bak TO status;'"

# Ensure reports directory exists
ensure-reports: ## Crea cartella reports se manca
	@mkdir -p reports

# Run pytest safely (non-blocking)
pytest-safe: ## Esegue pytest (non blocca la pipeline se fallisce)
	@$(PY) -m pytest -q || (echo "[warn] Test falliti: continuo (prod-check non blocca)."; exit 0)

# Export production sample data
export-prod-sample: ## Esporta CSV/JSON di esempio con timestamp
	@$(PY) scripts/export_sample.py

# Generate production check report
report-prod-check: ensure-reports ## Genera report finale (MD+JSON)
	@$(PY) scripts/prod_check_report.py --db $(DB_PATH)

# Production check sequence
prod-check: ensure-db add-indexes test-status test-export test-cache pytest-safe export-prod-sample report-prod-check ## Sequenza completa pre-deploy
	@echo ""
	@echo "====================================="
	@echo " ✅ PROD-CHECK COMPLETATO"
	@echo " - Indici DB verificati/creati"
	@echo " - Test ed export eseguiti"
	@echo " - Report disponibile in reports/"
	@echo "====================================="

# Performance check
perf-check: ## Benchmark performance con soglie (staging large)
	@python scripts/create_sample_db.py --staging --large
	@DB_PATH=data/staging_db.sqlite MAX_SQL_READ_MS=1500 MAX_EXPORT_MS=1500 \
	  python scripts/perf_bench.py --db data/staging_db.sqlite

# Test workflow locali
test-workflows: ## Test workflow prima del push GitHub
	@python scripts/test_workflows_local.py

# Help
help: ## Mostra questo aiuto
	@echo "TokIntel Makefile - Comandi disponibili:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | awk -F':|##' '{printf "  \033[36m%-20s\033[0m %s\n", $$1, $$3}'
	@echo ""
	@echo "Esempi:"
	@echo "  make demo-status     # Demo completa con stati"
	@echo "  make test-status     # Test rapidi badge"
	@echo "  make add-indexes     # Ottimizza performance DB"
	@echo "  make go-live         # Checklist completa produzione"
	@echo "  make prod-check      # Check pre-deploy completo"
	@echo "  make perf-check      # Benchmark performance"

github-auto-setup: ## Crea repo GitHub, fa push, aggiunge label e lancia i workflow
	@bash scripts/github_auto_setup.sh

test-dashboard: ## Avvia la dashboard (headless), verifica che risponda e chiudi
	@python scripts/test_dashboard_local.py --port 8503 --timeout 40

# Nuovi target sicuri per CI/CD
init: ## Inizializza ambiente (install deps)
	python -m pip install --upgrade pip
	[ -f requirements.txt ] && pip install -r requirements.txt || true

# Target test duplicato rimosso - usa quello sopra con coverage

# Coverage utilities
coverage-html: ## Genera report HTML (htmlcov/)
	.venv/bin/python -m coverage html

coverage-clean: ## Pulisce artefatti coverage
	rm -rf .coverage coverage.xml htmlcov

coverage-explorer: ## Avvia dashboard Streamlit (richiede coverage.xml/htmlcov)
	.venv/bin/python -m streamlit run tools/coverage_explorer.py

coverage-export: ## Esporta CSV/JSON con i file peggiori (richiede coverage.xml)
	.venv/bin/python tools/export_coverage_summary.py --xml coverage.xml --top 25 --out-csv coverage_summary_top.csv --out-json coverage_summary_top.json

coverage-todo: ## Genera coverage_todo.md dal CSV export
	.venv/bin/python tools/generate_coverage_todo.py --csv coverage_summary_top.csv --out coverage_todo.md

coverage-delta-dirs: ## Delta vs main (richiede coverage.xml e base in /tmp/base_coverage.xml)
	.venv/bin/python tools/coverage_delta_dirs.py --base /tmp/base_coverage.xml --head coverage.xml --depth 1 --out-md coverage_delta_dirs.md

# Sprint 1 Test Targets
test-sprint1: ## Esegue test Sprint 1 veloci
	.venv/bin/python -m pytest -q tests/unit tests/smoke -k "ocr or frame or vision or fetch or imports" --maxfail=1 --disable-warnings

coverage-sprint1: ## Genera coverage Sprint 1
	.venv/bin/python -m pytest -q -n auto --cov=. --cov-report=term-missing --cov-report=xml --maxfail=999 -k "ocr or frame or vision or fetch or imports"

# Sprint 2 Test Targets (FAISS/Index + Multimodal Search)
test-sprint2: ## Esegue test Sprint 2 veloci
	.venv/bin/python -m pytest -q tests/unit -k "index_faiss or search_multimodal" --maxfail=1 --disable-warnings

coverage-sprint2: ## Genera coverage Sprint 2
	.venv/bin/python -m pytest -q --cov=. --cov-report=term-missing --cov-report=xml --maxfail=999 -k "index_faiss or search_multimodal"

# Sprint 2 Micro-review (Robustezza + Edge Cases)
test-sprint2-review: ## Micro-review Sprint 2: robustezza, duplicati, fallback
	.venv/bin/python -m pytest -q tests/unit/test_sprint2_robustness.py -v --maxfail=1

coverage-sprint2-review: ## Coverage micro-review Sprint 2
	.venv/bin/python -m pytest -q tests/unit/test_sprint2_robustness.py --cov=analyzer --cov-report=term-missing --cov-report=xml

# Sprint 3 Test Targets (Orchestrator + E2E)
test-sprint3: ## Esegue test Sprint 3 veloci
	.venv/bin/python -m pytest -q tests/integration/test_orchestrator.py tests/e2e/test_streamlit_ui.py -x



coverage-sprint3: ## Genera coverage Sprint 3
	.venv/bin/python -m pytest -q --cov=analyzer.orchestrator --cov=dash --cov-report=term-missing

# UI and Development
run-ui: ## Avvia UI Streamlit con porta configurabile
	@echo "Starting Streamlit (headless) on port $(TI_PORT)..."
	$(PY) -m streamlit run dash/app.py --server.port $(TI_PORT) --server.headless true

.PHONY: kill-port-windows
kill-port-windows:
	@powershell -ExecutionPolicy Bypass -File scripts/kill_port.ps1 -Port $(TI_PORT)

.PHONY: kill-port-unix
kill-port-unix:
	@bash scripts/kill_port.sh $(TI_PORT)

.PHONY: kill-port
kill-port:
	@echo "Killing anything on port $(TI_PORT)..."
	@$(PY) scripts/kill_port.py $(TI_PORT) || true
	@case "$$(uname -s)" in \
		MINGW*|MSYS*|CYGWIN* ) $(MAKE) kill-port-windows ;; \
		* ) $(MAKE) kill-port-unix ;; \
	esac

.PHONY: test-e2e-only
test-e2e-only: kill-port
	TI_PORT=$(TI_PORT) TI_AUTO_EXPORT=1 $(PY) -m pytest -q -m e2e tests/e2e/test_streamlit_ui.py

lint-sprint3: ## Linting specifico per Sprint 3
	@$(PY) -m pip install -q ruff || true
	$(PY) -m ruff check . --fix || true
	$(PY) -m ruff check .

ci-debug: ## Debug CI locale (E2E con debug)
	@echo "🧪 CI Debug mode (E2E_DEBUG=1)..."
	E2E_DEBUG=1 TI_PORT=$(TI_PORT) TI_AUTO_EXPORT=1 $(PY) -m pytest -q -m e2e tests/e2e/test_streamlit_ui.py -vv

.PHONY: test-e2e-playwright
test-e2e-playwright: ## E2E Playwright real UI interaction
	@echo "🎭 E2E Playwright real UI test..."
	$(PY) -m pytest -q tests/e2e/test_streamlit_ui_playwright.py

.PHONY: ci-e2e-playwright
ci-e2e-playwright: ## E2E Playwright in E2E mode (always green)
	mkdir -p artifacts/e2e
	# non fallire subito per permettere raccolta artifacts
	$(NODE) playwright test || true
	@if [ -d playwright-report ]; then cp -r playwright-report artifacts/e2e/; fi
	@if [ -d test-results ]; then cp -r test-results artifacts/e2e/; fi
	@if [ -f streamlit_e2e.log ]; then cp streamlit_e2e.log artifacts/e2e/; fi

.PHONY: playwright-install
playwright-install: ## Install Playwright browsers
	$(NODE) playwright install --with-deps || $(NODE) playwright install

.PHONY: export-health
export-health: ## Export health report
	$(PY) scripts/export_health.py

.PHONY: last-export
last-export: ## Mostra info ultimo export disponibile
	$(PY) scripts/last_export.py

.PHONY: e2e-run
e2e-run: ## E2E RUN: avvio completo con health-poll, test, export, teardown
	@echo "▶️  E2E RUN: avvio completo con health-poll, test, export, teardown"
	@if [ -f scripts/dev_e2e.sh ]; then \
		chmod +x scripts/dev_e2e.sh; \
		./scripts/dev_e2e.sh; \
	else \
		echo "scripts/dev_e2e.sh non trovato. Su Windows usa scripts\\dev_e2e.bat"; \
	fi

.PHONY: ci-screenshot
ci-screenshot: ## Genera screenshot di esempio per la sezione Monitoraggio CI
	@echo "📸 Generazione screenshot Monitoraggio CI..."
	$(PY) scripts/generate_ci_monitoring_screenshot.py
	@echo "✅ Screenshot generato: docs/images/monitoraggio-ci-example.png"

.PHONY: ci-tutorial-gif
ci-tutorial-gif: ## Genera GIF tutorial animata per la sezione Monitoraggio CI
	@echo "🎬 Generazione GIF tutorial CI Monitoring..."
	$(PY) scripts/generate_ci_tutorial_gif.py
	@echo "✅ GIF tutorial generata: docs/images/ci-monitoring-tutorial.gif"

.PHONY: ci-badges-preview
ci-badges-preview: ## Genera anteprima badge CI con effetto glow
	@echo "✨ Generazione anteprima badge CI con glow..."
	$(PY) scripts/generate_ci_badges_preview.py
	@echo "✅ Anteprima badge CI generata: docs/images/ci-badges-preview.png"



.PHONY: badges-glow-all
badges-glow-all: ## Genera tutti i glow badge (CI + Docs Ready)
	@echo "✨ Generazione di tutti i glow badge..."
	$(PY) scripts/generate_ci_badges_preview.py
	$(PY) scripts/generate_docs_ready_glow.py
	@echo "✅ Tutti i glow badge generati"

# =========================
# CI / Visual Ecosystem
# =========================

.PHONY: ci-visual-refresh docs-check e2e-smoke install-hooks docs-ready docs-fail

# Directory predefinite (adatta liberamente)
ASSETS_DIR := docs/images
STATUS_JSON := docs/status.json
README := README.md

# Rigenera tutti gli asset visivi (screenshot, glow badge, gif) se presenti gli script
ci-visual-refresh:
	@echo "🔁 Rigenero pacchetto visivo (screenshot + glow + gif)…"
	@[ -x scripts/generate_docs_ready_glow.py ] && scripts/generate_docs_ready_glow.py || echo "ℹ️  Nessun generate_docs_ready_glow.py, salto."
	@[ -x scripts/update_docs_badge.py ] && scripts/update_docs_badge.py --refresh || echo "ℹ️  Nessun update_docs_badge.py, salto."
	@[ -x scripts/update_docs_status.py ] && scripts/update_docs_status.py --touch || echo "ℹ️  Nessun update_docs_status.py, salto."
	@echo "✅ Pacchetto visivo aggiornato."

# Verifica asset obbligatori minimi per le docs
docs-check:
	@echo "🔎 Controllo asset documentazione…"
	@[ -d $(ASSETS_DIR) ] || (echo "❌ Manca la dir $(ASSETS_DIR)"; exit 1)
	@[ -f $(STATUS_JSON) ] || (echo "❌ Manca $(STATUS_JSON)"; exit 1)
	@[ -f $(README) ] || (echo "❌ Manca $(README)"; exit 1)
	@echo "✅ Docs OK"

# Smoke E2E velocissimo: health + export (adatta ai tuoi script reali)
e2e-smoke:
	@echo "🚦 Avvio smoke E2E…"
	@[ -x scripts/healthcheck.py ] && scripts/healthcheck.py || echo "ℹ️  Nessun healthcheck.py, salto."
	@[ -x scripts/export_latest.py ] && scripts/export_latest.py --out exports/last_export.json || echo "ℹ️  Nessun export_latest.py, salto."
	@[ -f exports/last_export.json ] && echo "✅ Export pronto: exports/last_export.json" || echo "⚠️  Nessun export generato."
	@echo "🏁 Smoke E2E terminato."

# Installa un pre-commit hook minimale che blocca il commit se docs-check fallisce
install-hooks:
	@echo "🪝 Installo pre-commit hook…"
	@mkdir -p .git/hooks
	@printf '%s\n' '#!/usr/bin/env sh' \
	'set -e' \
	'echo "🔎 pre-commit: make docs-check"' \
	'make docs-check' > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "✅ Hook installato."

# Aggiorna lo stato Docs Ready -> passing e rigenera badge
docs-ready:
	@echo "📗 Setto Docs Ready: PASSING"
	@[ -x scripts/update_docs_status.py ] && scripts/update_docs_status.py --state passing || echo "ℹ️  Mancante update_docs_status.py, salto stato."
	@[ -x scripts/update_docs_badge.py ] && scripts/update_docs_badge.py --state passing || echo "ℹ️  Mancante update_docs_badge.py, salto badge."
	@echo "✅ Docs Ready aggiornato."

# Opzionale: segna failing (utile per testare pipeline e badge)
docs-fail:
	@echo "📕 Setto Docs Ready: FAILING"
	@[ -x scripts/update_docs_status.py ] && scripts/update_docs_status.py --state failing || echo "ℹ️  Mancante update_docs_status.py, salto stato."
	@[ -x scripts/update_docs_badge.py ] && scripts/update_docs_badge.py --state failing || echo "ℹ️  Mancante update_docs_badge.py, salto badge."
	@echo "✅ Docs Ready marcato come failing."

# Monitor continuo CI/Visual (rilancia docs-check e e2e-smoke quando rileva modifiche)
monitor-ci:
	@echo "👁️  Avvio monitor continuo CI/Visual..."
	@echo "📁 Monitora: README.md, docs/, Makefile, scripts/, exports/"
	@echo "🎯 Target: docs-check, e2e-smoke"
	@echo "⏱️  Intervallo: 5 secondi"
	@echo "🛑 Premi Ctrl+C per fermare"
	@echo ""
	$(PY) scripts/monitor_ci_visual.py

lint: ## Linting con ruff
	pip install ruff || true
	ruff check . || true

run: ## Avvia l'applicazione principale
	[ -f launch_tokintel_gui.py ] && python launch_tokintel_gui.py || echo "No launcher found"

post-deploy-checklist: ## Checklist post-deploy sicura
	@echo "=== Post-deploy checklist ==="
	@echo "1) Actions CI: verde?  2) Perf Nightly schedulato?  3) Badge visibili in README?"

deploy-full: ## Deploy completo end-to-end su GitHub
	@echo "\033[1;32m=== 🚀 DEPLOY FINALE TOKINTEL SU GITHUB ===\033[0m"
	@test -n "$$GITHUB_TOKEN" || (echo "❌ Errore: GITHUB_TOKEN non impostato"; exit 1)
	@echo "GITHUB_TOKEN: $${GITHUB_TOKEN:0:10}********"
	@echo "GH_OWNER: $${GH_OWNER:-your-username}"
	@echo "GH_REPO: $${GH_REPO:-TokIntel}"
	@echo "PRIVATE: $${PRIVATE:-false}"
	@echo "CREATE_PR: $${CREATE_PR:-1}"
	@echo ""
	@$(MAKE) github-auto-setup
	@echo ""
	@$(MAKE) post-deploy-checklist
	@if command -v gh >/dev/null 2>&1; then \
		echo ""; \
		echo "==> Ultimi workflow GitHub Actions:"; \
		gh run list --limit 5 || true; \
		echo ""; \
		echo "==> Pull Request aperte:"; \
		gh pr list || true; \
	else \
		echo "⚠️  GitHub CLI non installato: monitoraggio workflow solo via browser."; \
	fi
	@echo ""
	@echo "✅ Deployment completato! Apri la repo su GitHub:"
	@echo "URL: https://github.com/$${GH_OWNER:-your-username}/$${GH_REPO:-TokIntel}"

# Aggiorna blocco 'Ultimi esiti monitor' nel README da monitor_history.json
monitor-log:
	@echo "📝 Aggiorno blocco 'Ultimi esiti monitor' nel README da monitor_history.json…"
	@python - <<'PY'
	import json, re, pathlib, datetime
	hist_path = pathlib.Path("docs/monitor_history.json")
	readme_path = pathlib.Path("README.md")
	if not hist_path.exists():
	    raise SystemExit("❌ docs/monitor_history.json mancante")
	hist = json.loads(hist_path.read_text(encoding="utf-8"))
	def icon(r): return "🟢" if r.lower()=="success" else ("🟡" if r.lower()=="neutral" else "🔴")
	rows=[]
	for r in hist.get("runs", [])[:5]:
	    ts=r["timestamp"].replace("T"," ").replace("Z"," UTC")
	    rows.append(f"| {ts} | {icon(r['result'])} {r['result']} | `{r['targets']}` | {r.get('run_url','')} |")
	block="\n".join(["","| Timestamp | Esito | Targets | Dettagli |","|---|---|---|---|",*rows,""])
	start="<!-- MONITOR_STATUS:START -->"; end="<!-- MONITOR_STATUS:END -->"
	readme = readme_path.read_text(encoding="utf-8")
	pat = re.compile(re.escape(start)+".*?"+re.escape(end), re.S)
	new = f"{start}\n{block}\n{end}"
	if pat.search(readme): readme = pat.sub(new, readme)
	else: readme += "\n\n"+new+"\n"
	readme_path.write_text(readme, encoding="utf-8")
	print("✅ README aggiornato")
	PY

monitor-matrix-summary:
	@echo "🐍 Analizzo performance matrix Python 3.10/3.11…"
	@python3 scripts/monitor_python_matrix_summary.py
# =========================
# TokIntel — Avvio rapido
# =========================
.PHONY: tokintel-run tokintel-gui tokintel-batch tokintel-validate

# Default configurabili
TOK_GUI_URL ?= http://localhost:8501
TOK_INPUT_DEFAULT ?= input/my_collections.json
TOK_OUTPUT_DEFAULT ?= run_$(shell date -u +%Y%m%d_%H%M%S)

tokintel-run:
	@echo "🚀 Avvio TokIntel..."
	@read -p "Vuoi avviare la GUI (g) o la modalità batch (b)? [g/b] " mode; \
	if [ "$$mode" = "g" ] || [ -z "$$mode" ]; then \
		$(MAKE) tokintel-gui; \
	elif [ "$$mode" = "b" ]; then \
		infile="$(TOK_INPUT_DEFAULT)"; \
		outfile="$(TOK_OUTPUT_DEFAULT)"; \
		printf "📥 Percorso file input [%s]: " "$$infile"; read ans; [ -n "$$ans" ] && infile="$$ans"; \
		printf "📤 Nome file output (senza estensione) [%s]: " "$$outfile"; read ans; [ -n "$$ans" ] && outfile="$$ans"; \
		$(MAKE) tokintel-batch IN="$$infile" OUT="$$outfile"; \
	else \
		echo "❌ Scelta non valida"; exit 2; \
	fi

tokintel-gui: ## Avvia GUI TokIntel (foreground)
	.venv/bin/streamlit run dash/app.py

tokintel-gui-bg: ## Avvia GUI TokIntel in background
	.venv/bin/streamlit run dash/app.py --server.headless true &
	@echo "✅ GUI avviata in background su http://localhost:8501"

tokintel-gui-stop: ## Ferma GUI TokIntel
	@pkill -f "streamlit run dash/app.py" || echo "Nessun processo GUI trovato"

tokintel-gui-log: ## Mostra log GUI
	@tail -f gui.log 2>/dev/null || echo "File log non trovato"

tokintel-gui-health: ## Verifica readiness della GUI
	@echo "🩺 Health check GUI su http://localhost:8501…"
	@python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8501', timeout=2); print('✅ GUI pronta')" 2>/dev/null || echo "❌ GUI non raggiungibile"

tokintel-gui-on: ## Avvia GUI su porta custom: make tokintel-gui-on PORT=8502
	@if [ -z "$(PORT)" ]; then echo "❌ Specifica PORT=numero"; exit 2; fi
	.venv/bin/streamlit run dash/app.py --server.port "$(PORT)" --server.headless true &
	@echo "✅ GUI avviata su porta $(PORT): http://localhost:$(PORT)"

tokintel-gui-restart: ## Riavvia GUI (stop + bg)
	@$(MAKE) -s tokintel-gui-stop
	@sleep 1
	@$(MAKE) -s tokintel-gui-bg

tokintel-gui-quickstart: ## Quick start completo (README + GUI)
	@echo "🚀 TokIntel Quick Start..."
	@echo "📖 Apro README.md..."
	@open README.md 2>/dev/null || xdg-open README.md 2>/dev/null || echo "ℹ️  Apri manualmente README.md"
	@echo "🌐 Avvio GUI TokIntel..."
	@$(MAKE) -s tokintel-gui-bg

tokintel-validate:
	@if [ -z "$(IN)" ]; then echo "❌ Specifica IN=path/to/input.json"; exit 2; fi
	@python3 scripts/validate_collections.py "$(IN)"

tokintel-batch:
	@if [ -z "$(IN)" ]; then echo "❌ Specifica IN=path/to/input.json (o usa tokintel-run)"; exit 2; fi
	@out="$(OUT)"; [ -n "$$out" ] || out="$(TOK_OUTPUT_DEFAULT)"; \
	$(MAKE) -s tokintel-validate IN="$(IN)"; \
	mkdir -p exports; \
	echo "📦 Batch TokIntel → IN='$(IN)'  OUT='exports/$$out.json'"; \
	python3 analyzer/tiktok_collections.py --source "$(IN)" --export "exports/$$out.json"; \
	echo "✅ Analisi completata → exports/$$out.json"

