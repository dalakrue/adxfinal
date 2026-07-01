# Table 2 Schema Report

## Identity

Title: **Unified Lunch Trust and Decision History — Last 25 Broker Days**

Acceptance fixture: **600 rows × 126 columns**, covering **25 broker days**. Newest rows are first. The full export retains all available columns and H1 rows; mobile rendering sends only the selected page and column group.

## Column families

- Identity and quality: completed candle, day/hour, symbol, timeframe, session, source, run/generation/version, coverage, quality, missingness and validation.
- Prediction path: blue/red paths; H+1/H+2/H+3/H+6 forecasts, matured actuals, errors, trust and rank; interval bounds/coverage/width; stability, agreement, uncertainty and changepoint warning.
- Regimes: Lower/Middle/Higher regime, Alpha, Beta, Delta, duration, transition, hierarchy, uncertainty, reliability, trust and rank.
- Decisions: Entry, Buy/Sell/Net Pressure, Pullback, M1, Master, Hold, TP and Direction Confirmation with trust and rank.
- Protection: protected production direction, four-value research protective action and reason.

The machine-readable schema is in `TABLE2_SCHEMA.csv`.
