# Field 1 Table Rebuild and Navigation Repair — 2026-06-27

## Implemented
- Rebuilt Field 1 Table 1 as a read-only 25-broker-day outer collection of the ten Table 3 factor histories.
- Corrected empty diagnostics: missing factor evidence now displays `N/A`, not false `0.0` values.
- Strengthened the Field 1 publication bridge. When calculated outputs and a completed candle exist but identity aliases are absent, deterministic run/generation identity is rebound from those real outputs; no market history is fabricated.
- Rebuilt Field 1 Table 4 with Technical, Regime, Session, Data Mining and Sentiment next-H1 biases.
- Table 4 retains partial rows and uses the union of available source timestamps. One missing source no longer suppresses the table.
- Added a documented display-only reliability tie-break to reduce constant WAIT outcomes. It does not overwrite the protected production decision.
- Preserved Table 5 fallback for real timestamped decision/bias evidence when Table 4 has no usable source.
- Preserved the combined Fields 4–9 page and its top 25-day collection table.
- Preserved independent AI Assistant AirLLM Open/Closed mode and lazy loading.

## Important evidence rule
The repair does not invent 25 days of history. It displays up to 25 broker days from actual published tables and loaded completed OHLC. Missing source cells remain `MISSING`/blank and are never silently changed to WAIT.
