# Detailed Command — Lunch 3-Field / Field 1 Decision Table / Independent Field 456 + 789

Use this command when you want the same architecture again on a future version of the project.

## Command to the assistant

Inspect, repair, test and package the attached ADX Quant Pro project as one deployable ZIP.

### Non-negotiable protection
- Preserve every protected production calculation, Field 1 source-of-truth value, BUY / SELL / WAIT / HOLD / NO-TRADE rule, existing threshold, regime formula, Power BI central path, canonical snapshot identity, database record and settled historical outcome.
- Do **not** merge calculation logic just because displays are grouped together.
- Do **not** fabricate missing history, reliability, uncertainty or outcomes.
- Combine Fields 4+5+6 and Fields 7+8+9 in the **UI only**. Keep original engines, caches, functions, tables and persistence stores independent.

### Main structural target
Make **Lunch** contain exactly **three** selectable fields only:
1. Field 1 — Decision Table and Full Metric History
2. Field 2 — Power BI Price Prediction Projection
3. Field 3 — Regime and Three-Standards History

Move these out of Lunch into the **main app navigation** as independent tabs:
4. Field 456 — combined display-only page of original Fields 4+5+6
5. Field 789 — combined display-only page of original Fields 7+8+9

The app should therefore expose these six top-level pages:
- Settings
- Lunch
- AI Assistant
- Research
- Field 456
- Field 789

### Field 1 required top table
At the top of Field 1, add a read-only history table for the **last 25 completed broker days** using completed EURUSD H1 broker candles only, newest first.

Required columns:
- Date
- Weekday
- Hour
- Entry Strength Score
- Entry Strength Decision
- SELL Pressure Score
- SELL Pressure Decision
- BUY Pressure Score
- BUY Pressure Decision
- Net Pressure Score
- Pressure Decision
- Pullback Readiness Score
- Pullback Readiness Decision
- M1 Confirmation Score
- M1 Confirmation Decision
- Hold Safety Score
- Hold Safety Decision
- TP Quality Score
- TP Quality Decision
- Master Decision Score
- Master Decision
- Direction Confirmation Score
- Direction Confirmation Decision
- Decision Name
- Final Decision
- Decision Confidence
- Decision Reliability
- Uncertainty Percentage
- Error Percentage
- Realized Direction
- Decision Correct
- Outcome Status
- Canonical run_id
- Canonical generation_id

Rules:
- Put this table at the very top of Field 1.
- Build it from existing published/canonical data only.
- Do not recalculate protected decisions.
- If any score scale is unknown, render N/A rather than guessing.
- Field 1 remains the source-of-truth display.

### Synchronization target
Use Field 1 decision-table outputs as the core display reference for the other Lunch surfaces, but do this through read-only presentation sync only. Do not rewrite protected engines.

### Research overlay request
Add a documentation file listing 10 advanced quant / forecasting / calibration / drift / regime papers that can later be used to improve:
- direction confirmation,
- interval reliability,
- regime transition handling,
- session-aware forecasting,
- drift detection,
- evidence-weighted decision confidence.

Make clear that these are research overlays / future implementation ideas, not automatic live-rule replacements.

### Safety boundary
Do **not** silently lower NO-TRADE or HOLD thresholds inside protected production logic unless the user explicitly authorizes threshold changes in a separate isolated step.
Instead:
- keep the protected thresholds unchanged in code,
- document how a shadow/research layer could test lower thresholds offline,
- keep production and shadow layers separate.

### Delivery
Return:
- the repaired deployable ZIP,
- a concise changed-files summary,
- any limitations that were intentionally preserved for safety.
