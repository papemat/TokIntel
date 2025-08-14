#!/usr/bin/env python3
"""
Generatore di note di release da CHANGELOG_QUICKSTART.md
Riutilizzabile localmente e nei workflow CI/CD
"""

import os, re, sys, argparse, pathlib

def extract_section(changelog_path: str, tag: str) -> str:
    """Estrae la sezione del changelog per il tag specificato"""
    text = pathlib.Path(changelog_path).read_text(encoding="utf-8")
    pat = re.compile(rf"(^##\s+{re.escape(tag)}[\s\S]*?)(?=^##\s+v|\Z)", re.MULTILINE)
    m = pat.search(text)
    if m:
        return m.group(1).strip()
    # fallback: prima sezione
    pat2 = re.compile(r"(^##\s+v[\d\.]+[\s\S]*?)(?=^##\s+v|\Z)", re.MULTILINE)
    m = pat2.search(text)
    return m.group(1).strip() if m else f"TokIntel Quickstart Bundle {tag}"

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Genera note di release da CHANGELOG")
    ap.add_argument("tag", help="version tag, e.g. v1.1.0")
    ap.add_argument("--changelog", default="CHANGELOG_QUICKSTART.md", 
                   help="path to changelog file")
    args = ap.parse_args()
    print(extract_section(args.changelog, args.tag))
