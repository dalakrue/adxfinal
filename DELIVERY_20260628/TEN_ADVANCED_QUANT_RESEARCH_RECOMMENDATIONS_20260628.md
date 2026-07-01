# Ten Advanced Quant Research Directions for the Dinner Thesis Layer

## Research boundary

These ten additions belong in the Dinner/research layer. They should read the frozen canonical snapshot and historical outcomes, publish shadow evidence, and never overwrite Lunch production values. Every experiment should have a unique experiment ID, dataset hash, walk-forward split definition, parameters, runtime, and acceptance/rejection result.

---

## 1. Explicit-Duration Markov Switching / Hidden Semi-Markov Regimes

### Exact paper or established concept

**“Explicit-Duration Markov Switching Models” — Silvia Chiappa (2019).**  
Established concept: Hidden Semi-Markov Model (HSMM) with explicit state-duration distributions.

### Concept, belief, and theorem

A normal HMM assumes the probability of leaving a regime depends only on the current state. This creates a geometric dwell-time distribution, which often causes unrealistic rapid switching. An HSMM adds an explicit random duration for each latent state. The model estimates both the regime and how long that regime is likely to persist.

For regime `z_t`, observations follow a state-dependent distribution, while duration `D_k` can use Poisson, negative-binomial, log-normal, or empirical distributions. Transitions occur at segment boundaries rather than at every candle. Posterior inference combines emission likelihood, transition probability, and duration likelihood.

The research belief is that medium and higher standards should be persistent latent segments, not a noisy label independently re-decided every hour. Explicit duration is the mathematically appropriate way to encode that belief.

### How it upgrades this system

- Stops 5-day and long-horizon regimes from flipping several times per day.
- Produces regime age, posterior remaining duration, exit hazard, and transition probability.
- Gives a defensible thesis explanation for Lower/Middle/Higher lifecycle differences.
- Lets Dinner compare HMM versus HSMM persistence without altering the current production regime.
- Converts the current threshold rule into a testable probabilistic duration model.

### Copy-paste implementation command

```text
Inspect my complete ADX Quant Pro Streamlit project and add a research-only Explicit-Duration Markov Switching / Hidden Semi-Markov Model layer to the Dinner tab. Preserve every existing Lunch calculation, decision, table, threshold, and canonical snapshot. Read only completed EURUSD H1 candles from one frozen run_id/generation_id. Fit candidate HSMMs for BUY-regime, SELL-regime, compression, expansion, and transition states using explicit Poisson, negative-binomial, and empirical dwell-time distributions. Use purged walk-forward validation, never random cross-validation. Publish current shadow state, posterior state probabilities, regime age, expected total duration, expected remaining duration, state-exit hazard, and 1h/3h/6h transition probabilities. Compare HMM and HSMM by out-of-sample log loss, Brier score, duration calibration, transition false-alarm rate, and computational cost. Store all results under a new research namespace and do not promote any model unless predefined acceptance gates pass. Add tests proving that Medium and Higher regime display tables show only state-change intervals and that production outputs are byte-for-byte unchanged.
```

---

## 2. Bayesian Online Changepoint Detection (BOCPD)

### Exact paper or established concept

**“Bayesian Online Changepoint Detection” — Ryan Prescott Adams and David J. C. MacKay (2007).**

### Concept, belief, and theorem

BOCPD recursively estimates the posterior distribution of run length: the number of observations since the most recent structural change. At every new candle it evaluates two possibilities: the current regime continues, or a changepoint occurs. A hazard function supplies the prior chance of a change; a predictive model supplies the likelihood.

The core recursion is Bayesian message passing over run length. Instead of declaring a change from one threshold crossing, the method produces `P(change now | data)` and the full run-length posterior.

The research belief is that sudden changes in volatility, drift, pressure, spread, news tone, and model residuals should be detected jointly and probabilistically. A high changepoint posterior can reduce confidence before a regime label actually changes.

### How it upgrades this system

