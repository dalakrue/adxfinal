# Database migration report

Added idempotent append-only tables:

- shadow_dma_state_v15
- model_confidence_set_v15
- proper_scores_v15
- sequential_conformal_v15
- subset_ensemble_v15
- changepoint_v15
- hsmm_duration_v15
- har_volatility_v15
- venn_abers_v15
- conformal_risk_v15
- promotion_report_v15

Each table uses `(run_id, origin_time, horizon, entity_id)` as an immutable primary key. Duplicate inserts are rejected, WAL and busy timeout are enabled, and bounded retention defaults to 5,000 rows per table.
