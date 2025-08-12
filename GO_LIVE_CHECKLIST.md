# 🚀 TokIntel Go-Live Checklist

## ✅ Checklist Automatica (1 min)

Esegui il comando automatico per verificare tutto:

```bash
make go-live
```

Questo comando esegue automaticamente:
- ✅ Aggiunta indici database per performance
- ✅ Test sistema badge di stato
- ✅ Test completi con pytest
- ✅ Verifica setup generale

## 📋 Checklist Manuale (2 min)

### 1. Verifica Cache
```bash
make test-cache
```
Poi apri dashboard e verifica che il titolo sia aggiornato con `[CACHE-TEST]`.

### 2. Test Export
```bash
make test-export
```
Verifica che il file CSV sia creato con timestamp.

### 3. Test UI Fail-Soft
```bash
make test-fail-soft
```
Simula colonne mancanti e verifica che la dashboard non crashi.

### 4. Pannello Diagnostica
Apri dashboard e controlla il pannello "ℹ️ Diagnostics":
- ✅ Versione app
- ✅ Dimensione DB
- ✅ Cache abilitata/disabilitata
- ✅ Bottone "Forza refresh cache"

## 🔧 Feature Flags Disponibili

### Disabilitare Cache (Debug)
```bash
FF_DISABLE_CACHE=1 streamlit run dash/app.py
```

### Cache con TTL
```bash
CACHE_TTL_SECONDS=300 streamlit run dash/app.py  # 5 minuti
```

### Versione App
```bash
TOKINTEL_VERSION=1.0.0 streamlit run dash/app.py
```

## 🚀 Ottimizzazioni SQLite Attive

Il dashboard applica automaticamente:
- **WAL mode**: Migliore concorrenza (letture non bloccano scritture)
- **NORMAL sync**: Bilanciamento sicurezza/performance
- **Memory temp store**: Storage temporaneo in memoria
- **Memory mapping**: Per database grandi (se supportato)

## 📊 Comandi Utili

```bash
# Test rapidi
make test-status          # Test badge di stato
make test-cache           # Test cache
make test-export          # Test export

# Performance
make add-indexes          # Ottimizza DB
make verify               # Verifica setup

# Debug
FF_DISABLE_CACHE=1 make dash  # Dashboard senza cache
```

## 🎯 Stato "Prod-Ready"

Con questo hardening TokIntel è **prod-ready** con:

✅ **Robustezza**: UI fail-soft, gestione errori graceful  
✅ **Performance**: Cache intelligente, indici DB, ottimizzazioni SQLite  
✅ **Debugging**: Pannello diagnostica, feature flags  
✅ **Monitoring**: Badge di stato, metriche real-time  
✅ **Export**: CSV/JSON con timestamp  
✅ **Testing**: Suite completa automatica  

## 🔍 Troubleshooting

### Cache non si aggiorna
1. Usa bottone "Forza refresh cache" nel pannello diagnostica
2. Oppure: `FF_DISABLE_CACHE=1 make dash`

### Dashboard lenta
1. Verifica indici: `make add-indexes`
2. Controlla dimensione DB nel pannello diagnostica
3. Usa `CACHE_TTL_SECONDS=0` per cache infinita

### Errori UI
1. Verifica schema DB: `make migrate-schema`
2. Controlla colonne mancanti nel pannello diagnostica
3. UI dovrebbe fallire graceful con messaggi informativi

---

**🎉 TokIntel è pronto per la produzione!**
