#!/usr/bin/env python
import time, json, pandas as pd, os, sqlite3, sys
from pathlib import Path

def main():
    ts = time.strftime("%Y%m%d_%H%M%S")
    exports_dir = Path("exports")
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    db = os.environ.get("DB_PATH", "data/db.sqlite")
    if not os.path.exists(db):
        print(f"[warn] DB non trovato: {db}. Nessun export.")
        return 0
    
    try:
        con = sqlite3.connect(db)
        df = pd.read_sql_query("SELECT * FROM videos LIMIT 500", con)
        con.close()
        
        csv_path = exports_dir / f"tokintel_sample_{ts}.csv"
        json_path = exports_dir / f"tokintel_sample_{ts}.json"
        
        df.to_csv(csv_path, index=False)
        with open(json_path, "wb") as f:
            f.write(df.to_json(orient="records", force_ascii=False).encode("utf-8"))
        
        print(f"[export] CSV: {csv_path}")
        print(f"[export] JSON: {json_path}")
        return 0
        
    except Exception as e:
        print(f"[error] Export fallito: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
