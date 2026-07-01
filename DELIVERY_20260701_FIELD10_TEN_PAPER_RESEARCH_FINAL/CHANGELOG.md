# Change Log

## Field 10 placement and lazy flow

- Added Field 10 to the main Lunch selector.
- Removed the independent bottom-of-Lunch Field 10 render call.
- Kept the legacy renderer import marker for compatibility tests only.
- Left all Lunch fields closed after Settings calculation and automatic Lunch navigation.

## Field 10 tables

- Added broker Date and Broker Candle Time to the current summary.
- Added Timeframe, Calculation Status and Canonical Run ID.
- Added separate Higher-Standard Bias and Less-Risky Bias.
- Added session, session priority, average spread, spread quality, uncertainty, error percentage, trade permission and final action.
- Added deterministic 0–100 Rank Score, Rank Grade and Rank Reason.
- Excluded blocked/no-trade rows from the eligible basic rank pool.
- Preserved the daily Higher-standard lock until broker 23:00 and allowed the existing day-end review rule.
- Added date, session, regime, rank, data-quality, bias and action filters.
- Added restrained status coloring while retaining text labels.

## Ten-paper shadow validation

- Added Hamilton-style regime probability and lifecycle diagnostics.
- Added bounded Bai-Perron-style multiple-break segmentation.
- Added vectorized ADWIN-style drift detection.
- Added incremental Kalman state filtering.
- Added Brier score, log loss and calibration bins.
- Added conformal residual intervals with minimum-sample checks.
- Added Diebold-Mariano comparison with dependence-aware variance.
- Added Hansen SPA moving-block bootstrap and explicit OOS-verification status.
- Added one shared Ledoit-Wolf covariance fit per parent run.
- Added VaR/CVaR tail-risk diagnostics.
- Added model and SPA experiment registries in SQLite.

## Safety and integrity

- No new production BUY/SELL prediction engine was introduced.
- Unsupported research values publish `INSUFFICIENT_DATA` rather than invented numbers.
- Research outputs are versioned, hashed and linked to canonical run ID, symbol, timeframe and completed broker candle.
- Research ranks use separate `ELIGIBLE_OR_CAUTION` and `BLOCKED_OR_FAILED` pools.
- Post-run integrity display does not trigger heavy calculation.
