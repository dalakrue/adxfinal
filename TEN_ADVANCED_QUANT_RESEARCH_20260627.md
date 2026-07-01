# Ten Advanced Quant Research Foundations for ADX Quant Pro

## 1. The Probability of Backtest Overfitting — Bailey, Borwein, López de Prado, Zhu
Concept: combinatorially symmetric cross-validation estimates how often the selected strategy is an in-sample winner but an out-of-sample loser.
Belief: choosing the best result from many trials creates selection bias even when each test appears reasonable.
Theorem/logic: partition observations into symmetric train/test combinations; rank candidates in-sample and measure the out-of-sample relative rank of the selected candidate. The estimated probability of a negative out-of-sample logit is PBO.
System benefit: apply CSCV to every proposed threshold, model weight, Table 4 tie-break and regime rule before promotion. Store PBO beside each candidate. Reject changes with high PBO even if headline accuracy improves.

## 2. The Model Confidence Set — Hansen, Lunde, Nason
Concept: produce a statistically defensible set of models that cannot yet be distinguished from the best model under a chosen loss.
Belief: selecting one apparent winner ignores estimation uncertainty and correlated forecast errors.
Theorem/logic: repeatedly test equal predictive ability and eliminate the worst model until the null can no longer be rejected. Bootstrap loss differentials to preserve dependence.
System benefit: maintain an eligible ensemble set separately for direction, price, interval and regime losses. Do not force red=100% simply because one model recently ranks first; exclude only statistically inferior models.

## 3. Strictly Proper Scoring Rules, Prediction, and Estimation — Gneiting and Raftery
Concept: score full predictive distributions using losses that make truthful probabilities optimal.
Belief: accuracy alone encourages overconfident or strategically distorted forecasts.
Theorem/logic: a scoring rule is strictly proper when the expected score is uniquely optimized by reporting the true distribution. Use log score/Brier for direction, CRPS for a continuous price distribution and energy score for multivariate paths.
System benefit: drive model weights from rolling proper scores rather than hit rate alone. Separate sharpness from calibration and prevent a narrow but wrong forecast band from looking good.

## 4. Accurate Uncertainties for Deep Learning Using Calibrated Regression — Kuleshov, Fenner, Ermon
Concept: post-calibrate any regression model's predictive CDF so nominal probabilities match empirical frequencies.
Belief: a stated 80% interval is not useful unless it covers near 80% out of sample.
Theorem/logic: learn a monotone calibration mapping from predicted CDF values to empirical CDF frequencies; under sufficient calibration data, coverage converges to nominal calibration.
System benefit: recalibrate Power BI upper/lower bands by regime and horizon. Display raw and calibrated coverage, sample size, expiry and drift status. Disable confidence claims when the calibration window is too small.

## 5. Distribution-Free Predictive Inference for Regression — Lei, G'Sell, Rinaldo, Tibshirani, Wasserman
Concept: conformal prediction creates finite-sample prediction intervals with distribution-free marginal coverage under exchangeability.
Belief: uncertainty should have an explicit coverage guarantee instead of being an arbitrary volatility multiple.
Theorem/logic: use held-out conformity residuals; the appropriate empirical quantile expands the next prediction into an interval with at least approximately 1-alpha marginal coverage.
System benefit: add split-conformal H+1/H+3/H+6 bands and regime-conditional diagnostics. Use adaptive fallback to pooled calibration when regime samples are too small.

## 6. Conformalized Quantile Regression — Romano, Patterson, Candès
Concept: combine quantile regression's heteroskedastic intervals with conformal finite-sample calibration.
Belief: interval width should adapt to market conditions while retaining valid coverage.
Theorem/logic: estimate lower/upper conditional quantiles, calculate conformity errors on calibration data, and widen both bounds by a calibrated residual quantile.
System benefit: make bands widen during event clusters/high volatility and narrow in stable conditions for evidence-based reasons, not hard-coded visual rules. This directly improves TP-touch/SL-touch probability inputs.

## 7. A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle — James D. Hamilton
Concept: Markov-switching models represent latent regimes with probabilistic transitions.
Belief: financial dynamics are not governed by one fixed parameter set; states persist and transition stochastically.
Theorem/logic: latent state probabilities are updated recursively through transition probabilities and state-conditional likelihoods; filtered and smoothed probabilities distinguish current and historical regimes.
System benefit: estimate BULL/BEAR/RANGE/VOLATILE state probabilities, expected duration 1/(1-p_ii), transition risk and uncertainty. Avoid deterministic regime labels when posterior probability is diffuse.

## 8. Learning from Time-Changing Data with Adaptive Windowing — Bifet and Gavaldà
Concept: ADWIN detects drift by maintaining a variable-length window and testing whether two subwindows have significantly different means.
Belief: old observations should be removed only when there is statistical evidence of change, not using an arbitrary fixed lookback.
Theorem/logic: Hoeffding-style bounds control false drift alarms while identifying significant distribution changes.
System benefit: monitor proper score, calibration error, directional loss, feature distributions and API-source differences. On drift, shorten calibration/training windows, lower reliability and freeze automatic weight promotion.

## 9. A Reality Check for Data Snooping — Halbert White
Concept: correct performance significance when many strategies/models were searched on the same dataset.
Belief: the maximum observed performance is biased upward by repeated experimentation.
Theorem/logic: bootstrap the distribution of the maximum performance differential under the null that no candidate beats the benchmark.
System benefit: every batch of experimental indicators, thresholds or research-paper modules must pass a data-snooping-adjusted test against rolling mean/previous close/no-trade benchmarks before entering production.

## 10. Superior Predictive Ability — Peter R. Hansen
Concept: test whether the best candidate forecast is genuinely superior to a benchmark while reducing the influence of very poor alternatives.
Belief: White's Reality Check can lose power when many irrelevant bad models are included.
Theorem/logic: studentized loss differentials and a data-dependent recentering produce a more powerful bootstrap test of superior predictive ability.
System benefit: use SPA as the promotion gate for new Power BI models, regime classifiers and Table 4 fusion variants. Combine it with MCS: SPA answers “does anything beat the benchmark?” and MCS answers “which models remain statistically competitive?”

# Recommended implementation order

1. Proper-score registry and settled-forecast ledger.
2. Walk-forward/CSCV evaluation with PBO.
3. Benchmark-adjusted Reality Check and SPA.
4. MCS ensemble eligibility.
5. Regression calibration and conformal intervals.
6. Drift detection and adaptive windows.
7. Markov-switching regime lifecycle.
8. Only then permit dynamic thresholds or model-weight changes under shadow mode and immutable audit logs.
