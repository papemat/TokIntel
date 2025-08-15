# 🚀 TokIntel - Onboarding Sviluppatore

## Comandi Rapidi per Sviluppo

### 🎯 **Comandi Principali**

```bash
# Avvio dashboard con status e autostart
make dev

# Apre la dashboard nel browser (cross-platform)
make dev-open

# Mostra stato dashboard/porte/env
make dev-status

# Setup completo: env + test-fast + start-logs
make dev-ready

# Ferma dashboard
make dev-stop

# Reset pulito (svuota log + mostra env)
make dev-reset

# Restart completo (stop + ready)
make dev-restart

# Watch file changes e auto-restart
make dev-watch
```

### 🧪 **Testing**

```bash
# Test unitari rapidi
make test-fast

# Test completi con coverage
make test

# Test specifici per sprint
make test-sprint1
make test-sprint2
make test-sprint3
```

### 🔧 **Utilità Base**

```bash
# Mostra variabili env
make env-show

# Svuota log ingest
make logs-clear

# Verifica setup
make verify

# Aggiungi indici DB (performance)
make add-indexes
```

### 🌐 **Dashboard e UI**

```bash
# Avvia dashboard Streamlit
make dash

# Avvia su porta custom (es. 8600)
make start-port

# Avvia in background (non blocca terminale)
make tokintel-gui-bg

# Ferma dashboard in background
make tokintel-gui-stop
```

### 👁️ **Watch Mode (Auto-restart)**

```bash
# Watch file changes e auto-restart
make dev-watch

# Prerequisiti:
# macOS: brew install fswatch
# Linux: sudo apt install inotify-tools
```

### 📊 **Performance e Monitoraggio**

```bash
# Benchmark performance
make perf-check

# Dashboard performance trends
make perf-dash

# Monitor CI continuo
make monitor-ci
```

### 🐳 **Docker (se configurato)**

```bash
# Build container
make docker-build

# Avvia con Docker Compose
make docker-up

# Ferma container
make docker-down
```

### 🔄 **Workflow Completi**

```bash
# Demo completa con stati
make demo-status

# Checklist produzione
make go-live

# Check pre-deploy
make prod-check

# Setup GitHub automatico
make github-auto-setup
```

## 🎯 **Workflow Tipico per Nuovi Contributor**

1. **Setup iniziale:**
   ```bash
   make setup
   make verify
   ```

2. **Avvio sviluppo:**
   ```bash
   make dev-ready    # Setup completo
   make dev-open     # Apri browser
   ```

3. **Durante sviluppo:**
   ```bash
   make test-fast    # Test rapidi
   make dev-status   # Controlla stato
   ```

4. **Fine sessione:**
   ```bash
   make dev-stop     # Ferma tutto
   make dev-reset    # Reset pulito
   ```

5. **Restart rapido:**
   ```bash
   make dev-restart  # Stop + Ready in un colpo
   ```

## 📝 **Note Utili**

- **Porta default:** `8501` (configurabile con `PORT=8600`)
- **Log:** `~/.tokintel/logs/ingest.log`
- **DB:** `data/tokintel.db`
- **Export:** `exports/` directory

### Cambiare porta
Se `8501` è occupata:
```bash
make dev PORT=8502
```

Poi apri:
```bash
make dev-open PORT=8502
```

## 🆘 **Troubleshooting**

```bash
# Se la dashboard non si avvia
make dev-stop
make dev-reset
make dev-ready

# Se ci sono problemi con il DB
make ensure-db
make add-indexes

# Se i test falliscono
make test-fast
make verify
```

---

**💡 Pro tip:** Usa `make help` per vedere tutti i comandi disponibili!
