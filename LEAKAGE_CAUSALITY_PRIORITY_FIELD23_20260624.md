# Leakage and Causality

Only completed canonical H1 rows at or before forecast origin are consumed. Features are trailing rolling values. Forecast origin equals the final completed H1 candle. Rendering reads saved snapshots only. Historical rows are protected by idempotent primary keys. All candidates remain shadow-only.
