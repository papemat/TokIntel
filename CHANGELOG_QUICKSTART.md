# Changelog – Quickstart Bundle

## v1.1.0 (2025-08-14)
### Added
- `README_QUICKSTART.md`: guida setup in ~60s
- `scripts/run_tokintel.sh` (macOS/Linux): launcher con auto-install deps, `--lan`, `--port`, `--no-headless`, `--debug`, `--app`
- `scripts/run_tokintel.bat` (Windows): parità funzionale con lo script Unix
- `streamlit_config_example.toml`: config ottimizzata per uso locale/prod
- `FAQ_TROUBLESHOOTING.md`: top 10 problemi + fix
- Target `make`: `run`, `run-lan`, `run-debug`

### Changed
- `README.md`: aggiunto collegamento al quickstart e note sui launcher

### Notes
- Headless di default; per sviluppo usare `--no-headless`
- Se manca Streamlit, i launcher installano automaticamente da `requirements.txt`