- Adds an early-warning signal for structural breaks.
- Distinguishes ordinary volatility from a real generative-process change.
- Supports adaptive invalidation of stale cached training windows.
- Improves Power BI uncertainty bands after sudden market shifts.
- Provides a principled trigger for retraining rather than retraining every rerun.

### Copy-paste implementation command

```text
Add a Dinner-tab research-only Bayesian Online Changepoint Detection module based on Adams and MacKay. Do not change Lunch production logic. Consume the frozen completed-H1 snapshot and historical features: log return, realized volatility, ATR, pressure imbalance, projection residual, NLP direction score, and regime probability. Implement conjugate univariate BOCPD first, then a multivariate or ensemble version if validation supports it. Expose run-length posterior, probability of a changepoint now, expected run length, highest posterior run length, and evidence contributions by feature. Use a bounded/pruned posterior so phone mode remains efficient. Define shadow actions such as NORMAL, WATCH, CHANGE LIKELY, and CHANGE CONFIRMED, but never replace BUY/SELL/WAIT. Evaluate detection delay, false alarms, predictive log likelihood, and effect on forecast calibration with purged walk-forward testing. Persist experiment metadata and add tests for no look-ahead, completed-candle-only input, bounded memory, and unchanged canonical production values.
```

---

## 3. Adaptive Conformal Prediction for Time-Series Forecasting

### Exact paper or established concept

**“Adaptive Conformal Predictions for Time Series” — Zaffran, Dieuleveut, Féron, Goude, and Josse (2022).**  
Related concept: online/adaptive conformal inference under distribution shift.

### Concept, belief, and theorem

Conformal prediction wraps around a point forecast and converts recent nonconformity scores—usually absolute or asymmetric forecast errors—into prediction intervals. Adaptive conformal inference updates its effective significance level as coverage errors arrive, allowing intervals to react to non-stationarity.

The key guarantee is long-run empirical coverage under the stated online procedure, rather than assuming Gaussian residuals. For a nominal 90% interval, calibration measures whether approximately 90% of realized future values fall inside the band.

The research belief is that a Power BI interval should be judged by coverage, width, and conditional failure patterns, not by visual smoothness alone.

### How it upgrades this system

- Replaces arbitrary upper/lower bands with calibrated intervals.
- Produces separate H+1, H+3, and H+6 coverage diagnostics.
- Widens after drift and narrows when residual behavior stabilizes.
- Allows BUY/SELL/WAIT actionability to depend on interval position and width.
- Gives the thesis a rigorous uncertainty-quantification chapter.

### Copy-paste implementation command

```text
Implement a Dinner research layer for Adaptive Conformal Prediction around the existing Power BI H+1/H+3/H+6 point forecasts. Do not modify the existing production path or bands. Use only forecasts recorded before their realized candle and maintain a prediction ledger keyed by run_id, generation_id, symbol, timeframe, forecast origin, and horizon. Build symmetric, asymmetric, and normalized nonconformity scores; compare rolling conformal, Adaptive Conformal Inference, and expert-aggregated adaptive conformal methods. Target 80%, 90%, and 95% coverage. Publish empirical coverage, average width, interval score, under-coverage streak, conditional coverage by regime/session/direction, and calibration error. Prevent leakage with purged walk-forward evaluation and settle each forecast only when its exact future completed H1 candle exists. Add a shadow actionability rule that abstains when intervals are too wide, but do not alter production decisions. Add regression tests for ledger chronology, horizon alignment, target coverage computation, and no stale forecast substitution.
```

---

## 4. Dynamic Model Averaging (DMA) and Online Expert Weighting

### Exact paper or established concept

**“Online Prediction Under Model Uncertainty via Dynamic Model Averaging: Application to a Cold Rolling Mill” — Raftery, Kárný, and Ettler (2010).**

### Concept, belief, and theorem

DMA maintains posterior weights over multiple candidate models and updates those weights sequentially as new outcomes arrive. Forgetting factors allow both model probabilities and coefficients to evolve. It answers not only “what is the forecast?” but “which model deserves weight now?”

