# 🚀 GitHub Setup Instructions - TokIntel

## ✅ Completato Localmente

- ✅ Repository Git inizializzato
- ✅ Commit iniziale fatto
- ✅ Badge README aggiornati (placeholder)
- ✅ Dashboard performance testata

## 🔄 Prossimi Passi GitHub

### 1. Crea Repository su GitHub

**Opzione A: Con GitHub CLI**
```bash
gh repo create TokIntel --source=. --private --push
```

**Opzione B: Manuale**
1. Vai su [GitHub.com](https://github.com)
2. Crea nuovo repository "TokIntel"
3. **NON** inizializzare con README (già presente)
4. Esegui:
```bash
git remote add origin https://github.com/<TUO_USERNAME>/TokIntel.git
git push -u origin main
```

### 2. Aggiorna Badge nel README

Sostituisci `<ORG>/<REPO>` con i tuoi valori reali:

```bash
# Esempio per username "matteopapetti"
sed -i '' 's/<ORG>\/<REPO>/matteopapetti\/TokIntel/g' README.md
git add README.md
git commit -m "docs: update badge URLs with real GitHub repo"
git push
```

### 3. Abilita GitHub Actions

1. GitHub → **Settings → Actions → General**
2. ✅ **Allow all actions and reusable workflows**
3. ✅ **Allow GitHub Actions to create and approve pull requests**

### 4. (Opzionale) Configura Slack Notifications

1. GitHub → **Settings → Secrets → Actions**
2. Aggiungi `SLACK_WEBHOOK_URL` se vuoi alert

### 5. Crea Label per Performance

```bash
gh label create perf-regression --description "Performance regression detected by CI" --color FF0000
```

## 🧪 Test Workflow

### Prod Check (automatico)
- Si avvia automaticamente su push a `main`
- Verifica: GitHub → Actions → "Prod Check"

### Perf Nightly (manuale)
```bash
gh workflow run "Perf Nightly"
```
- Verifica: GitHub → Actions → "Perf Nightly"

## 📊 Dashboard Performance

### Locale
```bash
make perf-dash
# oppure
streamlit run dash/perf_dashboard.py
```

### Pubblica (opzionale)
1. Crea account su [Streamlit Cloud](https://streamlit.io/cloud)
2. Connetti il repo GitHub
3. Deploy automatico su ogni push

## 🔍 Verifica Setup

### Badge Status
- [ ] Prod Check CI: verde
- [ ] Perf Nightly: verde
- [ ] Go-Live Docs: link funzionante
- [ ] Enterprise Setup: link funzionante

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
sed -i '' 's/<ORG>\/<REPO>/TUO_USERNAME\/TokIntel/g' README.md

# Commit e push
git add README.md && git commit -m "docs: real badge URLs" && git push

# Test workflow manuale
gh workflow run "Perf Nightly"

# Dashboard locale
make perf-dash
```

## 📋 Checklist Finale

- [ ] Repository GitHub creato
- [ ] Badge README aggiornati
- [ ] GitHub Actions abilitati
- [ ] Workflow testati
- [ ] Dashboard funzionante
- [ ] Label perf-regression creata

---

**Status:** 🟡 In attesa di setup GitHub
**Prossimo:** Crea repo su GitHub e aggiorna badge
