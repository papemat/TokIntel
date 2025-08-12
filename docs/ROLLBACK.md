# TokIntel — Piano di Rollback

## Quando eseguire
- Test critici rossi o regressioni post‑deploy
- Report con metriche anomale (video count basso, export vuoti)
- Dashboard lenta/non responsiva

## Passi operativi
1. **Blocca nuove elaborazioni** se presenti (scheduler/cron).
2. **Ripristina versione stabile**:
   ```bash
   git checkout <tag_stabile>
   TOKINTEL_VERSION=<tag_stabile> FF_DISABLE_CACHE=1 make prod-check
   ```

3. **Ripristina DB (se necessario)** da backup più recente.
4. **Rigenera report**: allega `reports/prod_check_*.md` al log di incidente.

## Verifica post‑rollback

* Dashboard apre e filtri/ricerca funzionano
* Badge di stato coerenti e metriche visibili
* Export CSV/JSON funzionanti e non vuoti
* Report generato senza errori

## Prevenzione

* Esegui `make prod-check` su staging con DB realistico (200–500+ video)
* Mantieni aggiornato `.env` e usa feature flags per disattivare cache in debug
