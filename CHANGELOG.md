## [1.1.5-dev] — 2025-08-15
### Added
- Unit test per soglie timing FAST/SLOW e CSV export.
- Legenda soglie nella dashboard (env-driven).
- Target Make `test-fast` per test rapidi.

### Config
- Soglie timing configurabili via `.env`: `TIMING_FAST`, `TIMING_SLOW`.

---

## [1.1.4] — 2025-08-15

### Added

* Ingest Logs Panel avanzato con auto-refresh, filtro livelli, download/svuota, rotating logs.
* Sistema di timing per step e totale con colorazione soglie e pattern strutturati.
* Make targets: `test-timing`, `timing-demo`, `logs-tail`, `logs-open`, `logs-debug`.

### Config

* Variabile `LOG_LEVEL` e bootstrap macOS (`mac-bootstrap`, `mac-venv-rebuild`).


## [1.1.4] — 2025-08-15

### Added

* Ingest Logs Panel avanzato con auto-refresh, filtro livelli, download/svuota, rotating logs.
* Sistema di timing per step e totale con colorazione soglie e pattern strutturati.
* Make targets: `test-timing`, `timing-demo`, `logs-tail`, `logs-open`, `logs-debug`.

### Config

* Variabile `LOG_LEVEL` e bootstrap macOS (`mac-bootstrap`, `mac-venv-rebuild`).


# Changelog - TokIntel

## [1.1.4] — 2025-08-15
### Added
- Ingest Logs Panel avanzato con auto-refresh, filtro livelli, download/svuota, rotating logs.
- Sistema di timing per step e totale con colorazione soglie e pattern strutturati.
- Make targets: `test-timing`, `timing-demo`, `logs-tail`, `logs-open`, `logs-debug`.
### Config
- Variabile `LOG_LEVEL` e bootstrap macOS (`mac-bootstrap`, `mac-venv-rebuild`).

---

## v1.1.3 - 2025-08-12

### 🚀 Nuove funzionalità
- **Sistema di timing completo**: misurazione durata per step e totale ingest
- **Ingest Logs Panel**: visualizzazione log in tempo reale con auto-refresh
- **Statistiche ingest**: durate medie e identificazione colli di bottiglia
- **Rotating logs**: sistema di log rotanti con backup automatici

### 🔧 Miglioramenti
- Pattern log strutturati con emoji e colorazione automatica
- Dashboard con pannello log espandibile e filtri per livello
- Make targets per testing e demo del sistema timing
- Configurazione LOG_LEVEL per controllo granularità log

### 🐛 Correzioni
- Gestione robusta delle eccezioni nel sistema timing
- Compatibilità backward con ingest esistenti

---

## v1.1.2 - 2025-08-10

### 🚀 Nuove funzionalità
- **Sistema di monitoraggio CI**: Badge e indicatori visivi per stato CI
- **Documentazione dinamica**: Aggiornamento automatico badge e status
- **Workflow hardening**: Miglioramenti robustezza e gestione errori

### 🔧 Miglioramenti
- Script per generazione badge CI e monitoraggio
- Sistema di status badges per documentazione
- Workflow GitHub Actions ottimizzati

### 🐛 Correzioni
- Gestione errori migliorata nei workflow CI
- Compatibilità con diverse configurazioni ambiente

---

## v1.1.1 - 2025-01-14

### 🚀 Nuove funzionalità
- **Quickstart Bundle**: Pacchetto completo con launcher cross-platform (Unix/Windows)
- **Documentazione migliorata**: README_QUICKSTART.md con istruzioni dettagliate
- **FAQ Troubleshooting**: Guida per risolvere problemi comuni
- **Configurazione Streamlit**: File di esempio per configurazione rapida

### 🔧 Miglioramenti
- Launcher `run_tokintel.sh` per sistemi Unix con controlli automatici
- Launcher `run_tokintel.bat` per Windows con gestione errori
- Sistema di verifica prerequisiti integrato nei launcher
- Documentazione step-by-step per setup rapido

### 🐛 Correzioni
- Nessuna correzione in questa release

---

## v1.1.0 - 2025-01-13

### 🚀 Nuove funzionalità
- **Release automatica GitHub**: Workflow per creare release automatiche al push di tag `v*`
- **Generatore note**: Script Python per estrarre note di release dal changelog
- **Target Makefile**: Nuovi comandi `make notes`, `make quickstart-check`, `make run*`
- **Badge CI Release**: Indicatore visivo dello stato del workflow di release

### 🔧 Miglioramenti
- Integrazione completa con il sistema di release esistente
- Script riutilizzabili per generazione note in locale e CI
- Target Makefile coerenti con il workflow esistente

### 🐛 Correzioni
- Nessuna correzione in questa release

---

## v1.0.0 - 2025-01-01

### 🎉 Prima release
- Sistema di analisi multimodale completo
- GUI Streamlit integrata
- Workflow CI/CD robusto
- Documentazione completa
