# 👇 Step per GitHub Actions (jobs.<job>.steps)

      - name: Setup Docs System
        run: |
          chmod +x scripts/cursor_docs_strict.sh
          git config user.email "ci-bot@example.com"
          git config user.name "ci-bot"

      - name: Docs Idempotency (STRICT)
        shell: bash
        run: |
          set -euo pipefail
          echo "🔍 Verificando idempotenza docs..."
          ./scripts/cursor_docs_strict.sh
          echo "✅ Idempotenza verificata"

# 🔄 Workflow completo di esempio:
# 
# name: Docs Check
# on: [push, pull_request]
# jobs:
#   docs:
#     runs-on: ubuntu-latest
#     steps:
#       - uses: actions/checkout@v4
#       - uses: actions/setup-python@v4
#         with:
#           python-version: '3.11'
#       - name: Install dependencies
#         run: |
#           python -m pip install --upgrade pip
#           pip install -r requirements.txt || true
#       - name: Setup Docs System
#         run: |
#           chmod +x scripts/cursor_docs_strict.sh
#           git config user.email "ci-bot@example.com"
#           git config user.name "ci-bot"
#       - name: Docs Idempotency (STRICT)
#         shell: bash
#         run: |
#           set -euo pipefail
#           echo "🔍 Verificando idempotenza docs..."
#           ./scripts/cursor_docs_strict.sh
#           echo "✅ Idempotenza verificata"
