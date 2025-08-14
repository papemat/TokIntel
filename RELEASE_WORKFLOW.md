# 🚀 TokIntel Release Workflow

Workflow automatizzato per il rilascio di TokIntel con Quickstart Bundle.

## 📋 Prerequisiti

- Git configurato con remote `origin`
- Branch locale sincronizzato con `main`/`master` remoto
- (Opzionale) GitHub CLI (`gh`) per release automatiche

## 🎯 Workflow Completo

### 1. Pre-flight Check (Sempre Prima!)

```bash
# Testa la configurazione
make release-test

# Oppure direttamente
./scripts/test_release_workflow.sh
```

### 2. Dry-run (Sicuro)

```bash
# Simula il release senza creare tag/release
make release-dry

# Oppure direttamente
./scripts/release_after_merge.sh v1.1.0 --dry-run
```

### 3. Release Reale

```bash
# Esegue il release completo
make release

# Oppure direttamente
./scripts/release_after_merge.sh v1.1.0
```

## 🔧 Cosa Fa lo Script

1. **Sync Sicuro**: Fast-forward pull da `origin/main` (o `master`)
2. **Verifica File**: Controlla che tutti i file Quickstart siano presenti
3. **Tag Intelligente**: 
   - Controlla se il tag esiste già su remoto
   - Crea tag annotato con messaggio dal changelog
   - Push del tag
4. **Release GitHub**: (se `gh` CLI disponibile)
   - Crea release automatica
   - Usa sezione changelog come body

## 🛡️ Protezioni di Sicurezza

- **Fast-forward only**: Non permette merge automatici
- **File validation**: Verifica presenza file Quickstart
- **Remote tag check**: Evita duplicati
- **Cleanup automatico**: Ripristina branch originale in caso di errore
- **Dry-run mode**: Simulazione sicura

## 📁 File Richiesti

Lo script verifica la presenza di:

```
scripts/run_tokintel.sh          # Launcher Unix
scripts/run_tokintel.bat         # Launcher Windows  
README_QUICKSTART.md             # Guida rapida
FAQ_TROUBLESHOOTING.md           # FAQ e troubleshooting
streamlit_config_example.toml    # Config esempio
CHANGELOG_QUICKSTART.md          # Changelog bundle
```

## 🎨 Personalizzazione

### Cambiare Versione

```bash
# Modifica la versione negli script
./scripts/release_after_merge.sh v1.2.0 --dry-run
./scripts/release_after_merge.sh v1.2.0
```

### Modificare Makefile

```makefile
# Aggiungi target personalizzati
release-v2:
	@./scripts/release_after_merge.sh v2.0.0

release-patch:
	@./scripts/release_after_merge.sh v1.1.1
```

## 🚨 Troubleshooting

### "Branch diverged"
```bash
# Sincronizza con remoto
git fetch origin
git reset --hard origin/main
```

### "Missing Quickstart files"
```bash
# Genera i file mancanti
make docs-generate
```

### "Tag already exists"
```bash
# Verifica tag esistenti
git tag -l | grep v1.1.0
git ls-remote --tags origin | grep v1.1.0
```

## 📊 Esempi di Output

### Dry-run Success
```
[info] Dry-run mode: no tag creation/push, no GitHub release.
[info] Fetching origin…
[info] Switching to 'main' and fast-forward pulling…
[info] Verifying Quickstart files…
[dry-run] Would create annotated tag 'v1.1.0' with message:
----------
Quickstart Bundle: cross-platform launchers + docs

## v1.1.0 - 2024-01-15
- Added cross-platform launchers
- Improved documentation
----------
[dry-run] Would push tag 'v1.1.0' to origin.
[done] Release workflow (dry-run) completed for v1.1.0.
```

### Real Release Success
```
[info] Fetching origin…
[info] Switching to 'main' and fast-forward pulling…
[info] Verifying Quickstart files…
[info] Creating annotated tag v1.1.0
[info] Pushing tag v1.1.0 to origin…
[info] Creating GitHub release via gh CLI (if not exists)…
[done] Release workflow completed for v1.1.0.
```

## 🔗 Integrazione CI/CD

Per integrare in GitHub Actions, aggiungi questo workflow:

```yaml
name: Release on Tag
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Create Release
        run: |
          gh release create ${{ github.ref_name }} \
            --title "${{ github.ref_name }} - Quickstart Bundle" \
            --body-file <(awk 'f;/^## /{if(f)exit} /^## v/{f=1}1' CHANGELOG_QUICKSTART.md)
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 📝 Note

- Lo script è idempotente: può essere eseguito più volte
- Il dry-run è sempre sicuro: non modifica nulla
- I file Quickstart vengono generati automaticamente con `make docs-generate`
- Il changelog viene estratto automaticamente per il messaggio del tag
