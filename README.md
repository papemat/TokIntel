# TokIntel - Analisi Multimodale di Video

![Quickstart Ready](https://img.shields.io/badge/Quickstart-Ready-brightgreen)
![Cross‑Platform](https://img.shields.io/badge/Launchers-macOS%2FLinux%2FWindows-blue)
![Release v1.1.0](https://img.shields.io/badge/Release-v1.1.0--Quickstart-blue)

<p align="center">
  <img src="docs/images/docs-ready-badge-glow.png" alt="Docs Ready" height="24" />
  <a href="https://github.com/papemat/TokIntel/actions">
    <img src="https://img.shields.io/badge/CI-passing-brightgreen" alt="CI Status" />
  </a>
</p>

[![CI](https://github.com/papemat/TokIntel/actions/workflows/ci.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/ci.yml)
[![Docs Ready](https://img.shields.io/badge/docs-ready-passing-brightgreen)](docs/status.json)
[![E2E](https://github.com/papemat/TokIntel/actions/workflows/sprint3-e2e.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/sprint3-e2e.yml)
[![Exports](https://github.com/papemat/TokIntel/actions/workflows/export-health.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/export-health.yml)
[![Perf Nightly](https://github.com/papemat/TokIntel/actions/workflows/perf-nightly.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/perf-nightly.yml)
[![Coverage HTML (main)](https://img.shields.io/badge/Coverage%20HTML-main-blue)](https://papemat.github.io/TokIntel/main/index.html)
[![Codecov](https://codecov.io/gh/papemat/TokIntel/branch/main/graph/badge.svg)](https://codecov.io/gh/papemat/TokIntel)
[![Target ≥40%](https://img.shields.io/badge/Target-%E2%89%A540%25-success?color=brightgreen)](https://codecov.io/gh/papemat/TokIntel)
[![Go‑Live Docs](https://img.shields.io/badge/docs-go--live-brightgreen)](docs/GO_LIVE_CHECKLIST.md)
[![Enterprise Setup](https://img.shields.io/badge/docs-enterprise--setup-informational)](docs/ENTERPRISE_SETUP.md)
[![Performance Dashboard](https://img.shields.io/badge/dashboard-perf--trends-orange?style=flat&logo=chart-line)](http://localhost:8502)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](#)
[![Monitor Hourly](https://img.shields.io/github/actions/workflow/status/papemat/TokIntel/monitor-ci-hourly.yml?label=Monitor%20Hourly)](https://github.com/papemat/TokIntel/actions/workflows/monitor-ci-hourly.yml)
[![Quick Start Guard](https://github.com/papemat/TokIntel/actions/workflows/quickstart-guard.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/quickstart-guard.yml)
![Docs Idempotency](https://img.shields.io/badge/docs_idempotent-checked-success)

## 📈 Ultimi esiti monitor

> Stato automatico del workflow **Monitor CI/Visual** (cron + manuale).  
> Fonte: `docs/monitor_history.json` (aggiornato via GitHub Actions).

<!-- MONITOR_STATUS:START -->
_(in attesa del primo aggiornamento automatico)_
<!-- MONITOR_STATUS:END -->

TokIntel è un sistema di analisi multimodale per video che combina:
- **Estrazione audio** (Whisper)
- **Estrazione visiva** (OCR + CLIP)
- **Indicizzazione semantica** (FAISS)
- **Ricerca unificata** (testo + visivo)

## 📊 Monitoraggio CI

Questa sezione mostra lo stato in tempo reale dei workflow CI/CD per TokIntel e fornisce link diretti agli artifact prodotti.

| Badge | Descrizione | Frequenza | Artifact Principali |
|-------|-------------|-----------|---------------------|
| [![E2E](https://github.com/papemat/TokIntel/actions/workflows/sprint3-e2e.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/sprint3-e2e.yml) | **Test End-to-End completi** su tutti i componenti | Ad ogni push e PR | [E2E Artifacts](https://github.com/papemat/TokIntel/actions/workflows/sprint3-e2e.yml) *(contiene screenshot, report HTML)* |
| [![Exports](https://github.com/papemat/TokIntel/actions/workflows/export-health.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/export-health.yml) | Verifica che gli export siano presenti e aggiornati nelle ultime 24h | Giornaliero + manuale | [Latest Exports](https://github.com/papemat/TokIntel/actions/workflows/export-health.yml) |
| [![Lint Makefile](https://github.com/papemat/TokIntel/actions/workflows/sprint3-e2e.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/sprint3-e2e.yml) | Controlla che i comandi del Makefile usino TAB correttamente | Ad ogni PR | *(Nessun artifact — solo log)* |
| [![Smoke Test](https://github.com/papemat/TokIntel/actions/workflows/smoke-test.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/smoke-test.yml) | Heartbeat giornaliero: esegue test rapidi, verifica export e salva log | Giornaliero + manuale | [Latest Exports](https://github.com/papemat/TokIntel/actions/workflows/smoke-test.yml) · [Streamlit Log](https://github.com/papemat/TokIntel/actions/workflows/smoke-test.yml) |

### ℹ️ Come interpretare i badge
- **Verde** → tutto OK
- **Rosso** → errore nel workflow → aprire il log per dettagli
- **Grigio** → workflow non ancora eseguito

### 🎥 Tutorial: Come usare i badge CI

![Tutorial Monitoraggio CI](docs/images/ci-monitoring-tutorial.gif)

> Questa GIF mostra come:
> 1. Cliccare sul badge di un workflow
> 2. Aprire il run più recente
> 3. Scaricare gli artifact generati

## ⚡ Quick Start – TokIntel GUI

[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)
![Quickstart Ready](https://img.shields.io/badge/Quickstart-Ready-brightgreen)
![Cross‑Platform](https://img.shields.io/badge/Launchers-macOS%2FLinux%2FWindows-blue)

> **🚀 Nuovo!** [Quickstart completo](README_QUICKSTART.md) con script launcher e troubleshooting

### Fast launch
- macOS/Linux: `./scripts/run_tokintel.sh`
- Windows: `scripts\run_tokintel.bat`

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>


[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/