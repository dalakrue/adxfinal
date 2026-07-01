# Quant Research V8 Architecture Report

## Delivery architecture

The V8 upgrade preserves the V7 entry flow: `app.py` → `adx_dashpoard.py` → the existing app shell and `tabs/antd_page_router_20260615.py`. No new top-level page, sidebar item, or menu item was added.

The only heavy publication path remains the existing Settings **Run Calculation + Open Lunch** transaction. `core/settings_run_orchestrator_20260617.py` invokes `build_quant_research_v8_transaction(...)` once after the protected canonical calculation is already available. V8 consumes the same completed H1 frame, canonical calculation ID, generation, symbol, timeframe, settled outcomes and shared broker-time contract. It then stages normalized V8 history rows inside the same canonical `BEGIN IMMEDIATE` database transaction through `services/canonical_snapshot_store.py`.

Morning is now a dedicated read-only renderer: `tabs/doo_prime/morning_control_v8_20260622.py`. It contains only **Overview**, **Analysis**, **History**, and **Health / Readiness**. Overview and Health read the published canonical V8 payload. History queries each bounded table only after that table's Load control is enabled. Analysis imports the protected legacy Doo Prime account/risk/emergency workspace only when its expander is opened.

## New bounded V8 core modules

- `core/morning_quant_metrics_20260622.py`: Expected Shortfall, EWMA volatility, drawdown, exposure, risk budget, ATR stress, execution percentiles, capped Kelly shadow evidence and empirical survival proxy.
- `core/field1_data_quality_v8_20260622.py`: completed-H1 filtering and strict Field 1 identity validation.
- `core/adwin_monitor_v8_20260622.py`: compact detectors for the nine requested monitoring streams.
- `core/dynamic_ensemble_v8_20260622.py`: Bates–Granger, Fixed-Share and conditional trust evidence.
- `core/research_governance_v8_20260622.py`: temporal block bootstrap, SPA, White Reality Check, sampled CSCV/PBO and explicit promotion gates.
- `core/quant_production_readiness_v8_20260622.py`: PASS/WARN/FAIL/NOT APPLICABLE readiness contract with critical READY blocking.
- `core/morning_quant_store_20260622.py`: normalized migrations and bounded queries.
- `core/quant_research_v8_store_20260622.py`: Settings-only V8 transaction, failure containment and history staging.
- `core/transaction_guard_v8_20260622.py`: duplicate/debounce protection for user transactions.

## Compatibility and protection

`tabs/doo_prime/home_analytics.py` remains as a backward-compatible wrapper. Existing raw red/yellow/blue/consensus projection functions remain live; V8 CQR is appended to `core/powerbi_path_calibration_20260617.py` as shadow calibration. V8 production influence defaults to false and requires every governance gate plus explicit configuration.

No heavy calculation, refetch, retraining, recalibration or canonical publication is called by Morning, Lunch Field 1 expanders, Research display, Train Data display, copy serialization or tab switching.
