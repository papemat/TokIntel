# Sprint 4 Patch Set - Playwright E2E Upgrade

## 🎯 Obiettivo
Mini-upgrade per migliorare l'E2E testing con Playwright:
- Screenshot automatici quando l'E2E Playwright fallisce
- Uso del Python del venv in Playwright test
- Target Make per installare i browser
- Step CI per installare Chromium e lanciare l'Export Health Report dopo i test

## ✅ Modifiche Applicate

### 1. Playwright E2E: screenshot on failure + venv Python + selettori affidabili
**File**: `tests/e2e/test_streamlit_ui_playwright.py`

- ✅ Aggiunto `import sys` per usare `sys.executable`
- ✅ Creato `SCREEN_DIR = EXPORT_DIR / "screenshots"` per salvare artifacts
- ✅ Sostituito `"python"` con `sys.executable` nel subprocess
- ✅ Aggiunto try/catch con screenshot e HTML capture on failure
- ✅ Sostituito `time.sleep(3)` con `page.wait_for_timeout(2500)`
- ✅ Aggiunto `finally` block per chiudere browser
- ✅ **Selettori affidabili**: `get_by_placeholder("Type your query…")` e `get_by_role("button", name="Search")`
- ✅ **Polling elegante**: Conta export prima/dopo e aspetta fino a 10s per nuovi file

### 2. Makefile: target per install Playwright browsers
**File**: `Makefile`

- ✅ Aggiornato target `test-e2e-playwright` per usare `$(PY)`
- ✅ Aggiunto nuovo target `playwright-install`:
  ```makefile
  .PHONY: playwright-install
  playwright-install: ## Install Playwright browsers
      $(PY) -m pip install -q pytest-playwright playwright
      $(PY) -m playwright install chromium
  ```

### 3. CI: install browsers + export health dopo E2E
**File**: `.github/workflows/sprint3-e2e.yml`

- ✅ Aggiornato step "Install deps" per installare Playwright:
  ```yaml
  pip install pytest-playwright playwright
  python -m playwright install chromium
  ```
- ✅ Aggiunto step "Export health report" dopo E2E:
  ```yaml
  - name: Export health report
    run: python scripts/export_health.py
  ```
- ✅ Aggiornato upload artifacts per includere screenshots:
  ```yaml
  path: |
    exports/*.csv
    exports/*.json
    exports/screenshots/*.png
    exports/screenshots/*.html
  ```

### 4. UI Streamlit: selettori affidabili per E2E
**File**: `dash/app.py`

- ✅ Aggiornato text input con placeholder univoco: `placeholder="Type your query…", key="query_input"`
- ✅ Aggiornato search button con key univoco: `key="search_btn"`

### 5. README: nota screenshot e target playwright
**File**: `README.md`

- ✅ Aggiunto sotto "Sprint 4 Additions":
  - **Failure artifacts**: in caso di errore E2E Playwright, screenshot + HTML vengono salvati in `exports/screenshots/`
  - **Install browsers**: comando `make playwright-install` per installare browser prima del primo run

## 🚀 Comandi Rapidi

```bash
# 1) Installare browser Playwright (una volta)
make playwright-install

# 2) Eseguire E2E Playwright
make test-e2e-playwright

# 3) Report export (anche in CI)
make export-health
```

## 📁 Struttura Nuova

```
exports/
├── *.csv                    # Export files esistenti
├── *.json                   # Export files esistenti
└── screenshots/             # 🆕 Directory per artifacts
    ├── playwright_fail_YYYYMMDD_HHMMSS.png
    └── playwright_fail_YYYYMMDD_HHMMSS.html
```

## 🧪 Test Verificati

Tutti i 6 test del patch set sono passati:
- ✅ Playwright installation
- ✅ Screenshots directory
- ✅ Make targets
- ✅ Playwright test file
- ✅ CI workflow
- ✅ **E2E Playwright test completo** - selettori affidabili + polling + fallback per risultati

## 🔄 Prossimi Passi

1. **✅ Selettori aggiornati**: I selettori nel test Playwright sono ora affidabili:
   ```python
   textbox = page.get_by_placeholder("Type your query…")
   search_btn = page.get_by_role("button", name="Search")
   ```

2. **✅ Test E2E funzionante**: Il test Playwright completo passa con successo.

3. **Testare in CI**: Il prossimo push/PR attiverà il workflow aggiornato.

4. **Monitorare artifacts**: Verificare che screenshots e HTML vengano salvati correttamente in caso di failure.

## 📊 Impatto

- **Robustezza**: E2E test più affidabili con artifacts di debug
- **Debugging**: Screenshot e HTML salvati automaticamente in caso di failure
- **CI/CD**: Workflow più completo con installazione browser e health report
- **Developer Experience**: Target Make semplificano l'uso di Playwright
