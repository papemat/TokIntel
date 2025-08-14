# 📚 Docs System — Final Pack (idempotente)

## Comandi
- `make docs-generate` → build auto-detect (Sphinx/MkDocs/script custom).
- `make docs-idem-soft` → check non bloccante (pre-commit).
- `make docs-idem-strict` → check bloccante (CI/PR).
- `make docs-scan` → scan anti-timestamp/hash/uuid.
- `make docs-clean` → pulizia output.
- `make docs-help` → riepilogo.

## Matrix on demand
- PR normale → singolo Python (`3.x`) veloce.
- Aggiungi **label `test-matrix`** o commenta **`/test-matrix`** sulla PR → attiva matrice `3.10, 3.11, 3.12`.

## Suggerimenti Sphinx/MkDocs
- Sphinx `conf.py`:
  ```python
  import os
  today = os.getenv("DOCS_BUILD_DATE", "1970-01-01")
  html_last_updated_fmt = today
  ```

* MkDocs:

  ```bash
  DOCS_BUILD_DATE=1970-01-01 mkdocs build --clean --strict
  ```

## 🧩 Enterprise Add-ons
- **Hook pre-push (STRICT)** con bypass: `SKIP_DOCS_STRICT=1 git push`
- **Workflow avanzato**: trigger su *PR*, *push su main*, *tag v\** e *nightly*
- **Concurrency** CI per evitare run sovrapposti
- **Artifact retention** 10 giorni per i diff
- **Template matrix** Python (3.10/3.11/3.12) opzionale
- **Rollback** sicuro: `bash scripts/docs_enterprise_rollback.sh`
