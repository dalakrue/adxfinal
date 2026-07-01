# ADX Quant Pro — Detailed Repair Command (2026-06-27)

Inspect, repair, test, optimize, and package this Streamlit project while preserving every protected production calculation, threshold, BUY/SELL/WAIT/HOLD/NO-TRADE rule, model weight, TP/SL formula, broker-time rule, Power BI central path, regime calculation, database outcome, and canonical snapshot identity. Do not fabricate history, accuracy, reliability, news, outcomes, or evidence.

## Field 1 / Lunch
1. Replace the old Field 1 Table 1 display with a read-only 25-broker-day horizontal collection of every decision column published by Field 1 Table 3: Entry Strength, SELL Pressure, BUY Pressure, Net Pressure, Pullback Readiness, M1 Confirmation, Master Decision, Hold Safety, TP Quality, and Direction Confirmation. Outer-join on completed broker H1 candle. Prefer the richest Table 3 factor publisher over one-row confirmation archives. Keep missing values as N/A, never silently convert them to WAIT.
2. Repair canonical publication aliases after a successful Settings run by rebinding already-calculated Field 1 results to run_id, generation_id, symbol, timeframe, completed broker candle, source snapshot hash, and source signature. This bridge must perform no trading calculation.
3. Keep Table 3 fully visible and ensure Net Pressure and Direction Confirmation recover from compatible published score/decision columns.
4. Replace the old Table 4 with a 25-day outer-joined bias history containing:
   - Technical Bias for Next H1 from Field 1 Table 3 Entry Strength decision history.
   - Regime Bias for Next H1 from Field 3 lower-standard Less Risky Bias.
   - Session Bias for Next H1 from published session history; only when absent, use completed OHLC session momentum as a display-only fallback.
   - Data Mining Bias for Next H1 from Research/Data Mining Random Forest + KNN Priority, using Historical Next 1 Hour Direction or Prescriptive Label.
   - Sentiment Bias for Next H1 from Research/NLP 25-Day Regime Prediction History + NLP, using Regime Direction.
   - Combined Next-Hour Direction, source coverage, directional agreement, and confirmation strength.
5. Use an outer join and retain a row when any real source exists. Missing source values must show MISSING. Do not turn missing evidence into WAIT. If no Table 4 source exists, display Table 5 as a combined available decision/bias evidence fallback.

## Navigation and Fields 4–9
6. The floating/menu button “Field 4 to 9” must navigate directly to the combined Fields 4–9 workspace, never Settings.
7. At the top of that workspace, display a 25-day outer-joined collection of every timestamped decision, bias, direction, label, action, and priority column published by Fields 4–9 and Research. Preserve partial rows and show source coverage.
8. Render original Fields 4–6 and Fields 7–9 below the collection table without starting a new calculation.

## AI Assistant / AirLLM
9. Keep AirLLM only in the independent AI Assistant page. Provide one authoritative Closed/Open control. Closed mode must never load AirLLM and must use the deterministic canonical assistant. Open mode may lazy-load AirLLM only after a question is submitted and only when server environment variables and the optional package are valid. If AirLLM fails, fall back to the canonical deterministic answer and state the failure; never invent facts.
10. Required environment variables: ADX_ENABLE_AIRLLM=1, ADX_AIRLLM_MODEL_ID=<local-or-approved-model>, optional ADX_AIRLLM_ALLOW_DOWNLOAD=1 only on a server with measured disk/RAM/network capacity. Keep downloads disabled by default.

## Acceptance tests
- Import and compile all changed modules.
- Verify Table 1 merges Entry Strength, Net Pressure, and Direction Confirmation for the same candle.
- Verify Field 4–9 routes to the combined workspace.
- Verify Table 4 preserves partial rows and reports MISSING rather than replacing missing evidence with WAIT.
- Verify only one AirLLM open/close state controls execution.
- Keep app.py as the deployment entry point.
