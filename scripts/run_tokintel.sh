#!/bin/bash

# TokIntel Quickstart Launcher - Linux/macOS
# Avvia TokIntel con setup automatico e GUI Streamlit

set -e

echo "🚀 TokIntel Quickstart Launcher (Linux/macOS)"
echo "=============================================="

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzione per log colorato
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verifica Python
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 non trovato. Installa Python 3.11+ e riprova."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
log_info "Python $PYTHON_VERSION rilevato"

# Verifica se siamo nella directory corretta
if [ ! -f "pyproject.toml" ]; then
    log_error "File pyproject.toml non trovato. Assicurati di essere nella directory root di TokIntel."
    exit 1
fi

# Setup ambiente virtuale se non esiste
if [ ! -d ".venv" ]; then
    log_info "Creazione ambiente virtuale..."
    python3 -m venv .venv
    log_success "Ambiente virtuale creato"
fi

# Attiva ambiente virtuale
log_info "Attivazione ambiente virtuale..."
source .venv/bin/activate

# Installa dipendenze se necessario
if [ ! -f ".venv/pyvenv.cfg" ] || [ ! -d ".venv/lib" ]; then
    log_info "Installazione dipendenze..."
    pip install -r requirements.txt
    log_success "Dipendenze installate"
else
    log_info "Verifica dipendenze..."
    pip install -r requirements.txt --quiet
    log_success "Dipendenze aggiornate"
fi

# Crea database se non esiste
log_info "Verifica database..."
python -c "
import sqlite3
import os
if not os.path.exists('data/tokintel.db'):
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/tokintel.db')
    conn.close()
    print('Database creato')
else:
    print('Database esistente')
"

# Avvia GUI Streamlit
log_success "Avvio GUI TokIntel..."
log_info "Apri http://localhost:8501 nel browser"
log_info "Premi Ctrl+C per fermare"

export TI_AUTO_EXPORT=1
export TI_PORT=8501

streamlit run dash/app.py --server.port=8501 --server.address=0.0.0.0
