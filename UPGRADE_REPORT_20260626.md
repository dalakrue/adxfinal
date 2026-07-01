# ADX Quant Pro — Five-Field Lunch Upgrade

## Implemented

- Lunch selector reduced to exactly five display fields:
  1. Field 1 — Full Metric + Decision History
  2. Field 2 — Power BI Prediction Path
  3. Field 3 — Regime History
  4. Combined display for original Fields 4+5+6
  5. Combined display for original Fields 7+8+9
- Original calculation engines, caches, history stores, and protected decisions remain separate. Only their presentation is combined.
- Added **Decision History — Last 25 Days** at the top of Field 1 with Date, Weekday, Hour, Entry Strength, SELL Pressure, BUY Pressure, Net Pressure, Pullback Readiness, M1 Confirmation, Master Decision, Hold Safety, TP Quality, Direction Confirmation, final decision, confidence, reliability, uncertainty, error, and settled correctness.
- Field 1 now presents three history groups: Decision History, Overall Full Metric History, and All 10 Decision Histories.
- Added a research-only consensus diagnostic. It does not overwrite BUY/SELL/WAIT or automatically weaken HOLD/NO-TRADE thresholds.
- Preserved the two current-only copy buttons and the API Refresh + Quick Sync control.
- Added optional AirLLM integration with lazy import and deployment flags. Inference runs on the Streamlit server, not on the iPhone; the existing grounded assistant works when AirLLM is disabled.

## AirLLM deployment flags

- `ADX_ENABLE_AIRLLM=1`
- `ADX_AIRLLM_MODEL=<hugging-face-model-id>`

Do not enable AirLLM on a small Streamlit server until disk, RAM, and cold-start behavior are measured. It is intentionally optional and fail-safe.

## Validation completed

- Python compilation/AST validation passed for all modified/new modules.
- Static checks confirm five field labels, Decision History placement, combined 4+5+6 and 7+8+9 views, two-copy-button renderer, and refresh control.
- Full Streamlit runtime execution was not available in this container because the Streamlit package is not installed here.
