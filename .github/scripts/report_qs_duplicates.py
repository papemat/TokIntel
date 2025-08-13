import re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
HEADER = r"^##\s⚡ Quick Start – TokIntel GUI\s*$"

if not README.exists():
    print("❌ README.md non trovato", file=sys.stderr); sys.exit(1)

text = README.read_text(encoding="utf-8")
matches = list(re.finditer(HEADER, text, flags=re.M))
n = len(matches)
if n <= 1:
    print("✅ Nessun duplicato del blocco Quick Start.")
    sys.exit(0)

print(f"⚠️ Trovati {n} header Quick Start nel README.")
for i, m in enumerate(matches, 1):
    ln = text.count("\n", 0, m.start()) + 1
    print(f" - Occorrenza #{i} @ riga {ln}")
sys.exit(0)
