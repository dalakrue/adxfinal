# Model Card — ARERT Research Prototype

## Name and version

Adaptive Regime–Evidence Reliability Theory, `ARERT-0.3.0-RESEARCH-PROTOTYPE`.

## Intended use

Master’s/PhD research into reliability, uncertainty, regime persistence, analogue evidence, behavioral confirmation, and model stability around an existing quantitative decision system.

## Out-of-scope use

- autonomous trading or order execution;
- replacement of protected Lunch production decisions;
- guarantees of profit, correctness, or causal interpretation;
- use of incomplete rows, future data, or synthetic substitutes as production truth.

## Inputs

A frozen canonical snapshot, completed OHLC history, timestamped production decisions, and optional timestamped news. Missing sources lead to incomplete module status.

## Outputs

Twenty module records, ten Dinner fields, validation metadata, decomposed ARERT research score, CSV-ready tables, and an isolated research database.

## Performance

The included benchmark evaluates repeated same-candle module-cache behavior on deterministic synthetic data. It is not a live-market or device-wide performance guarantee.

## Ethical and scientific risks

Market non-stationarity, small samples, dependent evidence, multiple testing, selection bias, inaccurate news timestamps, proxy regimes, and over-interpretation of association can invalidate findings. The UI labels prototypes and incomplete advanced methods.

## Governance

Version all parameters and weights, preserve raw evidence, require final holdout testing, document failures, and prohibit automatic production overwrite or automatic model retirement.
