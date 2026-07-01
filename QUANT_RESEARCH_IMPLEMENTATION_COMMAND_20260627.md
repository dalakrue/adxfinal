# Detailed implementation command — Quant research reliability upgrade

Inspect the complete ADX Quant Pro project and implement the following as additive, research-bounded modules. Preserve every protected production calculation and decision rule. Do not fabricate history, sample size, accuracy, calibration, uncertainty, outcomes, model evidence, news, or performance improvement. All training, fitting, calibration, settlement, and research computation must run only inside Settings → Run Calculation + Open Lunch. Every renderer must remain read-only and consume the same immutable canonical run_id, generation_id, source snapshot hash, symbol, timeframe, and completed broker H1 candle.

## 1. Adaptive Conformal Predictions for Time Series
Add online adaptive interval calibration to the existing Power BI forecast residuals. Maintain separate nonconformity queues by horizon, regime, session, and volatility bucket. Update interval width only after outcomes settle. Publish nominal coverage, empirical coverage, coverage gap, interval width, calibration sample count, and fallback reason. Never move the protected central path.

## 2. Sequential Predictive Conformal Inference for Time Series
Model the next residual quantile from lagged settled residuals using a bounded, purged, chronological procedure. Use it only to improve lower/upper bands. Fall back to global conformal quantiles when the conditional residual model lacks evidence. Prohibit future leakage and overlapping-label leakage.

## 3. On Calibration of Modern Neural Networks
Calibrate BUY/SELL/WAIT probabilities with temperature scaling or multinomial calibration fitted only on settled chronological predictions. Report ECE, Brier score, log loss, reliability bins, sample count, and pre/post calibration metrics. Calibration may lower confidence or force WAIT but must never reverse the protected direction.

## 4. Conformalized Quantile Regression
Add quantile models for lower and upper forecast bounds, then conformalize them using a separate chronological calibration window. Keep central prediction unchanged. Publish quantile crossing checks, corrected coverage, interval sharpness, and fallback status.

## 5. A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle
Add a shadow Markov-switching regime layer using return, realized volatility, trend persistence, and spread/session proxies. Estimate transition probabilities and expected state duration. Use this only as regime evidence and reliability adjustment; do not replace the protected regime engine.

## 6. Regime Changes and Financial Markets
Create regime-conditioned validation tables for forecast error, direction accuracy, TP/SL touch order, interval coverage, and decision coverage. Require sufficient settled observations before a regime-specific statistic can influence confidence. Otherwise use a transparent global fallback.

## 7. The Probability of Backtest Overfitting
Implement combinatorially symmetric cross-validation or a practical purged approximation for candidate research models and thresholds. Publish probability of backtest overfitting, rank stability, and selection count. Do not promote a research candidate merely because it has the best in-sample score.

## 8. The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality
For every research strategy or decision overlay, calculate a deflated Sharpe ratio using the number of trials, skewness, kurtosis, and sample length. Do not use Sharpe alone. Block promotion when the deflated statistic is not supported.

## 9. The Model Confidence Set
Compare existing forecast contributors using loss series from settled forecasts, such as absolute error, CRPS, directional loss, and interval score. Retain a confidence set of statistically indistinguishable models instead of selecting one winner. Convert the confidence set into bounded display weights; never overwrite protected production weights.

## 10. Advances in Financial Machine Learning — Meta-Labeling and Purged Cross-Validation concepts
Add a meta-label that estimates whether the protected BUY/SELL decision is actionable, not its direction. Inputs may include regime reliability, calibrated confidence, interval width, session, drift, disagreement, and liquidity proxies. The only permitted actions are CONFIRM, REDUCE SIZE, PROTECT, or WAIT. Use purged chronological validation and embargo around overlapping H1–H6 labels.

## Mandatory engineering rules

- One canonical calculation transaction per button click.
- Use the latest completed broker H1 candle only.
- Store settled forecast outcomes separately from pending forecasts.
- Every research table must include origin time, target time, settlement time, run_id, generation_id, snapshot hash, horizon, regime, session, sample count, and evidence status.
- No random train/test split for time series.
- Apply purge and embargo for overlapping horizons.
- Fit scalers, calibrators, thresholds, and models inside each training fold only.
- Use deterministic seeds and bounded memory.
- Preserve mobile performance by storing compact summaries and lazy-rendering detailed histories.
- Add unit tests for leakage, canonical identity, broker-time alignment, insufficient-evidence fallback, calibration monotonicity, and no-direction-reversal policy.
- Add promotion gates: minimum sample size, positive out-of-sample skill, stable calibration, acceptable coverage, no identity mismatch, and no protected-hash change.
