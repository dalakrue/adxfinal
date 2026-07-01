# Field 8 Data Contract

Field 8 is restricted to EURUSD H1 and a 25-calendar-day window of completed candles.

## Identity
Every publication is keyed by `(run_id, generation_id, snapshot_hash)`. Every history row has a unique compound key including symbol, timeframe, broker candle time, forecast origin, horizon and target time. Mixed identities return no table.

## Maturity
- `SETTLED`: H+6 actual exists.
- `PARTIALLY_SETTLED`: at least H+1 or H+3 exists but H+6 does not.
- `PENDING`: no matured actual exists.

PENDING rows remain visible and are never treated as settled accuracy observations.

## Table
The renderer exposes one table with 70 columns spanning identity/maturity, Field 1 decision evidence, Field 2 prediction evidence, Field 3 regime evidence and integrated shadow evidence.

## Trust score
The implemented version follows the requested 20/40/30/10 component structure when settled path direction evidence exists, then subtracts structural-break and coverage-debt penalties. Insufficient settled path evidence remains `NaN`/`INSUFFICIENT_DATA`, not zero.
