# 🆘 FAQ & Troubleshooting - TokIntel

## ❓ Problemi Comuni

### Python non trovato
```bash
# Verifica installazione
python --version
python3 --version
```

### Dipendenze mancanti
```bash
# Reinstalla ambiente
rm -rf .venv
make setup
```

### Porta occupata
```bash
# Cambia porta
TI_PORT=8502 make run-ui
```

### Database corrotto
```bash
# Ricrea database
rm data/tokintel.db
make ensure-db
```

## 🆘 Supporto

- **Issues**: [GitHub Issues](https://github.com/papemat/TokIntel/issues)
- **Discussions**: [Community Help](https://github.com/papemat/TokIntel/discussions)

---

**💡 Suggerimento**: Prima di aprire un issue, cerca nella documentazione esistente.
