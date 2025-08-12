#!/usr/bin/env bash
set -euo pipefail

# === CONFIGURAZIONE: override via env ===
: "${GH_REPO:=TokIntel}"                          # nome repo remoto
: "${GH_OWNER:=your-username}"                    # owner (user/org)
: "${GITHUB_TOKEN:?Serve GITHUB_TOKEN exportato}" # token con permessi: repo + workflow
: "${PRIVATE:=true}"                              # true/false
: "${CREATE_PR:=1}"                               # 1 = crea PR fittizia per attivare i job PR
API="https://api.github.com"

# 0) Inizializza git se non esiste
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init
  git add .
  git commit -m "chore: init repo"
fi
git branch -M main || true

echo "[1/7] Creo/verifico repository $GH_OWNER/$GH_REPO..."
if curl -sH "Authorization: token $GITHUB_TOKEN" "$API/repos/$GH_OWNER/$GH_REPO" | grep -q '"full_name"'; then
  echo " - Repo già esistente."
else
  body='{"name":"'"$GH_REPO"'","private":'"$PRIVATE"',"description":"TokIntel: dashboards, CI, perf checks"}'
  if curl -sH "Authorization: token $GITHUB_TOKEN" "$API/user" | grep -q "\"login\":\"$GH_OWNER\""; then
    curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Content-Type: application/json" -d "$body" "$API/user/repos" >/dev/null
  else
    curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Content-Type: application/json" -d "$body" "$API/orgs/$GH_OWNER/repos" >/dev/null
  fi
  echo " - Repo creata."
fi

echo "[2/7] Push su main..."
git remote remove origin >/dev/null 2>&1 || true
git remote add origin "https://github.com/$GH_OWNER/$GH_REPO.git"
git push -u origin main

echo "[3/7] Creo label 'perf-regression' (idempotente)..."
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
  -d '{"name":"perf-regression","color":"FF0000","description":"Performance regression detected by CI"}' \
  "$API/repos/$GH_OWNER/$GH_REPO/labels" >/dev/null || true

echo "[4/7] Avvio workflow 'Perf Nightly'..."
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
  "$API/repos/$GH_OWNER/$GH_REPO/actions/workflows/perf-nightly.yml/dispatches" \
  -d '{"ref":"main"}' >/dev/null || true

if [ "$CREATE_PR" = "1" ]; then
  echo "[5/7] Creo branch feat/check e apro PR fittizia..."
  git checkout -B feat/check
  git commit --allow-empty -m "ci: trigger PR checks" || true
  git push -u origin feat/check
  curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
    -d '{"title":"CI check","head":"feat/check","base":"main","body":"Trigger PR checks (staging + performance matrix)."}' \
    "$API/repos/$GH_OWNER/$GH_REPO/pulls" >/dev/null || true
fi

echo "[6/7] Aggiorno badge nel README..."
sed -i'' -e "s|<ORG>/<REPO>|$GH_OWNER/$GH_REPO|g; s|your-username/TokIntel|$GH_OWNER/$GH_REPO|g" README.md || true
git add README.md && git commit -m "docs: update badges" || true
git push || true

echo "[7/7] Fatto! Workflow: https://github.com/$GH_OWNER/$GH_REPO/actions"
