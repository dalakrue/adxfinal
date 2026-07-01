# Research Hypotheses

All tests use chronological, point-in-time data. Hyperparameters are selected without the final holdout.

## H1 — Regime duration

- **Null H1₀:** duration adjustment does not improve out-of-sample transition probability calibration relative to a memoryless regime model.
- **Alternative H1₁:** duration adjustment improves out-of-sample transition probability calibration and reduces one-observation regime flips.

## H2 — Regime-conditioned conformal intervals

- **Null H2₀:** regime-conditioned conformal intervals do not improve empirical coverage or interval score relative to fixed production bands.
- **Alternative H2₁:** regime-conditioned conformal intervals improve coverage calibration or interval score at comparable width.

## H3 — Meta-labeling

- **Null H3₀:** rejecting weak primary decisions does not improve out-of-sample precision after accounting for reduced coverage.
- **Alternative H3₁:** meta-labeling improves precision and selective risk at a pre-registered minimum coverage.

## H4 — Historical analogues

- **Null H4₀:** analogue support does not improve outcome probability calibration over unconditional/regime-only baselines.
- **Alternative H4₁:** leakage-safe analogue support improves Brier score, calibration error, or log loss.

## H5 — Evidence diversity

- **Null H5₀:** evidence diversity has no incremental predictive value beyond raw indicator count and consensus.
- **Alternative H5₁:** independent-evidence diversity improves correctness or calibration after controlling for count and raw consensus.

## H6 — Behavioral NLP

- **Null H6₀:** prospect-theory adjustment does not improve event-response classification over raw NLP sentiment.
- **Alternative H6₁:** behaviorally adjusted sentiment improves chronologically evaluated event-response classification.

## H7 — ARERT

- **Null H7₀:** ARERT does not improve calibration or selective accuracy over the existing raw reliability score.
- **Alternative H7₁:** frozen, walk-forward ARERT improves calibration and selective accuracy without unacceptable coverage loss.

## Multiple-testing policy

Primary metrics and minimum sample/coverage requirements must be pre-registered. Secondary analyses are exploratory. Corrections or reality-check methods are required when many model/parameter alternatives are compared.
