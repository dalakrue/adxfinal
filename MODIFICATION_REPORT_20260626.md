# Modification Report — 2026-06-26

## Completed
- Lunch selector reduced to exactly Field 1, Field 2, and Field 3.
- Field 456 and Field 789 remain independent top-level lazy pages.
- Existing Field 1 `Decision History — Last 25 Days` renderer remains first in Field 1.
- Decision history keeps explicit 0–10 scale declarations, N/A for unknown values, completed-candle filtering, newest-first ordering, outcome settlement status, and canonical identity columns.
- Existing protected production formulas, thresholds, databases, outcome stores, Power BI path, and regime engines were not changed.
- Added a reusable implementation command describing the safe shadow-policy method for reducing HOLD/NO-TRADE rather than forcing an unvalidated production threshold cut.

## Validation
- Python syntax/compileall: PASS.
- Structural acceptance for 3-field Lunch + 6 top-level routes: PASS.
- Existing pytest suite: stopped because the execution environment does not have the declared Streamlit dependency installed (`ModuleNotFoundError: streamlit`). This is an environment dependency failure, not a syntax failure.
- One old acceptance assertion expects five Lunch selector fields. That assertion reflects the previous architecture and conflicts with the new requirement that Lunch contain only Fields 1–3.

## Protected behavior
No production BUY/SELL/WAIT/HOLD/NO-TRADE threshold was halved. A 50% reduction target must be tested as a shadow policy using purged walk-forward validation, costs, calibration, session/regime splits, and settled outcomes before promotion.
