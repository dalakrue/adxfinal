# Quant Research Upgrade Report — EURUSD H1 Dinner/Fields 4–9

## Promotion framework used for every method
All additions should begin as read-only shadow evidence attached to the same canonical run/generation. Use purged, embargoed, walk-forward splits by completed broker candle; fit scalers, thresholds, calibration, regimes, NLP models, and neighbors only on the training side. Promotion requires stable gains across sessions and regimes, no material latency/memory regression, and a rollback flag. None of these methods is a guarantee of trading profit.

## 1. The Probability of Backtest Overfitting — Bailey, Borwein, López de Prado and Zhu
**Concept and hypothesis.** Combinatorially Symmetric Cross-Validation (CSCV) measures how often the in-sample winner ranks below the median out of sample. The hypothesis is that strategy selection across many tried variants creates winner’s-curse bias that ordinary holdout testing understates.

**Theorem/guarantee status.** PBO is an estimator and diagnostic, not a theorem guaranteeing future performance. Its reliability depends on representative, sufficiently long return blocks.

**EURUSD H1 implementation.** Treat each threshold/model configuration as one strategy; split broker-time return paths into equal contiguous blocks; enumerate balanced train/test block combinations; calculate the logit of the selected model’s OOS rank and report PBO plus degradation probability. Apply to Tables 4/5 candidate weighting and decision thresholds, never to fabricate decisions.

**Leakage controls.** Purge label horizons (at least 6 H1 bars for a 6-hour target), embargo adjacent blocks, freeze transaction-cost assumptions, and include every attempted candidate—not only survivors.

**Shadow validation and promotion.** Run for at least 6–12 months or enough independent broker days. Promote only when PBO < 0.20, OOS performance degradation is bounded, and results remain stable by London/overlap/non-NY session. Benefit: rejects fragile “best” configurations. Risk: too little history makes estimates noisy.

## 2. The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality — Bailey and López de Prado
**Concept and hypothesis.** DSR adjusts an observed Sharpe ratio for multiple trials and non-Gaussian return skew/kurtosis. Hypothesis: a high raw Sharpe often reflects selection among many tests rather than genuine skill.

**Guarantee status.** A statistical significance correction under modeling assumptions; not a profit guarantee.

**EURUSD H1 implementation.** Compute net-of-spread/slippage hourly strategy returns for every tested Table 4/5 variant, estimate effective independent trials, and display DSR beside raw Sharpe. Use stationary/block bootstrap confidence bands.

**Leakage controls.** Record the full experiment ledger, use only completed candles, and never tune the number of trials after seeing DSR.

**Promotion.** Require DSR probability > 0.95, positive net expectancy, acceptable drawdown, and no collapse in the most recent walk-forward folds. Benefit: prevents promoting statistical flukes. Risk: trial-count estimation can be subjective.

## 3. Predicting Good Probabilities With Supervised Learning — Niculescu-Mizil and Caruana
**Concept and hypothesis.** Compare probability calibration methods such as Platt scaling and isotonic regression. Hypothesis: ranking accuracy and probability accuracy are different; calibrated probabilities improve decisions with explicit risk thresholds.

**Guarantee status.** Empirical methodology, no universal finite-sample guarantee. Isotonic calibration can overfit small samples.

**EURUSD H1 implementation.** Calibrate BUY/SELL/WAIT class probabilities separately per walk-forward fold using only prior completed outcomes. Report Brier score, log loss, reliability diagrams, expected calibration error, and calibration by regime/session.

**Leakage controls.** Calibration set must follow model training and precede test time; never calibrate on the evaluation fold. Settle outcomes only after the entire 1h/3h/6h horizon closes.

**Promotion.** At least 10% relative Brier-score improvement, lower ECE, unchanged or better net expectancy, and no subgroup calibration failure. Benefit: makes reliability and sizing interpretable. Risk: distribution shift invalidates old calibration.

## 4. SelectiveNet: A Deep Neural Network with an Integrated Reject Option — Geifman and El-Yaniv
**Concept and hypothesis.** Jointly learn prediction and a selection head that can abstain. Hypothesis: permitting WAIT/NO-TRADE improves error on covered trades by sacrificing coverage.

**Guarantee status.** The paper demonstrates a risk–coverage framework; empirical SelectiveNet performance is not a market guarantee. Target coverage is optimized through a constrained loss.

**EURUSD H1 implementation.** Use existing features only; train a small shadow model with class head, selection head, and auxiliary head. Map rejection to WAIT, never force BUY/SELL. Track selective risk against coverage from 20% to 90%.

**Leakage controls.** Purged time splits, train-only normalization, no same-candle future data, and no overlap between calibration and promotion folds.

**Promotion.** At a predefined 50–70% coverage, directional error must fall by ≥15%, net expectancy after costs must improve, and abstentions must not cluster solely in one session. Benefit: fewer weak trades. Risk: excessive abstention or unstable coverage.

## 5. A New Interpretation of Information Rate — J. L. Kelly Jr.
**Concept and hypothesis.** Kelly sizing maximizes expected logarithmic wealth under known probabilities/payoffs. Hypothesis: calibrated edge and payoff estimates can convert decision strength into consistent risk sizing.

**Guarantee status.** Log-growth optimality holds under correct stationary probabilities/payoffs and repeated betting assumptions. Those assumptions do not hold exactly in FX.

**EURUSD H1 implementation.** Use fractional Kelly only: `f = shrink × (p*b - q)/b`, with p from out-of-fold calibration, b from realized net reward/risk, hard caps by drawdown/session, and zero size for WAIT/conflict. Recommended shrink 0.10–0.25 until long validation.

**Leakage controls.** Estimate p and b strictly from prior folds; include spread, slippage, stop gaps, and correlated simultaneous signals.

