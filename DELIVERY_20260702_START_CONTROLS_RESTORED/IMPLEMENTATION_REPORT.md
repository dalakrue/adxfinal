# Critical Settings Start Controls Restored — 2026-07-02

## Result

The Settings startup flow now keeps all critical controls visible and usable on phone, desktop, and Streamlit Cloud:

1. Temporary Twelve Data key paste and one-click connect
2. Twelve Data + MT5 market connector
3. Finnhub connector
4. Multi-symbol selector
5. Exactly three calculation choices
6. One `Run Calculation + Open Lunch` button

The selector and the three calculation choices use normal bordered containers, not collapsible expanders. Mobile Lite may reduce decoration and table size, but it no longer has any path that removes these controls.

## Root cause repaired

The multi-symbol Settings renderer still had a render-time dependency path into the heavier multi-symbol runtime. An optional deployment import failure could replace the full selector with a single-symbol fallback. In the failing deployment this appeared as:

`Multi-symbol selector skipped safely: No module named 'cloudpickle'`

The critical UI is now independent from the runtime cache and serializer. It does not import the multi-symbol calculation engine, cloudpickle, pandas, or connector internals while rendering.

## Main changes

- Rebuilt `ui/multi_symbol_settings_20260701.py` as a dependency-light UI contract.
- Kept the public state keys identical to the calculation engine, so protected multi-symbol calculations remain unchanged.
- Made the multi-symbol section always visible and searchable.
- Made all three run choices always visible:
  - Quick — Fields 1–9 + AI
  - Full — Fields 1–9 + thesis + AI
  - Super Quick — Lunch Fields 1–3
- Added a visible emergency selector and visible emergency run-mode control in the page router. An import error is shown, but the controls are not removed.
- Converted the Twelve Data + MT5 and Finnhub startup connectors to non-collapsible visible containers.
- Added a minimal visible connector fallback if the advanced connector renderer fails.
- Placed critical startup controls before the run transaction.
- Preserved exactly one main calculation button.
- Synchronized the backward-compatible V9 split router source with the active router.
- Preserved existing protected decision, regime, Field 1–10, canonical snapshot, history, and model calculations.

## Validation

Automated tests were run in three isolated batches to avoid cross-test Streamlit module state:

- Batch 1: 167 passed
- Batch 2: 18 passed
- Batch 3: 18 passed
- Total: 203 passed

Additional checks:

- Full Python compile check passed.
- Missing-cloudpickle serializer fallback test passed.
- Selector import with cloudpickle and the multi-symbol engine blocked passed.
- Minimal Streamlit render simulation confirmed both always-visible sections render.
- Static startup-order test confirmed connectors, selector, and three modes occur before the run button.
- Known exposed API-key strings were not found in the delivered project.

## Deployment note

The sandbox did not contain the real Streamlit package, so a live browser session was not launched here. The complete project test suite was executed with a lightweight Streamlit import stub for non-browser tests. After uploading this project, reboot the Streamlit Cloud app so it installs `requirements.txt` and does not reuse the old deployment image.
