# TokIntel – FAQ & Troubleshooting

## 1) Port already in use (OSError: [Errno 98] / [WinError 10013])
**Fix:** choose another port:
```bash
PORT=9000 ./scripts/run_tokintel.sh
# or
scripts\run_tokintel.bat --port 9000
```

## 2) `ModuleNotFoundError: No module named 'streamlit'`

**Fix:** the launcher installs requirements automatically. If it fails, run:

```bash
python3 -m pip install -r requirements.txt
```

## 3) Python not found

**Fix:** install Python 3.10+ from python.org, then reopen terminal/PowerShell.

## 4) Permission denied on macOS/Linux running `.sh`

**Fix:**

```bash
chmod +x scripts/run_tokintel.sh
```

## 5) Firewall blocks on Windows when using `--lan`

**Fix:** allow Python/Streamlit in Windows Defender Firewall when prompted.

## 6) Browser doesn't open automatically

**Reason:** headless mode is on by default. **Fix:** use `--no-headless`.

## 7) Blank page / endless loading after install

**Fix:** clear cache and restart:

```bash
rm -rf ~/.cache/streamlit
./scripts/run_tokintel.sh --debug
```

## 8) Dependency mismatch (e.g., pandas version errors)

**Fix:** upgrade deps from `requirements.txt`:

```bash
python3 -m pip install --upgrade -r requirements.txt
```

## 9) `Address already in use` on LAN

**Fix:** another Streamlit is running. Kill it or pick a new port. On macOS/Linux:

```bash
lsof -i :8501
kill -9 <PID>
```

On Windows:

```bat
netstat -a -n -o | findstr :8501
TaskKill /PID <PID> /F
```

## 10) `No module named ...` for project imports

**Fix:** ensure you launched from repo root (the scripts `cd` there automatically) and that your venv is active if you use one.
