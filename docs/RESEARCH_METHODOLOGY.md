# Research Methodology

## Research questions

1. Does calibrated selective prediction improve EURUSD H1 decision reliability?
2. Does regime-conditioned calibration outperform global calibration?
3. Does meta-labeling reduce false BUY and false SELL actions?
4. Do adaptive conformal intervals improve empirical coverage?
5. Does Bellman interval control reduce width without damaging coverage?
6. Does multi-scale volatility improve WAIT PULLBACK classification?
7. Does event-response memory outperform plain sentiment?
8. Does CRCEF-SV outperform each individual evidence family?
9. Does drift-aware model blocking improve out-of-sample stability?
10. Does the complete framework remain effective after transaction costs?

## Hypotheses

- **H1:** CRCEF-SV produces a lower Brier score than the uncalibrated baseline.
- **H2:** Meta-labeling reduces false actionable signals without materially reducing profitable-signal recall.
- **H3:** Regime-conditioned conformal intervals achieve coverage closer to target than fixed-width intervals.
- **H4:** The complete framework produces higher leakage-safe expected utility than any individual module.

## Observation unit

One completed EURUSD H1 MetaTrader broker candle. Features, labels, forecasts, and outcomes are aligned to this unit. A row may use only information available at its completed candle.

## Data partitions

Chronological training, calibration, validation, and untouched test windows are separate. Overlapping label intervals are purged and an embargo is applied. Hyperparameters are selected through CPCV paths rather than one split.

## Outcome settlement

Forecast outcomes remain pending until the target broker candle completes. The system never fills incomplete outcomes from future candles. Event-response memory likewise excludes historical events whose response horizon was not already settled at the evaluated candle.

## Evaluation

Proper probability scores (Brier, log loss, ECE), directional and class metrics, interval coverage and width, expected utility after costs, maximum drawdown, turnover, PBO, path stability, and ablation results are reported together. Accuracy alone cannot promote a model.
