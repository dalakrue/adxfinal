# Research Methodology

## Research design

The system is an observational, time-series quantitative research laboratory for EURUSD H1 production evidence. Dinner research consumes a frozen completed-candle canonical snapshot; it does not alter production decisions.

## Population and sample

The unit of observation is a completed broker H1 candle. The sample may include timestamp-aligned OHLC, production decisions, multi-scale regime states, pressure, forecasts, uncertainty, internal model votes, NLP/news evidence, sessions, and settled H+1/H+3/H+6 outcomes. Each result states its actual sample period and size.

## Point-in-time feature construction

Features for a historical row use only information timestamped at or before that row. Forward returns appear only as labels after the horizon settles. The latest six rows are excluded from H+6 analogue outcome settlement. Current rows cannot match themselves.

## Validation

Experiments use expanding windows, rolling windows, walk-forward validation, purging where labels overlap, embargo periods where appropriate, and a final untouched holdout. Random train/test splitting is prohibited.

Classification reporting includes accuracy, balanced accuracy, precision, recall, F1, MCC, Brier score, log loss, calibration error, fixed-label confusion matrix, and sample size when data permit. Forecast reporting includes MAE, RMSE, direction accuracy, empirical interval coverage, width, interval score, and regime-conditioned errors.

## Module methods

1. Empirical run-length survival approximates HSMM duration behavior; full parametric HSMM fitting is future work.
2. Hierarchical states compare lower/middle/higher regime alignment without overwriting production regimes.
3. A robust online changepoint proxy is explicitly distinguished from a complete Bayesian posterior implementation.
4. Jumps are robust return outliers joined to news by valid timestamps; proximity is not causality.
5–6. Split/rolling conformal residuals create horizon intervals and temporary post-change widening.
7–8. Historical meta-label calibration and validation-only abstention thresholds preserve the primary decision.
9–10. Internal model weights use recent chronological loss and a finite research-capital scoring ledger.
11–12. Analogue distance uses standardized point-in-time features; weights combine similarity, recency, regime relevance, and quality.
13–15. Behavioral layers measure loss asymmetry, herding/fragility, and reference-point dependence.
16. Ecology tracks model fitness and deterioration without automatically disabling production models.
17. Event studies report estimated event-associated effects, not proven causality.
18. Entropy, mutual information, and redundancy identify evidence diversity; columns are never automatically deleted.
19. Chronological validity diagnostics report split periods, fold behavior, parameter stability, and PBO when feasible.
20. ARERT decomposes support and penalties using a versioned baseline.

## Reproducibility

Each module stores identity, versions, hashes, sample metadata, parameters, runtime, output, limitations, and isolated DB records. Same-candle repeats use cache only when the full cache identity matches.
