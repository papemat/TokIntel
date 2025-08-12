#!/usr/bin/env python
import os, sys, time, json, sqlite3, argparse
from pathlib import Path
from contextlib import contextmanager

REPORTS = Path("reports")
REPORTS.mkdir(parents=True, exist_ok=True)

@contextmanager
def timer(label: str, out: dict):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        out[label] = round((time.perf_counter() - t0) * 1000, 2)  # ms

def count_rows(db: str, table: str) -> int:
    con = sqlite3.connect(db)
    cur = con.cursor()
    try:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        return cur.fetchone()[0]
    except Exception:
        return 0
    finally:
        con.close()

def run_export_sample(db: str) -> dict:
    """Simula l'export CSV/JSON su 500 righe (se disponibili)."""
    import pandas as pd
    res = {}
    con = sqlite3.connect(db)
    try:
        with timer("sql_read_500", res):
            df = pd.read_sql_query("SELECT * FROM videos LIMIT 500", con)
        ts = time.strftime("%Y%m%d_%H%M%S")
        with timer("export_csv", res):
            df.to_csv(f"exports/tokintel_sample_{ts}.csv", index=False)
        with timer("export_json", res):
            open(f"exports/tokintel_sample_{ts}.json", "wb").write(
                df.to_json(orient="records", force_ascii=False).encode("utf-8")
            )
    finally:
        con.close()
    res["export_rows"] = len(df)
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.getenv("DB_PATH","data/staging_db.sqlite"))
    # soglie configurabili da ENV o CLI
    ap.add_argument("--max-sql-read-ms", type=float, default=float(os.getenv("MAX_SQL_READ_MS", "1500")))
    ap.add_argument("--max-export-ms", type=float, default=float(os.getenv("MAX_EXPORT_MS", "1500")))
    args = ap.parse_args()

    Path("exports").mkdir(exist_ok=True)
    totals = {"db_path": args.db, "ts": time.strftime("%Y%m%d_%H%M%S")}
    perf = {}

    # Bench: count rows
    videos_before = count_rows(args.db, "videos")
    perf["videos_count"] = videos_before

    # Bench: indexes creation (idempotent)
    with timer("add_indexes_ms", perf):
        os.system(f"{sys.executable} scripts/add_db_indexes.py > /dev/null 2>&1")

    # Bench: export timings
    perf.update(run_export_sample(args.db))

    # Bench: caching stress (3 iterazioni richiamo export)
    stress = {}
    for i in range(1, 4):
        with timer(f"stress_iter_{i}_ms", stress):
            run_export_sample(args.db)
    perf["cache_stress"] = stress

    # Save reports
    js = REPORTS / f"perf_{totals['ts']}.json"
    md = REPORTS / f"perf_{totals['ts']}.md"
    js.write_text(json.dumps({"meta": totals, "perf": perf}, indent=2), encoding="utf-8")
    md.write_text(
        f"""# Performance Bench

**DB:** `{args.db}`  
**Videos:** {perf['videos_count']}

## Timings (ms)
- add_indexes: {perf['add_indexes_ms']}
- sql_read_500: {perf['sql_read_500']}
- export_csv: {perf['export_csv']}
- export_json: {perf['export_json']}

## Cache Stress (3x)
- iter1: {perf['cache_stress']['stress_iter_1_ms']}
- iter2: {perf['cache_stress']['stress_iter_2_ms']}
- iter3: {perf['cache_stress']['stress_iter_3_ms']}

> Report generato da `scripts/perf_bench.py`.
""",
        encoding="utf-8",
    )

    print(f"[perf] JSON: {js}")
    print(f"[perf] Markdown: {md}")

    # ✅ Threshold checks
    violations = []
    if perf.get("sql_read_500", 0) > args.max_sql_read_ms:
        violations.append(f"sql_read_500>{args.max_sql_read_ms}ms ({perf['sql_read_500']}ms)")
    if perf.get("export_csv", 0) > args.max_export_ms:
        violations.append(f"export_csv>{args.max_export_ms}ms ({perf['export_csv']}ms)")
    if perf.get("export_json", 0) > args.max_export_ms:
        violations.append(f"export_json>{args.max_export_ms}ms ({perf['export_json']}ms)")

    if violations:
        print("[perf] ❌ Thresholds exceeded:\n - " + "\n - ".join(violations))
        return 2

    print("[perf] ✅ Thresholds OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
