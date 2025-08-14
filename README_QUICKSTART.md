# TokIntel – Quick Start

TokIntel is a local dashboard (Streamlit) that analyzes your sources. This guide gets you from zero to running in ~1 minute.

## Requirements
- Python 3.10 or 3.11
- pip (or uv/pipx)
- Git (optional)

> Recommended: create a virtual environment (`python3 -m venv .venv && source .venv/bin/activate` on macOS/Linux, `.venv\Scripts\activate` on Windows).

## Install
```bash
# From repo root
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Run (macOS/Linux)

```bash
./scripts/run_tokintel.sh
```

## Run (Windows)

```bat
scripts\run_tokintel.bat
```

The app defaults to [http://localhost:8501](http://localhost:8501)

## Useful flags

* `--lan` → bind to `0.0.0.0` (access from same network)
* `--port <num>` → custom port (default 8501)
* `--app <path>` → app entry (default `dash/app.py`)
* `--no-headless` → open browser automatically (dev mode)
* `--debug` → verbose logs

### Examples

```bash
# Share on LAN at port 9000
PORT=9000 ./scripts/run_tokintel.sh --lan

# Use custom app entry and open browser
./scripts/run_tokintel.sh --app dash/app.py --no-headless

# Windows, LAN mode
scripts\run_tokintel.bat --lan --port 9000
```

## Optional local Streamlit config

Copy the example file:

```bash
mkdir -p ~/.streamlit
cp streamlit_config_example.toml ~/.streamlit/config.toml
```

## Stop

Press `Ctrl+C` in the terminal where TokIntel is running.

## Troubleshooting

See **FAQ_TROUBLESHOOTING.md** for fixes to common issues (port conflicts, missing deps, permissions, etc.).
