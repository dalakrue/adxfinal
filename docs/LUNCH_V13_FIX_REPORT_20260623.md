# Project Quant Lunch V13 — Fix and Validation Report

**Date:** 2026-06-23  
**Delivery mode:** Complete project ZIP reconstructed exclusively from the supplied archive.

## Source recovery note

The supplied file had a `.zip` name but was a malformed concatenated archive. The project was recovered only from material inside that supplied file: its embedded audited backup plus the CRC-valid V12 overlay entries. No external project source was used.

## Protection result

- No production calculation, predictor, strategy rule, model weight, execution behavior, existing metric, history table, database schema/table, connector, copy function, canonical snapshot field, tab, or top-level navigation item was deleted or replaced.
- Settings remains the only owner of heavy research execution. Lunch and the existing Research Lab page read saved results only.
- New methods are shadow-only, have `production_changed = false`, and cannot promote themselves or alter BUY, SELL, or WAIT.
- Named protected production/core files are byte-for-byte identical to the recovered baseline; see `PROTECTED_HASH_AUDIT_V13_20260623.json`.
- Python deployment target remains `python-3.12`; Streamlit Cloud dependency declarations remain intact.
- New V13 work is split into bounded helper modules; the largest new helper is under 400 lines.

## Field 1 — true H1 25-day history

- `Date` plus `Hour` is normalized into one timezone-aware UTC event timestamp before filtering, freshness evaluation, deduplication, ordering, broker conversion, or display.
- `Date` never overrides a valid separate H1 `Hour`.
- Completed H1 rows are limited to the previous 25 days, newest first, with a maximum of 600 rows.
- Canonical deduplication can include event identity, symbol, timeframe, horizon, and model version.
- Existing ten decision histories and decision columns remain in place.
- A read-only quality report exposes source/display rows, finite values, missingness, duplicates, monotonicity, staleness, and provenance.
- Broker display conversion uses the shared provider. If a wrapper is absent, the history row’s own UTC event time is used as the display-only anchor; local PC/wall-clock time is never used as row identity.

## Field 2 — future bars from the saved path

- The renderer recursively reads stored canonical structures including `main_path`, `weighted_main`, `calibrated_close`, step-indexed frames, saved H+1/H+3/H+6 values, and saved upper/lower bands.
- It renders future bars from a valid stored point path even when interval-calibration history is sparse.
- Missing intervals are represented by a clearly labeled provisional zero-width bound; no coverage claim is made.
- Future actuals are always suppressed until settlement. Predictions and actuals remain separate.
- The Lunch helper imports no production predictor and performs no fit/train/recalculation.

## Field 3 — completed-H1 regime evidence

- Existing Lower, Middle, and Higher regime tables remain unchanged.
- One additive read-only matrix supplies up to 600 completed-H1 rows with UTC/broker time, close, 24/120/600-hour shadow regimes and z-scores, trend agreement, actionability, decision level out of 10, quality, evidence class, and settlement status.
- Every derived regime value is labeled shadow decision support and does not replace the protected production regime.

## Field 5 — question-aware grounded assistant

- Added dedicated routes for hold guidance, sessions, Field 6 evidence, and Field 7 research, alongside existing decision, entry, TP/SL, exit, regime, alpha/delta, reliability, uncertainty, forecast, similar-history, and news routes.
- Each route reads only the saved canonical snapshot and already-published evidence tables.
- Sparse evidence returns a deterministic canonical fallback or an honest unavailable statement.
- No external AI API and no heavy Lunch calculation were added.

## Fields 6 and 7 — sufficient evidence without fabricated settlement

- Stored settled histories remain primary.
- Sparse repositories can be supplemented from cached completed-H1 OHLC and prediction-time features only.
- Fallback rows carry event/broker time, close, momentum, trend, volatility, session, actionability, decision level, quality, evidence class, and settlement status.
- Fallback rows are labeled `COMPLETED_H1_SHADOW_DECISION_SUPPORT` and `NOT_A_SETTLED_OUTCOME`.
- The existing six principal Lunch gates are preserved. Field 7 is exposed through the existing Field 7/Research Lab architecture rather than adding a new principal gate or navigation item.

## Shared prediction/history quality layer

- One H1 normalization/projection module is reused by Lunch history consumers.
- It performs finite-value checks, chronological monotonicity checks, staleness flags, missingness/duplicate ratios, provenance, and canonical identity deduplication.
- No future-actual backfill, negative target shift, centered rolling window, random split, or full-sample scaler is used by the new research code.
- Outcome validation uses only matured settled outcomes with chronological ordering and overlapping-horizon embargo.

## Ten shadow-only Research Lab layers

The existing Settings research service now stores all ten requested methods under one immutable V13 result. The existing Research Lab route reads the stored catalog, contracts, warnings, sample sizes, and results without calculating.

1. A Simple Approximate Long-Memory Model of Realized Volatility.
2. Designing Realized Kernels to Measure the ex post Variation of Equity Prices in the Presence of Noise.
3. CAViaR: Conditional Autoregressive Value at Risk by Regression Quantiles.
4. Quantile Autoregression.
5. Quantile Regression Forests.
6. Data-Driven Distributionally Robust Optimization Using the Wasserstein Metric: Performance Guarantees and Tractable Reformulations.
7. Dynamic Trading with Predictable Returns and Transaction Costs.
8. Matrix Profile I: All Pairs Similarity Joins for Time Series: A Unifying View that Includes Motifs, Discords and Shapelets.
9. Robust Principal Component Analysis?
10. Dynamic Bayesian Predictive Synthesis in Time Series Forecasting.

For every layer, `research/v13_catalog.py` records the mathematical principle, input schema, prediction-time availability, outputs, failure states, computational budget, validation metrics, promotion gate, and exact EURUSD H1 benefit to Fields 1–7.

## Validation

- **Collection:** 40 test files, 426 unique tests.
- **Result:** 426 passed, 0 failed, 0 skipped, 0 errors.
- **V13 requested regressions:** 15 passed.
- **Relevant Lunch/Power BI/assistant/research regression batch:** 92 passed after final changes.
- **Compilation:** every changed Python module compiled successfully.
- **Execution:** bounded groups were used because monolithic causal/research processes exceeded the command execution limit; slow cases were isolated and passed.
- **Archive integrity:** verified separately during packaging with CRC validation.

## Accuracy and profit limitation

Improved timestamp correctness, evidence completeness, uncertainty reporting, calibration diagnostics, and data quality **do not guarantee future trading accuracy or profit**. No V13 shadow result is a validation certificate, proven edge, promotion approval, or execution instruction. Any future promotion must be supported by matured settled outcomes, chronological walk-forward testing, purging, embargo, stability checks, transaction-cost analysis, and explicit human review.
