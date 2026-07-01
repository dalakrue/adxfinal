# One-Hour Direction Confirmation v2

## Architecture
The existing connected module remains the single operational confirmation layer. `app.py` remains the only deployment entry point and continues to call `adx_dashpoard.main`. The Settings orchestrator calls the existing one-hour service after the canonical run. Quick mode does not import Field 8/9 research services; Fields 8/9 lazily render the compact stored ledger.

## Target and settlement
Forecast origin is the newest completed H1 candle. Target open is origin + 1 hour and target close is origin + 2 hours. Actual direction is based only on target open-to-close after the target candle is complete. Settlement uses an immutable forecast ID and updates only PENDING rows.

## Core formulas
- Alpha: `(current immutable raw 1H forecast - current completed origin close) / 0.0001`.
- Beta: `(previous immutable raw 1H forecast - previous forecast's own completed origin close) / 0.0001`.
- Robust Z: `abs(alpha-beta) / max(1.4826*MAD(historical differences), epsilon)`.
- Neutral threshold: maximum of estimated trading cost, completed ATR noise fraction, and micro-move floor.
- Safe path: clips protected raw displacement to the minimum of 50 pips, completed-candle ATR cap, and session-tail cap.
- Probabilities: loss-weighted dynamic mixture of path, completed-candle morphology, three-hour pressure, session outcomes, and session-regime outcomes. Every local distribution is empirically shrunk toward a parent prior.
- Reliability: weighted geometric mean of effective sample support, proper-score skill, calibration, alpha-beta stability, margin, data quality, canonical identity, subgroup support, transition risk, interval width, and drift protection. Missing required components produce UNAVAILABLE.

## Protection
The raw Power BI forecast is stored unchanged. The confirmation action is separate and never overwrites production BUY/SELL/WAIT, regime, canonical identity, or protected history.
