import os, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
readme = ROOT / "README.md"
badge = ROOT / "docs" / "badges" / "quickstart_ready_glow.svg"
png   = ROOT / "docs" / "images" / "tokintel_gui_home.png"
svg   = ROOT / "docs" / "images" / "tokintel_gui_home.svg"

def fail(msg):
    print(f"❌ {msg}")
    sys.exit(1)

def ok(msg):
    print(f"✅ {msg}")

if not readme.exists():
    fail("README.md non trovato")

text = readme.read_text(encoding="utf-8")

# Header presence
if "## ⚡ Quick Start – TokIntel GUI" not in text:
    fail("Sezione 'Quick Start – TokIntel GUI' non trovata nel README")

ok("Sezione Quick Start presente")

# Badge presence
if "docs/badges/quickstart_ready_glow.svg" not in text:
    fail("Badge 'quickstart_ready_glow.svg' non referenziato nel README")

if not badge.exists():
    fail("File badge SVG mancante: docs/badges/quickstart_ready_glow.svg")

ok("Badge SVG presente e referenziato")

# Table commands presence (basic grep)
required_cmds = [
    r"`make tokintel-gui-bg`",
    r"`make tokintel-gui-log`",
    r"`make tokintel-gui-health`",
    r"`make tokintel-gui-stop`",
    r"`make tokintel-gui-restart`",
    r"`make tokintel-gui-on PORT=8502`",
]
for cmd in required_cmds:
    if not re.search(cmd, text):
        fail(f"Comando mancante nella tabella Quick Start: {cmd}")

ok("Tutti i comandi Quick Start presenti")

# Image presence (PNG or SVG)
if not (png.exists() or svg.exists()):
    fail("Screenshot placeholder mancante (PNG o SVG)")

ok("Screenshot placeholder presente (PNG o SVG)")

print("✅ Quick Start validation OK")
