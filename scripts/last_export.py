#!/usr/bin/env python3
from pathlib import Path
import json, time
p = Path("exports")
files = sorted(p.glob("*_e2e-force.*"), key=lambda f: f.stat().st_mtime, reverse=True)
out = {
  "exists": bool(files),
  "latest": str(files[0]) if files else None,
  "mtime": int(files[0].stat().st_mtime) if files else None,
  "age_sec": int(time.time() - files[0].stat().st_mtime) if files else None,
}
print(json.dumps(out, indent=2))
