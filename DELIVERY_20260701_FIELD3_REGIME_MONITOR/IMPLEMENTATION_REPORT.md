# Field 3 Regime Intelligence, Bias Reliability and Lifecycle Monitor

Delivery date: 2026-07-01  
Implementation version: `field3-regime-lifecycle-monitor-20260701-v1`

## Scope

This delivery upgrades Lunch Tab Field 3 through a separate additive, shadow-only research sidecar. It does not replace or influence the protected production regime, Lower/Middle/Higher standards, production BUY/SELL/WAIT decision, KNN priority, Greedy priority, existing score, canonical snapshot, run identity, broker-time contract, exports, tables, charts, or other Field 3 outputs.

The preserved Field 3 renderer continues after the new monitor, so all pre-existing content remains available.

## New architecture

- Heavy builder: `core/field3_regime_lifecycle_monitor_20260701.py`
- Compressed idempotent store: `core/field3_regime_lifecycle_store_20260701.py`
- Read-only Lunch renderer: `ui/lunch_field3_regime_lifecycle_monitor_20260701.py`
- Settings-owned integration: `core/services/research_service.py`
- Additive Field 3 render integration: `lunch/field_03/renderer.py`
- Dedicated tests: `tests/test_field3_regime_lifecycle_monitor_20260701.py`

The builder is invoked inside the existing Settings research transaction. The Lunch renderer only reads the completed state payload. Display controls, table scrolling, expanders and downloads do not fit or retrain models.

## Implemented intelligence layers

1. Completed EURUSD H1 source gate with a maximum working history of 5,000 rows and a 600-observation display.
2. Shared canonical `run_id`, generation, snapshot hash and broker candle-time projection.
3. Data-quality gate for missing, duplicate, non-monotonic, stale and invalid OHLC records, abnormal spread and insufficient history.
4. Robust causal feature engine using shifted rolling median/IQR normalization.
5. Six-state semantic latent filter: BULL_TREND, BEAR_TREND, RANGE, COMPRESSION, EXPANSION and evidence-driven TRANSITION.
6. Full filtered state-probability vector, second-best state, margin, normalized entropy and model disagreement.
7. Existing Hamilton Markov-switching research output retained as an additional audit source.
8. Multivariate Student-t Bayesian Online Changepoint Detection adaptation with run-length posterior, probability, entropy, severity and persistence confirmation.
9. PELT retrospective auditor for return mean, variance, combined mean/variance, directional strength and volatility structure.
10. Causal explicit-duration empirical survival model with pooled-prior shrinkage, age, conditional remaining duration, 50%/80% intervals and 1H/3H/6H switch probabilities.
11. Chronological, maturity-aware isotonic calibration for regime confidence and switch probabilities.
12. Regime-conditioned GARCH approximation for conditional variance, persistence, 1H/3H volatility forecasts, shock/tail/skew/kurtosis and expected shortfall. It is explicitly disclosed as an approximation and is not mislabelled as full MS-GARCH.
13. Walk-forward H1/H3/H6 cost-adjusted BUY/SELL/WAIT probabilities, favourable/adverse excursion and expected value.
14. Conservative trust engine with separately retained posterior, calibration quality, stability, model agreement, duration confidence, data quality and drift risk.
15. TRADE/REDUCE/WAIT/BLOCK action gate with exact invalidation evidence.
16. Primary regime lifecycle and switch-risk timeline on one broker-time axis.
17. Main descending 600-row history and descending 25-broker-day summary.
18. CSV and JSON exports of stored results without recalculation.

## Important behavior

- Critical data quality preserves reference context but forces `BLOCK` and records the exact reason.
- TRANSITION is generated from low posterior separation, entropy, change risk and disagreement; it is not forced to behave as an ordinary persistent state.
- Smoothed probabilities and PELT are retrospective audit evidence only. They do not drive the live action gate.
- Probability calibration labels are eligible only after their full maturity horizon has completed.
- Sparse duration estimates shrink toward a pooled prior and are marked low-sample.
- No accuracy or profitability improvement is claimed. The validation payload reports `improvement_claimed: false` until the challenger beats preserved baselines out of sample.

## Main history schema

The first 14 columns are fixed in the required order. Remaining evidence is retained through horizontal scrolling. The table includes the protected Lower/Middle/Higher regimes, combined regime, bias, complete probability evidence, duration and switch estimates, BOCPD, PELT, volatility/tail risk, separate trust components, preserved KNN/Greedy/score values, H1/H3/H6 bias probabilities and EV, action, invalidation, run ID and snapshot hash.

## Preservation proof

No source file was removed. The following protected files have identical SHA-256 hashes before and after this upgrade:

- `core/regime_intelligence_stack_20260624.py`
- `core/shared_broker_time_20260622.py`
- `core/canonical_sync_v9.py`
- `ui/lunch_four_core_fields_20260619.py`
- `core/lunch_h1_data_quality_v13.py`
- `app.py`
- `adx_dashpoard.py`

See `PROTECTED_HASH_VERIFICATION.json` for exact hashes.
