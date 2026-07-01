# ADX Quant Pro — Final Performance, Mobile, Copy, Refresh and Research Report

## Protected scope
No trading formula, BUY/SELL/WAIT rule, threshold, regime formula, prediction calculation, Field 1 source-of-truth calculation, or protected numerical behavior was changed.

## Implemented runtime improvements
1. **Current-copy payload cache by canonical generation** — Copy Short and Copy Full are serialized once when the canonical identity changes and reused on Streamlit reruns. This removes repeated full-payload construction while navigating Lunch.
2. **Mobile-safe copy layout** — phone mode stacks the two clipboard components vertically, avoiding cramped side-by-side iframes and transparent overlay interception.
3. **Refresh API Data + Quick Sync Fields 1–3** — Lunch now has one button that calls the existing EURUSD H1 refresh service once, uses the existing Quick Fields 1–3 reuse/orchestration path, invalidates stale copy caches, and reruns against the new canonical generation.
4. **Single-field rendering preserved** — only the selected Lunch field is rendered/imported; unselected fields remain idle.
5. **No history in copy payloads** — current-generation Fields 1–3 only; unavailable placeholders and historical frames remain excluded.

## Validation
- Python compilation: passed for changed files and the active app/core/ui/tabs/services trees.
- Focused regression suite: **24 passed**.
- Covered Lunch field selection, one-click freshness/copy behavior, quick-source signatures, and navigation/quick-decision contracts.
- Full local Streamlit startup could not be executed in the packaging container because Streamlit is not installed there. The repository requirements retain Streamlit for deployment.

## 10 advanced quant research foundations for a future shadow layer
These should first be implemented as leakage-safe, read-only shadow evidence. Do not replace production truth until walk-forward evidence is strong.

### 1. The Probability of Backtest Overfitting — Bailey, Borwein, López de Prado, Zhu
**Concept:** Combinatorially Symmetric Cross-Validation estimates the probability that the best in-sample configuration will rank poorly out of sample.
**Belief:** Choosing the best result from many trials creates selection bias even when each individual backtest appears valid.
**Theorem/metric:** PBO is estimated from the distribution of out-of-sample logit ranks across combinatorial train/test partitions.
**System benefit:** Evaluate Field 1–3 thresholds, session adaptations, and direction-confirmation variants without trusting a single walk-forward split. Publish PBO as a reliability penalty, not a trading decision.

### 2. The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality — Bailey & López de Prado
**Concept:** Adjust observed Sharpe for multiple trials, sample length, skewness, and kurtosis.
**Belief:** A high raw Sharpe can be a statistical accident after many experiments.
**Theorem/metric:** DSR estimates the probability that an observed Sharpe exceeds an adjusted benchmark under non-normal returns.
**System benefit:** Gate promotion of new shadow filters and session-conditioned paths; require positive DSR before enabling any production influence.

### 3. A Reality Check for Data Snooping — Halbert White
**Concept:** Bootstrap the maximum performance across many candidate rules under a joint null.
**Belief:** Reusing the same EURUSD history for many ideas inflates apparent significance.
**Theorem/metric:** Reality Check p-value for the best rule after accounting for the entire tested family.
**System benefit:** Test all decision-score weight variants as one family; reject upgrades whose advantage disappears after data-snooping correction.

### 4. A Test for Superior Predictive Ability — Peter R. Hansen
**Concept:** A more powerful, studentized alternative to White’s Reality Check that reduces the influence of poor alternatives.
**Belief:** Comparison should focus on whether any candidate truly beats the protected benchmark, not on irrelevant weak models.
**Theorem/metric:** SPA bootstrap p-value using studentized loss differentials and a sample-dependent null.
**System benefit:** Compare shadow direction confirmation, path calibration, and session filters against the current production logic using directional loss, pinball loss, and trading utility.

### 5. A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle — James D. Hamilton
**Concept:** Latent Markov regimes generate different parameter states with probabilistic transitions.
**Belief:** EURUSD H1 behavior changes across persistent hidden states rather than one fixed distribution.
**Theorem/metric:** Hamilton filter and smoother estimate state probabilities and transition matrix probabilities.
**System benefit:** Add a shadow regime-probability panel beside the existing protected regime detector; use disagreement to lower reliability rather than overwrite the regime.

### 6. Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models — Robert F. Engle
**Concept:** Correlations vary through time while conditional volatilities follow GARCH-like dynamics.
**Belief:** EURUSD’s relation to volatility, dollar proxies, rates, and session behavior is nonconstant.
**Theorem/metric:** DCC decomposes conditional covariance into univariate volatility processes and a dynamic correlation matrix.
**System benefit:** Build a shadow instability metric that detects when historical analogues or cross-market evidence have become unreliable.

