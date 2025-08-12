# 🎬 TokIntel Multimodal Dashboard - Istruzioni Complete

## 🚀 Avvio Rapido

### 1. Setup Iniziale (se non fatto)
```bash
# Crea virtual environment e installa dipendenze
make setup

# Crea demo multimodale con indici
make multimodal-demo

# Crea immagini demo per test
make demo-images
```

### 2. Test Dashboard
```bash
# Verifica che tutto sia pronto
make test-dash
```

### 3. Avvia Dashboard
```bash
# Avvia Streamlit
make dash
```

### 4. Apri Browser
- **URL**: http://localhost:8501
- **Porta**: 8501
- **Host**: 0.0.0.0 (accesso esterno)

## 🎯 Come Usare il Dashboard

### Tab 1: 🔍 Ricerca Testuale

#### Ricerca Base
1. **Inserisci query** nel campo "Query di ricerca"
   - Esempi: "yoga breathing", "marketing conversion", "pilates core"
2. **Regola il peso** con lo slider "Peso Testo vs Visivo"
   - 0.0 = solo ricerca visiva
   - 1.0 = solo ricerca testuale
   - 0.6 = bilanciato (default)
3. **Imposta numero risultati** (1-50)
4. **Clicca "🔍 Cerca"**

#### Filtri Avanzati
- **Tag Filter**: Seleziona tag specifici per filtrare risultati
- **Score Threshold**: Imposta soglia minima per i risultati

#### Risultati
Ogni risultato mostra:
- **Thumbnail frame** del video
- **Titolo e URL** del video
- **Score dettagliati**:
  - Score Combinato (peso bilanciato)
  - Score Testuale (OCR + testo)
  - Score Visivo (CLIP)
- **Metadati**: Hook, Takeaways, Tags
- **OCR Text** (espandibile)

### Tab 2: 🖼️ Ricerca da Immagine

#### Upload Immagine
1. **Carica immagine** (JPG/PNG) con il file uploader
2. **Visualizza anteprima** dell'immagine caricata
3. **Imposta parametri**:
   - Numero risultati (1-50)
   - Soglia score minimo
4. **Clicca "🔍 Cerca Simili"**

#### Immagini Demo Disponibili
- `demo_images/yoga_breathing.jpg` - Testo yoga su sfondo verde
- `demo_images/pilates_core.jpg` - Testo pilates su sfondo coral
- `demo_images/marketing_conversion.jpg` - Testo marketing su sfondo giallo

#### Risultati
- **Score di similarità** per ogni video
- **Thumbnail frame** dei video simili
- **Metadati completi** come nella ricerca testuale

### Tab 3: ⚙️ Gestione Indici

#### Stato Indici
- **Indice Testuale**: ✅ Presente / ❌ Mancante
- **Indice Visivo**: ✅ Presente / ❌ Mancante

#### Ricostruzione Indici
- **"🔄 Ricostruisci Indice Testuale"**: Ricostruisce indice FAISS testuale
- **"🔄 Ricostruisci Indice Visivo"**: Ricostruisce indice FAISS visivo

#### Info Database
- **Numero video** nel database
- **Lista video** (espandibile, mostra primi 10)

## 🎬 Esempi di Ricerca

### Ricerca Testuale
```
Query: "yoga breathing"
Peso: 0.6 (bilanciato)
Risultati: 10

Risultato atteso:
1. Yoga Friday New Class
   Score: 0.757 (Testo: 0.744, Visivo: 0.778)
   Frame: [thumbnail]
   URL: https://tiktok.com/@yoga_master/video/123
```

### Ricerca da Immagine
```
Immagine: yoga_breathing.jpg
Risultati: 5
Soglia: 0.5

Risultato atteso:
1. Yoga Friday New Class
   Score: 0.824
   Frame: [thumbnail]
   URL: https://tiktok.com/@yoga_master/video/123
```

## 🔧 Troubleshooting

### Errore "Indici mancanti"
```bash
# Ricostruisci indici
make index-cpu
make visual-index
```

### Errore "Database vuoto"
```bash
# Crea demo
make multimodal-demo
```

### Errore "Dashboard non si avvia"
```bash
# Verifica porta
lsof -i :8501

# Cambia porta se necessario
streamlit run dash/app.py --server.port 8502
```

### Errore "Module not found"
```bash
# Verifica virtual environment
source .venv/bin/activate
pip install -r requirements.txt
```

## 📊 Interpretazione Risultati

### Score Combinato
- **Range**: 0.0 - 1.0
- **Più alto = più rilevante**
- **Formula**: `alpha * score_testuale + (1-alpha) * score_visivo`

### Score Testuale
- **Basato su**: OCR text + video metadata
- **Range**: 0.0 - 1.0
- **Più alto = più simile semanticamente**

### Score Visivo
- **Basato su**: CLIP embeddings
- **Range**: 0.0 - 1.0
- **Più alto = più simile visivamente**

## 🎨 Personalizzazione

### Modifica Configurazione
- **File**: `config/settings.yaml`
- **Parametri**: Modelli, percorsi, soglie

### Modifica Stile
- **File**: `dash/app.py`
- **Sezione**: CSS personalizzato

### Aggiungere Video
```bash
# Download video
make download URL="https://tiktok.com/@user/video/123"

# Pipeline completa
make pipeline URL="https://tiktok.com/@user/video/123"
```

## 🔄 Workflow Tipico

### 1. Setup Iniziale
```bash
make setup
make multimodal-demo
make demo-images
```

### 2. Test Funzionalità
```bash
make test-dash
make dash
# Apri http://localhost:8501
```

### 3. Ricerca Testuale
- Query: "yoga breathing"
- Peso: 0.6
- Verifica risultati

### 4. Ricerca da Immagine
- Carica: `demo_images/yoga_breathing.jpg`
- Confronta con risultati testuali

### 5. Gestione Indici
- Verifica stato indici
- Ricostruisci se necessario

## 🎉 Risultati Attesi

### Ricerca Testuale "yoga breathing"
- **Video yoga** con score alto (>0.7)
- **Score testuale** alto per contenuto OCR
- **Score visivo** alto per frame simili

### Ricerca da Immagine yoga_breathing.jpg
- **Video simili** per contenuto visivo
- **Score visivo** alto (>0.8)
- **Correlazione** con risultati testuali

### Performance
- **Ricerca**: <200ms per query
- **Upload**: <500ms per immagine
- **Interfaccia**: Aggiornamento istantaneo

---

**🎬 TokIntel Dashboard** - Interfaccia multimodale completa e funzionante! 🚀

Per supporto: controlla `DASHBOARD_SUMMARY.md` per dettagli tecnici.
