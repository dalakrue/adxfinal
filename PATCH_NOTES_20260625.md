# ADX Quant Pro — Patch Notes (2026-06-25)

## Delivered behavior

### Quick Run Fields 1–3 + Open Lunch

- Quick scope now bypasses live NLP/research, Similar-Day Field 4, history research, ten-paper research, Quant V3/V4/V6/V7/V8, Field 9, and Field 6–9 AI publication.
- Uses the existing Field 1, Power BI, regime, canonical, reliability, and risk dependencies required to publish Fields 1–3.
- Adds same-completed-H1 immutable generation reuse when the source signature and required Field 1/2/3 caches match.
- Opens Lunch on Field 1 after completion and does not calculate on field rendering.
- Full mode retains the existing Fields 1–9 + AI publication chain.

### Field 2

- Fixed missing `metric_text`, `normalize_scalar`, and `numpy` dependencies in the active cached renderer.
- Preserved the protected central Power BI path and calculation cache.
- Retained read-only recovery from a valid current saved path.
- Added the shared Auto/Manual FX Session Selector.
- Added a bounded session-adjusted shadow path based only on completed H1 data and settled forecasts.
- Uses empirical shrinkage and an ATR cap; the protected base path is unchanged.

### Field 3

- Added a daily publication lock over the existing regime analytics.
- Middle standard: latest 120 completed H1 candles.
- Higher standard: latest 600 completed H1 candles.
- Middle/Higher are reviewed at broker-day 00:00 and locked until the next review.
- Lower remains rolling.
- Added start, next-review, hours-remaining, sample-count, transition-risk, alpha/delta, and reliability cards.

### Copy Short / Copy Full

- Visible copy controls now use current-generation-only payloads.
- Exclude history tables, DataFrames, stale generations, placeholders, missing values, and `Unavailable` output.
- Copy Full contains more current detail but no history.
- Legacy export/history serializers were preserved for compatibility.

## Changed files

- `core/session_context_20260625.py`
- `core/session_adaptive_projection_20260625.py`
- `core/settings_run_orchestrator_v9_parts/part_001.py`
- `core/settings_run_orchestrator_v9_parts/part_002.py`
- `core/settings_run_orchestrator_v9_parts/part_003.py`
- `core/settings_run_orchestrator_v9_parts/part_004.py`
- `tabs/antd_page_router_20260615.py`
- `ui/canonical_copy_export_20260619.py`
- `ui/home_master_control_bar_20260615.py`
- `ui/lunch_four_core_fields_20260619.py`
- `ui/main_menu_drawer.py`
- `ui/powerbi_cached_renderer_20260619.py`

## Added files

- `core/daily_locked_regime_20260625.py`
- `core/quick_fields_123_reuse_20260625.py`
- `services/current_canonical_copy_20260625.py`
- `ui/shared_fx_session_selector_20260625.py`
- `ui/session_field1_summary_20260625.py`
- `ui/field3_daily_locked_regime_20260625.py`
- `tests/test_fields123_user_upgrade_20260625.py`
- `ADX_QUANT_FIELDS_1_3_UPGRADE_20260625.md`
- `PATCH_NOTES_20260625.md`

## Protected logic verification

`core/settings_run_orchestrator_20260617.py` was restored byte-for-byte after moving the Quick reuse hook to the non-protected router layer. All files listed by `PROTECTED_HASH_BASELINE_20260624.json` match their recorded hashes.

## Test results

- Compile check: passed.
- Focused new tests: 6 passed.
- Full test suite, split to avoid the aggregate execution timeout:
  - 304 passed.
  - 355 passed.
  - **659 passed total.**
- DuckDB 1.5.4 was installed because `requirements.txt` declares `duckdb>=0.10,<2`; no DuckDB tests were skipped.

## Honest performance note

The patch structurally eliminates Full-only work from Quick mode and adds same-candle reuse. No fixed percentage speedup is claimed because a valid before/after result requires the user's live API/broker feed, machine, history size, and equivalent cold/new-candle/same-candle runs.
