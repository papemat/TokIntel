# 📌 Prompt unico per Cursor - Badge di Stato Video

**TASK:**  
Aggiornare TokIntel per visualizzare lo **stato video** anche accanto al titolo, oltre che nella tabella.

---

## 1️⃣ Badge accanto al titolo video

**Dashboard (`dash/app.py`)**  
- Individuare dove viene renderizzato il titolo di ogni video nella lista dei risultati (funzione `display_results` o simile).
- Aggiungere, subito accanto al titolo, un badge colorato in base al campo `status`:
  - 🟢 `ok`
  - 🟡 `timeout`
  - 🔵 `skipped`
- Il badge deve avere **tooltip** con testo esplicativo:
  - "Elaborazione completata con successo"
  - "Timeout durante la trascrizione"
  - "Video saltato (modalità solo audio o escluso)"

---

## 2️⃣ Snippet HTML/CSS già pronto

Usa questo snippet HTML inline con `unsafe_allow_html=True`:

```html
<span title="Elaborazione completata con successo" style="
    display: inline-block;
    background-color: #10b981;
    color: white;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 10px;
    margin-left: 8px;
    font-weight: bold;
    vertical-align: middle;
">OK</span>
```

```html
<span title="Timeout durante la trascrizione" style="
    display: inline-block;
    background-color: #f59e0b;
    color: white;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 10px;
    margin-left: 8px;
    font-weight: bold;
    vertical-align: middle;
">TIMEOUT</span>
```

```html
<span title="Video saltato (modalità solo audio o escluso)" style="
    display: inline-block;
    background-color: #3b82f6;
    color: white;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 10px;
    margin-left: 8px;
    font-weight: bold;
    vertical-align: middle;
">SKIPPED</span>
```

**Implementazione in Streamlit:**
```python
def get_status_badge(status):
    if status == "ok":
        return '<span title="Elaborazione completata con successo" style="display: inline-block; background-color: #10b981; color: white; font-size: 10px; padding: 2px 6px; border-radius: 10px; margin-left: 8px; font-weight: bold; vertical-align: middle;">OK</span>'
    elif status == "timeout":
        return '<span title="Timeout durante la trascrizione" style="display: inline-block; background-color: #f59e0b; color: white; font-size: 10px; padding: 2px 6px; border-radius: 10px; margin-left: 8px; font-weight: bold; vertical-align: middle;">TIMEOUT</span>'
    elif status == "skipped":
        return '<span title="Video saltato (modalità solo audio o escluso)" style="display: inline-block; background-color: #3b82f6; color: white; font-size: 10px; padding: 2px 6px; border-radius: 10px; margin-left: 8px; font-weight: bold; vertical-align: middle;">SKIPPED</span>'
    return ""

# Uso nel rendering del titolo:
title_with_badge = f"{video_title} {get_status_badge(status)}"
st.markdown(title_with_badge, unsafe_allow_html=True)
```

---

## 3️⃣ Compatibilità

- Assicurarsi che la funzione `load_database()` recuperi sempre il campo `status` dal DB.
- Il badge deve essere mostrato **anche se la colonna tabella è nascosta**.
- Nessun impatto sulle altre funzionalità.

---

## 4️⃣ Testing

- Usare il comando:
  ```bash
  make smoke-status-demo
  make dash
  ```

per generare dati finti con i tre stati e verificare il rendering dei badge.

- Testare anche con un ingest reale in modalità:
  ```bash
  python scripts/ingest_collection.py --audio_only
  ```
  per generare stato `skipped`.

---

**Obiettivo finale:**
Gli utenti devono poter vedere lo **stato di ogni video** a colpo d'occhio accanto al titolo, con badge colorato e tooltip, senza dover consultare la tabella.
