# Ten advanced quant research foundations

1. **The Model Confidence Set — Peter R. Hansen, Asger Lunde, James M. Nason (2011)**
   - Concept: eliminate statistically inferior forecasting models while retaining a confidence set of superior models.
   - Belief: choosing one apparent winner understates model-selection uncertainty.
   - Theorem/guarantee: under the test/bootstrap conditions, the superior set contains the best model(s) at the chosen confidence level.
   - System use: evaluate RF, KNN, regime, technical, NLP and combined H1 forecasts by rolling loss; only models surviving MCS receive live display weight.

2. **Predicting Good Probabilities with Supervised Learning — Alexandru Niculescu-Mizil and Rich Caruana (2005)**
   - Concept: compare Platt scaling and isotonic regression for probability calibration.
   - Belief: ranking accuracy is not enough; a predicted 0.70 should win near 70% in comparable samples.
   - System use: calibrate BUY/SELL probabilities separately by session and regime; show Brier score, reliability curve and expected calibration error.

3. **Adaptive Conformal Inference Under Distribution Shift — Isaac Gibbs and Emmanuel Candès (2021)**
   - Concept: online adjustment of conformal miscoverage under changing distributions.
   - Belief: fixed prediction intervals fail during regime shifts.
   - Guarantee: long-run coverage frequency can track the target without assuming a stationary data-generating process.
   - System use: adapt Power BI H1 upper/lower bands and uncertainty by observed interval misses.

4. **Adaptive Conformal Predictions for Time Series — Margaux Zaffran et al. (2022)**
   - Concept: AgACI aggregates multiple adaptive-conformal learning rates for dependent time series.
   - Belief: no single adaptation speed works across calm and shock regimes.
   - System use: maintain several interval adapters and combine them by online expert weighting.

5. **Sequential Predictive Conformal Inference for Time Series — Chen Xu and Yao Xie (2022)**
   - Concept: estimate conditional quantiles of future residuals using temporal dependence.
   - Belief: residual sequence information can narrow intervals while retaining useful coverage.
   - System use: forecast H1 residual quantiles conditioned on session, volatility, regime and recent forecast errors.

6. **The Probability of Backtest Overfitting — David H. Bailey et al. (2014)**
   - Concept: combinatorially symmetric cross-validation estimates how often the selected strategy is an overfit.
   - Belief: trying many thresholds/models makes the best backtest deceptively optimistic.
   - System use: calculate PBO before promoting any reduced-WAIT threshold or new bias fusion rule.

7. **The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality — David H. Bailey and Marcos López de Prado (2014)**
   - Concept: adjust Sharpe evidence for multiple testing and non-Gaussian returns.
   - Belief: raw Sharpe is not reliable after extensive strategy search.
   - System use: require positive DSR and economic utility after spread/slippage before activating a research rule.

8. **Testing the Equality of Prediction Mean Squared Errors — Francis X. Diebold and Roberto S. Mariano (1995)**
   - Concept: test whether two forecasts have equal expected loss while accounting for serial correlation.
   - Belief: a lower sample MAE can be random noise.
   - System use: compare technical, regime, data-mining, NLP and combined H1 forecasts using directional, Brier and economic loss differentials.

9. **A Test of Superior Predictive Ability — Peter R. Hansen (2005)**
   - Concept: test whether any candidate genuinely beats a benchmark while controlling data snooping.
   - Belief: many-model searches require a multiple-comparison-aware benchmark test.
   - System use: benchmark every new research signal against the protected Field 1 decision and a no-change forecast.

10. **Learning from Time-Changing Data with Adaptive Windowing — Albert Bifet and Ricard Gavaldà (2007)**
   - Concept: ADWIN changes its effective window when statistically significant distribution change is detected.
   - Belief: stale history should lose influence automatically after drift.
   - System use: monitor feature, residual, calibration and decision-hit-rate streams; shorten training/history windows after confirmed drift and restore them gradually.

## Recommended implementation order

1. Leakage-safe walk-forward dataset and completed-candle identity.
2. Probability calibration and proper scoring.
3. MCS + SPA/DM model governance.
4. Adaptive conformal intervals.
5. ADWIN drift alarms.
6. PBO/DSR promotion gate.
7. Meta-label only after the above foundations are stable.