If models `M_k` produce predictive densities, posterior model probability is updated from prior weight times predictive likelihood. A model-averaged forecast is the weighted combination. Online expert algorithms can add regret guarantees against the best changing expert sequence.

The research belief is that technical, regime, session, NLP, KNN, Greedy, and Power BI evidence should not always have fixed weights. Their reliability changes by regime and time.

### How it upgrades this system

- Learns which existing evidence family is currently useful.
- Reduces dependence on one model during a failure period.
- Produces transparent time-varying weights.
- Can improve accuracy without adding a new directional engine.
- Supports phone efficiency by pruning consistently weak candidate models.

### Copy-paste implementation command

```text
Add a research-only Dynamic Model Averaging and online expert-weighting layer to Dinner. Treat the existing technical, regime, session, NLP, KNN, Greedy, data-mining, and Power BI outputs as immutable experts; do not change their calculations. Align every expert prediction to the exact completed H1 origin and settle it against the correct future horizon. Implement DMA with configurable coefficient and model-probability forgetting factors, plus a Hedge/exponentially weighted benchmark. Use predictive log likelihood for probability forecasts and bounded loss for direction forecasts. Publish current expert weights, weight entropy, dominant expert, turnover, ensemble probability, disagreement, and regret versus the best fixed expert. Use nested purged walk-forward validation to select forgetting factors. Add safeguards that prevent an expert with missing or future data from receiving weight. Store all results as shadow research and add tests proving the production master decision remains unchanged.
```

---

## 5. Wasserstein Distributionally Robust Optimization (DRO)

### Exact paper or established concept

**“Data-driven Distributionally Robust Optimization Using the Wasserstein Metric: Performance Guarantees and Tractable Reformulations” — Esfahani and Kuhn (2015).**

### Concept, belief, and theorem

Ordinary empirical optimization chooses a decision that performs well under the observed sample distribution. Wasserstein DRO instead considers every distribution inside a Wasserstein-distance ball around the empirical distribution and optimizes worst-case expected loss.

Under suitable assumptions, the apparently infinite optimization can be reformulated as a tractable finite convex problem. The radius of the ambiguity set controls conservatism and can be calibrated by validation or concentration bounds.

The research belief is that the next market distribution will not exactly match the last 25 days. A robust decision should remain acceptable under plausible shifts in return, spread, volatility, and forecast error.

### How it upgrades this system

- Adds explicit robustness to distribution shift.
- Produces worst-case expected utility and worst-case loss.
- Supports conservative position-sizing research without changing live size.
- Penalizes fragile rules that work only under one narrow sample.
- Creates a mathematically strong thesis contribution around reliability.

### Copy-paste implementation command

```text
Create a Dinner research module for Wasserstein Distributionally Robust Optimization using only settled historical predictions and outcomes. Preserve all existing trading decisions and position sizing. Define a research loss containing direction error, adverse excursion, interval miss, spread/slippage proxy, and abstention opportunity cost. Build an empirical distribution per regime/session and solve for the worst-case expected loss inside calibrated Wasserstein balls. Compare nominal empirical risk, robust risk, and stress distributions. Select ambiguity radius only in nested purged walk-forward validation. Publish robust expected utility, nominal utility, robustness gap, worst-case class probabilities, sensitivity to radius, and a research-only robust action/abstain recommendation. Include computational fallbacks for phone mode and reject publication if the convex solver or data sufficiency checks fail. Add tests for no future outcomes, monotonicity of worst-case risk with radius, immutable production values, and reproducible experiment hashes.
```

---

## 6. Triple-Barrier Event Labeling plus Meta-Labeling

### Exact paper or established concept

**Established quantitative concepts: Triple-Barrier Method and Meta-Labeling, popularized in financial machine learning.**

### Concept, belief, and theorem

