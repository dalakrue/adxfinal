# Database Migration Report

## Isolation

ARERT uses a separate database path:

```text
data/arert_research.sqlite3
```

It does not alter the protected production database schema.

## Additive migration

`research_quant.arert_store.migrate_arert_database` uses only:

- `CREATE TABLE IF NOT EXISTS`
- `CREATE INDEX IF NOT EXISTS`
- transaction commit/rollback

It never drops, renames, truncates, or silently rewrites an existing table.

## Research tables

- `research_runs`
- `research_feature_snapshots`
- `research_regime_duration`
- `research_changepoints`
- `research_jumps`
- `research_conformal_forecasts`
- `research_meta_labels`
- `research_model_weights`
- `research_analogues`
- `research_behavioral_scores`
- `research_event_responses`
- `research_information_scores`
- `research_validation_results`
- `research_arert_scores`

Each table contains an integer primary key, unique research record key, run/generation IDs, broker candle, symbol, timeframe, research version, module number/status, creation timestamp, and JSON payload.

## Preservation test

An automated test created a pre-existing `protected_production_table`, ran the migration, and confirmed its row remained unchanged. The test passed.

## Persistence behavior

Research envelope and module records use an identity-based upsert into research tables. The upsert is limited to the identical research record key; it cannot update production tables.
