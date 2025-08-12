import os
import sys
import time
import subprocess
import requests
import platform
import signal
from pathlib import Path
import pytest

# Set environment variables for headless mode
os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
os.environ.setdefault("PYTHONUNBUFFERED", "1")

PORT = int(os.environ.get("TI_PORT", "8510"))
EXPORT_DIR = Path(os.environ.get("TI_EXPORT_DIR", "exports"))
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def _kill_port():
    try: subprocess.run([sys.executable, "scripts/kill_port.py", str(PORT)], check=False)
    except Exception: pass

def start_app():
    env = os.environ.copy()
    env["TI_PORT"] = str(PORT)
    env["TI_AUTO_EXPORT"] = "1"
    cmd = [sys.executable, "-m", "streamlit", "run", "dash/app.py",
           "--server.port", str(PORT), "--server.headless", "true"]
    return subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def wait_for_health(timeout=18.0, attempts=20, pause=0.5):
    url = f"http://localhost:{PORT}/?health=1"
    deadline = time.time() + timeout
    for _ in range(attempts):
        try:
            r = requests.get(url, timeout=1.5)
            if r.status_code == 200 and "OK" in r.text:
                return True
        except Exception: pass
        if time.time() > deadline: break
        time.sleep(pause)
    return False

def teardown(proc):
    if proc and proc.poll() is None:
        try:
            proc.terminate() if platform.system().lower().startswith("win") else proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=5)
        except Exception:
            try: proc.kill()
            except Exception: pass

@pytest.mark.e2e
def test_streamlit_e2e_export():
    _kill_port()
    proc = start_app()
    try:
        assert wait_for_health(), "Streamlit health-check failed"
        r = requests.get(f"http://localhost:{PORT}/?trigger_search=1", timeout=5)
        assert r.status_code == 200
        time.sleep(2.0)
        exports = list(EXPORT_DIR.glob("*.csv")) + list(EXPORT_DIR.glob("*.json"))
        assert len(exports) >= 1, "No export files produced"
    finally:
        teardown(proc)

@pytest.mark.e2e
def test_marker_e2e_enabled():
    assert True
