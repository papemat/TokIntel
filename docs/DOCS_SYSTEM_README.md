# 📚 Docs System – One Shot

Questo sistema garantisce che la generazione/aggiornamento della documentazione sia **idempotente**.

## Componenti
- `scripts/cursor_docs_strict.sh` → Verifica STRICT (CI): 2 run consecutivi, fallisce se il secondo produce diff.
- Hook pre-commit (SOFT) → Avvisa ma **non blocca** i commit.
- Target Makefile:
  - `docs-generate` (facoltativo, se già presente verrà usato)
  - `docs-idem-soft` → Avvisa senza fallire
  - `docs-idem-strict` → Fallisce su non-idempotenza

## Uso rapido
```bash
bash setup_docs_system_one_shot.sh      # setup completo (questo file viene creato da Cursor)
make docs-idem-soft                     # warning ma non blocca
make docs-idem-strict                   # hard fail se non idempotente
```

## In CI (GitHub Actions)

Usa lo step in `CI_STRICT_STEP_YAML.md` per integrare nel workflow.
