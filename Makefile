# TokIntel Makefile

DB_PATH ?= data/db.sqlite
PY ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else which python; fi)
NODE ?= npx
COVERAGE_MIN ?= 40
TI_PORT ?= 8510



# >>> DOCS SYSTEM TARGETS START >>>
.PHONY: docs-generate docs-idem-soft docs-idem-strict docs-help docs-clean

## docs-generate: genera/aggiorna la documentazione (auto-detect Sphinx/MkDocs/script)
docs-generate:
	@bash scripts/docs_generate_auto.sh

## docs-idem-soft: verifica non bloccante (pre-commit)
docs-idem-soft:
	@echo "== 🧪 Docs Idempotency SOFT =="
	@bash -c 'set -euo pipefail; \
	 bash scripts/docs_generate_auto.sh; \
	 git add -A >/dev/null 2>&1 || true; \
	 bash scripts/docs_generate_auto.sh; \
	 if ! git diff --quiet; then \
	   echo "⚠️  Non idempotente (soft): il secondo run ha prodotto modifiche."; \
	   git --no-pager diff --stat || true; \
	 else \
	   echo "✅ Idempotenza OK (nessuna modifica al secondo run)"; \
	 fi'

## docs-idem-strict: verifica bloccante (CI/locale)
docs-idem-strict:
	@bash scripts/cursor_docs_strict.sh

## docs-help: aiuto rapido
docs-help:
	@echo "Docs targets:"
	@echo "  make docs-generate     # genera/aggiorna doc (auto-detect)"
	@echo "  make docs-idem-soft    # check non bloccante (pre-commit)"
	@echo "  make docs-idem-strict  # check bloccante (CI/PR)"
	@echo "  make docs-clean        # pulizia output docs"

## docs-clean: pulizia output doc/artefatti
docs-clean:
	@rm -rf docs/_build site docs_idempotency.diff || true
# <<< DOCS SYSTEM TARGETS END <<<