### 7. Strictly Proper Scoring Rules, Prediction, and Estimation — Gneiting & Raftery
**Concept:** A forecast should be evaluated with a scoring rule minimized only by reporting the true predictive distribution.
**Belief:** Accuracy alone encourages overconfident 0%/100% probabilities and hides poor uncertainty estimates.
**Theorem/metric:** Log score, Brier score, CRPS, and related strictly proper scores.
**System benefit:** Replace cosmetic reliability percentages in shadow evaluation with Brier/log score for direction probabilities and CRPS/pinball loss for the Power BI path and intervals.

### 8. On Calibration of Modern Neural Networks — Guo, Pleiss, Sun, Weinberger
**Concept:** Predictive confidence can be recalibrated after model fitting, commonly with temperature scaling.
**Belief:** Ranking ability and probability correctness are different properties.
**Theorem/metric:** Expected Calibration Error, reliability diagrams, and temperature-scaled probabilities.
**System benefit:** Calibrate BUY/SELL probability displays by session and regime; never show 0% or 100% unless mathematically forced and sufficiently supported.

### 9. Distribution-Free Predictive Inference for Regression — Lei, G’Sell, Rinaldo, Tibshirani, Wasserman
**Concept:** Conformal prediction creates finite-sample prediction sets under exchangeability with minimal model assumptions.
**Belief:** A point forecast without empirical coverage is incomplete.
**Theorem/metric:** Split-conformal interval with marginal coverage at least 1−alpha under exchangeability.
**System benefit:** Add shadow 1h/3h/6h interval bands around the protected central path, calibrated separately by session and volatility regime; publish coverage and width.

### 10. Learning from Time-Changing Data with Adaptive Windowing — Bifet & Gavaldà
**Concept:** ADWIN adapts the window length and detects statistically significant changes in streaming means.
**Belief:** Fixed lookbacks become stale when the market distribution changes.
**Theorem/metric:** Hoeffding-style bounds compare subwindows and trigger drift when their means differ beyond a confidence threshold.
**System benefit:** Monitor prediction error, calibration error, spread, ATR, and direction hit rate. On drift, lower reliability and shorten shadow-memory windows; do not change protected logic automatically.

## Recommended research implementation order
1. Proper scoring + calibration.
2. Walk-forward/CPCV/PBO and DSR governance.
3. Conformal intervals and empirical coverage.
4. Drift monitoring.
5. Hidden-regime and DCC evidence.
6. SPA/Reality Check before production promotion.

## Exact reusable command
Inspect, repair, optimize, test, and package the uploaded ADX Quant Pro Streamlit project as one deployable ZIP. Keep app.py as the only deployment entry point. Do not alter, replace, simplify, rename, weaken, average, or delete any protected trading logic, Field 1 source-of-truth calculation, BUY/SELL/WAIT rule, threshold, regime formula, prediction formula, historical calculation, or protected hash. Optimize only orchestration, imports, caching, state storage, API refresh, canonical publication, rendering, copy/export, mobile layout, duplicated UI, dead compatibility code, and deployment packaging. Make Quick Run refresh EURUSD H1 once, reuse an unchanged completed-candle/source generation, calculate and publish only Fields 1–3 plus strictly required dependencies, stop after publication, and open Lunch Field 1. Ensure all Lunch fields read one canonical run ID, generation, broker candle time, symbol, timeframe, and source signature. Add one Lunch button named “Refresh API Data + Quick Sync Fields 1–3” that refreshes once through existing connectors, republishes only Fields 1–3 through existing protected services, invalidates stale copy caches, and reruns. Make Copy Short and Copy Full real mobile-safe clickable controls. Cache their current-generation payloads by canonical identity; exclude history, DataFrames, stale values, unavailable placeholders, duplicates, failures, Fields 4–9, and AI research. Copy Full may contain all available necessary current Fields 1–3 facts but must remain bounded. Stack copy controls on phones and provide a safe download/manual fallback only when clipboard access is blocked. Keep one selected Lunch field rendered at a time and lazy-import all unselected fields. Remove duplicate visible controls, repeated serializers, redundant rerun maintenance, unused retained session-state frames, pycache, generated audit clutter, and nondeployment artifacts, but preserve required compatibility modules. Validate with compileall, focused tests for Quick Run, canonical identity, broker-time synchronization, Lunch selection, copy controls, refresh, and app routing. Produce a changed-file manifest, test report, limitations, deployment instructions, SHA-256 manifest, and final deployable ZIP.
