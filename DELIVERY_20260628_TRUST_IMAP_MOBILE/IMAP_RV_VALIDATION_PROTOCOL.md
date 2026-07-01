# IMAP-RV Validation Protocol

Required thesis protocol:

1. Freeze feature definitions.
2. Split chronologically into training, calibration, validation and untouched holdout.
3. Fit only on training; choose weights/thresholds only on validation.
4. Refit only during explicit Settings research runs.
5. Evaluate H+1/H+3/H+6 after maturity.
6. Report by regime, session and volatility state.
7. Compare equal weight, raw confidence, validated performance and diversity-adjusted baselines.
8. Report negative findings and missing evidence.

This delivery implements safety scaffolding and prototypes, not the complete empirical protocol.
