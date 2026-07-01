# Field 2 Data Contract

A reusable Field 2 publication must contain:

- `ok == True`;
- non-empty `main` DataFrame;
- parseable future time column;
- finite central path value column;
- finite summary anchor price;
- compatible `run_id`, `generation_id`, and `snapshot_hash` when present;
- current QUICK source signature including symbol, timeframe, completed candle, OHLC digest, selected session, session mode, protected hash, and feature versions.

Failure of any condition rejects reuse and triggers safe calculation.
