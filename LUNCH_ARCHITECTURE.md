# Modular Lunch Architecture

`app.py` is the preferred Streamlit entry point. The Lunch page loads one immutable `CanonicalRunSnapshot`, validates it, renders shared controls, then dispatches only the selected field through `lunch/registry.py` and `lunch/router.py`.

## Canonical synchronization

All fields receive the same `LunchRenderContext` and exact snapshot values: `run_id`, `broker_candle_time`, symbol, timeframe, decision, regime, priority, reliability, current price and predictions. Renderers never create a run ID or calculate broker time. Heavy work is produced by **Settings → Run Calculation + Open Lunch** and saved before Lunch opens.

## Registry and field contract

Each entry in `FIELD_REGISTRY` has an ID, titles, order, enabled/experimental flags, and lazily resolved `validate`, `build_view_model`, and `render` functions. `safe_render_field` isolates failures and logs run, time, field, operation, duration, status and error type.

## Adding or changing a field

1. Add `lunch/field_XX/contract.py`, `view_model.py`, `renderer.py`, optional `tables.py`/`charts.py`, and tests.
2. Register it in `lunch/registry.py`.
3. Keep data reads in the view model and UI work in the renderer.
4. Never call production prediction, regime, settlement or research orchestration from a renderer.
5. Run the field contract, registry, routing and no-heavy-render tests.

## Safe edit boundaries

Rendering-only files: `lunch/field_*/renderer.py`, `charts.py`, `tables.py`, shared Lunch UI modules. Data formatting: `view_model.py`. Protected calculations remain in existing core/research engines and Settings orchestration. Compatibility wrappers and legacy files remain preserved.

### To change Field 2

1. Edit `lunch/field_02/renderer.py` for display.
2. Edit `lunch/field_02/charts.py` for charts.
3. Edit `lunch/field_02/view_model.py` for data formatting.
4. Do not edit the Lunch router.
5. Do not edit canonical calculation logic.
6. Run Field 2 tests.
