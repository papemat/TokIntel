# 👇 Incolla questo step nel tuo workflow GitHub Actions (jobs.<job>.steps)

      - name: Docs Idempotency (STRICT)
        shell: bash
        run: |
          set -euo pipefail
          chmod +x scripts/cursor_docs_strict.sh
          git config user.email "ci-bot@example.com"
          git config user.name "ci-bot"
          ./scripts/cursor_docs_strict.sh
