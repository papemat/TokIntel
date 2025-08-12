# 🚀 GitHub Setup Manuale - TokIntel

## 📋 Setup Repository GitHub

### 1. Crea Repository su GitHub.com

1. Vai su [GitHub.com](https://github.com)
2. Clicca **"New repository"**
3. **Repository name:** `TokIntel`
4. **Description:** `Analisi Multimodale di Video - Performance Monitoring`
5. **Visibility:** Private (o Public se preferisci)
6. **❌ NON** inizializzare con README (già presente)
7. Clicca **"Create repository"**

### 2. Collega Repository Locale

```bash
# Dalla root del progetto TokIntel
git remote add origin https://github.com/TUO_USERNAME/TokIntel.git
git push -u origin main
```

### 3. Abilita GitHub Actions

1. GitHub → **Settings → Actions → General**
2. ✅ **Allow all actions and reusable workflows**
3. ✅ **Allow GitHub Actions to create and approve pull requests**
4. Clicca **"Save"**

### 4. (Opzionale) Configura Slack Notifications

1. GitHub → **Settings → Secrets → Actions**
2. Clicca **"New repository secret"**
3. **Name:** `SLACK_WEBHOOK_URL`
4. **Value:** `https://hooks.slack.com/services/TUO_WEBHOOK_URL`
5. Clicca **"Add secret"**

## 🏷️ Crea Label Performance

### Con GitHub CLI (se installato)
```bash
gh label create perf-regression --description "Performance regression detected by CI" --color FF0000
```

### Manuale
1. GitHub → **Issues → Labels**
2. Clicca **"New label"**
3. **Label name:** `perf-regression`
4. **Description:** `Performance regression detected by CI`
5. **Color:** `#FF0000` (rosso)
6. Clicca **"Create label"**

## 🧪 Test Workflow

### Prod Check (Automatico)
- Si avvia automaticamente dopo il push a `main`
- Verifica: GitHub → Actions → "Prod Check"

### Perf Nightly (Manuale)
1. GitHub → **Actions → Workflows**
2. Clicca **"Perf Nightly"**
3. Clicca **"Run workflow"**
4. Seleziona branch `main`
5. Clicca **"Run workflow"**

## 📊 Aggiorna Badge README

Dopo aver creato il repo, sostituisci `TUO_USERNAME` con il tuo username:

```bash
# Aggiorna badge con URL reali
sed -i '' 's/your-username/TUO_USERNAME/g' README.md

# Commit e push
git add README.md
git commit -m "docs: update badge URLs with real GitHub repo"
git push
```

## 🔍 Verifica Setup

### Badge Status
- [ ] Prod Check CI: verde
- [ ] Perf Nightly: blu
- [ ] Go-Live Docs: link funzionante
- [ ] Enterprise Setup: link funzionante
- [ ] Performance Dashboard: link locale funzionante

### Workflow Status
- [ ] Prod Check: completato con successo
- [ ] Perf Nightly: completato con successo
- [ ] Artifacts: scaricabili
- [ ] CSV storico: committato

### Dashboard
- [ ] Avvia localmente: `make perf-dash`
- [ ] Visualizza trend: grafici funzionanti
- [ ] Dati demo: visibili

## 🎯 Comandi Rapidi Post-Setup

```bash
# Aggiorna badge con repo reale
sed -i '' 's/your-username/TUO_USERNAME/g' README.md

# Commit e push
git add README.md && git commit -m "docs: real badge URLs" && git push

# Test workflow manuale (se hai gh CLI)
gh workflow run "Perf Nightly"

# Dashboard locale
make perf-dash
```

## 📋 Checklist Finale

- [ ] Repository GitHub creato
- [ ] Repository locale collegato
- [ ] GitHub Actions abilitati
- [ ] Badge README aggiornati
- [ ] Workflow testati
- [ ] Dashboard funzionante
- [ ] Label perf-regression creata
- [ ] (Opzionale) Slack webhook configurato

## 🔄 Workflow Automatici

### Prod Check
- **Trigger:** Push su `main`
- **Actions:** Test, export, report
- **Output:** Artifacts scaricabili

### Perf Nightly
- **Trigger:** Cron (02:00 UTC) + manuale
- **Actions:** Benchmark, aggregazione CSV
- **Output:** CSV storico committato

---

**Status:** 🟡 In attesa di setup GitHub manuale
**Prossimo:** Crea repo su GitHub.com e collega remote
