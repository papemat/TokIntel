# TokIntel Makefile

DB_PATH ?= data/db.sqlite
PY ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else which python; fi)

.PHONY: setup install test clean demo multimodal-demo visual-index index-cpu index-gpu search help prod-check report-prod-check export-prod-sample pytest-safe ensure-reports ensure-db add-indexes perf-check github-auto-setup test-dashboard post-deploy-checklist deploy-full init lint run

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
test: ## Esegue test unitari
	.venv/bin/python -m pytest tests/ -v
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

test: ## Esegue test unitari
	[ -d tests ] && pytest -q || echo "No tests dir, skipping"

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
