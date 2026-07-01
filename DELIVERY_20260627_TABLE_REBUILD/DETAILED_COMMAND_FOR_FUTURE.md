# Detailed future repair command

Inspect, repair, test, optimize, and package the attached ADX Quant Pro Streamlit project as one deployable ZIP. Keep `app.py` as the entry point.

## Non-negotiable protection

Preserve every protected production calculation, Field 1 source-of-truth value, BUY/SELL/WAIT/HOLD/NO-TRADE rule, threshold, Power BI central prediction path, regime formula, canonical snapshot identity, historical outcome, database record, model weight, TP/SL calculation, and broker-time rule. Do not fabricate history, news, evidence, identity, accuracy, reliability, uncertainty, outcomes, sample size, or performance.

## Field 1 Table 1

Delete/replace the old presentation renderer only. Build Table 1 as a read-only outer join of every available decision column from Field 1 Table 3 histories for the latest 25 broker days. Include Date, Weekday, Hour, Broker Candle Time, score and decision columns for Entry Strength, SELL Pressure, BUY Pressure, Net Pressure, Pullback Readiness, M1 Confirmation, Master Decision, Hold Safety, TP Quality, and Direction Confirmation. Prefer the richest Table 3 publisher over a one-row confirmation archive. Never fabricate missing candles. Keep missing values as N/A.

## Field 1 Table 3

Ensure Net Pressure and Direction Confirmation tabs render from their dedicated publisher frames. If those frames are absent but the same columns exist in the already-published overall Full Metric history, project those columns into display-only factor tables. Do not recalculate the production engine.

## Canonical identity

After Quick Run, publish and persist one immutable run_id, generation_id, source snapshot hash, source signature, symbol, timeframe, and latest completed broker candle. All pages must resolve the same publication, including after Streamlit navigation reruns. Search compatible nested publication wrappers only as a read-only recovery path. Never create fake identity strings.

## Field 1 Table 4

Build a 25-broker-day outer-joined bias table. Keep partial rows when any source is missing.

- Technical Bias for Next H1: Entry Strength Decision from Field 1 Table 3.
- Regime Bias for Next H1: Lower/Low Standard Less Risky Bias from Field 3 Three-Standard Summary.
- Session Bias for Next H1: existing published session bias first; otherwise derive a display-only bias from completed H1 OHLC using session/hour-specific rolling median absolute 3-hour return threshold. Label this fallback LOCAL_COMPLETED_OHLC.
- Data Mining Bias for Next H1: Prescriptive Label and/or Historical Next 1 Hour Direction from Research → Data Mining → Random Forest + KNN Priority.
- Sentiment Bias for Next H1: Regime Direction from Research → NLP → 25-Day Regime Prediction History + NLP hourly ranked rows. Preserve headline/title.

Normalize textual directions to BUY/SELL/WAIT only for display. Missing source must remain MISSING. Add Combined Next-Hour Direction, Available Sources, Directional Agreement, Coverage %, and Confirmation Strength. Do not change protected production weights.

If Table 4 has no timestamped source at all, create Table 5 at the same Field 1 location. Table 5 must recursively collect all real timestamped decision, bias, direction, label, action, and priority columns from published state, align by completed broker H1 time, retain partial rows, and cover the latest 25 broker days. Do not fabricate rows.

## Fields 4–9 navigation

The floating menu button for Field 456, Field 789, or Field 4 to 9 must route directly to one visible combined workspace, never Settings. At the top, show one 25-day collection history of every available decision/bias/direction/action/priority column from Fields 4, 5, 6, 7, 8, 9 and Research. Then render Fields 4+5+6 and Fields 7+8+9 together without merging their calculation engines.

## AIRLLM

In the independent AI Assistant tab add Open and Closed mode. Closed mode must not load AIRLLM. Open mode may lazy-load only after the user submits a question and only when the server dependency/model configuration is valid. Keep deterministic canonical grounding as fallback. Do not embed AIRLLM inside Field 5.

## Testing

Run compileall and focused pytest coverage for: 25-day Table 1 merge, direction/net-pressure recovery, completed-candle cutoff, score scaling, canonical identity after rerun, Table 4 empty/partial/full/news behavior, data-mining column, local OHLC session fallback, Field 4–9 menu route, combined history table, AIRLLM open/closed behavior, and app entry-point import. Package one deployable ZIP plus implementation report, changed-file list, test report, known limitations, SHA-256 manifest, deployment commands, and rollback commands.
