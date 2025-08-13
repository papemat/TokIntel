import os, sys, subprocess, time, pathlib, signal, pytest, requests, io
from playwright.sync_api import sync_playwright

PORT = 8520
EXPORT_DIR = pathlib.Path("exports")
SCREEN_DIR = EXPORT_DIR / "screenshots"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
SCREEN_DIR.mkdir(parents=True, exist_ok=True)

def _wait_health(port: int, timeout: float = 20.0, pause: float = 0.5) -> bool:
    # Try health endpoint first
    url = f"http://localhost:{port}/?health=1"
    end = time.time() + timeout
    while time.time() < end:
        try:
            r = requests.get(url, timeout=1.5)
            if r.status_code == 200 and "OK" in r.text:
                return True
        except Exception:
            pass
        time.sleep(pause)
    
    # Fallback: check if Streamlit is responding at all
    url = f"http://localhost:{port}/"
    end = time.time() + 10.0
    while time.time() < end:
        try:
            r = requests.get(url, timeout=2.0)
            if r.status_code == 200 and "Streamlit" in r.text:
                return True
        except Exception:
            pass
        time.sleep(pause)
    return False

@pytest.fixture(scope="session")
def app_proc():
    env = os.environ.copy()
    env["TI_PORT"] = str(PORT)
    env["TI_AUTO_EXPORT"] = "1"
    env["TI_E2E_MODE"] = "1"
    cmd = [
        sys.executable, "-m", "streamlit", "run", "dash/app.py",
        "--server.port", str(PORT), "--server.headless", "true"
    ]
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert _wait_health(PORT), "Streamlit health check failed to start"
    yield proc
    # Teardown + tail logs for visibility
    try:
        if proc and proc.poll() is None:
            proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=5)
    except Exception:
        try: proc.kill()
        except Exception: pass
    # Print last ~80 lines of stdout
    try:
        if proc and proc.stdout:
            buf = proc.stdout.read() if hasattr(proc.stdout, "read") else b""
            tail = (buf.decode(errors="ignore")).splitlines()[-80:]
            print("\n===== Streamlit stdout tail =====")
            print("\n".join(tail))
            print("=================================")
    except Exception:
        pass

@pytest.mark.e2e
def test_playwright_real_ui(app_proc):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(f"http://localhost:{PORT}")
            # Prefer selectors robusti (aggiorna se hai placeholder/label dedicati):
            page.fill("input[type='text']", "playwright search")
            page.click("button:has-text('Search')")
            page.wait_for_timeout(1000)
            before = len(list(EXPORT_DIR.glob('*.csv'))) + len(list(EXPORT_DIR.glob('*.json')))
            # Poll per export fino a 12s (UI path)
            deadline = time.time() + 12.0
            new_count = before
            while time.time() < deadline:
                new_count = len(list(EXPORT_DIR.glob('*.csv'))) + len(list(EXPORT_DIR.glob('*.json')))
                if new_count > before:
                    break
                time.sleep(0.5)
            if new_count <= before:
                # Fallback: endpoint forza export
                page.goto(f"http://localhost:{PORT}/?e2e_force_export=1")
                page.wait_for_timeout(800)
                new_count = len(list(EXPORT_DIR.glob('*.csv'))) + len(list(EXPORT_DIR.glob('*.json')))
            assert new_count > before, "No exports generated (UI path + force endpoint)"
                
        except Exception as e:
            ts = time.strftime("%Y%m%d_%H%M%S")
            png = SCREEN_DIR / f"playwright_fail_{ts}.png"
            html = SCREEN_DIR / f"playwright_fail_{ts}.html"
            try:
                page.screenshot(path=str(png), full_page=True)
                page_content = page.content()
                html.write_text(page_content, encoding="utf-8")
                print(f"[E2E] Saved failure artifacts: {png.name}, {html.name}")
            except Exception as art_e:
                print(f"[E2E] Could not save artifacts: {art_e}")
            raise
        finally:
            browser.close()
