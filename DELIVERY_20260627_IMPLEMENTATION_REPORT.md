# Implementation Report — 2026-06-27

## Implemented
- Field 1 Table 1 reads the richest published Table 3 factor histories and horizontally merges all ten decision families for the last 25 broker days.
- Net Pressure and Direction Confirmation are recovered from their published factor frames and no longer depend on the one-row current confirmation archive.
- Canonical identity recovery and a no-calculation publication bridge are present for successful runs whose legacy alias pointer was lost.
- Field 1 Table 4 collects technical, regime, session, data-mining, and NLP sentiment bias by completed H1 candle, keeps partial rows, exposes coverage, and has a Table 5 fallback.
- “Field 4 to 9” routes to a combined workspace with a top 25-day decision/bias collection table.
- AirLLM now uses one authoritative Closed/Open state. The duplicate toggle was removed from the independent AI page.
- Table 1 and Table 4 modules now lazy-import Streamlit inside render functions, improving testability without changing runtime behavior.

## Validation completed
- Python compilation passed for the modified modules.
- Focused tests passed: 5 tests covering Field 1 factor merge and priority/navigation repair.
- A direct synthetic publication test confirmed Entry Strength=BUY, Net Pressure=BUY, and Direction Confirmation=BUY are merged into one Table 1 row.

## Important limitation
The package contains no live API credentials or guaranteed historical publications. A real 25-day table can only display rows already published by successful connectors/calculations or persisted stores. Missing sources remain explicit and are not fabricated.
