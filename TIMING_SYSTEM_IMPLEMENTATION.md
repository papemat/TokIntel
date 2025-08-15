# ⏱️ TokIntel - Sistema di Timing Ingest

## 🎯 Obiettivo Completato

✅ **Misurazione durata di ogni step**  
✅ **Misurazione e visualizzazione tempo totale ingest**  
✅ **Logging durate in `tokintel.ingest`**  
✅ **Visualizzazione durate e tempo totale nella dashboard**  
✅ **Evidenziazione visiva step lenti**  

---

## 🛠️ Modifiche Implementate

### 1️⃣ `utils/timing.py` (Nuovo Helper)

**Context Manager per Step Individuali:**
```python
@contextmanager
def timed_step(logger, step_name):
    start = time.time()
    logger.info(f"⏳ Iniziando: {step_name}")
    try:
        yield
    finally:
        elapsed = time.time() - start
        logger.info(f"✅ Completato: {step_name} (durata: {elapsed:.2f}s)")
```

**Context Manager per Ingest Completo:**
```python
@contextmanager
def timed_ingest(logger):
    total_start = time.time()
    logger.info("🚀 Ingest avviato")
    try:
        yield
    finally:
        total_elapsed = time.time() - total_start
        logger.info(f"🏁 Ingest completato in {total_elapsed:.2f}s totali")
```

**Helper per Formattazione Durate:**
```python
def format_duration(seconds: float) -> str:
    # Converte secondi in formato leggibile (es. "1m 30s")
```

---

### 2️⃣ `scripts/ingest_collection.py` (Integrazione Timing)

**Import del Sistema Timing:**
```python
from utils.timing import timed_step, timed_ingest
```

**Wrapping Completo del Processo:**
```python
with timed_ingest(log):
    with timed_step(log, "Raccolta URL"):
        # Step 1: Raccolta URL
        update_progress("Raccolta URL")
        run(["python","-m","collector.collect_tiktok_collection",...])
    
    with timed_step(log, "Download video"):
        # Step 2: Download video
        update_progress("Download video")
        fetch_missing_with_callbacks(...)
    
    with timed_step(log, "Estrazione frame e OCR"):
        # Step 3: Estrazione frame e OCR
        update_progress("Estrazione frame e OCR")
        run(["python","-m","analyzer.build_visual_index",...])
    
    with timed_step(log, "Trascrizione audio"):
        # Step 4: Trascrizione audio
        update_progress("Trascrizione audio")
        run(["python","-m","analyzer.transcribe_whisper",...])
    
    with timed_step(log, "Costruzione indice testuale"):
        # Step 5: Costruzione indice testuale
        update_progress("Costruzione indice testuale")
        run(["python","-m","analyzer.index_faiss",...])
```

---

### 3️⃣ `dash/app.py` (Dashboard Enhancement)

**Funzione Colorazione Durate:**
```python
def colorize_durations(line: str) -> str:
    # Pattern per durate step individuali
    m = re.search(r"durata: ([0-9.]+)s", line)
    if m:
        secs = float(m.group(1))
        if secs > 60:
            return f":red[{line}]"      # 🔴 Rosso per step > 60s
        elif secs > 30:
            return f":orange[{line}]"   # 🟠 Arancione per step > 30s
        else:
            return f":green[{line}]"    # 🟢 Verde per step < 30s
    
    # Pattern per tempo totale
    if "🏁 Ingest completato in" in line:
        total_secs = float(re.search(r"([0-9.]+)s", line).group(1))
        return f":blue-background[{line}]" if total_secs < 60 else f":red-background[{line}]"
```

**Applicazione Colorazione nei Log:**
```python
# Ottieni le righe del log e applica colorazione
log_content = _tail_file(log_file, int(n_lines), level_filter)
log_lines = log_content.splitlines()
colored_lines = [colorize_durations(line) for line in log_lines]

# Mostra il log colorato
st.code("\n".join(colored_lines), language="log")
```

