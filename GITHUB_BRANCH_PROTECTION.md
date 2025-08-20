# 🛡️ PR Gate - Configurazione Suggerita

## 📍 **GitHub → Settings → Branch protection (main)**

### ✅ **Configurazioni obbligatorie**

1. **Require PR reviews**
   - ✅ Require a pull request before merging
   - ✅ Require review from code owners
   - ✅ Dismiss stale approvals on new commits

2. **Require status checks**
   - ✅ Require status checks to pass before merging
   - ✅ **Fast Tests** (obbligatorio)
   - ✅ **doctor** (opzionale, per diagnostica)

3. **Restrictions**
   - ✅ Restrict pushes that create files larger than 100 MB
   - ✅ Require linear history

### 🔧 **Configurazione Dependabot**

#### Etichette suggerite
- `deps` - Aggiornamenti dipendenze
- `safe-update` - Aggiornamenti sicuri (patch/minor)
- `breaking-change` - Aggiornamenti major

#### Auto-merge soft (opzionale)
```yaml
# .github/workflows/auto-merge.yml (se vuoi)
name: Auto-merge safe updates
on:
  pull_request:
    types: [labeled]

jobs:
  auto-merge:
    if: contains(github.event.pull_request.labels.*.name, 'safe-update')
    runs-on: ubuntu-latest
    steps:
      - name: Auto-merge
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.pulls.merge({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              merge_method: 'squash'
            })
```

### 📊 **Monitoraggio**

- **Badge CI**: Verifica che "Fast Tests" sia sempre verde
- **PR template**: Usa il template automatico per checklist
- **Code owners**: Review automatiche per `@papemat`

### 🚨 **In caso di problemi**

1. **Test rossi**: Blocca merge automaticamente
2. **Review mancanti**: Richiedi review da code owners
3. **Conflict**: Risolvi prima del merge
