# Walk-Forward Validation Report

## Implemented safeguards

- Chronological completed-candle ordering.
- H+h outcome maturity checks.
- No future row is required to calculate the current historical trust value.
- FDR correction for the prototype IC family.
- Equal-weight baseline for IMAP-RV.

## Incomplete validation work

A full expanding-window train/calibration/validation/final-holdout experiment with frozen thresholds, multiple optimizer starts, regime/session stratification, calibration curves and risk-coverage curves was not completed. Therefore current trust/protective thresholds must be treated as research baselines, not final thesis estimates.
