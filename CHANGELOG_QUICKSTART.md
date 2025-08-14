# Changelog - TokIntel Quickstart Bundle

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
