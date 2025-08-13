# 🚀 TokIntel CI/Visual Operational Runbook

## 📋 Runbook (uso quotidiano)

### Comandi principali

```bash
# Rigenera tutto il pacchetto visivo (screenshot + glow + gif)
make ci-visual-refresh

# Verifica che gli asset obbligatori esistano
make docs-check

# Stato Docs Ready (passing/failing) + badge README autoupdate
make docs-ready        # setta passing + rigenera glow
# make docs-fail       # se vuoi segnare "failing" per test

# E2E rapidi con health + export + last export JSON
make e2e-smoke
```

### Setup iniziale

```bash
# Installa hook pre-commit per TAB Makefile
make install-hooks

# Setup completo per nuovo clone
make install-hooks && make ci-visual-refresh && make docs-ready
```

## 🔍 Check CI in 30 secondi

### Workflow automatici

| Trigger | Workflow | Azione |
|---------|----------|---------|
| **PR/Push** | **Lint Makefile** | Blocca TAB sbagliati |
| **Giornaliero** | **Smoke Test** | Artifact (exports & log) |
| **Giornaliero/Manuale** | **Export Health** | Controllo 24h |
| **Push su main** | **Docs Ready** | Badge e data README aggiornati |

### Verifica rapida

1. **Badge nel README** → tutti verdi?
2. **Actions tab** → ultimi run passati?
3. **Artifacts** → presenti e aggiornati?

## 🚨 Failure Playbook (micro)

### Problemi comuni e soluzioni

#### Badge grigio/rosso
```bash
# 1. Apri il run su GitHub Actions
# 2. Scarica artifact "streamlit-log" o "latest-exports"
# 3. Controlla i log per errori specifici
```

#### Missing separator nel Makefile
```bash
# Errore: "missing separator" 
# Soluzione: ricette con TAB veri (non spazi)
# Verifica: make docs-check
```

#### Immagini non aggiornate
```bash
# Soluzione: rigenera tutto
make ci-visual-refresh

# Hook pre-commit le rigenera comunque automaticamente
```

#### Docs Ready non cambia
```bash
# Soluzione: aggiorna manualmente
make docs-ready
git add docs/status.json docs/images/docs-ready-badge-glow.png README.md
git commit -m "docs: update docs ready status"
git push
```

## 🛠️ Comandi di manutenzione

### Verifica asset
```bash
make docs-check
```

### Rigenerazione completa
```bash
make ci-visual-refresh
```

### Test rapidi
```bash
make e2e-smoke
```

### Gestione Docs Ready
```bash
make docs-ready    # passing
make docs-fail     # failing
```

## 📊 Monitoraggio

### Badge da controllare
- [![CI](https://github.com/papemat/TokIntel/actions/workflows/ci.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/ci.yml)
- [![E2E](https://github.com/papemat/TokIntel/actions/workflows/sprint3-e2e.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/sprint3-e2e.yml)
- [![Exports](https://github.com/papemat/TokIntel/actions/workflows/export-health.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/export-health.yml)
- [![Docs Ready](https://img.shields.io/badge/docs-ready-passing-brightgreen)](docs/status.json)

### Artifacts da verificare
- `latest-exports` - file CSV/JSON di export
- `streamlit-log` - log dell'applicazione
- `playwright-report` - screenshot e report E2E

## 🔧 Troubleshooting avanzato

### Hook pre-commit non funziona
```bash
# Reinstalla hook
make install-hooks

# Verifica permessi
ls -la .git/hooks/pre-commit
```

### Immagini non si generano
```bash
# Verifica dipendenze
pip install pillow matplotlib

# Rigenera manualmente
make ci-screenshot
make ci-badges-preview
make ci-tutorial-gif
```

### Workflow non si attiva
```bash
# Verifica trigger nel file .yml
# Controlla sintassi YAML
# Verifica permessi del repo
```

## 🎯 Handoff a Cursor

Se vuoi rifare tutto "from zero" su un nuovo clone:

1. Apri `tokintel_ci_visual_setup.cursor.txt` in Cursor → **Run**
2. `make install-hooks && make ci-visual-refresh && make docs-ready`
3. commit & push

## 📞 Supporto

Se ti serve altro (nuovi badge, nuovi workflow, o integrare altri check), dimmelo e lo cuciamo addosso al repo. 🚀

---

**Stato:** ✅ **OPERATIVO**
**Ultimo aggiornamento:** $(date)
**Versione:** 1.0
