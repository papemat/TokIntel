#!/usr/bin/env python3
import pathlib, sys, json

EXPORT_DIR = pathlib.Path("exports")
if not EXPORT_DIR.exists():
    print(json.dumps({"error": "no exports dir"}))
    sys.exit(0)

files = list(EXPORT_DIR.glob("*.*"))
report = {
    "count": len(files),
    "avg_size_bytes": sum(f.stat().st_size for f in files) / len(files) if files else 0,
    "max_size_bytes": max((f.stat().st_size for f in files), default=0),
    "extensions": sorted(set(f.suffix for f in files))
}
print(json.dumps(report, indent=2))
