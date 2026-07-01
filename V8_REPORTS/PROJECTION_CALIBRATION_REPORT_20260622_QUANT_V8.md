# Projection Calibration and Dynamic Trust Report

## CQR shadow calibration

V8 appends formal conformal calibration without replacing any existing path. Settled rows are normalized and pending, future-cutoff and same-row settlements are excluded. Nonconformity is:

`max(raw_lower - actual, actual - raw_upper, 0)`

For every horizon, V8 produces nested 80%, 90% and 95% intervals and records target coverage, achieved rolling coverage, sample count, interval width, interval score, calibration age, fallback level and alpha. Conditioning falls back in the required order: regime+session+horizon → regime+horizon → horizon → pooled settled evidence → explicit insufficient evidence.

## Adaptive conformal state

Alpha is bounded and updated only when a new settled observation is later than the forecast origin and later than the previously processed settlement for that horizon. Repeated misses lower alpha, which raises effective coverage and widens subsequent bands. Confirmed drift partially pools alpha toward the target rather than deleting history or replacing live predictions.

## Shadow ensemble and trust

Bates–Granger uses a bounded settled-error matrix, deterministic diagonal shrinkage, singular/ill-conditioned fallback, non-negative capped simplex weights, protected-weight blending, error correlation and effective expert count. Fixed-Share uses settled proper losses, bounded learning/share rates, nonzero weight floor, turnover and switch counts. Conditional trust returns TRUSTED/MIXED/WEAK/NOT TESTABLE and never claims superiority below its sample gate.

## Governance

SPA, White Reality Check, sampled CSCV/PBO and temporal block bootstrap are deterministic under fixed seeds. Production influence remains false unless leakage, sample, OOS loss, block stability, SPA, Reality Check, PBO, resource, readiness and explicit-promotion gates all pass.