The triple-barrier method labels an event by which barrier is reached first: profit-taking, stop-loss, or a vertical time limit. Unlike a fixed next-candle label, it reflects both path and horizon. Meta-labeling then trains a secondary model to decide whether a primary signal should be acted on, often estimating `P(primary signal is correct/actionable)` rather than generating a new direction.

The research belief is that the existing direction engine should remain primary. A research model should estimate when that direction is sufficiently reliable, when to abstain, and which horizon is appropriate.

### How it upgrades this system

- Separates direction generation from actionability.
- Handles 1h/3h/6h and 2–6 hour exit horizons consistently.
- Gives better class definitions than arbitrary hourly correctness.
- Supports precision-first filtering and calibrated abstention.
- Produces research labels suitable for thesis experiments.

### Copy-paste implementation command

```text
Add a research-only triple-barrier event-labeling and meta-labeling pipeline to Dinner. Keep the existing canonical BUY/SELL/WAIT/HOLD decision as the immutable primary signal. Create event start times only at completed H1 candles. Derive volatility-scaled upper and lower barriers and vertical barriers at H+1, H+3, and H+6; include spread/slippage assumptions explicitly. Record which barrier is touched first, time-to-touch, maximum favorable excursion, maximum adverse excursion, and unresolved status. Train a calibrated meta-model to estimate whether the primary signal is actionable, using only information available at event start. Use purged and embargoed walk-forward folds because labels overlap. Compare logistic regression, gradient boosting already available in the project, and a simple baseline. Publish actionability probability, calibrated threshold, expected value, abstain reason, and confusion/cost matrices. Do not let the meta-model reverse production direction. Add tests for barrier chronology, exact horizon settlement, overlap purging, and no mutation of production decisions.
```

---

## 7. Probability of Backtest Overfitting (PBO) with Combinatorially Symmetric Cross-Validation

### Exact paper or established concept

**“The Probability of Backtest Overfitting” — Bailey, Borwein, López de Prado, and Zhu (2015).**

### Concept, belief, and theorem

PBO asks: among many tried configurations, how often does the in-sample winner rank poorly out of sample? Combinatorially Symmetric Cross-Validation partitions the history into blocks, evaluates many balanced train/test combinations, and estimates the probability that selection was overfit.

The method focuses on model-selection risk rather than only one model’s average score. A low in-sample rank followed by a bad out-of-sample rank contributes to the overfitting probability.

The research belief is that trying many thresholds, feature sets, regime windows, and model variants creates hidden multiple-testing risk. A thesis system should report the number of trials and selection risk.

### How it upgrades this system

- Quantifies whether a “best” Dinner experiment is probably a statistical accident.
- Discourages endless threshold tuning.
- Creates a promotion gate for research candidates.
- Makes the thesis methodology much more defensible.
- Complements ordinary walk-forward tests rather than replacing them.

### Copy-paste implementation command

```text
Build a Dinner research-validation module implementing Combinatorially Symmetric Cross-Validation and Probability of Backtest Overfitting. Read only immutable experiment results and settled outcome series; never change production calculations. Define each candidate configuration explicitly and count every attempted configuration. Split the chronological sample into an even number of contiguous blocks, preserve chronology within blocks, and evaluate symmetric train/test combinations without leakage. Compute in-sample and out-of-sample ranks, logit rank transformation, estimated PBO, performance degradation, and selection consistency. Support Sharpe-like utility, Brier score, log loss, and cost-sensitive directional utility, but require minimum sample sizes. Publish a promotion gate that fails when PBO exceeds a predefined threshold. Add tests for deterministic combinations, no train/test overlap at event boundaries, correct trial counting, and honest failure when there is insufficient history.
```

---

## 8. Deflated Sharpe Ratio and Multiple-Testing Correction

### Exact paper or established concept

**“The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality” — Bailey and López de Prado (2014).**

### Concept, belief, and theorem

The ordinary Sharpe ratio is inflated by non-normal returns, short samples, and selecting the best result from many trials. The Deflated Sharpe Ratio adjusts the observed Sharpe using skewness, kurtosis, sample length, and the expected maximum Sharpe under multiple testing.

