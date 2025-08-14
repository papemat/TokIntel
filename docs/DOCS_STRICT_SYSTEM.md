# 🚀 Docs Strict System

Sistema di validazione e autofix per la documentazione con **idempotenza strict** - fallisce se il secondo run di autofix produce diff.

## 🎯 Componenti

### 1. **Cursore Strict** (`cursor_strict.sh`)
Script completo che:
- Crea branch `chore/docs-doctor-anti-dup`
- Esegue autofix + linkcheck + docs-doctor
- **Verifica idempotenza strict** (secondo run non deve produrre diff)
- Genera glow badges
- Committa e crea PR automaticamente

```bash
bash cursor_strict.sh
```

### 2. **Pre-commit Hook** (`.pre-commit-config.yaml`)
Hook che blocca il commit se l'autofix non è idempotente:

```yaml
- id: docs-doctor-idempotent
  name: Docs Doctor Idempotency
  entry: bash -c 'python3 .github/scripts/autofix_quickstart.py && python3 .github/scripts/autofix_quickstart.py && git diff --quiet'
  language: system
  pass_filenames: false
  stages: [commit]
```

### 3. **Makefile Targets**

#### `docs-idem-strict`
Verifica idempotenza strict:
```bash
make docs-idem-strict
```

#### `docs-ci-all`
Pipeline completa: autofix + linkcheck + lint + badges + idempotenza strict:
```bash
make docs-ci-all
```

#### `docs-doctor` (esistente)
Docs Doctor completo (validate + autofix + links):
```bash
make docs-doctor
```

## 🧪 Smoke Test

Test rapido del sistema:
```bash
scripts/test_docs_strict.sh
```

## 🔄 Workflow

1. **Pre-commit**: Hook verifica idempotenza
2. **CI**: `docs-ci-all` esegue pipeline completa
3. **Manual**: `cursor_strict.sh` per PR automatico

## ❌ Fallimenti

Il sistema fallisce se:
- Il secondo run di `autofix_quickstart.py` produce diff
- Linkcheck rileva link rotti
- Markdownlint rileva errori
- Duplicati nel Quick Start

## 🛠️ Setup

```bash
# Installa pre-commit hooks
pip install pre-commit
pre-commit install

# Test locale
make docs-ci-all
```

## 📋 Checklist

- [ ] Pre-commit hooks installati
- [ ] `cursor_strict.sh` eseguibile
- [ ] `scripts/test_docs_strict.sh` eseguibile
- [ ] Target Makefile funzionanti
- [ ] Smoke test passa
- [ ] Idempotenza verificata
