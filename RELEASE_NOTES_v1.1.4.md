# TokIntel v1.1.4 — Ingest Logs Panel + Step & Total Timing

## 🚀 What's New

### ⏱️ Sistema di Timing Completo
- **Durata per step**: ogni fase dell'ingest mostra il tempo impiegato
- **Tempo totale**: visualizzazione del tempo complessivo dell'ingest
- **Colorazione automatica**: 🟢 <30s, 🟠 30–60s, 🔴 >60s
- **Pattern strutturati**: `⏳ Iniziando:`, `✅ Completato: (durata: X.XXs)`, `🏁 Ingest completato in Y.YYs totali`

### 📜 Ingest Logs Panel Avanzato
- **Auto‑refresh** ogni 5s
- **Filtro per livello**: ALL/INFO/WARNING/ERROR
- **Download log**: `ingest.log` completo
- **Svuota log**: pulsante quick‑clear
- **Rotating logs**: `~/.tokintel/logs/ingest.log` (2MB, 3 backup)

### 📊 Statistiche Ingest
- **Durate medie per step** (min/max)
- **Tempo totale medio**
- **Evidenziazione step lenti** (collo di bottiglia)
- **Colori intuitivi**: 🟢 veloce, 🟠 normale, 🔴 lento

### 🔧 Configurazione
- **LOG_LEVEL**: DEBUG/INFO/WARNING/ERROR/CRITICAL
- **Make targets**: `test-timing`, `timing-demo`, `logs-tail`, `logs-open`, `logs-debug`
- **macOS bootstrap**: `mac-bootstrap`, `mac-venv-rebuild` (Python 3.11 Homebrew)

## 🧪 How to Use

```bash
make test-timing    # test unitari
make timing-demo    # demo con simulazione ingest

LOG_LEVEL=INFO make start-logs  # avvio con log live
make logs-tail      # tail live
make logs-open      # apri log nell'editor
```

**Dashboard**

* **📜 Ingest Logs**: verifica pattern timing (auto‑refresh ON)
* **📈 Statistiche Ingest**: popola dopo 2‑3 ingest

## 📎 Esempi

**Log colorato**

```
🚀 Ingest avviato
⏳ Iniziando: Raccolta URL
✅ Completato: Raccolta URL (durata: 2.50s)
⏳ Iniziando: Download video
✅ Completato: Download video (durata: 4.00s)
⏳ Iniziando: Estrazione frame e OCR
✅ Completato: Estrazione frame e OCR (durata: 11.30s)
⏳ Iniziando: Trascrizione audio
✅ Completato: Trascrizione audio (durata: 12.70s)
⏳ Iniziando: Costruzione indice testuale
✅ Completato: Costruzione indice testuale (durata: 4.30s)
🏁 Ingest completato in 34.80s totali
```

**Statistiche**

```
Durate medie per step:
• Raccolta URL: 2.5s (min 0.5s, max 5.2s)
• Download video: 4.0s (min 0.6s, max 15.0s)
• Estrazione frame e OCR: 11.3s (min 2.3s, max 44.0s)
• Trascrizione audio: 12.7s (min 2.1s, max 45.2s)
• Costruzione indice testuale: 4.3s (min 0.9s, max 12.8s)

⏱️ Tempo totale medio: 34.8s (normale)
Basato su 3 ingest completati
```

## 🧰 Troubleshooting

* **ffmpeg/yt-dlp non trovati**

  ```bash
  make mac-bootstrap && make mac-venv-rebuild
  ```
* **Log vuoti**: esegui un ingest reale, verifica **📜 Ingest Logs** con auto‑refresh ON, usa `make logs-tail`.
* **Colori non visibili**: assicurati che il pannello sia espanso e ci siano log con pattern timing.

## ⚙️ Performance

* **Overhead minimo**: <1ms per step
* **Backward compatibility**: nessun impatto sugli ingest esistenti
* **Robustezza**: eccezioni gestite senza perdita timing
* **Soglie colori** configurabili in `dash/app.py`

## ✅ Quality Gate

* Test unitari: ✅
* Demo timing: ✅
* Pattern log e colorazione: ✅
* Statistiche dashboard: ✅
