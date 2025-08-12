param([int]$Port = 8510)
Write-Host "🧪 Dev smoke starting on port $Port..."
try { python -c "import sys;import subprocess;sys.exit(subprocess.run(['python','scripts/kill_port.py','$Port']).returncode)" } catch {}
try { make kill-port TI_PORT=$Port } catch {}
$env:TI_AUTO_EXPORT="1"; $env:TI_PORT="$Port"
Write-Host "➡️  E2E headless";  & .\.venv\Scripts\python -m pytest -q -m e2e tests/e2e/test_streamlit_ui.py
Write-Host "➡️  Coverage Sprint 3"; & .\.venv\Scripts\python -m pytest -q --cov=analyzer.orchestrator --cov=dash --cov-report=term-missing
Write-Host "➡️  Lint"; & .\.venv\Scripts\python -m pip install -q ruff; & .\.venv\Scripts\python -m ruff check . --fix; & .\.venv\Scripts\python -m ruff check .
Write-Host "➡️  Orchestrator CLI smoke"; & .\.venv\Scripts\python -m analyzer.orchestrator --query "alpha beta" --topk 3 --export "exports/cli_smoke" 
Write-Host "✅ Dev smoke completed"
