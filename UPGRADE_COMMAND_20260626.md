# Reusable implementation command — ADX Quant Pro six-page decision-history upgrade

Inspect, repair, test, and package the attached ADX Quant Pro project as one deployable ZIP.

## Non-negotiable protection
Preserve every protected production calculation, Field 1 source-of-truth value, BUY/SELL/WAIT/HOLD/NO-TRADE rule, threshold, Power BI central path, regime formula, canonical snapshot identity, database record, cache, historical outcome, and settled result. Never fabricate history, accuracy, reliability, uncertainty, or outcomes. Display grouping must never merge engines or formulas.

## Main navigation: exactly six top-level tabs
Keep exactly these six top-level tabs: Settings, Lunch, AI Assistant, Research, Field 456, Field 789.

Lunch must expose exactly three selectable fields and render only the selected field:
1. Field 1 — Full Metric History and Decision History
2. Field 2 — Power BI Price Prediction Path
3. Field 3 — Regime History

Move original Fields 4+5+6 into independent top-level tab `Field 456`. Move original Fields 7+8+9 into independent top-level tab `Field 789`. Combine them only in the UI. Keep every original calculation engine, function, cache, table, database store, outcome store, and persistence identity independent.

## Field 1 top table
At the very top of Field 1 add `Decision History — Last 25 Days`, newest completed EURUSD H1 broker candle first. Use only completed broker candles and the same canonical run_id/generation_id as all other fields.

Required columns:
Date; Weekday; Hour; Broker Candle Time; FX Session; Entry Strength Score; Entry Strength Decision; SELL Pressure Score; SELL Pressure Decision; BUY Pressure Score; BUY Pressure Decision; Net Pressure Score; Pressure Decision; Pullback Readiness Score; Pullback Readiness Decision; M1 Confirmation Score; M1 Confirmation Decision; Hold Safety Score; Hold Safety Decision; TP Quality Score; TP Quality Decision; Master Decision Score; Master Decision; Direction Confirmation Score; Direction Confirmation Decision; Final Decision; Decision Confidence; Decision Reliability; Uncertainty Percentage; Error Percentage; Realized Direction; Decision Correct; Outcome Status; Canonical run_id; Canonical generation_id.

Scores must be 0–10 only when the source explicitly declares its scale. Unknown values must display N/A. Do not infer or invent missing scores. Unsettled rows must display Decision Correct = N/A.

## Synchronization contract
Field 1 is the source-of-truth display contract. Fields 2, 3, 456, and 789 must read the same immutable canonical snapshot and completed broker candle identity. Tab switching must perform zero protected recalculation. Show identity strips with run_id, generation_id, source hash, broker candle time, EURUSD, and H1.

## HOLD / NO-TRADE research candidate
Do not directly halve production HOLD/NO-TRADE thresholds. Add a shadow-only candidate policy that targets at most a 50% reduction in HOLD/NO-TRADE frequency, but promote it only if purged walk-forward and embargoed tests show all of the following by session and regime:
- increased settled directional hit rate or statistically non-inferior hit rate;
- positive net expected value after spread/slippage;
- no material deterioration in maximum drawdown, expected shortfall, calibration, interval coverage, or false-entry rate;
- minimum effective sample size and stable results across rolling windows;
- no look-ahead leakage.
The production decision remains unchanged until explicit promotion.

## Direction-confirmation research stack
Build the shadow confirmation from already-published features only: calibrated directional probability, BUY/SELL pressure margin, M1 agreement, session/regime conditional reliability, drift status, conformal uncertainty, forecast-path agreement, and transaction-cost-aware expected value. Use abstention when evidence conflicts or coverage is poor. Store shadow output separately from production decisions.

## Performance and testing
Use lazy imports and render only the selected field. Keep app.py as the Streamlit Cloud entry point. Run syntax compilation, structural navigation tests, canonical identity tests, no-recalculation-on-tab-switch tests, completed-candle tests, and decision-table schema tests. Report missing optional runtime dependencies separately from code failures. Package the final project as one deployable ZIP with a modification report and SHA-256 manifest.
