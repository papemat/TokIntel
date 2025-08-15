# 🚀 Quick Start — macOS TokIntel

Questa guida ti mostra come avviare TokIntel su macOS usando lo script **start_tokintel_auto.sh** integrato.

## ✨ Caratteristiche

- **Avvio intelligente**: Sceglie automaticamente tra Docker e virtualenv
- **Gestione porte**: Supporta porte personalizzate
- **Auto-browser**: Apre automaticamente il browser
- **Gestione processi**: Ferma processi esistenti e gestisce i log
- **Stop rapido**: Comando dedicato per fermare tutto

## 🎯 Comandi Principali

### 1️⃣ Avvio Smart
Sceglie automaticamente Docker (se disponibile) o virtualenv Python.

```bash
make start
```

oppure direttamente:
```bash
./start_tokintel_auto.sh
```

### 2️⃣ Modalità Specifiche

**Forza Docker:**
```bash
make start-docker
# oppure
./start_tokintel_auto.sh --mode docker
```

**Forza venv:**
```bash
make start-venv
# oppure
./start_tokintel_auto.sh --mode venv
```

### 3️⃣ Opzioni Avanzate

**Porta custom:**
```bash
PORT=8600 make start-port
# oppure
PORT=8600 ./start_tokintel_auto.sh
```

**Log in tempo reale:**
```bash
make start-logs
# oppure
./start_tokintel_auto.sh --logs
```

**Stop rapido:**
```bash
make stop
# oppure
./start_tokintel_auto.sh --stop
```

**Senza aprire browser:**
```bash
./start_tokintel_auto.sh --no-open
```

## 🌐 Accesso alla Dashboard

Una volta avviato, apri:
```
http://localhost:8501
```

Oppure la porta scelta (es. `http://localhost:8600`).

## ⚡ Alias per Avvio Rapido

Per avviare TokIntel da qualsiasi directory, aggiungi questi alias al tuo `~/.zshrc`:

```bash
alias tokintel-start="cd ~/Documents/TokIntel && ./start_tokintel_auto.sh"
alias tokintel-stop="cd ~/Documents/TokIntel && ./start_tokintel_auto.sh --stop"
alias tokintel-docker="cd ~/Documents/TokIntel && ./start_tokintel_auto.sh --mode docker"
alias tokintel-venv="cd ~/Documents/TokIntel && ./start_tokintel_auto.sh --mode venv"
```

Poi ricarica la configurazione:
```bash
source ~/.zshrc
```

Ora puoi avviare TokIntel semplicemente con:
```bash
tokintel-start
```

## 🔧 Variabili d'Ambiente

Puoi configurare il comportamento tramite variabili d'ambiente:

```bash
# Modalità (auto|docker|venv)
export MODE=auto

# Porta (default: 8501)
export PORT=8600

# Apri browser automaticamente (1=si, 0=no)
export OPEN_BROWSER=1
```

## 📋 Esempi Pratici

### Sviluppo locale con porta custom
```bash
PORT=8600 make start-logs
```

### Test Docker
```bash
make start-docker
```

### Avvio senza browser (per CI/automazione)
```bash
OPEN_BROWSER=0 ./start_tokintel_auto.sh
```

### Stop e riavvio
```bash
make stop
make start
```

## 🐛 Troubleshooting

### Porta già in uso
Lo script rileva automaticamente se la porta è occupata e termina il processo esistente.

### Docker non disponibile
Se Docker non è installato o non funziona, lo script passa automaticamente a virtualenv.

### Virtualenv non trovato
Lo script crea automaticamente un virtualenv se non esiste.

### Dipendenze mancanti
Lo script installa automaticamente le dipendenze da `requirements.txt` se necessario.

## 📚 Comandi Makefile Disponibili

| Comando | Descrizione |
|---------|-------------|
| `make start` | Avvio smart (auto docker/venv) |
| `make start-docker` | Forza Docker |
| `make start-venv` | Forza venv |
| `make start-logs` | Avvia e mostra i log |
| `make start-port` | Avvia su porta custom (8600) |
| `make stop` | Stop rapido |

## 🔗 Link Utili

- [README principale](../README.md)
- [Documentazione completa](../docs/)
- [Troubleshooting](../FAQ_TROUBLESHOOTING.md)
