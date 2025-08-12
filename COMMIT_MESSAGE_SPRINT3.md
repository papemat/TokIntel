feat: Sprint 3 - Orchestratore + Test E2E

🎯 Implementa orchestratore con DI e test end-to-end completi

## 🆕 Nuove funzionalità
- **Orchestratore** con Dependency Injection per indicizzazione e query multimodale
- **Test integration** deterministici per pipeline end-to-end
- **Test E2E** per UI Streamlit in headless con health-check
- **Auto-export** CSV/JSON per testing automatizzato

## 📁 File aggiunti/modificati
- `analyzer/orchestrator.py` - Orchestratore con DI (97% coverage)
- `tests/integration/test_orchestrator.py` - Test integration
- `tests/e2e/test_streamlit_ui.py` - Test E2E headless
- `tests/conftest.py` - NumpyIndex aggiornato per interfaccia orchestrator
- `dash/app.py` - Environment variables e auto-export
- `Makefile` - Target test-sprint3 e coverage-sprint3

## 🧪 Test Results
- ✅ Integration tests: 2/2 passed
- ✅ E2E tests: 1/1 passed  
- ✅ Coverage orchestrator: 97% (71/73 lines)
- ✅ Makefile targets: test-sprint3, coverage-sprint3

## 🔧 Funzionalità chiave
- Merge stabile con ordinamento (-final_score, original_idx)
- Fixture deterministiche per test stabili
- Environment variables per configurazione testing
- Health-check automatico per E2E

## 🚀 Utilizzo
```bash
make test-sprint3      # Test veloci
make coverage-sprint3  # Coverage completo
```

Closes #sprint3
