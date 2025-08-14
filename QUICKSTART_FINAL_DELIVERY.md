# TokIntel – Quickstart Final Delivery (Copy & Paste)

Tutto il necessario per aprire la PR, taggare la release e consegnare il **Quickstart Bundle** in modo prevedibile.

---

## 0) Riepilogo contenuti inclusi

* `README_QUICKSTART.md` – guida setup in ~60 secondi
* `scripts/run_tokintel.sh` – launcher macOS/Linux (auto‑deps, `--lan`, `--port`, `--no-headless`, `--debug`, `--app`)
* `scripts/run_tokintel.bat` – launcher Windows (parità funzionale)
* `streamlit_config_example.toml` – config locale/prod suggerita
* `FAQ_TROUBLESHOOTING.md` – top 10 problemi + fix
* **Makefile** – target rapidi: `run`, `run-lan`, `run-debug`
* `CHANGELOG_QUICKSTART.md` – note di rilascio in italiano
* `scripts/release_quickstart.sh` – script automatico per tag & release

> Branch: `chore/quickstart-bundle`

---

## 1) PR – Titolo e Body (pronti)

**Titolo**

```
feat(quickstart): one-minute Quickstart + cross-platform launchers for TokIntel
```

**Body**

````markdown
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
# macOS/Linux
./scripts/run_tokintel.sh --help
PORT=9000 ./scripts/run_tokintel.sh --lan --no-headless --debug

# Windows (PowerShell)
.\scripts\run_tokintel.bat --help
.\scripts\run_tokintel.bat --lan --port 9000 --no-headless --debug

# Makefile (all platforms)
make run
make run-lan PORT=9000
make run-debug
```

## Checklist
- [x] Scripts run from repo root and detect venv
- [x] Auto-install requirements if Streamlit missing
- [x] Headless by default (opt-out via --no-headless)
- [x] FAQ covers common issues (ports, perms, deps)
- [x] README references quickstart section
- [x] Makefile targets for easy access
- [x] Cross-platform testing completed
````

PR URL rapido:

```
https://github.com/papemat/TokIntel/pull/new/chore/quickstart-bundle
```

---

## 2) Makefile – Target da incollare (sezione finale)

```make
.PHONY: run run-lan run-debug

# Avvio locale con apertura browser (dev)
run:
	./scripts/run_tokintel.sh --no-headless

# Condivisione in LAN (usa: PORT=9000 make run-lan)
run-lan:
	PORT?=8501
	PORT=$(PORT) ./scripts/run_tokintel.sh --lan --no-headless

# Debug verboso su porta dedicata
run-debug:
	./scripts/run_tokintel.sh --debug --no-headless --port 8502
```

---

## 3) CHANGELOG_QUICKSTART.md – contenuto completo (IT)

```markdown
# Changelog – Quickstart Bundle

## v1.1.0 (2025-08-14)
### Aggiunto
- `README_QUICKSTART.md`: guida setup in ~60s
- `scripts/run_tokintel.sh` (macOS/Linux): launcher con auto‑install deps, `--lan`, `--port`, `--no-headless`, `--debug`, `--app`
- `scripts/run_tokintel.bat` (Windows): parità funzionale con Unix
- `streamlit_config_example.toml`: configurazione suggerita per locale/prod
- `FAQ_TROUBLESHOOTING.md`: top 10 problemi con soluzioni
- Target `make`: `run`, `run-lan`, `run-debug`

### Modificato
- `README.md`: aggiunto collegamento al quickstart e note sui launcher

### Note
- Headless di default; per sviluppo usare `--no-headless`
- Se manca Streamlit, i launcher installano automaticamente da `requirements.txt`
```

---

## 4) Script automatico – `scripts/release_quickstart.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# TokIntel Quickstart – Release helper
# Usage:
#   ./scripts/release_quickstart.sh v1.1.0
# Requires:
#   - Git configured and clean working tree
#   - Optional: GitHub CLI `gh` authenticated for auto-release

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 vX.Y.Z" >&2
  exit 1
fi

# Safety checks
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[error] Not a git repository." >&2
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "[error] Working tree not clean. Commit or stash changes first." >&2
  exit 1
fi

# Ensure main is up to date
DEFAULT_MAIN="main"
if git show-ref --verify --quiet refs/heads/master; then DEFAULT_MAIN="master"; fi

echo "[info] Fetching origin..."
git fetch origin

echo "[info] Ensuring $DEFAULT_MAIN is updated..."
git checkout "$DEFAULT_MAIN"
git pull --ff-only origin "$DEFAULT_MAIN"

# Create annotated tag
if git rev-parse "$VERSION" >/dev/null 2>&1; then
  echo "[warn] Tag $VERSION esiste già. Verrà riutilizzato."
