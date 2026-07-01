# Mathematical Definitions

## Probability calibration

```text
Brier = mean((p-y)^2)
LogLoss = -mean(y log p + (1-y) log(1-p))
ECE = Σ_b (n_b/N) |accuracy_b-confidence_b|
BrierSkill = 1 - Brier_model/Brier_reference
```

Implemented in `research_quant/calibration/calibration_metrics.py` and selected in `probability_calibration.py`.

## Regime lifecycle

```text
P_ij = P(S_t=j | S_(t-1)=i)
ExpectedDuration_j = 1/(1-P_jj)
EstimatedRemaining_j = max(0, ExpectedDuration_j-RegimeAge_j)
```

Implemented in `research_quant/regime/transition_model.py` and `regime_lifecycle.py`.

## Multi-scale volatility

```text
sigma_t^2 = base_variance × Π_k M_(k,t)
RiskCapacity = ExpectedMove/sqrt(ForecastVariance)
```

Implemented in `research_quant/multifractal/msm_model.py` and `volatility_capacity.py`.

## Conformal intervals

```text
residual_t = |actual_t-prediction_t|
q_t = quantile(recent OOS residuals, 1-alpha)
lower_t = prediction_t-q_t
upper_t = prediction_t+q_t
```

Implemented in `research_quant/conformal/enbpi.py` and `adaptive_intervals.py`.

## Bellman interval control

```text
Cost = coverage_penalty
     + lambda_width × width
     + lambda_instability × |width_t-width_(t-1)|
     + lambda_decision × decision_uncertainty
```

Implemented in `research_quant/bellman_conformal/interval_controller.py` and `interval_utility.py`.

## Evidence fusion

```text
weight_k = exp(quality_k/temperature) / Σ_j exp(quality_j/temperature)
Z_t = Σ_k weight_k × calibration_quality_k × regime_relevance_k × directional_value_k
```

Every directional value is clipped to [-1, +1]. Implemented in `research_quant/fusion/crcef_sv.py`.

## Uncertainty

```text
U_t = lambda_entropy × direction_entropy
    + lambda_conflict × conflict
    + lambda_drift × drift
    + lambda_interval × normalized_width
    + lambda_coverage × coverage_error
    + lambda_data × missing_data_penalty
```

Normalized to [0, 100].

## Expected utility

```text
EU(action) = p_correct × expected_gain
           - (1-p_correct) × expected_loss
           - transaction_cost
           - uncertainty_penalty
           - regime_transition_penalty
```

Implemented in `research_quant/meta_labeling/action_policy.py`.

## Event-response memory

```text
weight_i = exp(-distance_i/temperature) / Σ_j exp(-distance_j/temperature)
expected_response_h = Σ_i weight_i × historical_return_(i,h)
```

Implemented in `research_quant/nlp_event_memory/similarity_memory.py` and `response_estimator.py`.