**Box Statistiche Tempo Totale:**
```python
# Mostra statistiche se disponibili
if log_lines:
    last_line = log_lines[-1]
    if "🏁 Ingest completato in" in last_line:
        total_match = re.search(r"([0-9.]+)s totali", last_line)
        if total_match:
            total_secs = float(total_match.group(1))
            if total_secs < 60:
                st.success(f"✅ Ingest completato in {total_secs:.1f} secondi")
            else:
                st.warning(f"⚠️ Ingest completato in {total_secs:.1f} secondi (lento)")
```

**Pannello Statistiche Ingest:**
```python
# Statistiche Ingest
with st.expander("📊 Statistiche Ingest", expanded=False):
    # Analizza log per durate medie per step
    # Mostra metriche con colori basati su performance
    # Calcola tempo totale medio degli ultimi N ingest
```

---

## 🎨 Schema Colori Implementato

### Step Individuali:
- 🟢 **Verde**: < 30 secondi (veloce)
- 🟠 **Arancione**: 30-60 secondi (normale)  
- 🔴 **Rosso**: > 60 secondi (lento)

### Tempo Totale Ingest:
- 🔵 **Sfondo Blu**: < 60 secondi (veloce)
- 🔴 **Sfondo Rosso**: > 60 secondi (lento)

### Messaggi Speciali:
- 🔵 **Blu**: Step che iniziano (`⏳ Iniziando:`)
- 🟢 **Verde**: Step completati (`✅ Completato:`)
- 🔵 **Sfondo Blu**: Avvio ingest (`🚀 Ingest avviato`)

---

## 🧪 Test e Verifica

### Test Unitari (`tests/test_timing_system.py`):
- ✅ Test `timed_step` context manager
- ✅ Test `timed_ingest` context manager  
- ✅ Test timing annidato (ingest con step)
- ✅ Test `format_duration` helper
- ✅ Test timing con eccezioni

### Script Demo (`scripts/test_timing_demo.py`):
- ✅ Simulazione ingest normale (31s)
- ✅ Simulazione ingest veloce (5.5s)
- ✅ Simulazione ingest lento (108s)

### Comando Test:
```bash
# Test unitari
python3 -m pytest tests/test_timing_system.py -v

# Demo timing
python3 scripts/test_timing_demo.py
```

---

## 📊 Output Esempio

### Log Colorato:
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

### Statistiche Dashboard:
```
📈 Durate medie per step:
🟢 Raccolta URL: 2.5s (min: 0.5s, max: 5.2s)
🟢 Download video: 4.0s (min: 0.6s, max: 15.0s)  
🟠 Estrazione frame e OCR: 11.3s (min: 2.3s, max: 44.0s)
🟠 Trascrizione audio: 12.7s (min: 2.1s, max: 45.2s)
🟢 Costruzione indice testuale: 4.3s (min: 0.9s, max: 12.8s)

⏱️ Tempo totale medio:
🟡 34.8 secondi (normale)
Basato su 3 ingest completati
```

---

## 🔧 Configurazione Soglie

Le soglie di colore sono configurabili in `dash/app.py`:

```python
# Step individuali
if secs > 60:      # 🔴 Rosso
elif secs > 30:    # 🟠 Arancione  
else:              # 🟢 Verde

# Tempo totale
if total_secs < 60:    # 🔵 Sfondo blu
else:                  # 🔴 Sfondo rosso
```

---

## ✅ Benefici Implementati

1. **🎯 Visibilità Performance**: Ogni step mostra la sua durata
2. **🔍 Identificazione Colli di Bottiglia**: Step lenti evidenziati in rosso
3. **📊 Metriche Storiche**: Statistiche medie per step e tempo totale
4. **🎨 UX Migliorata**: Colorazione intuitiva per performance
5. **📈 Monitoraggio Trend**: Confronto tra ingest multipli
6. **🛠️ Debugging Facilitato**: Timing preciso per ottimizzazioni

---

## 🚀 Prossimi Passi

- [ ] **Alert Automatici**: Notifiche per step > soglia
- [ ] **Export Statistiche**: CSV con metriche timing
- [ ] **Grafi Performance**: Trend temporali per step
- [ ] **Ottimizzazioni Automatiche**: Suggerimenti basati su timing
- [ ] **Integrazione CI/CD**: Metriche timing nei test automatici
