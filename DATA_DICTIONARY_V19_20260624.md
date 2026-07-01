# Data Dictionary
Every V19 record carries `run_id`, `symbol`, `timeframe`, `broker_candle_time`, `source_data_hash`, `model_version`, `evidence_version`, `horizon`, `maturity_time`, `pending_matured_status`, and `content_hash`.

- `pending_matured_status`: PENDING or MATURED; outcomes are never settled before maturity.
- `content_hash`: SHA-256 of normalized stored row content.
- `evidence_sufficiency`: AVAILABLE only when the configured chronological minimum is met; otherwise INSUFFICIENT_EVIDENCE.
- `production_influence_enabled`: always false for V19.
- `consensus_regime`: may return `TRANSITION / INSUFFICIENT EVIDENCE / WAIT PREFERRED`.
