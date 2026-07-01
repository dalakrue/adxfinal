# ADX Quant Pro — Final Repair and Deployment Report

## Package scope

The project was inspected and repaired as a deployable Streamlit application while preserving the uploaded production calculation engines and source-of-truth modules. The Lunch workspace now exposes exactly five selectable display fields:

1. Field 1 — Full Metric History and Decision History
2. Field 2 — Power BI Price Prediction Path
3. Field 3 — Regime History
4. Combined display Fields 4+5+6
5. Combined display Fields 7+8+9

Fields 4+5+6 and Fields 7+8+9 are combined only by selector/presentation. Their existing engines, functions, caches, stores and calculation paths remain independent.

## Modified files

- `ui/lunch_four_core_fields_20260619.py`
  - Corrected the visible field count to exactly five.
  - Kept one-major-field-at-a-time rendering.
  - Added the exact `Refresh API Data + Quick Sync` control label.
  - Made copy-cache invalidation conditional on canonical identity change.
  - Added the shared read-only identity strip to all five displays.
  - Added explicit state summaries for Field 2 and Fields 7–9.
- `core/decision_table_20260626.py`
  - Fixed DataFrame truth-value handling.
  - Preserved genuine 0% and 100% values while retaining unavailable values as `N/A`.
  - Removed the full Decision History DataFrame from the duplicated canonical session-state snapshot; only the latest row and row count are retained.
- `ui/lunch_identity_strip_20260626.py`
  - New read-only run/generation/candle/symbol/timeframe/hash identity strip.
- `core/research_result_state_20260626.py`
  - New explicit state taxonomy: insufficient observations, unsettled future outcome, missing source data, stale generation, model failure, valid low-confidence result, valid result.
- `ui/lunch_data_state_20260626.py`
  - New state banner renderer using the explicit taxonomy.
- `core/direction_confirmation_shadow_policy_20260626.py`
  - New research-only anchored walk-forward threshold evaluator using candidates at 100%, 90%, 80%, 70%, 60% and 50% of the current threshold.
  - Includes directional-skill, conditional-loss, calibration, expected-value/transaction-cost, drawdown, effective-sample-size and session/regime stability gates.
  - Defaults to retaining the production threshold unless every promotion gate passes.
- `tests/test_upgrade_20260626.py`
  - New regression tests for the five-field layout, Field 1 table order, copy/refresh controls, missing-value handling, threshold retention and result-state taxonomy.

## Tests passed

- Python compile-all: **PASS**
- `app.py` import: **PASS**
- Key UI and optional AirLLM module imports: **PASS**
- Streamlit startup smoke test: **PASS**
- Streamlit `/_stcore/health`: **PASS**
- Upgrade regression tests: **6 passed**
- Lunch exactly five field labels: **PASS**
- Field 1 history order: Decision History first, Overall Full Metric second, All 10 Decision Histories third: **PASS**
- Combined 4+5+6 and 7+8+9 remain display-only selectors: **PASS by source inspection and lazy import structure**
- Copy Short / Copy Full labels and current-generation serializer wiring: **PASS**
- Refresh control and identity-aware copy invalidation: **PASS**
- AirLLM disabled fallback path: **PASS by import/static path inspection**
- AirLLM missing-package safe path: **PASS by guarded dynamic import inspection**

## Protected source verification

The following protected modules are byte-for-byte unchanged from the uploaded ZIP:

- `core/adx_shared_sync_20260615.py`
- `core/canonical_runtime_20260617.py`
- `core/quant_research_v6_store_20260622.py`
- `core/powerbi_path_calibration_20260617.py`
- `core/decision_policy_20260617.py`
- `core/decision_product_engine_20260617.py`

No protected production threshold, BUY/SELL/WAIT rule, Power BI central path, regime formula or canonical calculation engine was edited in this repair.

## Unresolved limitations

- Live Twelve Data, Finnhub, MT5 or broker API calls were not executed because credentials and live network feeds were not available in the test environment.
- Exact cross-field broker-candle equality can only be fully confirmed after one successful live canonical publication. The UI now displays the same canonical identity in every field and does not calculate Field 1 when switching fields.
- The research shadow policy requires settled historical rows with compatible direction-score and actual-direction columns. It safely retains the production threshold when those rows are absent or insufficient.
- AirLLM model inference was not run because no model was downloaded and the optional package/model configuration was not supplied. The app remains functional with AirLLM disabled, and missing-package/model conditions fail safely.
- Existing nested legacy renderers may contain their own non-top-level export/download controls. The authoritative Lunch top rail contains exactly the requested two clipboard controls, Copy Short and Copy Full.

## Deployment instructions

1. Upload the extracted project folder to GitHub or Streamlit Community Cloud.
2. Set the Streamlit main file to `app.py`.
3. Use the included `runtime.txt` and `requirements.txt`.
4. Add API secrets through Streamlit Secrets using `.streamlit/secrets.example.toml` as the template.
5. Leave `ADX_ENABLE_AIRLLM=0` unless the Streamlit server has sufficient disk/RAM and the optional AirLLM package/model is installed.
6. Start locally with:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

7. In the app, run the Settings calculation once, then open Lunch. Verify the canonical identity strip is identical across all five selectable fields.
