import os, sys, csv, json, argparse, xml.etree.ElementTree as ET
from typing import List, Dict, Tuple

def parse_cobertura(xml_path: str):
  tree = ET.parse(xml_path)
  root = tree.getroot()
  total_rate = float(root.attrib.get("line-rate", 0.0))
  packages = root.findall(".//packages/package")
  rows = []
  for pkg in packages:
    for cls in pkg.findall("./classes/class"):
      fn = cls.attrib.get("filename", "")
      rate = float(cls.attrib.get("line-rate", 0.0))
      tot = 0; cov = 0; missing = []
      for ln in cls.findall("./lines/line"):
        num = int(ln.attrib["number"])
        hits = int(ln.attrib.get("hits", "0"))
        tot += 1
        if hits > 0: cov += 1
        else: missing.append(num)
      rows.append({
        "filename": fn,
        "coverage_pct": round(rate*100, 2),
        "lines_total": tot,
        "lines_missed": tot - cov,
        "missing_lines": missing,
      })
  return round(total_rate*100, 2), rows

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--xml", default="coverage.xml")
  ap.add_argument("--top", type=int, default=20)
  ap.add_argument("--out-csv", default="coverage_summary_top.csv")
  ap.add_argument("--out-json", default="coverage_summary_top.json")
  args = ap.parse_args()

  if not os.path.exists(args.xml):
    print(f"[!] File non trovato: {args.xml}", file=sys.stderr)
    sys.exit(2)

  total_pct, rows = parse_cobertura(args.xml)
  # ordina per lines_missed desc, poi coverage asc
  rows_sorted = sorted(rows, key=lambda r: (-r["lines_missed"], r["coverage_pct"], r["filename"]))
  top = rows_sorted[: args.top]

  # CSV
  with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["filename","coverage_pct","lines_total","lines_missed","missing_lines"])
    for r in top:
      w.writerow([r["filename"], r["coverage_pct"], r["lines_total"], r["lines_missed"], " ".join(map(str, r["missing_lines"]))])

  # JSON
  with open(args.out_json, "w", encoding="utf-8") as f:
    json.dump({
      "total_coverage_pct": total_pct,
      "top_worst": top
    }, f, ensure_ascii=False, indent=2)

  print(f"[ok] Total: {total_pct}%. Esportati {len(top)} file peggiori in {args.out_csv} / {args.out_json}")

if __name__ == "__main__":
  main()
