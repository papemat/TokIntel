#!/usr/bin/env bash
set -euo pipefail
PATHS=()
[ -d "docs/_build" ] && PATHS+=("docs/_build")
[ -d "site" ] && PATHS+=("site")
[ ${#PATHS[@]} -eq 0 ] && echo "ℹ️  Nessun output docs trovato (scan no‑op)" && exit 0
echo "🔎 Scan output: ${PATHS[*]}"

PAT_DATE1='[0-9]{4}[-/][0-9]{2}[-/][0-9]{2}'
PAT_DATE2='[0-9]{2}[-/][0-9]{2}[-/][0-9]{4}'
PAT_TIME='[0-9]{2}:[0-9]{2}:[0-9]{2}'
PAT_UUID='[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}'
PAT_HASH='[a-f0-9]{7,40}'
EXCLUDES='-not -name "*.map" -not -name "*.png" -not -name "*.jpg" -not -name "*.jpeg" -not -name "*.gif" -not -name "*.pdf" -not -name "*.ico" -not -name "*.woff*" -not -name "*.ttf"'

FOUND=0
for p in "${PATHS[@]}"; do
  while IFS= read -r -d '' f; do
    if LC_ALL=C grep -Eaq "${PAT_DATE1}|${PAT_DATE2}|${PAT_TIME}|${PAT_UUID}" "$f"; then
      echo "⚠️  Pattern instabile in: $f"
      LC_ALL=C grep -EanH "${PAT_DATE1}|${PAT_DATE2}|${PAT_TIME}|${PAT_UUID}" "$f" | head -n 5 || true
      FOUND=1
    else
      case "$f" in
        *.html|*.htm|*.txt|*.md|*.json|*.yml|*.yaml)
          if LC_ALL=C grep -Eaq "${PAT_HASH}" "$f"; then
            CNT=$(LC_ALL=C grep -Eao "${PAT_HASH}" "$f" | sort -u | wc -l | tr -d ' ')
            if [ "${CNT:-0}" -ge 10 ]; then
              echo "⚠️  Possibili hash non deterministici in: $f (unique ~${CNT})"
              FOUND=1
            fi
          fi
        ;;
      esac
    fi
  done < <(eval find "$p" -type f $EXCLUDES -print0)
done

[ $FOUND -ne 0 ] && { echo "❌ Scan: pattern non deterministici trovati."; exit 2; }
echo "✅ Scan: nessun pattern problematico rilevato."
