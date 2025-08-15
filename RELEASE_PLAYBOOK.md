# 📘 RELEASE_PLAYBOOK — TokIntel (v1.1.3+)

Playbook per rilasciare TokIntel in modo **rapido, sicuro e tracciabile**, con pipeline CI/CD (Docker Smoke + Release on Tag), troubleshooting e changelog integrato.

---

## 🧭 Scopo

* Rilasci prevedibili e auditabili
* Minimizzare errori manuali
* Allineamento Team/Repo/CI con una procedura unica

---

## ✅ Prerequisiti

* Permessi su `main` + creazione tag
* Repo aggiornata a `origin/main`
* (Opz.) Docker installato
* Make + Shell o PowerShell

---

## ⚡ TL;DR — Rilascio rapido

**Bash**

```bash
git fetch origin main && git checkout main && git pull --ff-only origin main || git pull --no-rebase origin main
./scripts/run_tokintel.sh --help >/dev/null && echo "✅ launcher OK"
make quickstart-check || true
make test || true
command -v docker >/dev/null && make docker-build && make docker-up && sleep 8 && make docker-down
make badges-glow-all || true
make docs-ready || true
SKIP_DOCS_STRICT=1 git push origin main || true
NEW="v1.1.4"; git tag "$NEW" -m "TokIntel $NEW" && git push origin "$NEW"
```

**PowerShell**

```powershell
git fetch origin main; git checkout main; git pull --ff-only origin main
./scripts/run_tokintel.sh --help *> $null
make quickstart-check; make test
make badges-glow-all; make docs-ready
$env:SKIP_DOCS_STRICT="1"; git push origin main
$NEW="v1.1.4"; git tag $NEW -m "TokIntel $NEW"; git push origin $NEW
```

---

## 📋 Procedura Essenziale

1. **Check preliminari** → sync, launcher, test, (opz.) Docker smoke
2. **Aggiorna indicatori** → badge + docs
3. **Push & Tag** → SemVer + messaggio chiaro
4. **Monitor CI** → Docker Smoke e Release on Tag verdi
5. **Verifica post‑release** → badge README, templates, docs, target Makefile

---



---

## 🧯 Troubleshooting rapido

* **Hook docs-strict** → `SKIP_DOCS_STRICT=1`
* **Branch divergente** → `--ff-only` → fallback `--no-rebase`
* **Tag esistente** → bump successivo
* **Docker assente** → delega a CI
* **CI fallita** → fix + nuovo tag patch

---

## 🔄 Hotfix & Rollback

* Hotfix: branch → fix → bump patch
* Rollback: revert commit o nuovo tag stabile

---

## 🔐 Sicurezza

* No token/secret in repo
* Usa secrets GitHub e variabili locali

---

## 🧩 Appendici

* Issue Templates: `.github/ISSUE_TEMPLATE`
* CI Workflows: `.github/workflows`
* Docs Mini: `docs/index.md`
* Badge/Monitor: `docs/status.json`, `docs/monitor_history.json`

---

## 🗒️ Mini-Changelog

| Versione | Data       | Novità principali                                                                                              |
| -------- | ---------- | -------------------------------------------------------------------------------------------------------------- |
| v1.1.4   | YYYY-MM-DD | - Aggiornamento badge glow <br> - Migliorato Docker smoke locale <br> - Changelog integrato nel playbook       |
| v1.1.3   | 2025-08-15 | - Finalizzazione enterprise-ready <br> - CI/CD Docker Smoke + Release on Tag <br> - Makefile e Docs completati |