The research belief is that a research candidate should not be accepted merely because its raw simulated Sharpe is high. The system must ask whether that performance is statistically distinguishable from the best luck expected after all trials.

### How it upgrades this system

- Adds a robust significance test to every research strategy variant.
- Penalizes many attempted configurations.
- Accounts for skew and fat tails common in FX returns.
- Gives a minimum track-record requirement.
- Prevents thesis claims based on an inflated headline metric.

### Copy-paste implementation command

```text
Add Deflated Sharpe Ratio analysis to every Dinner research experiment that produces a return or utility series. Do not add this metric to production decision logic. For each candidate, record observation count, mean, volatility, skewness, excess kurtosis, ordinary Sharpe, probabilistic Sharpe, number of independent/effective trials, expected maximum Sharpe under the null, Deflated Sharpe Ratio, and minimum track-record length. Estimate effective trials conservatively when candidates are correlated. Combine this with the existing experiment registry so hidden retries cannot be omitted. Require settled, cost-adjusted outcomes and use annualization only when sampling frequency is explicit. Publish PASS/FAIL/INSUFFICIENT DATA without replacing any trading decision. Add numerical tests against known examples and tests proving that increasing the number of trials cannot improve the deflated result while all else is fixed.
```

---

## 9. White’s Reality Check and Hansen’s Superior Predictive Ability Test

### Exact paper or established concept

**“A Reality Check for Data Snooping” — Halbert White (2000).**  
**“A Test for Superior Predictive Ability” — Peter R. Hansen (2005).**

### Concept, belief, and theorem

Both tests evaluate many competing models against a benchmark while accounting for data snooping and dependence. White’s Reality Check tests whether the best observed model truly outperforms the benchmark after considering the search. Hansen’s SPA test improves power by studentizing losses and reducing the influence of poor alternatives.

Because forecast losses are serially dependent, block bootstrap methods preserve time dependence. The null is that no candidate has superior expected predictive ability relative to the benchmark.

The research belief is that a candidate should beat a simple benchmark after correcting for the fact that many candidates were tested—not merely have the best table value.

### How it upgrades this system

- Tests whether new research actually beats existing production or a naive baseline.
- Corrects for data snooping across many experiments.
- Handles serial dependence with stationary/block bootstrap.
- Produces p-values suitable for a thesis chapter.
- Stops weak variants from being promoted based on relative rank alone.

### Copy-paste implementation command

```text
Implement White’s Reality Check and Hansen’s Superior Predictive Ability test as a Dinner research-validation component. Use immutable out-of-sample loss differentials for each candidate versus explicit benchmarks: naive previous-direction, always-WAIT, current production forecast, and uncalibrated Power BI forecast where applicable. Use a stationary or moving-block bootstrap with block length selected from serial dependence diagnostics. Report candidate mean loss differential, studentized statistic, Reality Check p-value, SPA p-value, bootstrap settings, effective sample size, and benchmark identity. Require all candidate losses to share exactly aligned forecast origins and horizons. Do not test in-sample fitted values. Store seeds and dataset hashes for reproducibility. Add tests using synthetic equal-skill and superior-skill cases, and prove that no result changes the protected production decision.
```

---

## 10. Double/Debiased Machine Learning for Causal Research

### Exact paper or established concept

**“Double/Debiased Machine Learning for Treatment and Structural Parameters” — Chernozhukov et al. (2018).**

### Concept, belief, and theorem

Predictive association does not establish that a feature causes improved outcomes. Double Machine Learning estimates a low-dimensional causal or structural parameter while flexible machine-learning models estimate high-dimensional nuisance functions. Neyman-orthogonal scores reduce first-order sensitivity to nuisance estimation errors; cross-fitting reduces overfitting bias.

For this system, a “treatment” could be the presence of a strong NLP event, a regime-transition warning, London/NY overlap, or an actionability filter. The outcome could be signed return, forecast error, or adverse excursion. The estimand must be carefully defined and assumptions stated.

