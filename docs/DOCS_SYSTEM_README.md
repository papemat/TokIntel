# 📚 Docs System — Final Pack (idempotente)

Sistema universale per garantire **idempotenza** nella generazione/aggiornamento della documentazione.

## Come funziona
- `scripts/docs_generate_auto.sh` rileva automaticamente **Sphinx**, **MkDocs** o script custom.
- Preset **riproducibili** (env/seed/scrub) riducono differenze (timestamp, hash, uuid, ordinamenti).
- `scripts/cursor_docs_strict.sh` esegue due run consecutivi e fallisce se il secondo produce diff.

## Target Makefile
- `make docs-generate` → genera/aggiorna doc (auto-detect).
- `make docs-idem-soft` → check non bloccante (pre-commit).
- `make docs-idem-strict` → check bloccante (CI/PR).
- `make docs-clean` → pulizia output.
- `make docs-help` → riepilogo.

## Sphinx/MkDocs (suggerimenti)
- Sphinx `conf.py`:
  ```python
  import os
  today = os.getenv("DOCS_BUILD_DATE", "1970-01-01")
  html_last_updated_fmt = today
  ```

- MkDocs:
  ```bash
  DOCS_BUILD_DATE=1970-01-01 mkdocs build --clean --strict
  ```

## Badge (facoltativo)

`![Docs Idempotency](https://img.shields.io/badge/docs_idempotent-checked-success)`
