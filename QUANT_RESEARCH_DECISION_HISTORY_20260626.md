# Ten research foundations for Decision-History improvements

These are research/shadow recommendations. They must not silently overwrite protected production thresholds. Promotion requires walk-forward, session-stratified, cost-aware out-of-sample evidence.

1. **Hamilton (1989), “A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle.”** Use filtered regime probabilities and transition risk to condition direction confirmation rather than forcing one global threshold.
2. **López de Prado, “Advances in Financial Machine Learning” / Meta-Labeling.** Keep Field 1 direction as the primary side label; train a secondary actionability model to decide TRADE versus HOLD/NO-TRADE.
3. **Bailey et al., “The Probability of Backtest Overfitting.”** Use combinatorially symmetric cross-validation and probability-of-overfitting gates before accepting any reduction in HOLD/NO-TRADE.
4. **Bailey & López de Prado, “The Deflated Sharpe Ratio.”** Penalize multiple testing and non-normal returns when comparing candidate direction-confirmation rules.
5. **Niculescu-Mizil & Caruana (2005), “Predicting Good Probabilities with Supervised Learning.”** Calibrate BUY/SELL probabilities with Platt scaling or isotonic regression before using probability margins.
6. **Gneiting & Raftery (2007), “Strictly Proper Scoring Rules, Prediction, and Estimation.”** Rank direction models with Brier/log scores, not accuracy alone; preserve honest uncertainty.
7. **Xu & Xie, “Conformal Prediction for Time Series.”** Wrap the existing Field 2 path in sequential prediction intervals and record empirical coverage in history.
8. **Zaffran et al., “Adaptive Conformal Predictions for Time Series.”** Adapt interval width under session/regime distribution shift instead of applying a fixed uncertainty band.
9. **Page (1954), “Continuous Inspection Schemes.”** Add CUSUM drift alarms to block aggressive threshold changes when error distributions shift.
10. **Lundberg & Lee (2017), “A Unified Approach to Interpreting Model Predictions.”** Store factor-level explanations for each historical decision so conflicts and HOLD causes are auditable.

## Safe method to target fewer HOLD/NO-TRADE decisions

Do not directly divide thresholds by two. Add a shadow meta-label called `actionable_probability`, calibrated separately by London, overlap, and other sessions. Promote a WAIT/HOLD row only when: calibrated actionability exceeds a walk-forward threshold; BUY-versus-SELL margin is stable; conformal uncertainty is below its session limit; regime transition risk is acceptable; expected value remains positive after spread/slippage; and the candidate passes a minimum sample-size gate. Measure whether HOLD/NO-TRADE frequency falls by at least 50%, but reject the change if selective accuracy, Brier score, drawdown, or realized utility deteriorates beyond predeclared tolerances.
