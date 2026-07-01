# Research Papers for Future Field 1 / Lunch Upgrades

These are **research overlays only**. They are not wired into live protected production logic automatically.

## Verified paper set
1. Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting
2. Conformal Prediction for Time Series
3. Learning under Concept Drift: A Review
4. Time Series Forecasting With Deep Learning: A Survey
5. Deep Switching State Space Model for Nonlinear Time Series Forecasting
6. TACTiS: Transformer-Attentional Copulas for Time Series
7. Domain Adaptation for Time Series Forecasting via Attention Sharing
8. Self-Interpretable Time Series Prediction with Counterfactual Explanations
9. Towards Non-Parametric Drift Detection via Dynamic Adapting Window Independence Drift Detection
10. Reassessing How to Compare and Improve the Calibration of Machine Learning Classifiers

## How to use them later
- TFT: improve Field 2 path quality, multi-horizon context, and feature attribution.
- Conformal prediction: wrap Field 2 and directional confidence with calibrated uncertainty bands.
- Concept drift + DAWIDD-style detection: detect when old evidence should be down-weighted.
- Time-series survey: benchmark candidate forecasting architectures before replacement.
- Deep switching state-space + TACTiS + DAF: improve regime-sensitive path modeling and cross-context adaptation.
- Counterfactual explanations: explain why a BUY/SELL/HOLD/NO-TRADE call happened.
- Calibration paper: convert raw directional scores into usable confidence and abstention thresholds.

## Production boundary
Any future implementation should be done as:
1. shadow evidence,
2. offline evaluation,
3. walk-forward validation,
4. guarded promotion into production only after passing acceptance criteria.

## Important safety note
I did **not** lower live NO-TRADE or HOLD thresholds inside protected production logic in this package. That should be tested first in a shadow layer and only promoted after validation.
