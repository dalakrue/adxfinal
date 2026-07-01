# Drift and Structural-Break Report

## ADWIN-style drift

A bounded, vectorized concentration-bound adaptive window processes completed observations chronologically. Outputs include drift status, adaptive window size, magnitude, old/new mean, removed stale count and recalibration requirement.

## Bai–Perron-style breaks

A bounded global dynamic-programming segmentation minimizes segment SSE and selects the number of breaks with BIC. Outputs include break indices/times, strength, current segment start and recalibration requirement.

Both layers are shadow validation. A severe drift or recent structural break blocks the research trade permission but does not overwrite production.
