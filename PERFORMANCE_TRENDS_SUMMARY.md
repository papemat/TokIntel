# 📈 Performance Trends System - TokIntel

## Overview

Sistema completo per monitoraggio performance con:
- **Nightly cron** (GitHub Actions)
- **Aggregazione CSV** (storico trend)
- **Dashboard Streamlit** (visualizzazione)

## 🕐 Nightly Performance Workflow

**File:** `.github/workflows/perf-nightly.yml`

Esegue ogni notte alle 02:00 UTC:
1. Setup staging DB large
2. Benchmark performance
3. Aggregazione CSV storico
4. Upload artifacts
5. Commit automatico CSV (opzionale)

### Trigger manuale:
```bash
gh workflow run "Perf Nightly"
```

## 📊 Aggregazione Storico

**Script:** `scripts/perf_aggregate.py`

Legge tutti i `perf_*.json` e genera `reports/perf_history.csv`:

```bash
# Aggrega automaticamente
python scripts/perf_aggregate.py

# Output personalizzato
python scripts/perf_aggregate.py --dir reports --out custom_history.csv
```

### Schema CSV:
- `ts`: timestamp
- `db_path`: path database
- `videos_count`: numero video
- `add_indexes_ms`: tempo indici
- `sql_read_500`: lettura SQL 500 record
- `export_csv`: export CSV
- `export_json`: export JSON
- `stress_iter_*_ms`: stress test cache

## 📈 Dashboard Streamlit

**File:** `dash/perf_dashboard.py`

Visualizza trend performance nel tempo:
- Overview tabellare (ultimi 20 record)
- Grafici trend per metrica
- Fallback automatico da JSON se CSV manca

### Avvio:
```bash
# Via Makefile
make perf-dash

# Diretto
streamlit run dash/perf_dashboard.py
```

## 🧰 Comandi Rapidi

```bash
# Nightly manuale
gh workflow run "Perf Nightly"

# Dashboard locale
make perf-dash

# Aggregazione manuale
python scripts/perf_aggregate.py

# Test performance locale
make perf-check
```

## 📋 Configurazione

### Environment Variables (nightly):
```yaml
DB_PATH: data/staging_db.sqlite
PERFORMANCE_TEST: "1"
FF_DISABLE_CACHE: "0"
CACHE_TTL_SECONDS: "0"
MAX_SQL_READ_MS: "2000"
MAX_EXPORT_MS: "2000"
```

### Soglie Performance:
- SQL read 500: < 1500ms
- Export CSV/JSON: < 1500ms
- Add indexes: < 500ms

## 🔄 Workflow Completo

1. **Nightly (02:00 UTC)**: Esegue benchmark
2. **Aggregazione**: Genera CSV storico
3. **Artifacts**: Upload report + CSV
4. **Commit**: Aggiorna CSV nel repo
5. **Dashboard**: Visualizza trend

## 📊 Metriche Monitorate

- **Database**: letture SQL, indici
- **Export**: CSV/JSON performance
- **Cache**: stress test iterazioni
- **Trend**: confronto temporale

## 🎯 Benefici

- **Monitoraggio continuo** performance
- **Trend detection** regressioni
- **Alerting** automatico (via soglie)
- **Storico** completo per analisi
- **Dashboard** interattiva

## 🔧 Debug

```bash
# Disabilita cache per debug
FF_DISABLE_CACHE=1 make perf-check

# Solo aggregazione
python scripts/perf_aggregate.py

# Dashboard con dati custom
streamlit run dash/perf_dashboard.py
```

---

**Status:** ✅ Implementato e testato
**Badge:** ![Performance Trends](https://img.shields.io/badge/perf-trends-blue?style=flat&logo=chart-line)
