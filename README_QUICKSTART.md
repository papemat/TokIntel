# TokIntel – Quick Start

TokIntel è una dashboard locale (Streamlit). Avvio in ~60 secondi.

## Requisiti
- Python 3.10 o 3.11
- pip
- (Consigliato) venv

## Install
```bash
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

Default: [http://localhost:8501](http://localhost:8501)

## Opzioni utili

* `--lan` → bind `0.0.0.0`
* `--port <num>` → porta custom
* `--app <path>` → entry app (default `dash/app.py`)
* `--no-headless` → apre il browser (dev)
* `--debug` → log verbosi

### Esempi

```bash
PORT=9000 ./scripts/run_tokintel.sh --lan
./scripts/run_tokintel.sh --app dash/app.py --no-headless
scripts\run_tokintel.bat --lan --port 9000
```

## Config Streamlit (opzionale)

```bash
mkdir -p ~/.streamlit
cp streamlit_config_example.toml ~/.streamlit/config.toml
```

## Stop

`Ctrl+C` nella shell dove gira TokIntel.

## Troubleshooting

Vedi **FAQ_TROUBLESHOOTING.md**.
