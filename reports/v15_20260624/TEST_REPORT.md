# Test report

## Passed

Command:
`python -m pytest -q tests/test_field8_quant_research_v15_20260624.py tests/test_field8_research_stack_20260624.py`

Result: **31 passed**.

Covered: analytic/sample CRPS, energy score, variogram score, deterministic seeded MCS, horizon-isolated DMA, maturity gating, interval origin immutability, HAR volatility, calibration monotonicity, conformal risk, append-only migration, and no automatic promotion.

Compilation command:
`python -m compileall -q core/field8_quant_research_v15_20260624.py core/field8_quant_research_store_v15_20260624.py core/services/field8_quant_research_v15_service.py lunch/field_08 core/settings_run_orchestrator_20260617.py`

Result: **passed (exit 0)**.

## Existing-suite findings not silently altered

`tests/test_field8_20260624.py` contains three failures because it expects two rows (one per origin), while the supplied Field 8 engine currently emits six rows (one per H1/H3/H6 horizon for two origins).

`tests/test_field8_alpha_beta_delta_20260624.py` contains one failure because its first returned horizon row is `FULLY_SETTLED`, while the test expects an origin-level `PARTIALLY_SETTLED` aggregate.

Changing those semantics would alter the supplied Field 8 schema/behavior, so this delivery documents the inconsistency rather than making an unsafe silent rewrite.

## Startup/import limitation

Core v15 modules import successfully. Importing the Streamlit renderer could not be verified in this container because `streamlit` is not installed in the execution environment. The source compiles successfully and the project requirements retain Streamlit.
