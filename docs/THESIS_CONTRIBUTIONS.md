# Thesis Contributions

## Main contribution

A canonical, regime-calibrated, uncertainty-aware evidence-fusion framework that separates directional prediction, actionability, entry timing, position maintenance, and abstention while enforcing leakage-safe validation and immutable broker-candle snapshots.

## Paper-to-code mapping

| Research foundation | System concept | Implementation |
|---|---|---|
| Bailey, Borwein, López de Prado & Zhu — *The Probability of Backtest Overfitting* | CPCV and PBO | `research_quant/validation/` |
| Niculescu-Mizil & Caruana — *Predicting Good Probabilities with Supervised Learning* | Platt/isotonic/beta calibration and proper scores | `research_quant/calibration/` |
| Joubert — *Meta-Labeling: Theory and Framework* | direction versus actionability | `research_quant/meta_labeling/` |
| Ang & Timmermann — *Regime Changes and Financial Markets* | state persistence and transition lifecycle | `research_quant/regime/` |
| Calvet & Fisher — *Regime-Switching and the Estimation of Multifractal Processes* | multi-scale volatility | `research_quant/multifractal/` |
| Xu & Xie — *Conformal Prediction for Time Series* | EnbPI/adaptive residual intervals | `research_quant/conformal/` |
| Yang, Candès & Lei — *Bellman Conformal Inference: Calibrating Prediction Intervals for Time Series* | sequential coverage-width control | `research_quant/bellman_conformal/` |
| Bifet & Gavaldà — *Learning from Time-Changing Data with Adaptive Windowing* | ADWIN drift detection | `research_quant/drift/` |
| Lim, Arik, Loeff & Pfister — *Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting* | optional 1H/3H/6H quantile adapter | `research_quant/forecasting/` |
| Araci — *FinBERT: Financial Sentiment Analysis with Pre-trained Language Models* | finance-aware entity sentiment and event memory | `research_quant/nlp_event_memory/` |

## Original extensions

- exact-run six-field canonical identity for all evidence;
- five-action selective policy preserving WAIT PULLBACK and HOLD;
- quality-, calibration-, and regime-conditioned evidence weighting;
- uncertainty combining entropy, conflict, drift, width, coverage error, and missingness;
- promotion blocking tied to immutable audit evidence;
- Dinner 4/6/7/8/9 disagreement-preserving decision history.
