#!/usr/bin/env python
import json, csv, sys, argparse
from pathlib import Path

def collect_perf_reports(report_dir: Path):
    rows = []
    for js in sorted(report_dir.glob("perf_*.json")):
        data = json.loads(js.read_text(encoding="utf-8"))
        meta = data.get("meta", {})
        perf = data.get("perf", {})
        rows.append({
            "ts": meta.get("ts"),
            "db_path": meta.get("db_path"),
            "videos_count": perf.get("videos_count"),
            "add_indexes_ms": perf.get("add_indexes_ms"),
            "sql_read_500": perf.get("sql_read_500"),
            "export_csv": perf.get("export_csv"),
            "export_json": perf.get("export_json"),
            "stress_iter_1_ms": perf.get("cache_stress", {}).get("stress_iter_1_ms"),
            "stress_iter_2_ms": perf.get("cache_stress", {}).get("stress_iter_2_ms"),
            "stress_iter_3_ms": perf.get("cache_stress", {}).get("stress_iter_3_ms"),
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="reports")
    ap.add_argument("--out", default="reports/perf_history.csv")
    args = ap.parse_args()

    d = Path(args.dir); d.mkdir(parents=True, exist_ok=True)
    rows = collect_perf_reports(d)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "ts","db_path","videos_count","add_indexes_ms","sql_read_500",
        "export_csv","export_json","stress_iter_1_ms","stress_iter_2_ms","stress_iter_3_ms"
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"[agg] scritto {out} con {len(rows)} righe")
    return 0

if __name__ == "__main__":
    sys.exit(main())
