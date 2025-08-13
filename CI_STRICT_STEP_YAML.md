# 🔧 CI Strict Step YAML — Ready to Paste

Step da aggiungere al tuo workflow `.github/workflows/quickstart-guard.yml` per l'idempotenza strict in CI:

## 🎯 Step da aggiungere

```yaml
      - name: Idempotenza strict (hard-fail)
        run: |
          echo "🔁 Verifica idempotenza strict..."
          python3 .github/scripts/autofix_quickstart.py
          python3 .github/scripts/autofix_quickstart.py
          if ! git diff --quiet; then
            echo "❌ Non idempotente: diff dopo secondo run!"
            git --no-pager diff
            exit 2
          fi
          echo "✅ Idempotenza strict OK"
```

## 🔄 Workflow completo aggiornato

```yaml
name: Quick Start Guard

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  docs-guard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt || true
          pip install markdown-it-py linkify-it-py
      
      - name: Validate Quick Start
        run: |
          python .github/scripts/validate_quickstart.py
      
      - name: Report duplicati (solo log)
        run: |
          python3 .github/scripts/report_qs_duplicates.py || true
      
      - name: Autofix Quick Start (anti-duplicati idempotente)
        run: |
          python3 .github/scripts/autofix_quickstart.py
      
      - name: Idempotenza strict (hard-fail)
        run: |
          echo "🔁 Verifica idempotenza strict..."
          python3 .github/scripts/autofix_quickstart.py
          python3 .github/scripts/autofix_quickstart.py
          if ! git diff --quiet; then
            echo "❌ Non idempotente: diff dopo secondo run!"
            git --no-pager diff
            exit 2
          fi
          echo "✅ Idempotenza strict OK"
      
      - name: Enforce no-diff on PR (fallisci se autofix ha modificato README)
        if: ${{ github.event_name == 'pull_request' }}
        run: |
          git add README.md || true
          if ! git diff --cached --quiet; then
            echo "::error::Il blocco Quick Start è stato corretto automaticamente. Committa le modifiche localmente e riprova."
            git diff --cached --unified=0 -- README.md || true
            exit 1
          fi
          echo "✅ Nessuna modifica necessaria in PR."
      
      - name: Auto-commit autofix su push
        if: ${{ github.event_name == 'push' }}
        run: |
          git config user.email "actions@github.com"
          git config user.name "github-actions"
          git add README.md || true
          if git diff --cached --quiet; then
            echo "Nessun cambiamento da committare."
          else
            git commit -m "docs(quickstart): apply anti-duplicate autofix (CI)"
            git push
          fi
      
      - name: Offline link-check (relative links only)
        run: |
          python3 .github/scripts/docs_linkcheck.py
      
      - name: Dry-run Makefile targets
        run: |
          make -n tokintel-gui-bg
          make -n tokintel-gui-log
          make -n tokintel-gui-health
          make -n tokintel-gui-stop
          make -n tokintel-gui-quickstart
```

## 🎯 Comportamento

- ✅ **Strict**: Fallisce se il secondo run produce diff
- ✅ **PR**: Blocca se autofix ha modificato README
- ✅ **Push**: Auto-commit delle correzioni
- ✅ **Linkcheck**: Verifica link relativi

## 🚀 Uso

1. **Copia lo step** nel tuo workflow
2. **Posizionalo** dopo l'autofix e prima del linkcheck
3. **Testa** con una PR che ha duplicati

Il workflow ora garantisce idempotenza strict in CI! 🎯
