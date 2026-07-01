# Field 9 Test Results

## Commands executed

```bash
python -m compileall -q .
pytest -q tests/test_field9_eurusd_h1_20260624.py tests/test_research_grade_shadow_20260624.py
pytest -q tests/test_field_registry.py tests/test_lunch_router.py tests/test_no_heavy_render_calculation.py tests/test_streamlit_cloud_preflight_20260619.py
pytest -x -q --tb=short
```

## Actual results

- Full project compile: **PASS** (exit code 0).
- Field 9 + protected research-grade regression: **PASS — 27 passed in 4.21s**.
- Registry/router/no-heavy/Streamlit preflight subset: **PASS — 7 passed in 0.16s**.
- Full suite first run: **380 passed before one environmental failure**: `duckdb is unavailable` in the pre-existing regime-trust test.
- Full suite excluding that DuckDB file progressed beyond 66% but exceeded the execution limit in a pre-existing long-running section; no final pass is claimed.

## Targeted output

```text
...........................                                              [100%]
27 passed in 4.21s
```

## Regression output

```text
.......                                                                  [100%]
7 passed in 0.16s
```

## Full-suite environmental failure

```text
........................................................................ [ 13%]
........................................................................ [ 26%]
........................................................................ [ 39%]
........................................................................ [ 52%]
........................................................................ [ 65%]
....................F
=================================== FAILURES ===================================
__________ test_duckdb_history_updates_incrementally_and_deduplicates __________
tests/test_regime_transition_trust_20260621.py:111: in test_duckdb_history_updates_incrementally_and_deduplicates
    store = RegimeTrustStore(Path(directory) / "trust.duckdb")
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<string>:4: in __init__
    ???
core/regime_trust_store_20260621.py:138: in __post_init__
    raise RuntimeError("duckdb is unavailable")
E   RuntimeError: duckdb is unavailable
=========================== short test summary info ============================
FAILED tests/test_regime_transition_trust_20260621.py::test_duckdb_history_updates_incrementally_and_deduplicates - RuntimeError: duckdb is unavailable
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 380 passed in 26.51s
```
