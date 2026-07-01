# Copy-Paste Implementation Command

Use the supplied audited project as the only source and return one complete tested ZIP.

## Critical protection rules

1. Do not delete, reduce, rename, move, replace, bypass, simplify, or change any existing calculation, prediction engine, production formula, strategy rule, model weight, metric, history table, database table, copy function, connector, Lunch field, tab, UI section, expected hash, or canonical snapshot field.
2. Do not add a top-level tab, page, sidebar item, or menu item.
3. Heavy calculations may run only from Settings → Run Calculation + Open Lunch.
4. Lunch must read one saved immutable canonical snapshot and must never perform heavy recalculation.
5. Preserve Python 3.12 and Streamlit Cloud compatibility.
6. Use only information available at prediction time. Use only matured settled outcomes for validation. Enforce chronological ordering, purging, and overlapping-horizon embargo.
7. Every new research method must begin shadow-only and must not change production BUY/SELL/WAIT decisions, protected weights, or execution behavior.
8. Do not invent missing rows, outcomes, confidence, certificates, forecast accuracy, market data, or validation results.
9. Keep every wrapper and field module below the existing architecture line limits; split implementation into bounded helper modules when needed.

## Field 1 — force true H1 25-day history

- Trace the exact source renderer and repository used by Field 1.
- When legacy history contains separate Date and Hour columns, combine them into one timezone-aware UTC event timestamp before filtering, freshness checks, deduplication, ordering, broker-time conversion, or display.
- Never select Date alone when Hour is available.
- Return distinct completed H1 candles for the previous 25 days, newest first, up to 600 rows.
- Preserve the existing decision columns and all ten decision histories.
- Use the shared canonical broker-time provider for display; never use local PC time or datetime.now/utcnow as row identity.

## Field 2 — future bar chart must use the saved prediction path

- Read the canonical saved prediction bundle recursively, including compatible keys such as main_path, weighted_main, calibrated_close, step-indexed forecast frames, 1h/3h/6h values, and saved upper/lower bands.
- Render future bars whenever a valid saved path exists, even when interval-calibration history is sparse.
- When bounds are unavailable, show the point forecast with a clearly provisional zero-width bound rather than hiding the chart.
- Never compute a new forecast inside Lunch and never display a future actual before settlement.
- Preserve existing production prediction formulas and weights.

## Field 3 — fill unused space with 25-day H1 regime evidence

- Preserve the existing Lower, Middle, and Higher standard tables exactly.
- Add one read-only 25-day completed-H1 regime decision matrix below them, up to 600 rows.
- Include H1 event/broker time, close, lower 24H regime, middle 120H regime, higher 600H regime, their z-scores, trend agreement, actionability, decision level /10, data quality, evidence class, and settlement status.
- Clearly mark derived rows as shadow decision support and never replace the protected production regime.

## Field 5 — grounded assistant must understand the question

- Use a question-aware intent/evidence router as the primary answer path.
- Read only the saved canonical snapshot and already-published Lunch/Research evidence.
- Support questions about decision, entry, hold, TP, exit risk, regime, alpha, delta, reliability, uncertainty, prediction path, similar history, news, session, Field 6, and Field 7.
- Select evidence relevant to the actual question rather than returning one generic summary.
- Provide a deterministic canonical fallback when evidence is sparse.
- Do not call external AI APIs and do not trigger heavy calculations from the assistant.
- State missing evidence honestly instead of hallucinating.

## Fields 6 and 7 — sufficient, efficient decision-level evidence

- Keep settled stored research/validation histories as the primary source.
- When those repositories are sparse, supplement them with completed-H1 evidence derived only from cached canonical OHLC and prediction-time features.
- Show up to 25 days of H1 rows with time, close, momentum/trend, volatility/session evidence, actionability, decision level, data-quality score, evidence class, and settlement status.
- Label fallback rows COMPLETED_H1_SHADOW_DECISION_SUPPORT and NOT_A_SETTLED_OUTCOME.
- Never fabricate a validation certificate, proven edge, settled outcome, promotion status, or production decision.

## Prediction-path and history data-quality improvements

- Add shared timestamp normalization and one causal completed-H1 projector used by all Lunch history fields.
- Deduplicate by canonical event identity, symbol, timeframe, horizon, and model/version where applicable.
- Add finite-value checks, monotonic-time checks, stale-data flags, missingness ratios, duplicate ratios, and source provenance.
- Keep actuals and predictions in separate columns and prohibit future actual leakage.
- Improve uncertainty display and coverage diagnostics without claiming guaranteed accuracy.

## Next ten shadow-only research layers

Add Research Lab implementations and compact Lunch summaries for:

1. Fulvio Corsi — A Simple Approximate Long-Memory Model of Realized Volatility.
2. Barndorff-Nielsen, Hansen, Lunde, Shephard — Designing Realized Kernels to Measure the ex post Variation of Equity Prices in the Presence of Noise.
3. Engle and Manganelli — CAViaR: Conditional Autoregressive Value at Risk by Regression Quantiles.
4. Koenker and Xiao — Quantile Autoregression.
5. Meinshausen — Quantile Regression Forests.
6. Esfahani and Kuhn — Data-Driven Distributionally Robust Optimization Using the Wasserstein Metric: Performance Guarantees and Tractable Reformulations.
7. Gârleanu and Pedersen — Dynamic Trading with Predictable Returns and Transaction Costs.
8. Yeh et al. — Matrix Profile I: All Pairs Similarity Joins for Time Series: A Unifying View that Includes Motifs, Discords and Shapelets.
9. Candès, Li, Ma, Wright — Robust Principal Component Analysis?
10. McAlinn and West — Dynamic Bayesian Predictive Synthesis in Time Series Forecasting.

For each layer, document the mathematical principle, input schema, prediction-time availability, outputs, failure states, computational budget, validation metrics, promotion gate, and exact benefit to EURUSD H1 Fields 1–7.

## Required tests

- Date + Hour combines into distinct H1 timestamps and never collapses to D1 rows.
- Field 1 returns completed H1 rows across 25 days in descending time order.
- Field 2 renders 1H/3H/6H future bars from a saved canonical path with and without saved intervals.
- No Lunch renderer recalculates the prediction engine.
- Field 3 keeps all existing standard tables and adds the 25-day H1 matrix.
- Field 5 routes different questions to different relevant evidence and never recalculates.
- Fields 6 and 7 show decision-support evidence when settled repositories are sparse while clearly preserving unsettled status.
- No look-ahead, no overlapping-horizon leakage, no fabricated settlement.
- Existing protected architecture, expected hashes, production weights, tabs, copy functions, connectors, and Streamlit Cloud preflight tests remain green.
- Compile all changed modules and run the complete test suite in bounded chunks if one monolithic process exceeds the execution limit.

## Delivery

Return a complete ZIP, a changed-file list, a concise fix report, exact test totals, and a transparent statement that improved data quality and calibration do not guarantee future trading accuracy or profit.
