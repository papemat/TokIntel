# Post-Release Checklist - TokIntel v1.1.1

## ✅ Checklist (30s)

- [ ] Release `v1.1.1` visibile con note corrette
- [ ] Badge **Latest Release** aggiornato
- [ ] Quickstart (launcher) → OK su macOS/Linux/Windows
- [ ] Docker `compose up --build` → OK (su macchina con Docker)
- [ ] FAQ/README linkati dalla homepage del repo

## 🔍 Verifiche Rapide

### Release GitHub
- [ ] https://github.com/papemat/TokIntel/releases/tag/v1.1.1
- [ ] Note di release presenti e corrette
- [ ] Assets (se presenti) scaricabili

### Badge Status
- [ ] Badge "Latest Release" mostra `v1.1.1`
- [ ] Badge "Release" workflow verde
- [ ] Badge CI principali verdi

### Quickstart Test
```bash
# macOS/Linux
git clone https://github.com/papemat/TokIntel.git
cd TokIntel
./scripts/run_tokintel.sh --help

# Windows
git clone https://github.com/papemat/TokIntel.git
cd TokIntel
scripts\run_tokintel.bat --help
```

### Docker Test
```bash
# Se Docker disponibile
git clone https://github.com/papemat/TokIntel.git
cd TokIntel
docker compose up --build
# Apri http://localhost:8501
```

## 📋 Documentazione

- [ ] README.md aggiornato con sezione Docker
- [ ] README_QUICKSTART.md presente
- [ ] FAQ_TROUBLESHOOTING.md presente
- [ ] streamlit_config_example.toml presente

## 🚀 Annuncio

Template per Slack/Discord/GitHub:

```
🎉 TokIntel v1.1.1 — Quickstart + Docker

* ⏱️ Avvio in ~60s con launcher cross‑platform
* 🧩 Quickstart: README_QUICKSTART.md
* 🐧/🪟 Launchers: scripts/run_tokintel.sh & scripts/run_tokintel.bat
* 🐳 Docker: Dockerfile + docker-compose.yml (dev live-reload)
* 🧰 Troubleshooting: FAQ_TROUBLESHOOTING.md
* ⚙️ Config: streamlit_config_example.toml
* 🤖 Release automation: tag v1.1.1 → GitHub Release auto con changelog

Start here:
* macOS/Linux: `./scripts/run_tokintel.sh`
* Windows: `scripts\run_tokintel.bat`
* Docker: `docker compose up --build`

Repo: https://github.com/papemat/TokIntel
```
