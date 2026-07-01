# Regime Data Dictionary

The canonical `regime_intelligence_20260624` object contains:
- `data_quality`: readiness, reasons, sample count, gaps and completed candle time.
- `features`: feature names, scaling method, missing fraction and provenance.
- `shift_detection`: per-variable CUSUM statistics and combined score.
- `bocpd`: run-length posterior, mode, expectation and change probabilities.
- `structural_breaks`: proposed and confirmed PELT break indices.
- `lower_standard`, `middle_standard`, `higher_standard`: posterior vectors, winner, runner-up, margin and entropy.
- `filardo`: transition matrix, 1h/3h/6h probabilities and driver contributions.
- `hsmm`: age-conditioned total and remaining duration distributions.
- `persistent_shadow`: sticky persistence and unknown-state evidence.
- `ood`: nearest regime, distance, score, status and feature contributions.
- `ensemble`: posterior probabilities, weights and exclusions.
- `current`: regime, trust score, reliability boolean, components and failed gates.
- `history_25d`: point-in-time-safe display rows; unavailable historical metrics remain N/A.
- `provenance`: data signature, row count and settled-outcome count.
