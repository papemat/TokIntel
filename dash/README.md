# 🎬 TokIntel Multimodal Dashboard

Dashboard Streamlit per ricerca multimodale in TokIntel con supporto per ricerca testuale e ricerca da immagine.

## 🚀 Avvio Rapido

```bash
# Avvia il dashboard
make dash

# Oppure direttamente
.venv/bin/streamlit run dash/app.py --server.port 8501 --server.address 0.0.0.0
```

Poi apri: [http://localhost:8501](http://localhost:8501)

## ✨ Funzionalità

### 🔍 Ricerca Testuale Multimodale
- **Query testuale** → ricerca in indici testuali e visivi
- **Slider Alpha** → regola peso tra ricerca testuale (0.0-1.0) e visiva
- **Filtri avanzati** → per tag e soglia score minimo
- **Risultati combinati** → score testuale + visivo + combinato

### 🖼️ Ricerca da Immagine
- **Upload immagine** (JPG/PNG) → embedding CLIP → ricerca visiva
- **Anteprima immagine** caricata
- **Risultati simili** con score di similarità
- **Thumbnail frame** dei video trovati

### ⚙️ Gestione Indici
- **Stato indici** → verifica presenza indici testuali e visivi
- **Ricostruzione indici** → pulsanti per ricostruire indici
- **Info database** → numero video e lista
- **Gestione errori** → feedback visivo per operazioni

## 🎯 Interfaccia

### Tab 1: Ricerca Testuale
```
┌─────────────────────────────────────────────────────────┐
│ Query: [yoga breathing]  Peso: [0.6]  Risultati: [10]  │
│ Filtri: [tag]  Soglia: [0.0]  [🔍 Cerca]              │
├─────────────────────────────────────────────────────────┤
│ 1. Yoga Friday New Class                                │
│    Score: 0.757 (Testo: 0.744, Visivo: 0.778)          │
│    [Frame] [URL] [Hook] [Tags] [OCR Text...]            │
└─────────────────────────────────────────────────────────┘
```

### Tab 2: Ricerca da Immagine
```
┌─────────────────────────────────────────────────────────┐
│ [Upload Image]  [Immagine caricata]                     │
│ Risultati: [10]  Soglia: [0.0]  [🔍 Cerca Simili]     │
├─────────────────────────────────────────────────────────┤
│ 1. Video Simile                                         │
│    Score: 0.824                                         │
│    [Frame] [URL] [Hook] [Tags] [OCR Text...]            │
└─────────────────────────────────────────────────────────┘
```

### Tab 3: Gestione Indici
```
┌─────────────────────────────────────────────────────────┐
│ ✅ Indice Testuale: Presente  [🔄 Ricostruisci]        │
│ ✅ Indice Visivo: Presente    [🔄 Ricostruisci]        │
│                                                         │
│ Video nel database: 3                                   │
│ [📋 Lista Video...]                                     │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Configurazione

Il dashboard usa automaticamente:
- **Config**: `config/settings.yaml`
- **Database**: `data/db.sqlite`
- **Indici**: `data/indexes/`
- **Frame**: `data/frames/`

## 📊 Risultati

Ogni risultato mostra:
- **Thumbnail frame** del video
- **Titolo e URL** del video
- **Score dettagliati**:
  - Score combinato (ricerca testuale)
  - Score testuale (OCR + testo)
  - Score visivo (CLIP)
- **Metadati**: Hook, Takeaways, Tags
- **OCR Text** (espandibile)

## 🎨 Stile

- **Design moderno** con CSS personalizzato
- **Layout responsive** con colonne
- **Icone emoji** per navigazione intuitiva
- **Colori coerenti** con tema TokIntel
- **UTF-8 safe** per caratteri speciali

## 🚨 Requisiti

- **Streamlit** >= 1.25
- **Indici FAISS** presenti
- **Database SQLite** con video
- **Frame estratti** per thumbnail

## 🔄 Workflow Tipico

1. **Setup**: `make setup` + `make multimodal-demo`
2. **Avvio**: `make dash`
3. **Ricerca testuale**: Inserisci query, regola alpha, cerca
4. **Ricerca immagine**: Carica foto, cerca simili
5. **Gestione**: Ricostruisci indici se necessario

## 🐛 Troubleshooting

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

### Errore "Frame mancanti"
```bash
# Estrai frame
make frames VIDEO="path/to/video.mp4" OUT="data/frames/"
```

---

**🎬 TokIntel Dashboard** - Interfaccia multimodale per analisi video intelligente
