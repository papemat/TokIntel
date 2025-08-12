import argparse, xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
def parse(xml_path: str):
  root = ET.parse(xml_path).getroot()
  data=[]
  for cls in root.findall(".//packages/package/classes/class"):
    fn = cls.attrib.get("filename",""); cov=tot=0
    for line in cls.findall("./lines/line"):
      tot+=1; hits=int(line.attrib.get("hits","0")); cov += 1 if hits>0 else 0
    data.append((fn,cov,tot))
  return data
def bucketize(data, depth=1):
  buckets=defaultdict(lambda: {"covered":0,"total":0})
  for fn,cov,tot in data:
    if not tot: continue
    parts=Path(fn).as_posix().split("/")
    key = parts[0] if len(parts)==1 else "/".join(parts[:depth])
    buckets[key]["covered"]+=cov; buckets[key]["total"]+=tot
  return buckets
def pct(c,t): return 0.0 if t==0 else round(c*100.0/t,2)
def main():
  ap=argparse.ArgumentParser()
  ap.add_argument("--base", required=True); ap.add_argument("--head", required=True)
  ap.add_argument("--depth", type=int, default=1); ap.add_argument("--out-md", default="coverage_delta_dirs.md")
  a=ap.parse_args()
  bbase=bucketize(parse(a.base), depth=a.depth); bhead=bucketize(parse(a.head), depth=a.depth)
  keys=sorted(set(bbase.keys())|set(bhead.keys()))
  rows=[]
  for k in keys:
    bb=bbase.get(k,{"covered":0,"total":0}); bh=bhead.get(k,{"covered":0,"total":0})
    pb=pct(bb["covered"],bb["total"]); ph=pct(bh["covered"],bh["total"]); d=round(ph-pb,2)
    rows.append((k,pb,ph,d,bh["covered"],bh["total"]))
  rows.sort(key=lambda r:(r[3], r[2]), reverse=True)
  lines=["### 📊 Coverage Delta per Directory (vs `main`)","", "| Directory | Base % | Head % | Δ | Covered/Total |","|-----------|--------:|-------:|---:|---------------:|"]
  for k,pb,ph,d,cov,tot in rows:
    arrow = "▲" if d>0 else ("▼" if d<0 else "•")
    lines.append(f"| `{k}` | {pb:.2f}% | {ph:.2f}% | {d:+.2f}% {arrow} | {cov}/{tot} |")
  Path(a.out_md).write_text("\n".join(lines), encoding="utf-8"); print(f"[ok] scritto {a.out_md}")
if __name__=="__main__": main()
