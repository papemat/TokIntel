# 🔧 Variante Soft (Opzionale)

Se vuoi una versione "soft" che non blocca i commit in locale ma fallisce solo in CI:

## 🔩 Hook Pre-commit (Soft)

Aggiungi questo hook al tuo `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      # Hook strict (blocca commit)
      - id: docs-doctor-idempotent
        name: Docs Doctor Idempotency (Strict)
        entry: bash -c 'python3 .github/scripts/autofix_quickstart.py && python3 .github/scripts/autofix_quickstart.py && git diff --quiet'
        language: system
        pass_filenames: false
        stages: [commit]
      
      # Hook soft (solo warning)
      - id: docs-doctor-idempotent-soft
        name: Docs Doctor Idempotency (Soft)
        entry: bash -c 'python3 .github/scripts/autofix_quickstart.py && python3 .github/scripts/autofix_quickstart.py && git diff --quiet || echo "⚠️ Non idempotente (soft mode)"'
        language: system
        pass_filenames: false
        stages: [commit]
        always_run: false
```

## 🎯 Differenze

| Hook | Comportamento | Uso |
|------|---------------|-----|
| **Strict** | Blocca commit se non idempotente | CI, pre-commit rigoroso |
| **Soft** | Solo warning, non blocca | Sviluppo locale veloce |

## 🚀 Setup

```bash
# Installa pre-commit
pip install pre-commit

# Installa hooks
pre-commit install

# Test hook soft
pre-commit run docs-doctor-idempotent-soft
```

## 💡 Raccomandazione

- **Produzione**: Usa solo lo hook **strict**
- **Sviluppo**: Usa entrambi (strict per CI, soft per locale)
- **Velocità**: Usa solo lo hook **soft**

La variante soft è utile per sviluppo rapido senza bloccare i commit locali, mentre la strict garantisce qualità in CI.
