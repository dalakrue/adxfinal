# Data Leakage Controls

1. **Canonical cutoff:** all context tables are filtered at or before the frozen completed broker candle.
2. **Completed candles only:** no forming-candle values are accepted as settled historical evidence.
3. **Forward labels separated:** H+1/H+3/H+6 returns are labels and are unavailable until their horizons settle.
4. **Analogue self-exclusion:** the current row is removed before distance calculation; unsettled tail rows are excluded.
5. **Chronological splits:** training precedes validation, which precedes final test.
6. **Purging:** samples whose label horizons overlap the next split must be removed.
7. **Embargo:** a post-split gap is used where model selection could leak adjacent labels.
8. **Validation-only selection:** abstention thresholds and future fitted ARERT weights cannot use the final test set.
9. **Timestamped news:** event/news evidence is joined only by valid historical timestamps; no title-based future lookup.
10. **Cache identity:** cache reuse requires matching candle, symbol, timeframe, module, versions, and source snapshot identity.
11. **Isolated persistence:** research records are stored separately and cannot silently rewrite production tables.
12. **No fake imputation:** missing production outputs remain missing or produce an explicit incomplete status.

Automated tests cover future-row filtering, analogue self-match prevention, chronological split behavior, finite numerical outputs, cache behavior, and production non-overwrite metadata.