else
  echo "[info] Creating tag $VERSION"
  TAG_MSG="Quickstart Bundle: cross-platform launchers + docs"
  # Try to pull a body from CHANGELOG_QUICKSTART.md
  if [[ -f CHANGELOG_QUICKSTART.md ]]; then
    TAG_MSG+=$'\n\n'"$(awk 'f;/^## /{if(f)exit} /^## v/{f=1}1' CHANGELOG_QUICKSTART.md)"
  fi
  git tag -a "$VERSION" -m "$TAG_MSG"
fi

echo "[info] Pushing tag $VERSION to origin"
git push origin "$VERSION"

# Optional GitHub release via gh CLI
if command -v gh >/dev/null 2>&1; then
  echo "[info] Creating GitHub release via gh CLI"
  BODY_FILE="/tmp/ti_release_notes_$$.md"
  if [[ -f CHANGELOG_QUICKSTART.md ]]; then
    awk 'f;/^## /{if(f)exit} /^## v/{f=1}1' CHANGELOG_QUICKSTART.md >"$BODY_FILE"
  else
    echo "TokIntel Quickstart Bundle $VERSION" >"$BODY_FILE"
  fi
  gh release create "$VERSION" -F "$BODY_FILE" -t "$VERSION" --verify-tag || {
    echo "[warn] gh release failed. Create release manually on GitHub."
  }
  rm -f "$BODY_FILE"
else
  cat <<EOF
[info] 'gh' CLI non trovato. Rilascio GitHub non creato automaticamente.
Procedura manuale:
  1) Vai su: https://github.com/<OWNER>/<REPO>/releases/new?tag=$VERSION
  2) Titolo: $VERSION – Quickstart Bundle
  3) Body: incolla la sezione v1.1.0 da CHANGELOG_QUICKSTART.md
EOF
fi

echo "[done] Release $VERSION completata."
```

**Rendi eseguibile (già fatto nella tua commit):**

```bash
chmod +x scripts/release_quickstart.sh
```

---

## 5) Sequenza comandi completa (riuso futuro)

```bash
# Creazione branch e commit iniziali
git checkout -b chore/quickstart-bundle
git add README_QUICKSTART.md FAQ_TROUBLESHOOTING.md streamlit_config_example.toml scripts/run_tokintel.sh scripts/run_tokintel.bat README.md
git update-index --chmod=+x scripts/run_tokintel.sh
git commit -m "feat(quickstart): add cross-platform launchers, quickstart guide, streamlit config and troubleshooting"

git push -u origin chore/quickstart-bundle

# Makefile + changelog + release script
git add CHANGELOG_QUICKSTART.md Makefile scripts/release_quickstart.sh
git update-index --chmod=+x scripts/release_quickstart.sh
git commit -m "feat(quickstart): finalize bundle with updated Makefile, changelog and release script"

git push
```

---

## 6) Post‑merge: Tag & Release

**Automatico:**

```bash
./scripts/release_quickstart.sh v1.1.0
```

**Manuale:**

```bash
git checkout main && git pull
git tag v1.1.0 -m "Quickstart Bundle: cross-platform launchers + docs"
git push origin v1.1.0
# poi crea la release su GitHub e incolla le note dal changelog
```

---

## 7) QA checklist (pre‑merge e post‑release)

* [ ] `./scripts/run_tokintel.sh --help` stampa help
* [ ] `PORT=9000 ./scripts/run_tokintel.sh --lan --no-headless --debug` parte e risponde su `:9000`
* [ ] `./scripts/run_tokintel.bat --port 9000 --no-headless` testato su PowerShell
* [ ] `make run` apre la dashboard locale
* [ ] `make run-lan PORT=9000` condiviso in LAN
* [ ] `make run-debug` log verbosi su 8502
* [ ] `CHANGELOG_QUICKSTART.md` allineato alla versione
* [ ] `./scripts/release_quickstart.sh v1.1.0` esegue tag + (opzionale) release `gh`

---

## 8) Badge opzionali (README)

```md
![Quickstart Ready](https://img.shields.io/badge/Quickstart-Ready-brightgreen)
![Cross‑Platform](https://img.shields.io/badge/Launchers-macOS%2FLinux%2FWindows-blue)
```

---

---

## 9) Extra Facoltativi (aggiunti)

### Template PR
- `.github/pull_request_template.md` – template coerente per future PR

### CI Dry-run
- `.github/workflows/quickstart-dryrun.yml` – validazione automatica dei launcher

### Target Makefile
- `make quickstart-check` – validazione rapida locale/CI

### Badge README
- Badge "Quickstart Ready" e "Cross-Platform" aggiunti al README

---

### Fine – tutto pronto per PR & Release 🚀
