# Limitations and Safe Fallbacks

1. The statistical implementations are bounded, CPU-safe shadow diagnostics designed for Streamlit Cloud. They reproduce the relevant testing logic, not every numerical option from each original paper.
2. Conformal coverage is reported as empirical rolling coverage only. The software does not claim guaranteed coverage when exchange-rate nonstationarity, dependence, or sample sufficiency invalidates assumptions.
3. Conditional regime/session/volatility calibration falls back to regime, horizon-global, or unavailable. Insufficient evidence is never replaced with fabricated certainty.
4. The Hamilton layer uses a fixed high-persistence three-state transition structure estimated from the available return scale. It is a shadow filter, not a replacement for the production regime.
5. The full TFT/transformer model is disabled by default. The active layer is a sparse gated, deterministic, CPU-safe fusion approximation.
6. MCS and SPA use a bounded default of 199 block-bootstrap replications. This is suitable for routine shadow monitoring but lower than a publication-grade offline replication count.
7. Causal/DML-labelled Field 9 values remain associational unless identification assumptions hold. The payload states this explicitly.
8. Missing API keys are supported, but live data quality naturally depends on whatever fallback data is available to the existing application.
9. Mobile validation is a static layout/lazy-render smoke test plus Streamlit startup health; no physical iPhone browser was available in the execution container.
10. The measured performance gain applies only to repeated publication of an identical `run_id` in the benchmark environment. No universal end-to-end speed claim is made.
