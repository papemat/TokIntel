#!/usr/bin/env python
import argparse, os, signal, socket, subprocess, sys, time
from urllib.request import urlopen, URLError

def is_port_open(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def wait_http(url, timeout=30):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urlopen(url, timeout=2) as r:
                code = r.getcode()
                if 200 <= code < 500:  # Streamlit returns 200 on root; accettiamo anche 3xx
                    return True
        except URLError:
            pass
        time.sleep(0.5)
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8503)
    ap.add_argument("--timeout", type=int, default=40)
    ap.add_argument("--path", default="dash/perf_dashboard.py")
    args = ap.parse_args()

    # Se già in esecuzione su quella porta, prova direttamente l'HTTP
    if is_port_open(args.port):
        print(f"[info] Porta {args.port} occupata. Provo richiesta HTTP…")
        ok = wait_http(f"http://127.0.0.1:{args.port}", timeout=args.timeout)
        print("✅ Dashboard raggiungibile" if ok else "❌ Dashboard non raggiungibile")
        return 0 if ok else 2

    # Avvia Streamlit headless
    cmd = ["streamlit", "run", args.path, "--server.port", str(args.port), "--server.headless", "true"]
    print(f"[run] {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid)

    try:
        ok = wait_http(f"http://127.0.0.1:{args.port}", timeout=args.timeout)
        if not ok:
            print("❌ Timeout nel bootstrap della dashboard.")
            # stampa ultimi log
            try:
                out = proc.stdout.read()
                print("---- streamlit logs ----")
                print(out[-2000:])
            except Exception:
                pass
            return 2
        print("✅ Dashboard online. Effettuo GET di test…")
        try:
            with urlopen(f"http://127.0.0.1:{args.port}", timeout=3) as r:
                print(f"[http] status={r.getcode()}")
        except Exception as e:
            print(f"[warn] GET di test fallita: {e}")

        return 0
    finally:
        # Termina Streamlit pulitamente
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:
            pass

if __name__ == "__main__":
    sys.exit(main())
