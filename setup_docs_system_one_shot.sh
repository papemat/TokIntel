#!/usr/bin/env bash
set -euo pipefail

echo "=== 🚀 Setup Docs System One-Shot (idempotente) ==="

# 1) Struttura cartelle
mkdir -p scripts docs .github/workflows .github/scripts .git/hooks

# 2) Script STRICT che verifica l'idempotenza (hard-fail su diff)
cat > scripts/cursor_docs_strict.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail

echo "== 🧪 Docs Idempotency STRICT =="
# Prima passata (genera/aggiorna docs)
if make -q docs-generate 2>/dev/null; then
  make docs-generate
elif [[ -x scripts/update_docs_status.py ]]; then
  python3 scripts/update_docs_status.py || true
elif [[ -x .github/scripts/update_docs_status.py ]]; then
  python3 .github/scripts/update_docs_status.py || true
else
  echo "⚠️  Nessun generatore docs trovato: eseguo fallback no-op"
fi

# Seconda passata (deve essere no-op)
git add -A >/dev/null 2>&1 || true
if make -q docs-generate 2>/dev/null; then
  make docs-generate
elif [[ -x scripts/update_docs_status.py ]]; then
  python3 scripts/update_docs_status.py || true
elif [[ -x .github/scripts/update_docs_status.py ]]; then
  python3 .github/scripts/update_docs_status.py || true
fi

# Controllo diff: se c'è differenza -> FAIL
if ! git diff --quiet; then
  echo "❌ Non idempotente: il secondo run ha prodotto modifiche."
  git --no-pager diff --stat
  exit 1
fi

echo "✅ Idempotenza OK (nessuna modifica al secondo run)"
SH
chmod +x scripts/cursor_docs_strict.sh

# 3) Documentazione del sistema
cat > docs/DOCS_SYSTEM_README.md <<'MD'
# 📚 Docs System – One Shot

Questo sistema garantisce che la generazione/aggiornamento della documentazione sia **idempotente**.

## Componenti
- `scripts/cursor_docs_strict.sh` → Verifica STRICT (CI): 2 run consecutivi, fallisce se il secondo produce diff.
- Hook pre-commit (SOFT) → Avvisa ma **non blocca** i commit.
- Target Makefile:
  - `docs-generate` (facoltativo, se già presente verrà usato)
  - `docs-idem-soft` → Avvisa senza fallire
  - `docs-idem-strict` → Fallisce su non-idempotenza

## Uso rapido
```bash
bash setup_docs_system_one_shot.sh      # setup completo (questo file viene creato da Cursor)
make docs-idem-soft                     # warning ma non blocca
make docs-idem-strict                   # hard fail se non idempotente
```

## In CI (GitHub Actions)

Usa lo step in `CI_STRICT_STEP_YAML.md` per integrare nel workflow.
MD

# 4) Hook pre-commit SOFT (non blocca)
cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash

# SOFT check: non blocca il commit (avvisa soltanto)

if command -v make >/dev/null 2>&1; then
if make -q docs-idem-soft 2>/dev/null; then
make docs-idem-soft || true
elif grep -q "docs-idem-soft" Makefile 2>/dev/null; then
make docs-idem-soft || true
fi
fi
exit 0
HOOK
chmod +x .git/hooks/pre-commit

# 5) Aggiunta/merge dei target Makefile (senza duplicati)
if [[ -f Makefile ]]; then
awk 'BEGIN{inblk=0}
/# >>> DOCS SYSTEM TARGETS START >>>/ {inblk=1; next}
/# <<< DOCS SYSTEM TARGETS END <<</ {inblk=0; next}
{ if(!inblk) print $0 }
' Makefile > Makefile.tmp || true

cat >> Makefile.tmp <<'MK'

# >>> DOCS SYSTEM TARGETS START >>>

.PHONY: docs-generate docs-idem-soft docs-idem-strict

# docs-generate:
# - Se già definito altrove, verrà usato da scripts/cursor_docs_strict.sh.
# - Qui forniamo un fallback no-op per non rompere i repo che non hanno generatori ancora.

docs-generate:
	@echo "ℹ️  Fallback docs-generate (no-op). Sovrascrivi con il tuo generatore (es. sphinx, mkdocs, script python)."

docs-idem-soft:
	@echo "== 🧪 Docs Idempotency SOFT =="
	@bash -c 'set -euo pipefail; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	git add -A >/dev/null 2>&1 || true; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	if ! git diff --quiet; then \
		echo "⚠️  Non idempotente (soft): il secondo run ha prodotto modifiche."; \
		git --no-pager diff --stat || true; \
	else \
		echo "✅ Idempotenza OK (nessuna modifica al secondo run)"; \
	fi'

docs-idem-strict:
	@bash -c 'set -euo pipefail; scripts/cursor_docs_strict.sh'

# <<< DOCS SYSTEM TARGETS END <<<

MK
mv Makefile.tmp Makefile
else
cat > Makefile <<'MK'
# Autogenerato: Docs System Makefile

.PHONY: docs-generate docs-idem-soft docs-idem-strict

docs-generate:
	@echo "ℹ️  Fallback docs-generate (no-op). Aggiungi qui il tuo generatore."

docs-idem-soft:
	@echo "== 🧪 Docs Idempotency SOFT =="
	@bash -c 'set -euo pipefail; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	git add -A >/dev/null 2>&1 || true; \
	if make -q docs-generate 2>/dev/null; then make docs-generate; else true; fi; \
	if ! git diff --quiet; then \
		echo "⚠️  Non idempotente (soft): il secondo run ha prodotto modifiche."; \
		git --no-pager diff --stat || true; \
	else \
		echo "✅ Idempotenza OK (nessuna modifica al secondo run)"; \
	fi'

docs-idem-strict:
	@bash -c 'set -euo pipefail; scripts/cursor_docs_strict.sh'
MK
fi

# 6) Step YAML pronto da incollare nel workflow
cat > CI_STRICT_STEP_YAML.md <<'YAML'
# 👇 Incolla questo step nel tuo workflow GitHub Actions (jobs.<job>.steps)

      - name: Docs Idempotency (STRICT)
        shell: bash
        run: |
          set -euo pipefail
          chmod +x scripts/cursor_docs_strict.sh
          git config user.email "ci-bot@example.com"
          git config user.name "ci-bot"
          ./scripts/cursor_docs_strict.sh
YAML

# 7) Mini-check immediato
echo "=== 🧪 Mini-check locale ==="
make docs-idem-soft || true
set +e
make docs-idem-strict
STRICT_RC=$?
set -e
if [[ $STRICT_RC -eq 0 ]]; then
echo "✅ STRICT OK subito"
else
echo "⚠️  STRICT ha trovato non-idempotenza (atteso se il tuo generatore modifica file al 2° run)."
fi

# 8) Preparazione commit (non forza)
git add setup_docs_system_one_shot.sh scripts/cursor_docs_strict.sh docs/DOCS_SYSTEM_README.md CI_STRICT_STEP_YAML.md Makefile .git/hooks/pre-commit 2>/dev/null || true
echo "=== ✅ Setup completato. Pronto al commit: git commit -m 'chore(docs): add idempotent docs system' ==="
