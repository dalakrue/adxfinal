# ADX Quant Pro — Five-Surface Decision Architecture

## Delivered architecture

The main app now exposes five selectable decision surfaces:

1. **Lunch** — exactly Field 1, Field 2 and Field 3, with one selected field rendered at a time.
2. **Field 456** — independent top-level display page with choices for original Fields 4, 5 and 6.
3. **Field 789** — independent top-level display page with choices for original Fields 7, 8 and 9.
4. **AI Assistant** — independent canonical-grounded assistant.
5. Existing Morning, Research, Settings and Other utility pages remain available.

Fields 4+5+6 and Fields 7+8+9 are combined only at the presentation layer. Their engines, caches, histories, persistence and calculations remain independent.

## Field 1

Field 1 displays three synchronized 25-broker-day history surfaces in this order:

1. Decision History — requested scores and decisions, including Date, Weekday, Hour, Entry Strength, SELL Pressure, BUY Pressure, Net Pressure, Pullback Readiness, M1 Confirmation, Master Decision, Hold Safety, TP Quality, Direction Confirmation, Decision Name, Final Decision, reliability, uncertainty, error and settled outcome fields.
2. Overall Full Metric History.
3. All 10 Decision Histories, presented as selectable inner tabs.

The decision-table adapter is read-only. It does not fabricate unavailable scores and does not rewrite production decisions.

## HOLD / NO-TRADE requirement

Protected production HOLD/NO-TRADE thresholds were not automatically cut in half. Doing so without out-of-sample evidence could materially increase false entries. The Field 1 table publishes consensus, conflict and coverage diagnostics that can be used to test a lower abstention threshold as a shadow policy. Promotion should require walk-forward evidence, calibrated probability improvement, acceptable drawdown and statistically credible utility improvement.

## Field 2

The operational safe prediction path remains explicitly rendered as the green series, separate from the protected raw central path. No protected forecast calculation was changed.

## Copy controls

Copy Short and Copy Full remain real clickable clipboard controls, sourced from the current canonical Fields 1–3 generation. History frames and unavailable placeholders remain excluded from the bounded copy payload.

## Ten advanced quant research foundations

1. **The Probability of Backtest Overfitting** — Bailey, Borwein, López de Prado and Zhu. Use CSCV/PBO to reject direction-threshold variants selected by data mining.
2. **The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality** — Bailey and López de Prado. Require a positive DSR before promoting a lower HOLD/NO-TRADE shadow policy.
3. **A Reality Check for Data Snooping** — Halbert White. Test all score-weight and threshold variants as one family.
4. **A Test for Superior Predictive Ability** — Peter R. Hansen. Compare shadow direction confirmation against protected production using studentized loss differentials.
5. **A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle** — James D. Hamilton. Add hidden-regime probabilities as reliability evidence, not as a replacement for the protected regime.
6. **Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models** — Robert F. Engle. Detect changing cross-market and volatility relationships that make historical direction evidence stale.
7. **Strictly Proper Scoring Rules, Prediction, and Estimation** — Gneiting and Raftery. Evaluate BUY/SELL/neutral probabilities with Brier/log score and paths with CRPS/pinball loss.
8. **On Calibration of Modern Neural Networks** — Guo, Pleiss, Sun and Weinberger. Calibrate displayed direction confidence by session and regime.
9. **Distribution-Free Predictive Inference for Regression** — Lei, G’Sell, Rinaldo, Tibshirani and Wasserman. Add empirically covered conformal intervals around the protected central path.
10. **Learning from Time-Changing Data with Adaptive Windowing** — Bifet and Gavaldà. Use ADWIN to lower reliability when direction hit rate, calibration or market distribution drifts.

## Validation performed

- Existing focused suite: 24 passed.
- Added five-surface acceptance suite: verifies navigation, independent routing, three Field 1 history surfaces, Decision Name, green Field 2 path and both copy controls.
- Python compilation and package integrity checks are included in the final test report.
