# TokIntel — Go‑Live Checklist

Questa checklist guida il pre‑deploy in produzione: test, export di esempio e report automatici.

## ✅ Pre‑requisiti
- Python 3.10+ (consigliato 3.11)
- `requirements.txt` installato (`pip install -r requirements.txt`)
- `pytest` installato
- Makefile aggiornato con `prod-check`, `ensure-db`, `add-indexes`, `test-*`

## 🚀 Comando unico
```bash
make prod-check
```

### Cosa fa

1. Verifica/crea DB (`ensure-db`)
2. Aggiunge indici (`add-indexes`)
3. Esegue test rapidi (`test-status`, `test-export`, `test-cache`)
4. Esegue `pytest` non‑bloccante (`pytest-safe`)
5. Esporta campione CSV/JSON (`export-prod-sample`)
6. Genera report MD+JSON in `reports/` (`report-prod-check`)

## 🔧 Variabili d'ambiente utili

* `TOKINTEL_VERSION` → versione/commit da tracciare nel report (es. `1.0.0` o `main-<sha>`)
* `FF_DISABLE_CACHE` → `1` per disabilitare la cache Streamlit (debug live)
* `CACHE_TTL_SECONDS` → TTL della cache (0 = infinito)
* `DB_PATH` → percorso DB (default `data/tokintel.db`)

Esempio:

```bash
TOKINTEL_VERSION=1.0.0 FF_DISABLE_CACHE=1 CACHE_TTL_SECONDS=3600 DB_PATH=data/tokintel.db make prod-check
```

## 📊 Output atteso

* **Reports:** `reports/prod_check_YYYYMMDD_HHMMSS.md|json`
* **Exports:** `exports/tokintel_sample_YYYYMMDD_HHMMSS.csv|json`

## 🧐 Come leggere il report

Apri `reports/prod_check_*.md`:

* **Environment**: valori env, versione app, Python
* **Database**: path, size MB, modified
* **Metrics**:

  * `Video count` >= valore atteso?
  * **Status distribution**: numeri coerenti (ok/pending/timeout/skipped/error)
  * **Indexes on videos**: presenti `idx_videos_status`, `idx_videos_title`, eventuali `collection_id`

## 🧪 Smoke test manuale consigliato

1. Avvia dashboard, filtra per stato e cerca: la UI resta fluida?
2. Export CSV/JSON dal front‑end: file scaricati? contenuto consistente?
3. Modifica 1 record nel DB e verifica aggiornamento UI (cache invalidata su mtime)

## 🚨 Troubleshooting rapido

* **Test rossi**: guarda l'output; `prod-check` non blocca. Valuta se sono critici per il deploy.
* **Export vuoto**: controlla `DB_PATH` e permessi.
* **Report "n/d"**: tabelle/indici mancanti → riesegui `make add-indexes`.
* **Cache sospetta**: usa `FF_DISABLE_CACHE=1` temporaneamente o "Forza refresh cache" dal pannello diagnostica.
