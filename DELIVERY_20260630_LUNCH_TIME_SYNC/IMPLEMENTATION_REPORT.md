# Lunch Tab MetaTrader Time Synchronization Repair

## Result
All current/last-update candle timestamps displayed by the Lunch tab now resolve from one shared completed-H1 MetaTrader broker-clock contract. UTC remains the storage identity, while broker time is the display clock.

## Root causes repaired

1. A restored session could keep an old canonical object from 2026-06-17 even when a newer completed-H1 market frame was already loaded.
2. Field 1 cache selection stopped at the first valid cache instead of comparing timestamps across all published metric and OHLC candidates.
3. Some display paths updated the main timestamp but left stale `Date`, `Weekday`, `Hour`, `Time`, `Datetime`, `Timestamp`, `Broker Candle Time`, or completed-candle aliases unchanged.
4. Field 2 Plotly axes were serialized as UTC-naive values, allowing Field 2 to disagree with the broker-hour display used elsewhere.
5. Unified trust-history caching did not include the broker-clock contract and offset in its cache identity.
6. Some Field 1 Tables 4/5 and Field 3 matrix paths bypassed the shared broker display projection.

## Repairs implemented

- Upgraded the shared broker-time contract to `broker-time-contract-20260630-v4`.
- The freshest completed-H1 timestamp is selected across the active canonical object and loaded authoritative market frames.
- The frame being rendered is treated as authoritative freshness evidence, preventing an old canonical object from filtering newer rows.
- Every visible date/time alias is rebuilt from the same broker-aware timestamp on every render.
- Field 1 validates and repairs its publication pointer every time the field opens.
- Field 1 metric/OHLC bridge now chooses the newest valid publication rather than the first cache key.
- Field 1 Tables 4 and 5, unified trust history, identity strips, and sync cards use the shared clock.
- Field 2 chart axes, cached history tables, session history, and latest-H1 caption use the same broker-clock projection.
- Field 3 completed-H1 regime matrix uses the shared broker-clock projection.
- Cache signatures now include latest completed H1, broker offset, and clock-contract version so an old table cannot survive an offset or generation change.
- No local PC clock or `datetime.now()` value is used as candle identity. Processing time remains metadata only.

## Important behavior

Historical rows keep their own true historical candle times. The newest/current/last-update row is synchronized to the latest completed MetaTrader H1 candle available in the project state. The system does not invent the current wall-clock hour when no completed broker candle exists.

When broker offset evidence is unavailable, the UI says broker time is unavailable instead of silently guessing an offset.
