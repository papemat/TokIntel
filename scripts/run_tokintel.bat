@echo off
REM TokIntel Quickstart Launcher - Windows
echo 🚀 TokIntel Quickstart Launcher (Windows)
echo ==============================================

REM Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python non trovato. Installa Python 3.11+ e riprova.
    pause
    exit /b 1
)

REM Verifica directory
if not exist "pyproject.toml" (
    echo [ERROR] File pyproject.toml non trovato.
    pause
    exit /b 1
)

REM Setup ambiente virtuale
if not exist ".venv" (
    echo [INFO] Creazione ambiente virtuale...
    python -m venv .venv
)

REM Attiva ambiente virtuale
call .venv\Scripts\activate.bat

REM Installa dipendenze
pip install -r requirements.txt --quiet

REM Crea database
python -c "import sqlite3; import os; os.makedirs('data', exist_ok=True) if not os.path.exists('data') else None; conn = sqlite3.connect('data/tokintel.db') if not os.path.exists('data/tokintel.db') else None; conn.close() if 'conn' in locals() else None"

REM Avvia GUI
echo [SUCCESS] Avvio GUI TokIntel...
echo [INFO] Apri http://localhost:8501 nel browser
set TI_AUTO_EXPORT=1
set TI_PORT=8501
streamlit run dash/app.py --server.port=8501 --server.address=0.0.0.0
pause
