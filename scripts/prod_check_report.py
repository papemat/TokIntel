#!/usr/bin/env python
import os, sys, json, time, sqlite3, argparse, platform, subprocess
from pathlib import Path

def git_rev():
    try:
        return subprocess.check_output(["git","rev-parse","--short","HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "n/a"

def db_info(db):
    p=Path(db)
    if not p.exists(): return {"path": str(p), "exists": False}
    return {
        "path": str(p),
        "exists": True,
        "size_mb": round(p.stat().st_size/1_048_576,2),
        "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_mtime)),
    }

def fetch_stats(db):
    if not Path(db).exists():
        return {"video_count": 0, "status_dist": {}, "columns": [], "indexes": []}
    con = sqlite3.connect(db)
    cur = con.cursor()
    try:
        cur.execute("PRAGMA table_info(videos)")
        cols = [r[1] for r in cur.fetchall()]
        try:
            cur.execute("SELECT COUNT(*) FROM videos")
            total = cur.fetchone()[0]
        except sqlite3.Error:
            total = 0
        dist = {}
        if "status" in cols:
            cur.execute("SELECT LOWER(COALESCE(TRIM(status),'pending')) AS s, COUNT(*) FROM videos GROUP BY s")
            dist = {row[0]: row[1] for row in cur.fetchall()}
        cur.execute("PRAGMA index_list(videos)")
        idxs = [r[1] for r in cur.fetchall()]
        return {"video_count": total, "status_dist": dist, "columns": cols, "indexes": idxs}
    finally:
        con.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/tokintel.db")
    args = ap.parse_args()

    ts = time.strftime("%Y%m%d_%H%M%S")
    reports_dir = Path("reports"); reports_dir.mkdir(parents=True, exist_ok=True)

    env = {
        "TOKINTEL_VERSION": os.getenv("TOKINTEL_VERSION","local"),
        "FF_DISABLE_CACHE": os.getenv("FF_DISABLE_CACHE","0"),
        "CACHE_TTL_SECONDS": os.getenv("CACHE_TTL_SECONDS","0"),
        "PYTHON": platform.python_version(),
    }

    info = {
        "timestamp": ts,
        "git_rev": git_rev(),
        "environment": env,
        "database": db_info(args.db),
        "stats": fetch_stats(args.db),
    }

    json_path = reports_dir / f"prod_check_{ts}.json"
    json_path.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

    md_path = reports_dir / f"prod_check_{ts}.md"
    status_lines = "\n".join([f"- **{k.upper()}**: {v}" for k,v in info["stats"]["status_dist"].items()]) or "- n/d"
    idx_lines = "\n".join([f"- {i}" for i in info["stats"]["indexes"]]) or "- n/d"
    md = f"""# TokIntel – Production Check Report

**Timestamp:** {ts}  
**Git Rev:** `{info['git_rev']}`

## App / Environment
- Version: `{env['TOKINTEL_VERSION']}`
- Python: `{env['PYTHON']}`
- FF_DISABLE_CACHE: `{env['FF_DISABLE_CACHE']}`
- CACHE_TTL_SECONDS: `{env['CACHE_TTL_SECONDS']}`

## Database
- Path: `{info['database']['path']}`
- Exists: `{info['database'].get('exists', False)}`
- Size (MB): `{info['database'].get('size_mb','n/a')}`
- Modified: `{info['database'].get('modified','n/a')}`

## Metrics
- Video count: **{info['stats']['video_count']}**

### Status distribution
{status_lines}

### Indexes on `videos`
{idx_lines}

> Report generato automaticamente da `scripts/prod_check_report.py`.
"""
    md_path.write_text(md, encoding="utf-8")

    print(f"[report] JSON: {json_path}")
    print(f"[report] Markdown: {md_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
