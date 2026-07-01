# Research Limitations and Incomplete Items

The delivered ARERT layer is a working research prototype, not a fully validated thesis conclusion.

## Explicitly incomplete or approximate

- Module 1 uses empirical run-length survival as an HSMM approximation; full parametric HSMM estimation is not implemented.
- Module 3 uses a robust online changepoint proxy; full Bayesian Adams–MacKay posterior recursion is not implemented.
- Module 5 falls back to pooled conformal calibration when regime/session groups are too small.
- Module 7 uses historical empirical calibration rather than a fully trained, nested-walk-forward meta-model.
- Module 9 uses inverse recent loss rather than a full posterior dynamic Bayesian model average.
- Module 13 uses a documented baseline loss-aversion parameter until sufficient training/validation history supports selection.
- Module 17 reports timestamp-associated event effects and does not establish causality.
- Module 19 does not yet implement complete Deflated Sharpe, White Reality Check, or SPA workflows.
- Module 20 uses equal support weights. Walk-forward fitted ARERT weights are incomplete.

## Data limitations

Live outcomes, broker-clock configuration, news timestamps/entity labels, and production column availability determine what can be evaluated. Missing rows are not fabricated. A 25-day view may be too small for higher-regime, event-category, information-theoretic, and calibration conclusions.

## Performance limitation

The benchmark demonstrates repeated same-candle research-cache savings on deterministic synthetic data. It does not prove a device-wide 30–50% reduction on every phone, data feed, or live project run. Mobile peak RAM must be profiled on the target device for that claim.
