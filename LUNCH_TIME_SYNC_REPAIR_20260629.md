# Lunch Time Synchronization Repair — 2026-06-29

## Fixed
- The shared broker-time provider no longer blindly prefers a restored stale canonical timestamp.
- It compares the canonical completed-H1 timestamp with loaded market frames and selects the newest authoritative candle.
- Lunch visible `Date`, `Weekday`, and `Hour` columns are rebuilt from the same broker timestamp.
- Field 1 can bridge up to 600 missing H1 rows instead of only 24 hours when loaded market data is newer than its cached history.
- No protected trading score, decision, forecast, regime, TP, or SL calculation was changed.

## Regression evidence
- Stale canonical: `2026-06-17 15:00 UTC`
- Loaded newest H1: `2026-06-28 20:00 UTC`
- Result: shared clock and visible table columns display `2026-06-28 20:00`.
- Tests: `7 passed`.