**Promotion.** Shadow for ≥250 settled opportunities; require lower or equal max drawdown, positive log-growth uplift, no risk-cap breaches, and calibration stability. Benefit: coherent sizing. Risk: probability error causes overbetting.

## 6. A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle — James D. Hamilton
**Concept and hypothesis.** Markov-switching autoregression models parameters as governed by an unobserved discrete regime. Hypothesis: EURUSD behavior differs across persistent volatility/trend states.

**Guarantee status.** A likelihood-based latent-state model under specified Markov and distribution assumptions; regime labels are probabilistic, not certain.

**EURUSD H1 implementation.** Fit 2–4 states to returns, realized volatility, range, and trend features using expanding windows. Publish filtered state probabilities for live use; reserve smoothed probabilities for historical diagnostics because they use future observations.

**Leakage controls.** Never use smoothed state probabilities in live backtests; identify label switching deterministically; refit only on scheduled completed candles.

**Promotion.** Regime-conditioned thresholds must improve OOS log loss/expectancy in at least 70% of walk-forward folds, with stable transition matrices and no single-state collapse. Benefit: adaptive thresholds. Risk: unstable states and overparameterization.

## 7. Conformalized Quantile Regression — Romano, Patterson and Candès
**Concept and hypothesis.** Combine quantile regression with conformal correction to create adaptive prediction intervals. Hypothesis: heteroscedastic EURUSD ranges require interval widths that vary with market conditions.

**Guarantee status.** Marginal finite-sample coverage under exchangeability for split conformal prediction. Financial time dependence weakens exact exchangeability; block/rolling conformal methods are therefore required and guarantees become approximate.

**EURUSD H1 implementation.** Predict lower/upper 1h/3h/6h return quantiles, calculate nonconformity scores on a rolling calibration window, and widen intervals by the calibrated quantile. Display empirical coverage and width by session/regime.

**Leakage controls.** Calibration residuals must be fully settled and strictly earlier; use block-aware rolling windows and never revise historical intervals with later outcomes.

**Promotion.** 90% intervals must achieve 88–92% OOS coverage, beat the current interval width by ≥5% at comparable coverage, and maintain subgroup coverage. Benefit: honest uncertainty bands. Risk: abrupt drift causes temporary undercoverage.

## 8. Learning from Time-Changing Data with Adaptive Windowing — Bifet and Gavaldà
**Concept and hypothesis.** ADWIN maintains an adaptive window and cuts old data when statistically significant mean change is detected. Hypothesis: online errors and feature distributions drift, so a fixed lookback is suboptimal.

**Guarantee status.** Provides probabilistic change-detection bounds for bounded streams under its assumptions; it does not identify economic causes or guarantee profitable adaptation.

**EURUSD H1 implementation.** Feed settled Brier loss, directional error, interval miss, and selected feature summaries into separate ADWIN detectors. A detection raises a drift flag, tightens WAIT thresholds, and starts shadow retraining; it must not overwrite the canonical decision automatically.

**Leakage controls.** Input only settled prior outcomes; one detector per metric; predefine delta and cooldown.

**Promotion.** Detection must lead degradation by useful time with false alarms below a preset monthly limit, and post-drift shadow models must recover metrics faster than fixed windows. Benefit: earlier drift response. Risk: event-volatility false alarms.

## 9. The Distance-Weighted k-Nearest-Neighbor Rule — S. A. Dudani
**Concept and hypothesis.** Closer neighbors receive greater voting weight than distant neighbors. Hypothesis: recent EURUSD states most similar in normalized regime/volatility/session space are more informative than equally weighted neighbors.

**Guarantee status.** A classification rule with empirical motivation; no universal finite-sample trading guarantee. kNN consistency requires standard asymptotic conditions and appropriate k growth.

**EURUSD H1 implementation.** Build a leakage-safe archive of fully settled feature vectors and 1h/3h/6h outcomes. Use robust train-fold scaling, session/regime filters, distance weighting, minimum effective-neighbor count, and return WAIT when neighbors disagree or are too distant.

**Leakage controls.** Exclude overlapping target horizons and the query candle; fit feature scaling only on the historical search set; deduplicate near-identical rows from one event.

**Promotion.** Improve directional balanced accuracy and Brier score over unweighted KNN, keep effective sample size above threshold, and demonstrate stability across k and distance metrics. Benefit: local analog evidence. Risk: curse of dimensionality and stale analogs.

## 10. FinBERT: Financial Sentiment Analysis with Pre-trained Language Models — Dogu Araci
**Concept and hypothesis.** Finance-domain BERT transfer learning improves sentiment classification over generic language models. Hypothesis: domain-specific language understanding produces more reliable EUR/USD event sentiment.

**Guarantee status.** Empirical benchmark improvement, not a theorem and not proof of return predictability.

**EURUSD H1 implementation.** Classify deduplicated news into positive/negative/neutral, then map sentiment separately to EUR and USD entities before deriving pair direction. Combine impact, novelty, source time, and event type; decay old articles; aggregate duplicates before category consensus.

**Leakage controls.** Use publication timestamps available at decision time, prevent revised articles from backdating, split by time/event family, and train entity-to-return mapping only on prior settled windows.

**Promotion.** Improve labeled-news macro-F1 and calibration, then demonstrate incremental OOS Brier/expectancy benefit above technical/regime baselines with no lookahead. Benefit: better contextual sentiment. Risk: headline ambiguity, source duplication, and model/domain drift.

## Recommended order
1. Experiment ledger + PBO/DSR. 2. Probability calibration. 3. CQR uncertainty. 4. ADWIN monitoring. 5. Distance-weighted KNN. 6. Hamilton shadow regimes. 7. FinBERT entity sentiment. 8. SelectiveNet abstention. 9. Fractional Kelly only after calibration is proven.
