## What's inside
- README_QUICKSTART.md (setup in ~60s)
- scripts/run_tokintel.sh (macOS/Linux) – auto deps, --lan, --port, --no-headless, --debug, --app
- scripts/run_tokintel.bat (Windows) – parity with Unix script
- streamlit_config_example.toml – production-friendly defaults
- FAQ_TROUBLESHOOTING.md – top 10 issues with fixes
- Makefile targets (run, run-lan, run-debug)

## Why
Lower friction for new users; consistent launcher behavior across platforms.

## How to test
```bash
./scripts/run_tokintel.sh --help
PORT=9000 ./scripts/run_tokintel.sh --lan --no-headless --debug
.\scripts\run_tokintel.bat --help
.\scripts\run_tokintel.bat --lan --port 9000 --no-headless --debug
make run
make run-lan PORT=9000
make run-debug
```

## Checklist

* [ ] Scripts run from repo root and detect venv
* [ ] Auto-install requirements if Streamlit missing
* [ ] Headless default (opt-out via --no-headless)
* [ ] FAQ covers common issues (ports, perms, deps)
* [ ] README references quickstart section
* [ ] Makefile targets for easy access
* [ ] Cross-platform sanity checks completed
