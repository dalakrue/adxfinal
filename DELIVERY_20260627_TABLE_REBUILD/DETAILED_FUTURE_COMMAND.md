# Detailed command for a future repair run

Inspect, repair, test, and package the attached ADX Quant Pro Streamlit project as one deployable ZIP. Keep `app.py` as the deployment entry point and preserve all protected production formulas, thresholds, decisions, broker-time rules, outcomes, model weights, TP/SL logic, canonical identity, and database records.

## Field 1 Lunch requirements

1. Remove only the obsolete display implementations of Field 1 Table 1 and Table 4; do not delete their source publishers or protected calculations.
2. Rebuild Table 1 as a read-only 25-broker-day outer join of every available decision column used by Field 1 Table 3: Entry Strength, SELL Pressure, BUY Pressure, Net Pressure, Pullback Readiness, M1 Confirmation, Master Decision, Hold Safety, TP Quality, and Direction Confirmation. Include scores, Date, Weekday, Hour, completed broker candle, run_id, generation_id, outcome status, and reliability fields when published.
3. Table 1 must read existing published rows only. It may reshape, alias, and align columns, but must not recalculate or fabricate historical decisions.
4. Ensure Net Pressure and Direction Confirmation Table 3 tabs are populated from their exact publishers. If their dedicated frame is absent, project the matching columns from the existing overall Field 1 history. Do not create prior candles.
5. Rebuild Table 4 as a 25-broker-day H1 outer join with these columns:
   - Technical Bias for Next H1: Field 1 Table 3 Entry Strength Decision.
   - Regime Bias for Next H1: Field 3 lower-standard Less Risky Bias.
   - Session Bias for Next H1: existing session publisher; when absent, use a leakage-safe adaptive session threshold from completed OHLC only.
   - Data Mining Bias for Next H1: Historical Next 1 Hour Direction and Prescriptive Label from the Research/Data Mining Random Forest + KNN Priority table.
   - Sentiment Bias for Next H1: Regime Direction from the Research/NLP 25-Day Regime Prediction History + NLP hourly-ranked table.
6. Table 4 must retain partial rows, show MISSING per unavailable source, calculate coverage from actually published sources, and never convert missing evidence into WAIT.
7. Canonical identity must display real run_id, generation_id, symbol, timeframe, completed broker candle, snapshot hash, and source signature from the same immutable generation used by the tables.

## Navigation and Fields 4–9

8. The floating-menu button must open one combined `Field 4 to 9` page, never Settings.
9. At the top of that page, render a 25-day outer-joined history of every timestamped decision, bias, direction, label, action, and priority column published by Fields 4, 5, 6, 7, 8, 9, Data Mining, NLP, and regime modules. Keep original engines independent and combine display only.
10. Keep each field's original renderer available below the collection table.

## AI Assistant / AirLLM

11. Add an explicit AirLLM Open/Closed control in the independent AI Assistant tab.
12. Closed mode must use the lightweight deterministic canonical assistant.
13. Open mode must lazy-load AirLLM only after question submission, use the frozen canonical fact contract as grounding, and fall back safely without inventing facts when AirLLM is unavailable.

## Testing and delivery

14. Verify `python -m compileall`, import paths, navigation aliases, canonical identity consistency, partial-source Table 4 behavior, 25-day cutoffs, newest-first ordering, and mobile-safe rendering.
15. Add focused tests for Net Pressure, Direction Confirmation, Table 4 partial sources, combined Fields 4–9 route, collection-history alignment, and AirLLM mode.
16. Package one deployable ZIP plus implementation report, changed-file list, test report, limitations, deployment commands, and SHA-256 checksum.
