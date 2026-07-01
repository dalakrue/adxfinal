# Decision History and Five-Field Lunch Upgrade — 2026-06-26

## Implemented
- Field 1 begins with `Decision History — Last 25 Days`.
- Columns include Date, Weekday, Hour, Entry Strength score/decision, SELL Pressure score/decision, BUY Pressure score/decision, Net Pressure score/decision, Pullback Readiness score/decision, M1 Confirmation score/decision, Master score/decision, Hold Safety score/decision, TP Quality score/decision, Direction Confirmation score/decision, final decision, confidence, reliability, uncertainty, error and settled outcome fields.
- Rows are newest completed broker candle first and bounded to the latest 25 distinct broker dates.
- Scores are normalized for display to 0–10 without rewriting protected source calculations.
- Lunch now exposes exactly five selectable display fields: Field 1, Field 2, Field 3, Field 456, Field 789.
- Field 456 combines Fields 4+5+6 only in presentation. Field 789 combines Fields 7+8+9 only in presentation. Original engines, caches, histories and stores remain independent.

## Safety decision
The production HOLD/NO-TRADE gates were not mechanically cut by 50%. A research consensus diagnostic is displayed instead. Any threshold change must pass chronological walk-forward validation, session/regime stratification, probability calibration, transaction-cost tests and a rollback gate before promotion.

## Validation
- Python AST/compile checks passed for changed modules.
- Synthetic decision-history contract test passed with 25 dates and 35 output columns.
- Full Streamlit runtime test was not executed in this container because Streamlit is not installed in the execution environment.
