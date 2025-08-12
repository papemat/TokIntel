import os, pathlib, xml.etree.ElementTree as ET
from typing import List, Dict, Tuple
import streamlit as st

st.set_page_config(page_title="Coverage Explorer", layout="wide")

def parse_cobertura(xml_path: str):
  tree = ET.parse(xml_path); root = tree.getroot()
  cov_total = float(root.attrib.get("line-rate", 0.0))
  files = []
  for cls in root.findall(".//packages/package/classes/class"):
    filename = cls.attrib.get("filename", "")
    line_rate = float(cls.attrib.get("line-rate", 0.0))
    lines_total = lines_covered = 0; missing = []
    for line in cls.findall("./lines/line"):
      num = int(line.attrib["number"]); hits = int(line.attrib.get("hits", "0"))
      lines_total += 1
      if hits > 0: lines_covered += 1
      else: missing.append(num)
    files.append({"filename": filename,"line_rate": line_rate,"lines_total": lines_total,"lines_covered": lines_covered,"lines_missed": lines_total - lines_covered,"missing_lines": missing})
  return cov_total, files

def percent(x: float) -> float: return round(x * 100.0, 2)

def build_html_index(htmlcov_dir: str) -> Dict[str, str]:
  idx = {}
  if not os.path.isdir(htmlcov_dir): return idx
  for root, _, files in os.walk(htmlcov_dir):
    for f in files:
      if f.endswith(".html"): idx[f] = os.path.join(root, f)
  return idx

def guess_html_for_source(src: str, html_index: Dict[str, str]) -> str:
  if not html_index: return ""
  cand1 = src.replace(os.sep, "_").replace("/", "_") + ".html"
  if cand1 in html_index: return html_index[cand1]
  parts = src.replace("\\", "/").split("/")
  if parts:
    base = "_".join(parts) + ".html"
    if base in html_index: return html_index[base]
    suff = []
    for p in reversed(parts):
      suff.append(p); key = "_".join(suff[::-1]) + ".html"
      if key in html_index: return html_index[key]
  last = os.path.basename(src)
  if last:
    cand = f"{last.replace('.', '_')}.html"
    if cand in html_index: return html_index[cand]
    for k, v in html_index.items():
      if last.replace(".", "_") in k: return v
  return ""

st.title("📊 Coverage Explorer")
xml_path = st.text_input("Percorso coverage.xml", os.environ.get("COVERAGE_XML", "coverage.xml"))
htmlcov_dir = st.text_input("Cartella htmlcov", os.environ.get("COVERAGE_HTML_DIR", "htmlcov"))
if not os.path.exists(xml_path):
  st.warning(f"File non trovato: {xml_path}. Esegui `make test && make coverage-html`."); st.stop()

cov_total, files = parse_cobertura(xml_path)
st.subheader(f"Coverage complessivo: **{percent(cov_total)}%**")
html_index = build_html_index(htmlcov_dir)

c1, c2, c3, c4 = st.columns([2,1,1,2])
with c1: query = st.text_input("Filtra path/filename", "")
with c2: min_pct = st.slider("Soglia minima % file", 0, 100, 0, 1)
with c3: sort_key = st.selectbox("Ordina per", ["% coverage ⬇","% coverage ⬆","missed ⬇","missed ⬆","filename A→Z","filename Z→A"])
with c4: show_only_missing = st.checkbox("Solo file con linee mancanti", value=False)

rows = []
for f in files:
  pct = percent(f["line_rate"])
  if pct < min_pct: continue
  if query and query.lower() not in f["filename"].lower(): continue
  if show_only_missing and f["lines_missed"] == 0: continue
  html_link = guess_html_for_source(f["filename"], html_index) if html_index else ""
  rows.append({"file": f["filename"],"coverage_%": pct,"lines_total": f["lines_total"],"lines_missed": f["lines_missed"],"missing_lines": f["missing_lines"],"html": html_link})

def sorter_key(r):
  return {
    "% coverage ⬇": (-r["coverage_%"], r["file"]),
    "% coverage ⬆": (r["coverage_%"], r["file"]),
    "missed ⬇": (-r["lines_missed"], r["file"]),
    "missed ⬆": (r["lines_missed"], r["file"]),
    "filename A→Z": (r["file"],),
    "filename Z→A": (r["file"],)
  }.get(sort_key, (-r["coverage_%"], r["file"]))
reverse = sort_key in ["% coverage ⬆","missed ⬆","filename Z→A"]
rows_sorted = sorted(rows, key=sorter_key, reverse=reverse)

st.markdown("### Dettaglio file")
for r in rows_sorted:
  exp = st.expander(f'{r["file"]} — {r["coverage_%"]}% (missed: {r["lines_missed"]}/{r["lines_total"]})', expanded=False)
  with exp:
    if r["missing_lines"]: st.code(", ".join(map(str, r["missing_lines"])), language="text")
    else: st.write("✅ Nessuna linea mancante.")
    if r["html"]: st.write(f'🔗 **HTML (locale)**: `{r["html"]}`')
    else: st.caption("HTML non trovato. Esegui `coverage html` e verifica mapping.")
