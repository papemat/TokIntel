import os
import pathlib
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple
import streamlit as st

st.set_page_config(page_title="Coverage Explorer", layout="wide")

def parse_cobertura(xml_path: str):
  tree = ET.parse(xml_path)
  root = tree.getroot()
  # Cobertura schema by coverage.py: <coverage line-rate="">, per class/file <class ... filename="" line-rate="">
  cov_total = float(root.attrib.get("line-rate", 0.0))
  packages = root.findall(".//packages/package")
  files = []
  for pkg in packages:
    for cls in pkg.findall("./classes/class"):
      filename = cls.attrib.get("filename", "")
      line_rate = float(cls.attrib.get("line-rate", 0.0))
      lines_total = 0
      lines_covered = 0
      missing_lines: List[int] = []
      for line in cls.findall("./lines/line"):
        num = int(line.attrib["number"])
        hits = int(line.attrib.get("hits", "0"))
        lines_total += 1
        if hits > 0:
          lines_covered += 1
        else:
          missing_lines.append(num)
      files.append({
        "filename": filename,
        "line_rate": line_rate,
        "lines_total": lines_total,
        "lines_covered": lines_covered,
        "lines_missed": lines_total - lines_covered,
        "missing_lines": missing_lines,
      })
  return cov_total, files

def percent(x: float) -> float:
  return round(x * 100.0, 2)

def build_html_index(htmlcov_dir: str) -> Dict[str, str]:
  """Indicizza tutti i file .html in htmlcov per mapping rapido."""
  index: Dict[str, str] = {}
  if not os.path.isdir(htmlcov_dir):
    return index
  for root, _, files in os.walk(htmlcov_dir):
    for f in files:
      if f.endswith(".html"):
        full = os.path.join(root, f)
        index[f] = full
  return index

def guess_html_for_source(src: str, html_index: Dict[str, str]) -> str:
  """
  Prova a mappare il path sorgente (src) al file HTML generato da coverage.py.
  Heuristics:
    1) sostituzione separatori in "_" + ".html"
    2) match per suffix su nome file (es. ".../pkg/mod.py" → "pkg_mod_py.html")
    3) ricerca fuzzy per componenti del path
  """
  if not html_index:
    return ""
  # 1) sostituzione diretta
  cand1 = src.replace(os.sep, "_").replace("/", "_") + ".html"
  if cand1 in html_index:
    return html_index[cand1]
  # 2) suffix match (basename con underscore)
  parts = src.replace("\\", "/").split("/")
  if parts:
    base = "_".join(parts) + ".html"
    # prova match diretto
    if base in html_index:
      return html_index[base]
    # prova suffix progressivi (dalla coda)
    suff = []
    for p in reversed(parts):
      suff.append(p)
      key = "_".join(suff[::-1]) + ".html"
      if key in html_index:
        return html_index[key]
  # 3) fuzzy: cerca html che contenga l'ultimo segmento
  last = os.path.basename(src)
  if last:
    cand = f"{last.replace('.', '_')}.html"
    # prova esatto
    if cand in html_index:
      return html_index[cand]
    # scan per parziale
    for k, v in html_index.items():
      if last.replace(".", "_") in k:
        return v
  return ""

st.title("📊 Coverage Explorer")

# Paths
default_xml = os.environ.get("COVERAGE_XML", "coverage.xml")
default_htmlcov = os.environ.get("COVERAGE_HTML_DIR", "htmlcov")
xml_path = st.text_input("Percorso coverage.xml", default_xml)
htmlcov_dir = st.text_input("Cartella htmlcov", default_htmlcov)

if not os.path.exists(xml_path):
  st.warning(f"File non trovato: {xml_path}. Genera prima i report (es: `make test && make coverage-html`).")
  st.stop()

cov_total, files = parse_cobertura(xml_path)
html_index = build_html_index(htmlcov_dir)
st.subheader(f"Coverage complessivo: **{percent(cov_total)}%**")

# Controls
c1, c2, c3, c4 = st.columns([2,1,1,2])
with c1:
  query = st.text_input("Filtra per path/filename (substring)", "")
with c2:
  min_pct = st.slider("Soglia minima % file", 0, 100, 0, 1)
with c3:
  sort_key = st.selectbox("Ordina per", ["% coverage ⬇", "% coverage ⬆", "missed ⬇", "missed ⬆", "filename A→Z", "filename Z→A"])
with c4:
  show_only_missing = st.checkbox("Mostra solo file con linee mancanti", value=False)

# Filter
rows: List[Dict] = []
for f in files:
  pct = percent(f["line_rate"])
  if pct < min_pct:
    continue
  if query and query.lower() not in f["filename"].lower():
    continue
  if show_only_missing and f["lines_missed"] == 0:
    continue

  html_link = ""
  if html_index:
    html_link = guess_html_for_source(f["filename"], html_index)

  rows.append({
    "file": f["filename"],
    "coverage_%": pct,
    "lines_total": f["lines_total"],
    "lines_missed": f["lines_missed"],
    "missing_lines": f["missing_lines"],
    "html": html_link or "",
  })

# Sort
def sorter_key(r):
  if sort_key == "% coverage ⬇": return (-r["coverage_%"], r["file"])
  if sort_key == "% coverage ⬆": return (r["coverage_%"], r["file"])
  if sort_key == "missed ⬇": return (-r["lines_missed"], r["file"])
  if sort_key == "missed ⬆": return (r["lines_missed"], r["file"])
  if sort_key == "filename A→Z": return (r["file"],)
  if sort_key == "filename Z→A": return (tuple(),)  # placeholder
  return (-r["coverage_%"], r["file"])
reverse = sort_key in ["% coverage ⬆", "missed ⬆", "filename Z→A"]
rows_sorted = sorted(rows, key=sorter_key, reverse=reverse)

# Table
st.markdown("### Dettaglio file")
for r in rows_sorted:
  exp = st.expander(f'{r["file"]} — {r["coverage_%"]}% (missed: {r["lines_missed"]}/{r["lines_total"]})', expanded=False)
  with exp:
    if r["missing_lines"]:
      st.code(", ".join(map(str, r["missing_lines"])), language="text")
    else:
      st.write("✅ Nessuna linea mancante.")
    if r["html"]:
      st.write(f'🔗 **HTML (locale)**: `{r["html"]}`')
    else:
      st.caption("HTML non trovato. Genera con `coverage html` e verifica il mapping dei nomi.")

st.info("Suggerimento: in CI scarica l'artifact `coverage-html` e apri `index.html`. Localmente avvia `make coverage-html` e poi questa app.")
