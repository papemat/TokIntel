#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import signal
import time
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8510
def run(cmd):
    try: return subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception: return None
def main():
    sysname = platform.system().lower()
    if "windows" in sysname and os.path.exists("scripts/kill_port.ps1"):
        run(["powershell","-ExecutionPolicy","Bypass","-File","scripts/kill_port.ps1","-Port",str(PORT)]); return
    if "windows" not in sysname and os.path.exists("scripts/kill_port.sh"):
        run(["bash","scripts/kill_port.sh",str(PORT)]); return
    if "windows" not in sysname:
        out = run(["ps","aux"])
        if out and out.stdout:
            for l in [x for x in out.stdout.splitlines() if "streamlit" in x and ("dash/app.py" in x or "--server.port" in x)]:
                parts = l.split()
                if len(parts)>1 and parts[1].isdigit():
                    try: os.kill(int(parts[1]), signal.SIGTERM)
                    except Exception: pass
            time.sleep(1.0)
if __name__ == "__main__": main()
