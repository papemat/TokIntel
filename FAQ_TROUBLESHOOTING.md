# TokIntel – FAQ & Troubleshooting

## 1) Port already in use
**Fix:** usa un'altra porta:
```bash
PORT=9000 ./scripts/run_tokintel.sh
scripts\run_tokintel.bat --port 9000
```

## 2) ModuleNotFoundError: streamlit

**Fix:** i launcher installano automaticamente; in caso:

```bash
python3 -m pip install -r requirements.txt
```

## 3) Python not found

Installa Python 3.10+ e riapri terminale/PowerShell.

## 4) Permission denied (.sh)

```bash
chmod +x scripts/run_tokintel.sh
```

## 5) Firewall Windows con --lan

Consenti Python/Streamlit quando richiesto.

## 6) Browser non si apre

Headless attivo: usa `--no-headless`.

## 7) Pagina bianca/loop

```bash
rm -rf ~/.cache/streamlit
./scripts/run_tokintel.sh --debug
```

## 8) Mismatch dipendenze

```bash
python3 -m pip install --upgrade -r requirements.txt
```

## 9) Address in use su LAN

macOS/Linux:

```bash
lsof -i :8501
kill -9 <PID>
```

Windows:

```bat
netstat -a -n -o | findstr :8501
TaskKill /PID <PID> /F
```

## 10) Import di progetto

Assicurati di avviare dalla root (gli script lo fanno) e venv attiva.
