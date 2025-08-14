@echo off
setlocal ENABLEDELAYEDEXPANSION

set SCRIPT_DIR=%~dp0
for %%I in ("%SCRIPT_DIR%..") do set ROOT_DIR=%%~fI
cd /d "%ROOT_DIR%"

if not defined PORT set PORT=8501
set HOST=localhost
set APP=dash/app.py
set HEADLESS=1
set DEBUG=0

:parse
if "%~1"=="" goto after_parse
if "%~1"=="--lan"        ( set HOST=0.0.0.0 & shift & goto parse )
if "%~1"=="--no-headless" ( set HEADLESS=0   & shift & goto parse )
if "%~1"=="--debug"       ( set DEBUG=1      & shift & goto parse )
if "%~1"=="--port"        ( set PORT=%~2     & shift & shift & goto parse )
if "%~1"=="--app"         ( set APP=%~2      & shift & shift & goto parse )
if "%~1"=="-h"  ( goto help )
if "%~1"=="--help" ( goto help )
shift
goto parse

:after_parse
set PY=
if exist .venv\Scripts\python.exe set PY=.venv\Scripts\python.exe
if not defined PY (
  for %%P in (python.exe py.exe) do (
    where %%P >nul 2>nul && if not defined PY set PY=%%P
  )
)
if not defined PY (
  echo [error] Python not found. Install Python 3.10+.
  exit /b 1
)

"%PY%" -c "import streamlit" >nul 2>nul
if errorlevel 1 (
  echo [info] Installing Streamlit / requirements...
  "%PY%" -m pip install --upgrade pip
  if exist requirements.txt (
    "%PY%" -m pip install -r requirements.txt
  ) else (
    "%PY%" -m pip install streamlit
  )
)

if "%HEADLESS%"=="1" set STREAMLIT_SERVER_HEADLESS=true
if "%HEADLESS%"=="0" set STREAMLIT_SERVER_HEADLESS=false
if "%DEBUG%"=="1" set STREAMLIT_LOG_LEVEL=debug

"%PY%" -m streamlit run "%APP%" --server.port="%PORT%" --server.address="%HOST%"
exit /b %errorlevel%

:help
@echo TokIntel launcher (Windows)
@echo.
@echo Usage: scripts\run_tokintel.bat [options]
@echo   --lan             Bind to 0.0.0.0 (share on LAN)
@echo   --port ^<num^>      Server port (default 8501 or %%PORT%%)
@echo   --app ^<path^>      Streamlit app entry (default dash/app.py)
@echo   --no-headless     Open browser automatically
@echo   --debug           Verbose logs
@echo   -h, --help        Show this help
exit /b 0
