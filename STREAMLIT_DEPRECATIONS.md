# Streamlit Deprecations - Note per macOS

## ⚠️ Warning Configurazioni Deprecate

Se durante l'avvio di TokIntel vedi questi warning:

```
"runner.installTracer" is not a valid config option
"runner.fixMatplotlib" is not a valid config option
```

### 🔧 Soluzione

Apri il file di configurazione Streamlit sul tuo Mac:

```bash
# Apri con editor di default
open ~/.streamlit/config.toml

# Oppure con nano
nano ~/.streamlit/config.toml
```

**Rimuovi** queste righe se presenti:

```toml
runner.installTracer = ...
runner.fixMatplotlib = ...
```

### 📝 Note

- Queste configurazioni sono state deprecate nelle versioni recenti di Streamlit
- La rimozione non influisce sul funzionamento dell'applicazione
- Il warning è solo informativo e non blocca l'avvio

### 🚀 Quick Fix

Se vuoi rimuovere rapidamente tutte le configurazioni deprecate:

```bash
# Backup della configurazione attuale
cp ~/.streamlit/config.toml ~/.streamlit/config.toml.backup

# Rimuovi le righe deprecate
sed -i '' '/runner\.installTracer/d; /runner\.fixMatplotlib/d' ~/.streamlit/config.toml
```

---

**TokIntel funziona correttamente anche con questi warning presenti.**
