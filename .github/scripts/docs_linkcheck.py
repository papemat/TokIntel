import os, re, sys, pathlib, glob

ROOT = pathlib.Path(__file__).resolve().parents[2]
FILES = [ROOT/"README.md", *[pathlib.Path(p) for p in glob.glob(str(ROOT/"docs/**/*.md"), recursive=True)]]

MD_LINK = re.compile(r"\]\((?!https?://)([^)]+)\)")  # only relative links

missing = []
for md in FILES:
    if not md.exists(): continue
    txt = md.read_text(encoding="utf-8", errors="ignore")
    for m in MD_LINK.finditer(txt):
        target = m.group(1).split("#")[0].strip()
        if not target: continue
        path = (md.parent / target).resolve()
        if not path.exists():
            missing.append((md.relative_to(ROOT), target))
if missing:
    print("❌ Broken relative links:")
    for f,t in missing:
        print(f" - {f}: {t}")
    sys.exit(1)
print("✅ Relative links OK")
