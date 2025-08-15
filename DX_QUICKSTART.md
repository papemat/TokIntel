# TokIntel DX Quickstart

## 🚀 Setup Completo (Idempotente)

```bash
# Esegui il setup completo una volta
./scripts/dx_super_setup.sh
```

## 🛠️ Uso Rapido

### Comandi Principali

```bash
make dev            # Status + avvio se non è up
make dev-open       # Apre browser (PORT variabile)
make dev-status     # Porta + health check
make dev-ready      # Env + test-fast + dashboard
make dev-restart    # Stop + ready
make dev-stop       # Ferma tutto
make dev-reset      # Reset log + env
make dev-watch      # Hot reload (riavvio su modifiche)
```

### Variabili d'Ambiente

```bash
make env-show       # Mostra TIMING_FAST, TIMING_SLOW, PORT
```

### Test Veloci

```bash
make test-fast      # Pytest veloce (timing & CSV)
```

### Watcher (Hot Reload)

```bash
make watch-install  # Installa watcher consigliati
make dev-watch      # Avvia hot reload
```

## 🔧 Configurazione

### File `.env.example`

```bash
TIMING_FAST=30
TIMING_SLOW=60
PORT=8501
```

### Porta Personalizzata

```bash
PORT=8600 make dev  # Avvia su porta 8600
```

## 📋 Health Check

Il sistema include health check automatici:

- **Porta**: Verifica se la dashboard è in ascolto
- **HTTP**: Testa la risposta HTTP (curl/wget)
- **Processi**: Controlla processi attivi

## 🔄 Watcher Multi-Backend

Il sistema supporta diversi watcher:

1. **watchexec** (preferito)
2. **entr**
3. **fswatch**
4. **inotifywait**
5. **Python watchdog**
6. **Polling fallback**

## 🚀 CI/CD

- **Fast Tests**: Workflow automatico per test veloci
- **Post-Merge Hook**: Status automatico dopo pull

## 📝 Esempi d'Uso

### Sviluppo Tipico

```bash
# 1. Setup iniziale
./scripts/dx_super_setup.sh

# 2. Avvio sviluppo
make dev

# 3. Hot reload durante sviluppo
make dev-watch

# 4. Verifica stato
make dev-status

# 5. Reset per nuovo ciclo
make dev-reset
```

### Debug

```bash
# Verifica configurazione
make env-show

# Test veloci
make test-fast

# Stop completo
make dev-stop

# Restart pulito
make dev-restart
```

## 🎯 Target Disponibili

```bash
make help | grep -E "(dev|watch|env|test)"
```

## 🔍 Troubleshooting

### Warning Makefile
I warning "overriding commands" sono normali - il sistema funziona correttamente.

### Porta Occupata
```bash
make dev-stop    # Ferma tutto
make dev-ready   # Riavvia
```

### Watcher Non Funziona
```bash
make watch-install  # Installa dipendenze
make dev-watch      # Prova di nuovo
```
