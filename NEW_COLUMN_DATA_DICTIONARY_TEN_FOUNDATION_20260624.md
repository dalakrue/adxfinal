# New Column Data Dictionary

## `ten_foundation_snapshots`
`run_id` deterministic canonical run key; `broker_candle_time` canonical market origin; `symbol`; `timeframe`; `production_decision` unchanged Field 1 decision; `payload_hash` integrity digest; `payload_json` complete immutable research snapshot; `created_at` database audit time.

## `ten_foundation_origins`
`run_id`, `horizon` composite origin key; `origin_broker_time`; `symbol`; `timeframe`; `settlement_status`; `origin_prediction`; `origin_lower`; `origin_upper`; `origin_weights_json`; `origin_regime_json`; `origin_changepoint_json`; `origin_actionability_json`; `origin_counterfactual_json`; settlement-only `actual`, `realized_error`, `settled_at`.
