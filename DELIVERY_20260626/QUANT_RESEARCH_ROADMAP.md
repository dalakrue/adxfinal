# Ten research papers and direct ADX Quant Pro use

1. **James D. Hamilton (1989), “A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle.”**
   Use a shadow Markov-switching probability vector to condition direction-confirmation reliability by regime. Do not replace the protected regime formula; compare agreement and transition risk.

2. **M. Hashem Pesaran and Allan Timmermann (1992), “A Simple Nonparametric Test of Predictive Performance.”**
   Evaluate whether BUY/SELL direction hits are statistically better than chance, globally and by London, overlap and Asian sessions.

3. **Francis X. Diebold and Roberto S. Mariano (1995), “Comparing Predictive Accuracy.”**
   Compare the current Field 2 path against each shadow candidate using loss differentials rather than raw in-sample accuracy.

4. **Peter F. Christoffersen (1998), “Evaluating Interval Forecasts.”**
   Test Field 2 upper/lower bands for unconditional coverage and independence. Widen or narrow only a shadow interval until violations are neither too frequent nor clustered.

5. **Tilmann Gneiting, Fadoua Balabdaoui and Adrian E. Raftery (2007), “Probabilistic Forecasts, Calibration and Sharpness.”**
   Require confidence and reliability to be calibrated while keeping forecast distributions sharp. This directly improves uncertainty, reliability and no-trade decisions.

6. **Albert Bifet and Ricard Gavaldà (2007), “Learning from Time-Changing Data with Adaptive Windowing.”**
   Apply ADWIN to settled direction error, pressure conflict and forecast residuals. When drift is detected, reduce confidence or freeze threshold promotion rather than retraining production logic silently.

7. **Yaniv Romano, Evan Patterson and Emmanuel J. Candès (2019), “Conformalized Quantile Regression.”**
   Build session-conditional, heteroscedastic shadow prediction intervals for Field 2 with finite-sample marginal coverage targets.

8. **Peter R. Hansen (2005), “A Test for Superior Predictive Ability.”**
   Protect against data snooping when testing many candidate direction-confirmation rules or threshold variants. Promote only candidates that beat production after multiplicity control.

9. **Peter R. Hansen, Asger Lunde and James M. Nason (2011), “The Model Confidence Set.”**
   Keep a statistically defensible set of non-inferior shadow models instead of selecting one unstable winner. Use their weighted consensus only as research evidence.

10. **Harvey, Liu and Zhu (2016), “… and the Cross-Section of Expected Returns.”**
    Apply stricter multiple-testing hurdles to the many Field 7–9 research signals. This reduces false discoveries and prevents noisy research factors from influencing core decisions.

## Threshold-reduction protocol

Test candidate HOLD/NO-TRADE thresholds at 90%, 80%, 70%, 60% and 50% of the current protected threshold. Use anchored walk-forward folds, completed H1 candles only, session-stratified reporting, spread/slippage costs, embargo around overlapping labels, and settled outcomes. Promotion requires: higher net expected value, non-inferior maximum drawdown, acceptable turnover, calibrated confidence, positive Pesaran–Timmermann direction skill, and SPA/MCS survival. Until all conditions pass, retain production thresholds.
