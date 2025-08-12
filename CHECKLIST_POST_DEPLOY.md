# ✅ Checklist Post-Deploy — TokIntel

## 1) Repo & Branch
- [ ] Repo GitHub creato
- [ ] `main` impostato come default
- [ ] Primo push completato

## 2) GitHub Actions
- [ ] Workflow `perf-nightly.yml` visibile con un run avviato
- [ ] Workflow `prod-check.yml` visibile
- [ ] PR di test aperta (se `CREATE_PR=1`) e job PR partiti

## 3) Badge & README
- [ ] Badge CI/CD aggiornati nel README
- [ ] I badge puntano ai run corretti

## 4) Label & Issues
- [ ] Etichetta `perf-regression` presente
- [ ] (Opz.) Template Issue/PR attivi

## 5) Secrets / Vars (se richiesti dai workflow)
- [ ] `DASHBOARD_URL` (es. http://localhost:8503)
- [ ] `PERF_THRESHOLD` (ms)
- [ ] `ENV=prod`

## 6) Branch Protection (consigliato)
- [ ] Protezione su `main` → *Require status checks to pass before merging*
- [ ] Selezionati i check dei workflow
- [ ] *Require a pull request before merging*
- [ ] (Opz.) *Require linear history*, *Dismiss stale approvals*

## 7) Schedule
- [ ] `perf-nightly.yml` ha cron attivo (es. 02:00 UTC)
- [ ] Run schedulati visibili nella tab Actions

## 8) Smoke Test Locale
- [ ] `make test-dashboard` → "Dashboard raggiungibile ✅"

---

### Comandi utili (facoltativi)
```bash
# Verifica ultimi run (se hai gh CLI)
gh run list --limit 10

# Imposta secrets/vars di esempio
gh secret set DASHBOARD_URL --body "http://localhost:8503"
gh secret set PERF_THRESHOLD --body "250"
gh variable set ENV --body "prod"
```

### Note

* Se Actions non partono, controlla **Settings → Actions → General** (Allow all actions).
* Se branch protection blocca il primo push, rilassa temporaneamente e riattiva dopo.
