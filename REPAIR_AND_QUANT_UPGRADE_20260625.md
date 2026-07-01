# Repair and Quant Upgrade — 2026-06-25

## Repairs applied

1. Fixed the Lunch Previous/Next selector crash. The buttons no longer mutate the Streamlit widget key after widget creation. They write a pending selection and rerun safely.
2. Repaired the Pre Original history-engine compatibility loader. It now discovers every shipped `part_*.py` file dynamically instead of relying on a stale hard-coded part count.
3. Verified Python compilation for the changed modules.
4. Passed 18 focused tests covering the Lunch selector, Lunch fields, Field 8, and Settings restoration.

## Important data-integrity rule

Zeros, 100%, N/A, and INSUFFICIENT must not be replaced with invented values. Field 7–9 should publish a metric only when its minimum sample, immutable generation identity, source hash, and settled-outcome requirements are satisfied. Until then, show an explicit evidence status and corrective action. This prevents false confidence while allowing the production decision logic to remain unchanged.

## Recommended implementation order

1. Restore all missing split-source folders and add a packaging test that imports every compatibility wrapper from a clean extracted ZIP.
2. Make Settings connectors submit-driven: one form submit writes encrypted/session configuration, tests the connector once, stores success/failure, and does not reconnect on normal reruns.
3. Preserve the current Field 2 path. Add a read-only green lower-risk path derived from already-published Field 1 decision history, Field 2 intervals, and Field 3 regime reliability. It must not replace the protected path or decision.
4. Store red, blue, yellow, and green path snapshots in one 25-day ledger keyed by run_id, generation_id, broker candle, horizon, source hash, and settlement status.
5. Move the assistant renderer to the independent AI Assistant route. Keep exactly one current question and one current answer in session state; clear the prior answer on every new submit.
6. Use lazy imports and one selected Lunch field at a time; cache immutable data, not rendered widgets.
7. Batch SQLite writes in one transaction after a successful canonical calculation; use WAL and indexed run/generation/time columns.
8. Add profiling gates. Claim 30–50% reduction only when before/after peak RSS, CPU time, wall time, import time, and ZIP size measurements demonstrate it.

## Ten research directions

1. Adaptive Conformal Predictions for Time Series — adaptive, distribution-shift-aware prediction intervals.
2. Sequential Predictive Conformal Inference for Time Series — residual-quantile modelling under temporal dependence.
3. Adaptive Conformal Inference for Multi-Step Ahead Time Series — horizon-specific coverage control.
4. Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting — feature gating and interpretable multi-horizon attention.
5. Learning from Time-Changing Data with Adaptive Windowing — statistically controlled drift-window resizing.
6. Learning under Concept Drift: A Review — detect, understand, and adapt to changing distributions.
7. The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality — controls false discoveries from repeated strategy testing.
8. White's Reality Check — tests whether the best observed rule beats a benchmark after data snooping.
9. A Test for Superior Predictive Ability (Hansen SPA) — more powerful multiple-model comparison against a benchmark.
10. Diebold–Mariano predictive-accuracy testing — compares forecast loss series without treating small sample differences as proof.

## Acceptance tests still required with live dependencies/data

- Clean-environment `pip install -r requirements.txt` and Streamlit startup test.
- Twelve Data/MT5/Finnhub one-click connection tests with real credentials.
- A completed H1 canonical run that populates 25-day ledgers and settles outcomes.
- Before/after CPU, RAM, and calculation-time profiling on the deployment machine.
- Mobile browser test for copy buttons, API-key paste, Field selector, and AI question submission.
