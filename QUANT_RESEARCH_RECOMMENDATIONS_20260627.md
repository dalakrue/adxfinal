# Ten Quant Research Foundations for ADX Quant Pro

1. **The Model Confidence Set** — Peter R. Hansen, Asger Lunde, James M. Nason (Econometrica, 2011).  
Concept: iteratively remove models with statistically inferior loss until a superior set remains.  
Belief/theorem: finite data may not identify one winner; the honest output is a confidence set containing the best model at a chosen confidence level.  
System use: apply MCS to RF, KNN, regime, session, technical, and NLP models using rolling H1 Brier/log loss and directional loss. Only models inside the current MCS contribute full weight; excluded models become shadow evidence.

2. **Online Prediction Under Model Uncertainty via Dynamic Model Averaging: Application to a Cold Rolling Mill** — Adrian E. Raftery, Miroslav Kárný, Pavel Ettler (Technometrics, 2010).  
Concept: posterior model probabilities evolve through time with forgetting factors.  
Belief/theorem: when the data-generating mechanism changes, model weights should adapt rather than remain fixed.  
System use: replace static display-fusion weights with shadow DMA weights updated only from settled outcomes; retain protected production weights until walk-forward promotion gates pass.

3. **The Probability of Backtest Overfitting** — David H. Bailey, Jonathan M. Borwein, Marcos López de Prado, Qiji Jim Zhu.  
Concept: combinatorially symmetric cross-validation estimates the probability that the selected backtest winner will underperform out of sample.  
Belief/theorem: selecting the best of many tried configurations creates winner’s curse even when ordinary holdout results look good.  
System use: calculate PBO for every proposed threshold, weighting, and WAIT-reduction experiment before promotion.

4. **The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality** — David H. Bailey, Marcos López de Prado.  
Concept: deflate observed Sharpe for multiple trials and non-normal returns.  
Belief/theorem: raw Sharpe is overstated when many strategies were tested or returns are skewed/heavy-tailed.  
System use: report DSR and minimum track-record length beside every strategy-level performance claim; never promote based on raw Sharpe alone.

5. **Conformal Prediction for Time Series** — Chen Xu, Yao Xie.  
Concept: EnbPI wraps ensemble forecasts to produce distribution-free sequential prediction intervals without classical exchangeability.  
Belief/theorem: uncertainty intervals can achieve bounded coverage error under temporal dependence with suitable assumptions.  
System use: calibrate Power BI 1h/3h/6h upper/lower bands from rolling residuals and report empirical coverage by regime/session.

6. **Adaptive Conformal Predictions for Time Series** — Margaux Zaffran et al.  
Concept: Adaptive Conformal Inference changes the miscoverage level online; AgACI aggregates learning rates.  
Belief/theorem: fixed calibration is inadequate under non-stationarity; online error feedback can restore target coverage.  
System use: widen/narrow only the uncertainty bands after each settled H1 error, not the protected central prediction path.

7. **Bellman Conformal Inference: Calibrating Prediction Intervals for Time Series** — Zitong Yang, Emmanuel Candès, Lihua Lei.  
Concept: dynamic programming chooses interval-control policies using multi-step forecasts.  
Belief/theorem: long-run coverage can be maintained under distribution shift and temporal dependence while reducing interval length.  
System use: coordinate 1h/3h/6h bands so they do not contradict each other and optimize useful width subject to coverage constraints.

8. **Domain Specific Concept Drift Detectors for Predicting Financial Time Series** — Filippo Neri.  
Concept: detect market-phase changes directly from financial data or model errors with low computational cost.  
Belief/theorem: drift detection must be evaluated jointly with the learner and can be cheaper than continuous retraining.  
System use: add a shadow drift gate using PSI/KS/error CUSUM plus domain-specific return/volatility shifts; freeze weight updates during unstable transitions.

9. **Learning under Concept Drift: A Review** — Jie Lu et al.  
Concept: taxonomy of sudden, gradual, incremental, and recurring drift; detection, understanding, and adaptation.  
Belief/theorem: no single adaptation method is optimal for every drift type.  
System use: classify detected drift type, then choose reset, faster forgetting, recurring-regime memory, or no action rather than always retraining.

10. **Conformal Prediction Set for Time-Series** — Chen Xu, Yao Xie.  
Concept: ERAPS constructs adaptive prediction sets for categorical sequential outcomes.  
Belief/theorem: a prediction set can retain coverage under unknown sequential dependencies and can be more honest than forcing one class.  
System use: output calibrated action sets such as {BUY}, {SELL}, {BUY, WAIT}, or {SELL, WAIT}; map singleton sets to stronger confirmation and multi-action sets to explicit uncertainty instead of arbitrary WAIT.

## Recommended promotion order
First implement measurement-only MCS, PBO/DSR, calibration curves, and drift monitoring. Next add shadow DMA and conformal bands. Promote any threshold or weight change only after purged walk-forward evaluation, transaction-cost stress, regime/session stratification, and a frozen out-of-sample period.
