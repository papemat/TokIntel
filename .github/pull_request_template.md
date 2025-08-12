## Sprint 3 — Hardening & E2E

### Checklist
- [ ] Orchestrator CLI funzionante
- [ ] E2E headless green su 3.10/3.11
- [ ] Auto-export CSV/JSON verificato
- [ ] Badge workflow verde

### Note
- Comandi di verifica:
  ```bash
  make kill-port TI_PORT=8510
  TI_AUTO_EXPORT=1 TI_PORT=8510 make run-ui
  make test-e2e-only && make coverage-sprint3
  ```

### Changes
<!-- Descrivi le modifiche principali -->

### Testing
<!-- Come hai testato le modifiche -->

### Screenshots
<!-- Se applicabile -->
