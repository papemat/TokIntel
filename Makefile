# TokIntel Makefile

DB_PATH ?= data/db.sqlite
PY ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else which python; fi)
NODE ?= npx
COVERAGE_MIN ?= 40
TI_PORT ?= 8510



# >>> DOCS SYSTEM TARGETS START >>>

.PHONY: docs-generate docs-idem-soft docs-idem-strict docs-help

# docs-generate:
# - Se già definito altrove, verrà usato da scripts/cursor_docs_strict.sh.
# - Qui forniamo un fallback no-op per non rompere i repo che non hanno generatori ancora.

docs-generate:
	@echo "ℹ️  Fallback docs-generate (no-op)."
	@echo "   Sovrascrivi con il tuo generatore (es. sphinx, mkdocs, script python)."

docs-idem-soft:
	@echo "== 🧪 Docs Idempotency SOFT =="
	@bash -c 'set -euo pipefail; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	git add -A >/dev/null 2>&1 || true; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	if ! git diff --quiet; then \
		echo "⚠️  Non idempotente (soft): il secondo run ha prodotto modifiche."; \
		git --no-pager diff --stat || true; \
	else \
		echo "✅ Idempotenza OK (nessuna modifica al secondo run)"; \
	fi'

docs-idem-strict:
	@bash -c 'set -euo pipefail; scripts/cursor_docs_strict.sh'

docs-help:
	@echo "📚 Docs System - Comandi disponibili:"
	@echo "  make docs-generate    # Genera docs (fallback no-op)"
	@echo "  make docs-idem-soft   # Test soft (warning, non blocca)"
	@echo "  make docs-idem-strict # Test strict (fallisce se non idempotente)"
	@echo "  make docs-help        # Questo aiuto"

# <<< DOCS SYSTEM TARGETS END <<<

