# TokIntel – Mini Runbook Operativo

Benvenuto nel runbook operativo ultra‑rapido per l'ecosistema **CI/Visual TokIntel**.

## 🔧 Setup rapido (una tantum)
```bash
make install-hooks
```

* Installa l'hook `pre-commit` che esegue `make docs-check` ad ogni commit.

## 🚀 Comandi quotidiani

```bash
# Rigenera screenshot/glow/gif/badge se presenti gli script dedicati
make ci-visual-refresh

# Verifica asset obbligatori (README, status.json, immagini docs/)
make docs-check

# Aggiorna lo stato Docs Ready a PASSING e rigenera il badge nel README
make docs-ready

# Smoke E2E veloce (health + export)
make e2e-smoke
```

## 🔍 Check CI in 30 secondi

| Trigger             | Workflow      | Cosa controlla                     |
| ------------------- | ------------- | ---------------------------------- |
| PR / Push           | Lint Makefile | TAB corretti e sintassi Make       |
| Giornaliero         | Smoke Test    | Health + Export (artifact)         |
| Giornaliero/Manuale | Export Health | Controllo export nelle ultime 24h  |
| Push su main        | Docs Ready    | Badge + data aggiornata nel README |

## 🧯 Failure Playbook (lampo)

* **Badge grigio/rosso** → Apri il run del workflow → scarica artifact → leggi `logs/*.txt`.
* **`missing separator` nel Makefile** → Le ricette DEVONO usare **TAB** (non spazi).
* **Immagini non aggiornate** → `make ci-visual-refresh`.
* **Docs Ready non cambia** → `make docs-ready`, poi commit & push.

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

## 📦 Artifact di riferimento

* `exports/last_export.json` (dallo smoke `e2e-smoke`)
* `docs/status.json` (stato "Docs Ready" + timestamp)
* `docs/images/*` (badge e asset visivi)

## 📗 Policy "Docs Ready"

* **passing** = badge verde + data aggiornata su `README.md`
* **failing** = badge rosso (usa `make docs-fail` per test pipeline)

## 🧰 Troubleshooting rapido

* **Hook non parte** → `chmod +x .git/hooks/pre-commit`
* **Script mancanti** → i target sono "best effort": se uno script non esiste, viene saltato (vedi messaggio "ℹ️")
* **Percorsi diversi** → allinea le variabili nel Makefile (`ASSETS_DIR`, `STATUS_JSON`, `README`)

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
