# Database Migration Report — Quant Research V8

## New normalized tables

Six requested Morning histories are created idempotently:

1. `morning_account_state_history`
2. `morning_position_exposure_history`
3. `morning_risk_budget_stress_history`
4. `morning_forecast_outcome_history`
5. `morning_execution_api_health_history`
6. `clock_sync_audit_history`

Five compact governance/monitoring tables are also added:

- `conformal_calibration_state_v8`
- `conformal_alpha_history_v8`
- `research_experiment_registry_v8`
- `drift_epoch_history_v8`
- `quant_readiness_history_v8`

## Migration behavior

`ensure_schema()` uses `CREATE TABLE IF NOT EXISTS`, inspects `PRAGMA table_info`, and adds missing columns with idempotent `ALTER TABLE`. New V8 tables use composite event/generation identities and bounded indexes for available event time, calculation ID, generation, symbol, timeframe, horizon and status columns.

Normal rows use `INSERT OR IGNORE` where an unchanged event identity is semantically immutable. Forecast/outcome rows use an upsert that keeps a pending forecast unchanged until a matching row contains a settled actual; then settlement, errors and coverage fields are updated. Secret-like strings are redacted before persistence.

The V8 bundle is inserted inside the existing authoritative canonical transaction. Any exception rolls the transaction back. A V8 calculation-side failure returns the previous valid V8 payload when available and cannot overwrite the last valid canonical generation.

## Validation evidence

Tests cover creation of all eleven tables, migration from a partial old schema, account snapshot deduplication, settled outcome update, secret redaction, idempotency and failure containment. No existing database file was deleted or replaced in the delivered project.
