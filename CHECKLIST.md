# 🚀 TokIntel PR Checklist

## ✅ Pre-PR Checklist

### 🧪 Test
- [ ] `make test-fast` passa (4 test)
- [ ] `make dev-status` mostra stato corretto
- [ ] `make env-show` mostra variabili corrette

### 🔧 DX Setup
- [ ] `./scripts/dx_super_setup.sh` eseguito (idempotente)
- [ ] `.env.example` presente e aggiornato
- [ ] `scripts/dev_watch.sh` eseguibile

### 📝 Documentazione
- [ ] README aggiornato se necessario
- [ ] CHANGELOG aggiornato per breaking changes
- [ ] Documentazione API aggiornata se necessario

### 🔒 Sicurezza
- [ ] Nessun credenziale hardcoded
- [ ] Variabili sensibili in `.env` (non committate)
- [ ] Permessi file corretti

## 🚀 Post-PR Checklist

### ✅ CI/CD
- [ ] Fast-tests workflow passa
- [ ] Coverage non diminuita significativamente
- [ ] Linting passa

### 🧪 Test Manuali
- [ ] Dashboard avvia correttamente
- [ ] Funzionalità principali testate
- [ ] Errori gestiti gracefully

### 📊 Performance
- [ ] Nessun regressione performance
- [ ] Memory usage controllato
- [ ] Startup time accettabile

## 🎯 Quick Commands

```bash
# Pre-PR
./scripts/dx_super_setup.sh
make test-fast
make dev-status

# Post-PR
make dev
make dev-watch  # per sviluppo
```

---

**DX Setup: ✅ READY**
