# Implementation Report — 2026-06-28

## Result

The uploaded Streamlit project was repaired and extended with a separate ARERT Dinner thesis laboratory while retaining the protected Lunch production system.

## User-visible repairs

1. **Lunch Field 3 mixed timestamp error**
   - Added a display-boundary UTC sort helper that safely compares strings, timezone-aware timestamps, timezone-naive timestamps, and invalid values.
   - Replaced the failing direct sort in the Field 3 regime matrix.
   - Added safe component boundaries so one legacy research renderer cannot close the full Lunch eight-field surface.

2. **Lunch Field 1 Table 5 missing data**
   - Table 5 now coalesces genuine Table 1 publications by normalized completed H1 candle.
   - The visible Table 1 remains authoritative; older aliases and the read-only builder fill only blank cells.
   - Entry Strength, BUY/SELL Pressure, M1 Confirmation, Master Decision, outcomes, correctness, and canonical identity columns are included when published.
   - Completely blank display columns are removed from the view only; stored source data is preserved.
   - Protective display columns map existing evidence to `HOLD & PROTECT` or `WAIT FOR PULLBACK` without replacing raw production decisions.

3. **Dinner Combined History**
   - Added a stable 20-column protective-action audit schema at the front of the stored table.
   - All populated action values use only `HOLD & PROTECT` or `WAIT FOR PULLBACK`.
   - Original BUY/SELL/WAIT values remain available for audit and export.
   - Empty or single-row columns are omitted only from the compact phone display.

4. **AI summary moved to Lunch Field 1**
   - Added a current-candle, read-only AI Summary at the bottom of Field 1.
   - It reads canonical, Table 5, Dinner, and cached ARERT evidence and does not start an API call or heavy calculation.

5. **Copy Short / Copy Full**
   - Payload extraction now requires the exact current completed canonical H1 candle.
   - A stale previous-hour row is not copied as current evidence.
   - The existing mobile clipboard component retains secure clipboard, parent clipboard, `execCommand`, selected-text, keyboard, and touch fallbacks.
   - Payloads are cached by canonical identity to avoid repeated serialization.

## ARERT Dinner thesis laboratory

Created `Adaptive Regime–Evidence Reliability Theory — ARERT` as a separate Layer B research system.

- 20 research module implementations are registered.
- 10 Dinner research fields are rendered from cached results.
- Field 1 opens by default; Fields 2–10 are closed by default.
- Opening/closing fields never runs a model.
- Missing data produces an explicit incomplete status; production values are not fabricated.
- Every module records canonical identity, versions, sample metadata, status, limitations, runtime, memory, input hash, and output hash.
- Same-candle cache identity includes candle, symbol, timeframe, module, model version, parameter version, and snapshot identity.
- Research persistence is isolated in `data/arert_research.sqlite3` and uses additive migrations only.

## Settings and navigation

Added exact controls:

- **Run Full Dinner Thesis Research + Open Dinner**
- **Run Selected Dinner Research Module**

The selected run reads the latest valid frozen canonical snapshot and navigates to Dinner. It does not rerun the protected Lunch production engine.

## AI research access

- OpenRouter remains optional and secret-backed.
- The Assistant can receive bounded ARERT module summaries and limitations.
- Transient OpenRouter 429/5xx/network errors are retried once.
- Any failure activates the existing deterministic local grounded pipeline.
- ARERT/research/thesis questions are accepted by the domain boundary.

## Production protection evidence

The two principal Field 1 decision/Table 3 source files match the uploaded ZIP byte-for-byte:

- `ui/lunch_decision_table_20260626.py`: unchanged SHA-256 `d9f68a82e19c73efe2714a40781d9475cf826f9ce4c42007605336ebb5de89f2`
- `core/decision_table_20260626.py`: unchanged SHA-256 `2c808100d6836689aa7f288c0fbd69cca21ce60b3e4d48b8ada81b06f3aa4b89`

No project file was deleted.

## Recommended main entry

Use:

```powershell
streamlit run app.py
```

`adx_dashpoard.py` remains a backward-compatible entry and uses the same `core.app_shell.run_app` implementation.
