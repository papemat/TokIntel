import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
readme = ROOT / "README.md"

SNIPPET = """## ⚡ Quick Start – TokIntel GUI

[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](#)

| Azione                  | Comando | Descrizione |
|-------------------------|---------|-------------|
| ▶️ **Avvio rapido**     | `make tokintel-gui-bg` | Avvia in background e apre il browser |
| 📡 **Monitoraggio log** | `make tokintel-gui-log` | Mostra log in tempo reale |
| 🩺 **Health check**     | `make tokintel-gui-health` | Verifica se la GUI è attiva (HTTP 200) |
| ⏹ **Stop pulito**       | `make tokintel-gui-stop` | Ferma il processo GUI in esecuzione |
| 🔄 **Riavvio**          | `make tokintel-gui-restart` | Stop + start in un solo comando |
| ⚙️ **Porta custom**     | `make tokintel-gui-on PORT=8502` | Avvia su una porta specifica |

<p align="left">
  <img src="docs/images/tokintel_gui_home.png" alt="TokIntel GUI Home" width="720" onerror="this.src='docs/images/tokintel_gui_home.svg'">
</p>
"""

def main():
    text = readme.read_text(encoding="utf-8")
    hdr = "## ⚡ Quick Start – TokIntel GUI"
    if hdr not in text:
        # inserisci in cima alla sezione "Usage" o subito dopo il primo titolo
        if "## Usage" in text:
            text = text.replace("## Usage", SNIPPET + "\n\n## Usage", 1)
        else:
            # dopo il titolo principale
            m = re.search(r"^# .*$", text, re.M)
            if m:
                i = m.end()
                text = text[:i] + "\n\n" + SNIPPET + "\n\n" + text[i:]
            else:
                text = SNIPPET + "\n\n" + text
        readme.write_text(text, encoding="utf-8")
        print("✅ Quick Start inserito.")
        return

    # sostituisci blocco esistente fino al prossimo header di secondo livello
    pattern = r"## ⚡ Quick Start – TokIntel GUI[\\s\\S]*?(?=\\n##\\s)"
    if re.search(pattern, text):
        text = re.sub(pattern, SNIPPET + "\n\n", text)
        readme.write_text(text, encoding="utf-8")
        print("✅ Quick Start aggiornato.")
    else:
        # header presente ma blocco non catturabile → reinserisci forzando
        text = text.replace(hdr, SNIPPET)
        readme.write_text(text, encoding="utf-8")
        print("✅ Quick Start rigenerato (fallback).")

if __name__ == "__main__":
    main()
