# Changed Files — CRCEF-SV Repair 2026-06-27

- Modified existing source/config files: **23**
- New source/document/test files: **83**
- Modified original data/history files: **0**
- New runtime data files in project data/: **0**
- Deleted original files: **0**

Original history/data files were restored after testing; no original data file remains modified. Runtime research databases initialize on demand.

## Modified existing source/config files

- `adx_dashpoard.py`
- `app.py`
- `core/app/runner.py`
- `core/canonical_lookup_20260626.py`
- `core/config/defaults.py`
- `core/decision_table_20260626.py`
- `core/less_risky_projection_20260625.py`
- `core/navigation_authority_20260625.py`
- `core/navigation_transaction_20260622.py`
- `core/post_run_consistency_20260626.py`
- `core/settings_one_click_controller_20260624.py`
- `core/settings_run_orchestrator_20260617.py`
- `core/tab_state_stability_20260615.py`
- `tabs/antd_page_router_20260615.py`
- `tabs/field456789_page_20260626.py`
- `ui/antd_navigation_20260615.py`
- `ui/field4to9_collection_history_20260627.py`
- `ui/home_master_control_bar_20260615.py`
- `ui/liquid_menu_popup_20260615.py`
- `ui/lunch_decision_table_20260626.py`
- `ui/lunch_four_core_fields_20260619.py`
- `ui/lunch_next_hour_bias_history_20260626.py`
- `ui/powerbi_cached_renderer_20260619.py`

## New source, documentation, and test files

- `core/canonical_identity_20260627.py`
- `core/navigation_state_20260627.py`
- `docs/ABLATION_STUDY_PLAN.md`
- `docs/CRCEF_SV_ARCHITECTURE.md`
- `docs/DINNER_INTEGRATION.md`
- `docs/EXPERIMENT_PLAN.md`
- `docs/LIMITATIONS_AND_ETHICS.md`
- `docs/LUNCH_INTEGRATION.md`
- `docs/MATHEMATICAL_DEFINITIONS.md`
- `docs/MODEL_PROMOTION_POLICY.md`
- `docs/RESEARCH_METHODOLOGY.md`
- `docs/RESEARCH_PAPER_IMPLEMENTATION_MAP.md`
- `docs/THESIS_CONTRIBUTIONS.md`
- `docs/VALIDATION_AND_LEAKAGE_CONTROL.md`
- `research_quant/__init__.py`
- `research_quant/bellman_conformal/__init__.py`
- `research_quant/bellman_conformal/interval_controller.py`
- `research_quant/bellman_conformal/interval_policy.py`
- `research_quant/bellman_conformal/interval_utility.py`
- `research_quant/calibration/__init__.py`
- `research_quant/calibration/calibration_metrics.py`
- `research_quant/calibration/probability_calibration.py`
- `research_quant/calibration/reliability_diagram.py`
- `research_quant/canonical_adapter.py`
- `research_quant/config.py`
- `research_quant/conformal/__init__.py`
- `research_quant/conformal/adaptive_intervals.py`
- `research_quant/conformal/coverage_metrics.py`
- `research_quant/conformal/enbpi.py`
- `research_quant/drift/__init__.py`
- `research_quant/drift/adwin_monitor.py`
- `research_quant/drift/drift_registry.py`
- `research_quant/drift/promotion_guard.py`
- `research_quant/forecasting/__init__.py`
- `research_quant/forecasting/multi_horizon_dataset.py`
- `research_quant/forecasting/quantile_forecast.py`
- `research_quant/forecasting/tft_adapter.py`
- `research_quant/fusion/__init__.py`
- `research_quant/fusion/crcef_sv.py`
- `research_quant/fusion/evidence_registry.py`
- `research_quant/fusion/explanation.py`
- `research_quant/fusion/selective_policy.py`
- `research_quant/meta_labeling/__init__.py`
- `research_quant/meta_labeling/action_policy.py`
- `research_quant/meta_labeling/actionability_model.py`
- `research_quant/meta_labeling/primary_direction_adapter.py`
- `research_quant/multifractal/__init__.py`
- `research_quant/multifractal/msm_model.py`
- `research_quant/multifractal/volatility_capacity.py`
- `research_quant/multifractal/volatility_components.py`
- `research_quant/nlp_event_memory/__init__.py`
- `research_quant/nlp_event_memory/deduplication.py`
- `research_quant/nlp_event_memory/entity_sentiment.py`
- `research_quant/nlp_event_memory/event_embedding.py`
- `research_quant/nlp_event_memory/response_estimator.py`
- `research_quant/nlp_event_memory/similarity_memory.py`
- `research_quant/orchestrator.py`
- `research_quant/persistence/__init__.py`
- `research_quant/persistence/model_registry.py`
- `research_quant/persistence/outcome_store.py`
- `research_quant/persistence/research_store.py`
- `research_quant/regime/__init__.py`
- `research_quant/regime/markov_switching.py`
- `research_quant/regime/regime_lifecycle.py`
- `research_quant/regime/transition_model.py`
- `research_quant/schemas.py`
- `research_quant/tests/__init__.py`
- `research_quant/tests/test_crcef_sv.py`
- `research_quant/tests/test_persistence.py`
- `research_quant/ui/__init__.py`
- `research_quant/ui/audit_view.py`
- `research_quant/ui/dinner_research.py`
- `research_quant/ui/lunch_research.py`
- `research_quant/ui/validation_dashboard.py`
- `research_quant/validation/__init__.py`
- `research_quant/validation/cpcv.py`
- `research_quant/validation/embargo.py`
- `research_quant/validation/metrics.py`
- `research_quant/validation/pbo.py`
- `research_quant/validation/purging.py`
- `research_quant/validation/threshold_audit.py`
- `tests/test_priority_repair_20260627.py`
- `tests/test_projection_integrity_20260627.py`

## Original data/history changes

- None

## New project data files

- None (database is created by the initialization command)

## Deleted original files

- None
