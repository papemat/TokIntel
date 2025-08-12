import csv
import argparse
from pathlib import Path
def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--csv", default="coverage_summary_top.csv")
  ap.add_argument("--out", default="coverage_todo.md")
  args = ap.parse_args()
  p = Path(args.csv) 
  if not p.exists(): raise SystemExit(f"[!] File CSV non trovato: {p}")
  rows = list(csv.DictReader(p.open(encoding="utf-8")))
  md = []
  md += ["# 🧪 Coverage Action Plan","", "Questa lista mostra i file con più linee scoperte in ordine di priorità.","Obiettivo: aumentare la copertura totale alzando la % di questi file.","", "| Stato | File | % Copertura | Linee Totali | Linee Mancanti | Linee da Coprire |","|-------|------|-------------|--------------|----------------|------------------|"]
  for r in rows:
    missing = r.get("missing_lines","").strip() or "-"
    md.append(f"| [ ] | `{r['filename']}` | {r['coverage_pct']}% | {r['lines_total']} | {r['lines_missed']} | `{missing}` |")
  Path(args.out).write_text("\n".join(md), encoding="utf-8"); print(f"[ok] Generato {args.out}")
if __name__=="__main__": main()
