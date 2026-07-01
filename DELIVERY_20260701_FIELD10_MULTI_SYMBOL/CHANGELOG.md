# Change Log — Field 10 Multi-Symbol Upgrade (2026-07-01)

## Added

- Lunch **Field 10 — Multi-Symbol Rank, Data Quality and Higher-Regime Monitor**.
- Searchable multi-select and full checkbox-list selection in Settings.
- Select All, Clear All, and active-symbol controls.
- One main **Run Calculation + Open Lunch** button with Quick, Full, and Super Quick modes behind one mode selector.
- Parent multi-symbol run ID and child symbol IDs.
- Sequential selected-symbol orchestration with per-symbol status, progress, error isolation, compressed state cache, and active-symbol restore without recalculation.
- Provider-neutral symbol aliases for EURUSD, USDJPY, AUDUSD, GBPUSD, USDCAD, USDCHF, EURJPY, GBPJPY, EURGBP, NZDUSD, XAUUSD, BTCUSD, NAS100, and US500.
- MT5 alias/suffix lookup and Twelve Data aliases for the new symbol set.
- SQLite persistence for run status, hourly cross-symbol quality/rank evidence, and the daily Higher-standard lock.
- Hourly **Rank**, **Data Quality Score**, and **Data Quality Grade (A/B/C/D)**.
- Today-only Higher-standard regime, less-risky bias, reliability, transition risk, alpha, delta, rank, and data-quality table.
- Broker-day lock: the first valid daily result remains immutable before broker 23:00; broker 23:00 is the day-end review point.
- Field 10 search, summary tables, hourly history, quality bar chart, reliability scatter plot, grade distribution, and resource report.
- Post-run Field 1–9 integrity observer per symbol.
- Automated tests and synthetic 1/5/10-symbol performance benchmark.

## Changed

- Settings now exposes one heavy calculation trigger instead of three separate run buttons.
- Existing Quick, Full, and Super Quick scopes remain available without changing their protected calculation logic.
- Field 3 now always shows raw Middle-standard and Higher-standard 25-day history when Field 3 is open. Existing compressed regime-episode tables remain unchanged below them.
- Symbol universe now includes NAS100 and US500 while retaining SPX compatibility.
- Lunch root now mounts Field 10 after the existing Field 1–3 renderer.
- Runtime artifacts for Field 10 are excluded from source control.

## Preserved

No existing Field 1–9 calculation, BFP/SFP output, KNN priority, Greedy priority, source history, canonical run, source ID, broker-time calculation, chart, metric, export, or decision formula was intentionally replaced. The new orchestration calls the existing single-symbol Settings transaction once per selected symbol and reads saved results in Lunch.
