# Adaptive Regime–Evidence Reliability Theory — ARERT

## Central belief

A quantitative market decision is not reliable merely because a model reports high confidence or a direction. Academic reliability should depend on persistence of the market regime, independent agreement, calibration, historical analogues, evidence diversity, model stability, behavioral confirmation, uncertainty, and conflict fragility.

## Research equation

For time *t*:

\[
ARERT_t = \left(\sum_{j\in S_t} w_{j,t} X_{j,t}\right) \times \left(1-\frac{\bar P_t}{200}\right)
\]

where support components are:

- \(R_t\): regime-persistence reliability
- \(A_t\): directional/model agreement
- \(C_t\): probability-calibration quality
- \(H_t\): historical-analogue support
- \(E_t\): independent-evidence diversity
- \(M_t\): model stability
- \(B_t\): behavioral/news confirmation

and penalty components are:

- \(U_t\): uncertainty penalty
- \(F_t\): evidence-conflict and fragility penalty

All components are normalized to 0–100. `S_t` contains only components with valid observations. The current implementation stores the raw value, normalized value, applied weight, weighted contribution, component type, and weight version.

## Weight governance

The initial implementation uses an explicitly labelled equal-weight baseline over available support components. It does **not** claim that equal weights are optimal. Walk-forward fitted weights remain incomplete until sufficient settled component histories are available. A fitted version must:

1. use training and validation periods only;
2. purge overlapping labels and apply embargo where needed;
3. constrain support weights to be non-negative and sum to one;
4. compare against equal weights;
5. freeze the selected weight version before final holdout testing;
6. save all tested and promoted weight versions.

## Initial research classes

- 85–100: exceptionally supported
- 70–84: strongly supported
- 55–69: moderately supported
- 40–54: weak or conflicting
- below 40: unreliable or insufficient evidence

These are preliminary thesis thresholds. They require walk-forward calibration and must not be interpreted as live BUY/SELL commands.

## Falsifiability

ARERT is supported only if it improves out-of-sample calibration and selective accuracy relative to raw confidence/reliability baselines without hidden leakage or unacceptable coverage collapse. A higher in-sample score alone is not evidence.
