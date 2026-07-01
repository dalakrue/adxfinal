# Morning History Data Dictionary

All event identities are stored in UTC. Broker and Myanmar columns are display/export projections. Tables are newest-first in the UI, searchable, row-bounded and CSV-exportable.

## Table 1 — `morning_account_state_history`

| Column | Purpose |
|---|---|
| `event_time_utc` | Authoritative UTC event identity. |
| `broker_time` | Shared broker-time projection. |
| `myanmar_time` | Asia/Yangon display projection. |
| `calculation_id` | Canonical calculation identity. |
| `generation_id` | Canonical publication generation. |
| `balance` | Normalized V8 history field. |
| `equity` | Normalized V8 history field. |
| `floating_profit` | Normalized V8 history field. |
| `used_margin` | Normalized V8 history field. |
| `free_margin` | Normalized V8 history field. |
| `margin_level` | Normalized V8 history field. |
| `drawdown_pct` | Normalized V8 history field. |
| `open_position_count` | Normalized V8 history field. |
| `data_quality_status` | Published quality/readiness status. |

## Table 2 — `morning_position_exposure_history`

| Column | Purpose |
|---|---|
| `event_time_utc` | Authoritative UTC event identity. |
| `broker_time` | Shared broker-time projection. |
| `calculation_id` | Canonical calculation identity. |
| `generation_id` | Canonical publication generation. |
| `symbol` | Normalized V8 history field. |
| `position_id_or_stable_key` | Broker position ID or deterministic stable key. |
| `side` | Normalized V8 history field. |
| `lots` | Normalized V8 history field. |
| `entry_price` | Normalized V8 history field. |
| `current_price` | Normalized V8 history field. |
| `notional_exposure` | Normalized V8 history field. |
| `stop_distance` | Normalized V8 history field. |
| `atr_risk` | Normalized V8 history field. |
| `unrealized_profit` | Normalized V8 history field. |
| `exposure_concentration` | Normalized V8 history field. |
| `source` | Normalized V8 history field. |

## Table 3 — `morning_risk_budget_stress_history`

| Column | Purpose |
|---|---|
| `event_time_utc` | Authoritative UTC event identity. |
| `broker_time` | Shared broker-time projection. |
| `calculation_id` | Canonical calculation identity. |
| `generation_id` | Canonical publication generation. |
| `risk_per_trade` | Normalized V8 history field. |
| `planned_trade_count` | Normalized V8 history field. |
| `planned_total_risk` | Normalized V8 history field. |
| `used_daily_risk` | Normalized V8 history field. |
| `remaining_daily_risk` | Normalized V8 history field. |
| `expected_shortfall_95` | Normalized V8 history field. |
| `expected_shortfall_99` | Normalized V8 history field. |
| `stress_1atr` | Normalized V8 history field. |
| `stress_2atr` | Normalized V8 history field. |
| `stress_3atr` | Normalized V8 history field. |
| `risk_status` | Normalized V8 history field. |

## Table 4 — `morning_forecast_outcome_history`

| Column | Purpose |
|---|---|
| `forecast_event_time_utc` | UTC forecast-origin identity. |
| `settlement_time_utc` | UTC time when the actual outcome became settled. |
| `broker_forecast_time` | Normalized V8 history field. |
| `calculation_id` | Canonical calculation identity. |
| `generation_id` | Canonical publication generation. |
| `horizon_hours` | Normalized V8 history field. |
| `raw_prediction` | Normalized V8 history field. |
| `calibrated_prediction` | Normalized V8 history field. |
| `lower_80` | Normalized V8 history field. |
| `upper_80` | Normalized V8 history field. |
| `lower_90` | Normalized V8 history field. |
| `upper_90` | Normalized V8 history field. |
| `lower_95` | Normalized V8 history field. |
| `upper_95` | Normalized V8 history field. |
| `actual_price` | Normalized V8 history field. |
| `absolute_error` | Normalized V8 history field. |
| `error_pct` | Normalized V8 history field. |
| `direction_correct` | Normalized V8 history field. |
| `covered_80` | Normalized V8 history field. |
| `covered_90` | Normalized V8 history field. |
| `covered_95` | Normalized V8 history field. |
| `reliability` | Normalized V8 history field. |
| `regime` | Normalized V8 history field. |
| `session` | Normalized V8 history field. |

## Table 5 — `morning_execution_api_health_history`

| Column | Purpose |
|---|---|
| `event_time_utc` | Authoritative UTC event identity. |
| `broker_time` | Shared broker-time projection. |
| `calculation_id` | Canonical calculation identity. |
| `generation_id` | Canonical publication generation. |
| `connector` | Normalized V8 history field. |
| `connection_status` | Normalized V8 history field. |
| `symbol` | Normalized V8 history field. |
| `timeframe` | Normalized V8 history field. |
| `fetch_duration_ms` | Normalized V8 history field. |
| `row_count` | Normalized V8 history field. |
| `latest_completed_h1_utc` | Normalized V8 history field. |
| `freshness_lag_seconds` | Normalized V8 history field. |
| `spread` | Normalized V8 history field. |
| `slippage` | Normalized V8 history field. |
| `retry_count` | Normalized V8 history field. |
| `failure_type` | Normalized V8 history field. |
| `last_safe_error` | Redacted bounded connector error; secrets are never stored. |
| `data_quality_status` | Published quality/readiness status. |

## Table 6 — `clock_sync_audit_history`

| Column | Purpose |
|---|---|
| `event_time_utc` | Authoritative UTC event identity. |
| `broker_time` | Shared broker-time projection. |
| `myanmar_time` | Asia/Yangon display projection. |
| `broker_offset_minutes` | Normalized V8 history field. |
| `broker_timezone` | Normalized V8 history field. |
| `clock_resolution_source` | Normalized V8 history field. |
| `latest_completed_h1_utc` | Normalized V8 history field. |
| `field1_latest_utc` | Normalized V8 history field. |
| `calculation_id` | Canonical calculation identity. |
| `generation_id` | Canonical publication generation. |
| `symbol` | Normalized V8 history field. |
| `timeframe` | Normalized V8 history field. |
| `contract_version` | Shared broker-time contract version. |
| `field1_sync_status` | Strict Field 1 identity result. |
| `cross_table_sync_status` | Cross-table identity result. |
| `reason` | Normalized V8 history field. |
