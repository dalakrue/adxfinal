# Next 10 Quant Research Layers for EURUSD H1 Lunch Architecture

All layers must start shadow-only, use information available at prediction time, read the canonical run snapshot, and remain unable to alter production decisions until chronological validation and promotion gates pass.

## 1. A Simple Approximate Long-Memory Model of Realized Volatility — Fulvio Corsi

**Core principle:** Realized volatility at short, medium, and long horizons can be represented with a heterogeneous autoregressive structure. Daily, weekly, and monthly components approximate long-memory behavior without a heavy fractional-integration model.

**System integration:** Build completed-H1 realized-volatility features over 24H, 120H, and 600H windows. Store them in Research Lab and expose compact volatility-state summaries in Field 3 and interval-width inputs in Field 2.

**Benefit:** Better volatility persistence estimates, more stable regime duration estimates, and prediction bands that expand or contract with multi-horizon volatility rather than one noisy rolling standard deviation.

## 2. Designing Realized Kernels to Measure the ex post Variation of Equity Prices in the Presence of Noise — Barndorff-Nielsen, Hansen, Lunde, and Shephard

**Core principle:** High-frequency realized variance is distorted by market microstructure noise. Realized kernels use autocovariance-weighted estimators to recover ex-post variation more robustly under noise.

**System integration:** For M1-derived evidence, compute a shadow realized-kernel volatility estimate only from completed bars. Compare it with ordinary realized variance and write a quality flag when the two diverge materially.

**Benefit:** Cleaner M1-to-H1 volatility features, fewer false high-volatility alerts, and more reliable Field 6 session/overlap evidence.

## 3. CAViaR: Conditional Autoregressive Value at Risk by Regression Quantiles — Robert F. Engle and Simone Manganelli

**Core principle:** Model the selected conditional quantile directly as an autoregressive process instead of assuming a full return distribution.

**System integration:** Fit causal lower and upper return quantiles for 1H, 3H, and 6H horizons. Use them as a shadow tail-risk layer beside the existing prediction bands; never overwrite protected bands until coverage tests pass.

**Benefit:** Better asymmetric downside/upside risk estimates and fewer misleading symmetric intervals during shocks.

## 4. Quantile Autoregression — Roger Koenker and Zhijie Xiao

**Core principle:** Autoregressive coefficients may differ across quantiles, allowing conditioning variables to change the location, scale, and shape of the future distribution.

**System integration:** Estimate non-crossing shadow quantiles for the EURUSD H1 path using lagged returns, volatility, session, regime, alpha, delta, and prediction disagreement. Enforce chronological training and quantile monotonicity checks.

**Benefit:** A distributional future path rather than one mean path, stronger tail diagnostics, and more informative Field 2 future bars.

## 5. Quantile Regression Forests — Nicolai Meinshausen

**Core principle:** Random-forest neighborhood weights can estimate the full conditional response distribution and conditional quantiles non-parametrically.

**System integration:** Train a lightweight shadow QRF on settled H1 examples only. Predict 10th/25th/50th/75th/90th percentiles for each horizon and compare its coverage and width with the existing path.

**Benefit:** Captures nonlinear interactions among regime, session, trend, volatility, and news features while producing calibrated distributional outputs.

## 6. Data-Driven Distributionally Robust Optimization Using the Wasserstein Metric: Performance Guarantees and Tractable Reformulations — Peyman Mohajerin Esfahani and Daniel Kuhn

**Core principle:** Optimize against a Wasserstein ambiguity set around the empirical distribution, providing robustness to sampling error and distribution shift under stated assumptions.

**System integration:** Use a shadow robust decision gate that asks whether BUY, SELL, or WAIT retains positive expected utility across plausible nearby distributions. Feed the result only into Research Lab and a Field 7 evidence column.

**Benefit:** Reduces overconfident decisions from small or unstable samples and makes WAIT more principled during drift.

## 7. Dynamic Trading with Predictable Returns and Transaction Costs — Nicolae Gârleanu and Lasse H. Pedersen

**Core principle:** With predictable returns and trading costs, the optimal policy aims ahead of the current target and trades only partially toward that aim.

**System integration:** Add a shadow cost-aware actionability score using spread, forecast decay, signal half-life, horizon, and turnover. Do not execute orders or modify protected production decisions.

**Benefit:** Prevents weak H1 forecasts from being treated as actionable when expected edge is smaller than trading friction; improves the meaning of decision level and WAIT.

## 8. Matrix Profile I: All Pairs Similarity Joins for Time Series: A Unifying View that Includes Motifs, Discords and Shapelets — Yeh et al.

**Core principle:** The matrix profile stores nearest-neighbor distances for every subsequence and unifies motif discovery, anomaly detection, and shapelet-style pattern analysis.

**System integration:** Build causal H1 subsequences from returns, range, volatility, and direction. For the current window, retrieve prior similar completed windows and their settled 1H/3H/6H outcomes. Exclude overlapping and embargoed examples.

**Benefit:** Gives Fields 6 and 7 useful historical analog evidence, detects novel market states, and improves assistant answers about “what happened in similar conditions?”

## 9. Robust Principal Component Analysis? — Emmanuel Candès, Xiaodong Li, Yi Ma, and John Wright

**Core principle:** Under suitable incoherence and sparsity assumptions, a data matrix can be decomposed into low-rank structure plus sparse corruption through Principal Component Pursuit.

**System integration:** Apply shadow RPCA to the feature/history matrix to separate persistent common structure from isolated bad ticks, missing-value artifacts, API spikes, and abnormal news shocks. Keep original values and record correction flags rather than silently replacing production data.

**Benefit:** Higher history-table data quality, more stable model inputs, and clear anomaly provenance.

## 10. Dynamic Bayesian Predictive Synthesis in Time Series Forecasting — Kenichiro McAlinn and Mike West

**Core principle:** Dynamically synthesize forecast densities while adapting to time-varying bias, miscalibration, and dependence among contributing models.

**System integration:** Combine the existing protected path, quantile autoregression, QRF, HAR-volatility interval layer, and similar-pattern forecast as shadow agents. Learn horizon-specific dynamic weights only from matured outcomes.

**Benefit:** Improves resilience when one model becomes biased, provides a coherent combined path and uncertainty distribution, and supplies transparent per-model contribution evidence for Field 2 and the assistant.

## Recommended implementation order

1. Realized kernels and RPCA for input quality.
2. HAR-RV for multi-horizon volatility state.
3. CAViaR and Quantile Autoregression for direct tail/path distributions.
4. Quantile Regression Forests for nonlinear conditional distributions.
5. Matrix Profile for causal historical analogs.
6. Dynamic Bayesian Predictive Synthesis for model combination.
7. Wasserstein robustness and transaction-cost actionability as final shadow decision gates.

## Required validation for every layer

- Settled outcomes only.
- Strict event-time ordering.
- Purged walk-forward folds.
- Overlapping-horizon embargo.
- No current/future candle leakage.
- Coverage, calibration, Brier/log score or pinball loss as appropriate.
- Regime/session breakdown.
- Minimum sample and effective-sample-size gate.
- Drift and stability checks.
- Shadow-only until explicit promotion criteria pass.
