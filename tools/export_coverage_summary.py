import os
import sys
import csv
import argparse
import xml.etree.ElementTree as ET

def parse_cobertura(xml_path: str):
  tree = ET.parse(xml_path); root = tree.getroot()
  total_rate = float(root.attrib.get("line-rate", 0.0))
  rows = []
  for cls in root.findall(".//packages/package/classes/class"):
    fn = cls.attrib.get("filename", ""); rate = float(cls.attrib.get("line-rate", 0.0))
    tot = cov = 0; missing = []
    for ln in cls.findall("./lines/line"):
      num = int(ln.attrib["number"]); hits = int(ln.attrib.get("hits", "0"))
      tot += 1; cov += 1 if hits > 0 else 0
      if hits == 0: missing.append(num)
    rows.append({"filename": fn,"coverage_pct": round(rate*100,2),"lines_total": tot,"lines_missed": tot-cov,"missing_lines": missing})
  return round(total_rate*100,2), rows
def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--xml", default="coverage.xml")
  ap.add_argument("--top", type=int, default=25)
  ap.add_argument("--out-csv", default="coverage_summary_top.csv")
  ap.add_argument("--out-json", default="coverage_summary_top.json")
  args = ap.parse_args()
  if not os.path.exists(args.xml): print(f"[!] File non trovato: {args.xml}", file=sys.stderr); sys.exit(2)
  total_pct, rows = parse_cobertura(args.xml)
  rows_sorted = sorted(rows, key=lambda r: (-r["lines_missed"], r["coverage_pct"], r["filename"]))[:args.top]
  with open(args.out_csv,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["filename","coverage_pct","lines_total","lines_missed","missing_lines"])
    for r in rows_sorted: w.writerow([r["filename"], r["coverage_pct"], r["lines_total"], r["lines_missed"], " ".join(map(str, r["missing_lines"]))])
  with open(args.out_json,"w",encoding="utf-8") as f:
    import json; json.dump({"total_coverage_pct":total_pct,"top_worst":rows_sorted}, f, ensure_ascii=False, indent=2)
  print(f"[ok] Total: {total_pct}%. Export in {args.out_csv} / {args.out_json}")
if __name__=="__main__": main()
