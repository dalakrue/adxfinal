# Unified Research-Grade Shadow Architecture

## Boundary

The implementation is an additive sidecar. It consumes the completed immutable Field 1 canonical snapshot and matured historical records. It never writes Field 1, never recalculates production formulas, and never changes BUY, SELL, WAIT, or the production regime.

Heavy work is reachable only through Settings → Run Calculation + Open Lunch. Fields 2–9 render the saved `research_grade_system_v17_20260624` payload through closed, read-only expanders. Repeated publication of the same `run_id` loads the immutable stored payload rather than recomputing it.

## Shared contract

Every current research output carries `run_id`, `origin_id`, symbol, timeframe, broker candle time, data cutoff, method/model version, feature-schema hash where applicable, and status. Contract validation rejects mixed run IDs, mixed broker times, future feature timestamps, future data cutoffs, and actuals recorded before maturity.

## Field 2

H1, H3, and H6 are evaluated independently. Each origin stores point/median/quantile forecasts, immutable conformal bounds, raw and calibrated direction probabilities, shadow model membership/weights, uncertainty, disagreement, fallback reason, and evidence status. MAE, RMSE, signed bias, directional accuracy, Brier score, log loss, CRPS, coverage, width, Winkler score, calibration error, and after-cost directional value remain horizon-specific.

## Field 3

A three-state Hamilton filter and recursive Bayesian online changepoint detector are independent shadow layers. The payload includes posterior probabilities, persistence, transition probabilities, expected/remaining duration, changepoint probability, run-length posterior, hysteresis warning state, production/shadow agreement, confusion matrix, and evidence sufficiency. The production regime is read-only.

## Validation and model governance

The sidecar includes chronological Platt, isotonic, and beta calibration; Giacomini–White conditional evidence; dependence-aware Model Confidence Sets; Hansen SPA; overlapping-horizon Diebold–Mariano tests with HAC and small-sample correction; a multi-horizon comparison summary; and a CPU-safe TFT-inspired sparse gated fusion layer. The large transformer path is disabled by default.

## Storage

The migration is additive and idempotent. Normalized tables store forecast origins, matured horizon outcomes, origin intervals, calibration, regime/changepoint posteriors, conditional evidence, MCS, SPA, DM, decision impact, and warnings. Unique constraints prevent duplicate rerun writes; origin rows use insert-ignore semantics to prevent historical interval rewrites.
