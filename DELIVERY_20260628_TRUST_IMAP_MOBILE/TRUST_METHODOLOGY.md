# Trust Methodology

## Purpose

Trust is a research reliability score, not a guarantee of profit. Scores are calculated only from completed-candle information and matured historical outcomes. Missing evidence remains missing.

## Scale

Available values are clipped to 0–10. Unavailable components remain `N/A`; they are never replaced by zero. Grades are A+ (9–10), A (8–<9), B (7–<8), C (6–<7), D (5–<6), E (<5), and N/A.

## Forecast trust

For horizon h, error is normalized by contemporaneous ATR. An exponentially decaying accuracy score is combined with direction hit rate and rolling maturity-safe evidence. H+h realized prices enter the evaluation only after candle t+h completes.

## Regime trust

Lower, Middle and Higher standards use different rolling horizons. Trust considers persistence, trend/volatility structure, reliability and hierarchy agreement. The Middle and Higher standards use longer windows and therefore resist a one-row reversal.

## Decision trust

Decision families are evaluated against subsequent completed-candle direction or outcome evidence. Trust uses rolling sample support and stability. M1 confirmation remains unavailable unless an actual M1 publication exists.

## Protective action

The research protective output is restricted to `ALLOWED`, `WAIT FOR PULLBACK`, `HOLD AND PROTECT`, or `NO TRADE`. BUY/SELL/WAIT remains separate as the protected production direction. Current thresholds are documented research baselines, not holdout-validated final thesis thresholds.