The research belief is that thesis claims should distinguish “predicts” from “causes or has incremental structural effect.”

### How it upgrades this system

- Measures incremental effect after controlling for confounders.
- Tests whether news or a session feature adds value beyond technical state.
- Produces confidence intervals and sensitivity analysis.
- Prevents misleading feature-importance interpretations.
- Creates a strong master’s/PhD research contribution without touching live logic.

### Copy-paste implementation command

```text
Add a Dinner-only causal research framework using Double/Debiased Machine Learning. Do not use causal results in production trading. Define one estimand at a time, such as the conditional average incremental effect of a high-impact EUR/USD news event, a regime-transition warning, or London/NY overlap on H+1/H+3 signed return, forecast error, or adverse excursion. Build a causal diagram and list identification assumptions before coding. Use chronological cross-fitting with purging and embargo rather than random folds. Estimate propensity/treatment and outcome nuisance functions with simple regularized models first, then compare approved existing ML models. Use Neyman-orthogonal scores, overlap diagnostics, balance checks, confidence intervals, placebo tests, and sensitivity analysis for unobserved confounding. Publish results as ASSOCIATION ONLY unless identification requirements pass. Store the exact cohort, feature timestamp, treatment definition, and outcome horizon. Add tests for temporal ordering, fold isolation, overlap failure, and immutable production outputs.
```

---

# Recommended implementation order

1. Prediction ledger and triple-barrier settlement.
2. Adaptive conformal intervals.
3. BOCPD change warning.
4. HSMM regime duration.
5. Dynamic model averaging.
6. DSR and PBO experiment validation.
7. Reality Check and SPA.
8. Wasserstein DRO.
9. Double Machine Learning.

The first four improve the integrity of labels, uncertainty, and regimes. The validation methods should be in place before large-scale model searches. Causal work should come last because its assumptions are stricter than prediction.

# Minimum thesis acceptance gates

A new research candidate should remain shadow-only unless all applicable gates pass:

- Completed-candle-only chronology and no leakage.
- Purged/embargoed walk-forward evaluation.
- Minimum data count by regime and horizon.
- Better out-of-sample Brier/log loss or explicit cost-sensitive utility than the declared benchmark.
- Calibration error and conformal coverage within target tolerance.
- PBO below the predeclared threshold.
- Positive Deflated Sharpe evidence when a return series is claimed.
- SPA/Reality Check evidence when many alternatives are compared.
- Stable results across sessions/regimes, not only one subgroup.
- Runtime and memory within phone-mode budget.
- Production snapshot unchanged in regression tests.

# Primary references

- Chiappa, S. “Explicit-Duration Markov Switching Models.” arXiv:1909.05800.
- Adams, R. P., and MacKay, D. J. C. “Bayesian Online Changepoint Detection.” arXiv:0710.3742.
- Zaffran, M. et al. “Adaptive Conformal Predictions for Time Series.” arXiv:2202.07282.
- Raftery, A. E., Kárný, M., and Ettler, P. “Online Prediction Under Model Uncertainty via Dynamic Model Averaging: Application to a Cold Rolling Mill.” Technometrics 52 (2010): 52–66.
- Esfahani, P. M., and Kuhn, D. “Data-driven Distributionally Robust Optimization Using the Wasserstein Metric: Performance Guarantees and Tractable Reformulations.” arXiv:1505.05116.
- Bailey, D. H. et al. “The Probability of Backtest Overfitting.” Journal of Computational Finance.
- Bailey, D. H., and López de Prado, M. “The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality.” Journal of Portfolio Management 40(5), 2014.
- White, H. “A Reality Check for Data Snooping.” Econometrica 68(5), 2000.
- Hansen, P. R. “A Test for Superior Predictive Ability.” Journal of Business & Economic Statistics, 2005.
- Chernozhukov, V. et al. “Double/Debiased Machine Learning for Treatment and Structural Parameters.” The Econometrics Journal 21(1), 2018.
