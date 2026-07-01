# ADX Quant Pro — Five-Surface Lunch Architecture

## Implemented

- Field 1 starts with **Decision History — Last 25 Days**.
- Decision History is newest completed broker H1 first and includes Date, Weekday, Hour, Entry Strength, SELL Pressure, BUY Pressure, Net Pressure, Pullback Readiness, M1 Confirmation, Master Decision, Hold Safety, TP Quality, direction confirmation, final decision, confidence, reliability, uncertainty, error, settlement and correctness.
- Scores are normalized for display to 0–10 without rewriting protected source values.
- Lunch contains only Field 1, Field 2 and Field 3.
- Field 456 is a separate top-level display tab for original Fields 4+5+6.
- Field 789 is a separate top-level display tab for original Fields 7+8+9.
- Combining is display-only. Original engines, functions, caches, history stores, database stores and calculations remain independent.
- Visible top-level navigation is exactly: Settings, Lunch, AI Assistant, Research, Other, Field 456, Field 789.
- Quick Run remains bounded to Fields 1–3.

## Safety decision on HOLD / NO-TRADE

The package does not blindly halve protected production HOLD/NO-TRADE thresholds. A fixed 50% reduction can materially increase false entries and invalidate historical identity. The existing research-only consensus diagnostic remains visible in Field 1. Threshold promotion should occur only after walk-forward, session-stratified, settled-outcome validation demonstrates higher utility with bounded drawdown, error and turnover.

## Validation

- Python compileall: PASS
- Targeted regression tests: 6 passed
- Main Streamlit entry: app.py
