# Docs System — Strict + Soft

## Obiettivi
- Anti-duplicati blocco **Quick Start**
- **Idempotenza** (due run consecutivi → nessuna diff)
- **Linkcheck**, **Markdownlint**, **Glow badges**
- **Locale soft**, **CI strict**

## Uso rapido
- Strict end‑to‑end + PR:  
  ```bash
  scripts/cursor_docs_strict.sh
  ```

* Mini check idempotenza:

  ```bash
  python3 .github/scripts/autofix_quickstart.py && \
  python3 .github/scripts/autofix_quickstart.py && \
  git diff --quiet && echo "✅ OK" || echo "❌ Non idempotente"
  ```

## Flow consigliato

1. Sviluppo locale: **soft**
2. Prima della PR: `make docs-idem-strict` (deve passare)
3. CI/PR: **strict** (blocca se non idempotente)
