@echo off
setlocal enabledelayedexpansion

set PORT=%TI_E2E_PORT%
if "%PORT%"=="" set PORT=8520
set LOG=%TI_E2E_LOG%
if "%LOG%"=="" set LOG=streamlit_e2e.log

if not exist artifacts\e2e mkdir artifacts\e2e
if not exist exports mkdir exports

echo ▶️  Avvio Streamlit su :%PORT% (headless) con E2E mode...
start /b cmd /c "set TI_E2E_MODE=1&& set TI_AUTO_EXPORT=1&& python -m streamlit run dash/app.py --server.port %PORT% --server.headless true > %LOG% 2>&1"

echo ⏳ Health check con retry (max 60s)...
set /a tries=0
:retry
curl -fsS "http://localhost:%PORT%/?health=1" | findstr /I "OK" >nul 2>&1
if %errorlevel%==0 goto healthy
set /a tries+=1
if %tries% GEQ 60 (
  echo ❌ Health check timeout dopo 60s. Ultime righe log:
  powershell -Command "Get-Content -Tail 200 -Path '%LOG%'"
  goto fail
)
ping -n 2 127.0.0.1 >nul
goto retry

:healthy
echo ✅ App pronta. Eseguo test E2E...
make ci-e2e-playwright
if errorlevel 1 (
  echo ❌ E2E fallito. Tail log:
  powershell -Command "Get-Content -Tail 200 -Path '%LOG%'"
  goto fail
)

echo 🧪 Export health:
make export-health

echo 🎉 Completato!
exit /b 0

:fail
echo 🧹 Prova a chiudere Streamlit...
for /f "tokens=2" %%a in ('tasklist ^| findstr /I "streamlit"') do taskkill /PID %%a /F >nul 2>&1
exit /b 1
