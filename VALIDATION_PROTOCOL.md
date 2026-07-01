# Validation Protocol

## Split protocol

1. Reserve the final chronological 20% as untouched holdout.
2. Use earlier data for expanding and rolling walk-forward folds.
3. Purge observations whose H-step labels overlap validation/test boundaries.
4. Apply an embargo of at least the maximum forecast horizon when dependence warrants it.
5. Select thresholds, calibration mappings, analogue weights, and ARERT weights using training/validation only.
6. Freeze the model and parameter version before one final holdout evaluation.

## Required metrics

### Classification
Accuracy, balanced accuracy, precision, recall, F1, MCC, Brier score, log loss, expected calibration error, maximum calibration error, fixed-label confusion matrix, and sample size.

### Probability calibration
Reliability bins, calibration intercept, calibration slope, ECE, MCE, and Brier score.

### Forecast intervals
MAE, RMSE, directional accuracy, empirical coverage, average width, Winkler/interval score, under-coverage rate, and regime/session-conditioned errors.

### Selective prediction
Coverage, abstention, selective accuracy/risk, calibration, and sample size at each threshold. The chosen threshold must be selected without the final test set.

## Overfitting controls

Record every hypothesis, feature set, parameter set, number of alternatives, periods, folds, and performance decay. Use PBO when feasible. Deflated Sharpe Ratio, White’s Reality Check, and SPA are required when their assumptions and sample sizes are satisfied; current placeholders are explicitly incomplete.

## Promotion criteria

A research model may be described as supported only when it beats a declared baseline out of sample, remains stable across regimes/folds, retains acceptable coverage/sample size, passes leakage checks, and survives sensitivity analysis. Research promotion never automatically changes production logic.
