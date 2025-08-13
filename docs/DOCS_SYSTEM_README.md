# 📚 Docs System – Final One Shot

Sistema universale per garantire **idempotenza** nella generazione/aggiornamento della documentazione.

## 🎯 Obiettivi
- ✅ **Idempotenza**: Due run consecutivi → nessuna modifica
- ✅ **Universale**: Funziona in qualsiasi repo
- ✅ **Smart**: Rileva generatori automaticamente
- ✅ **Soft**: Hook pre-commit non bloccante
- ✅ **Strict**: CI che fallisce su non-idempotenza

## 🔧 Componenti

### Script Strict
- `scripts/cursor_docs_strict.sh` → Verifica STRICT (CI)
- Rileva automaticamente: Makefile, Python, Sphinx, MkDocs
- Fallisce se il secondo run produce diff

### Hook Pre-commit
- `.git/hooks/pre-commit` → Verifica SOFT (locale)
- Avvisa ma **non blocca** i commit
- Perfetto per sviluppo veloce

### Target Makefile
- `docs-generate` → Generatore principale (fallback no-op)
- `docs-idem-soft` → Warning senza fallire
- `docs-idem-strict` → Hard fail su non-idempotenza

## 🚀 Uso Rapido

```bash
# Setup completo
bash setup_docs_system_final.sh

# Test locale (non blocca)
make docs-idem-soft

# Test strict (fallisce se non idempotente)
make docs-idem-strict

# Integrazione CI
# Copia lo step da CI_STRICT_STEP_YAML.md
```

## 🔍 Generatori Supportati

Il sistema rileva automaticamente:
1. **Makefile**: `make docs-generate`
2. **Python**: `scripts/update_docs_status.py`
3. **Sphinx**: `docs/conf.py` + `sphinx-build`
4. **MkDocs**: `mkdocs.yml` + `mkdocs build`
5. **Fallback**: No-op se nessun generatore trovato

## 📋 Workflow Consigliato

1. **Sviluppo**: Hook soft → sviluppo veloce
2. **Pre-PR**: `make docs-idem-strict` → verifica locale
3. **CI**: Step strict → garanzia qualità

## 🛠️ Personalizzazione

### Aggiungere un generatore custom
```make
docs-generate:
	@echo "Generando docs..."
	@python3 scripts/my_docs_generator.py
	@echo "✅ Docs generate"
```

### Hook pre-commit custom
```bash
# Modifica .git/hooks/pre-commit per aggiungere altri controlli
```

## 🎯 Integrazione CI

Usa lo step in `CI_STRICT_STEP_YAML.md` per integrare nel workflow GitHub Actions.
