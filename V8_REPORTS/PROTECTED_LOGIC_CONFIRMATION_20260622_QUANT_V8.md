# Protected Raw Logic Confirmation

The baseline manifest contains 585 Python files. **573 existing Python files are byte-for-byte unchanged.** The 12 existing Python files that changed are integration, time-contract, display/copy, transaction, persistence wiring, two superseded architecture tests, and the calibration extension file.

For `core/powerbi_path_calibration_20260617.py`, AST hashes were computed for every 18 pre-existing function definitions. **All 18 pre-existing function ASTs are unchanged.** Six new V8 functions were appended: `conformal_nonconformity`, `_v8_settled_outcomes`, `_finite_sample_quantile`, `_conditioned_calibration_rows`, `fit_conformal_cqr_intervals`, and `update_adaptive_conformal_alpha`.

Protected modules including `core/adx_shared_sync_20260615.py`, `core/canonical_runtime_20260617.py`, `core/quant_research_v6_store_20260622.py`, existing strategy/model engines, existing raw projection construction, regime engines, priority engines and decision formulas retain their baseline SHA-256 hashes.

V8 outputs are marked shadow/validation/monitoring. `production_influence_enabled` defaults to false. Existing raw paths are preserved and copied into the V8 evidence contract without replacement.
