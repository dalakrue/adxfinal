# Data Dictionary

All normalized rows include: `run_id`, `origin_id`, `broker_candle_time`, `data_cutoff`, `symbol`, `timeframe`, `horizon` where applicable, `method_version`, `status`, and `created_time`.

| Table | Purpose | Key research fields | Uniqueness |
|---|---|---|---|
| `rg17_run` | Immutable complete payload by canonical run | payload hash and JSON | `run_id` |
| `rg17_forecast_origins` | Current origin forecasts | point, median, quantiles, probabilities, selected models, weights, uncertainty | origin+horizon+method |
| `rg17_horizon_outcomes` | Matured historical outcomes | maturity, actual return, settlement state, origin metrics | origin+horizon+maturity+method |
| `rg17_origin_intervals` | Origin-time conformal intervals | lower/upper, calibration count, fallback, coverage debt | origin+horizon+method |
| `rg17_probability_calibration` | Chronological calibration evidence | target, raw/calibrated probability, method, Brier/log loss/ECE/MCE, bins | origin+horizon+target+method |
| `rg17_regime_posteriors` | Hamilton posterior | regime probability, persistence, duration | origin+regime+method |
| `rg17_changepoint_posteriors` | BOCPD run-length posterior | run length, posterior, changepoint probability | origin+run length+method |
| `rg17_conditional_model_evidence` | Giacomini–White evidence | model, condition key, statistic, p-value, sample size | origin+horizon+model+condition+method |
| `rg17_model_confidence_set_results` | MCS membership/elimination | member, order, statistic, p-value, sample size | origin+horizon+model+method |
| `rg17_spa_results` | SPA evidence | gross/net improvement, statistic, bootstrap p-value, eligibility | origin+horizon+model+method |
| `rg17_dm_results` | DM comparisons | chronological block, loss difference, statistic, p-value, status | origin+horizon+model+block+method |
| `rg17_decision_impact_results` | BUY/SELL/WAIT impact | gross/net/downside, probability, weighted value, counterfactual, regret | origin+action+method |
| `rg17_validation_warnings` | Explicit limitations/errors | warning code and text | origin+warning+method |
