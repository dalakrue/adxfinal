# ADX Quant Pro Dinner Repair — Implementation Report

## Base archive
The larger and more complete second uploaded archive was used as the repair base. The first archive was not modified.

## Implemented
- Added a real visible top-level Dinner route and removed separate Field 456/789 entries from the fallback menu.
- Preserved `Field 4 to 9`, `Field 456+789`, `Field 456`, and `Field 789` as backward-compatible aliases normalized to Dinner by the navigation authority.
- Dinner now renders the combined Fields 4–9 workspace from the already-published canonical state; opening it does not invoke a calculation engine.
- Kept component error isolation through the router’s `_safe_component` wrapper and the independent Field 456/789 renderers.
- Rebuilt the 25-day Dinner history collector to recurse through nested mappings, lists, record arrays, and DataFrames; removed the old 12-column truncation; included deeply nested Field 9 values.
- Added broker-time display conversion using the shared published timezone when present, otherwise `Asia/Yangon`.
- Rebuilt Tables 4 and 5 to use only original direction-eligible source columns. Generated history/Table 4/Table 5 keys are excluded from their own inputs.
- Added exact source-column audit output.
- Excluded confidence, reliability, rank, probability, coverage, unsigned scores, uncertainty, error and percentage columns from direction voting.
- Added explicit BUY+SELL conflict → WAIT handling.
- Added category-first aggregation for Technical, Sentiment, Regime, Pattern, Field 6, Field 7, Field 8 and Field 9 to prevent duplicate-column domination.
- Updated AirLLM default model to `Qwen/Qwen2.5-0.5B-Instruct`, preserved lazy import, retained the real `airllm.AutoModel.from_pretrained` interface, added automatic CPU/CUDA selection, and expanded canonical grounding fields.
- Added a compatibility-locked `requirements-airllm.txt` and included it from normal deployment requirements.
- Added the requested ten-topic quant research report.

## Validation results
- Syntax compilation: **PASS** (`python -m compileall -q .`).
- Dinner-focused regression suite: **7 passed, 0 failed**.
- Complete available legacy suite: **65 passed, 6 failed**.
- Streamlit startup health probe: **NOT RUN successfully** because the execution environment does not have the `streamlit` package installed (`No module named streamlit`).
- AirLLM real model download/inference: **NOT PERFORMED**. This environment did not install AirLLM/model weights and no network-heavy model download was attempted.

## Remaining failures
1. Five legacy failures are environment dependency failures caused by missing Streamlit.
2. One legacy failure is an existing unrelated test mismatch: `ui.lunch_next_hour_bias_history_20260626` does not expose a module-level `st` attribute expected by the test.

These are reported as remaining failures; this delivery does not claim a fully passing complete suite or verified model inference.

## Key changed files
- `core/app/registry.py`
- `core/navigation_authority_20260625.py`
- `core/navigation_parts/main.py`
- `tabs/antd_page_router_20260615.py`
- `tabs/field456789_page_20260626.py`
- `ui/field4to9_collection_history_20260627.py`
- `services/airllm_backend_20260626.py`
- `requirements.txt`
- `requirements-airllm.txt`
- `tests/test_dinner_repair_20260627.py`
- `RESEARCH_REPORT_DINNER_QUANT_20260627.md`
