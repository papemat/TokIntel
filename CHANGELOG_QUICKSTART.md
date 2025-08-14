# Changelog – Quickstart Bundle

## v1.1.0 (2025-08-14)
### Aggiunto
- `README_QUICKSTART.md`: guida setup in ~60s
- `scripts/run_tokintel.sh` (macOS/Linux): launcher con auto‑install deps, `--lan`, `--port`, `--no-headless`, `--debug`, `--app`
- `scripts/run_tokintel.bat` (Windows): parità funzionale con Unix
- `streamlit_config_example.toml`: configurazione suggerita per locale/prod
- `FAQ_TROUBLESHOOTING.md`: top 10 problemi con soluzioni
- Target `make`: `run`, `run-lan`, `run-debug`, `quickstart-check`
- Template PR e workflow CI di dry‑run

### Modificato
- `README.md`: badge Quickstart e Cross‑Platform + note launcher

### Note
- Headless di default; usare `--no-headless` in sviluppo
- Auto‑install da `requirements.txt` se Streamlit manca
