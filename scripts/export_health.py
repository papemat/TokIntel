#!/usr/bin/env python3
from pathlib import Path
import sys, time, json

def main():
    root = Path("exports")
    if not root.exists():
        print(json.dumps({"ok": False, "error": "exports/ not found"}))
        sys.exit(1)

    files = sorted(
        (f for f in root.glob("*_e2e-force.*") if f.is_file()),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not files:
        print(json.dumps({"ok": False, "error": "no *_e2e-force.* files"}))
        sys.exit(1)

    now = time.time()
    recent = [f for f in files if now - f.stat().st_mtime < 24 * 3600]
    summary = {
        "ok": bool(recent),
        "count": len(files),
        "recent_count": len(recent),
        "latest": str(files[0]) if files else None,
        "extensions": sorted({f.suffix for f in files}),
        "avg_size_bytes": round(sum(f.stat().st_size for f in files) / len(files), 1),
        "max_size_bytes": max(f.stat().st_size for f in files),
    }
    print(json.dumps(summary, indent=2))
    if not recent:
        sys.exit(1)

if __name__ == "__main__":
    main()
