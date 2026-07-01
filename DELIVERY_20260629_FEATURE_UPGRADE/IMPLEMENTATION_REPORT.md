# ADX Quant Pro Feature Upgrade — 2026-06-29

## Deployment entry points

- Preferred: `streamlit run app.py`
- Backward-compatible: `streamlit run adx_dashpoard.py`
- Python pin: `.python-version` = `3.12`, `runtime.txt` = `python-3.12`

## Implemented requirements

### Global symbol synchronization

- Added a single shared symbol authority in `core/symbol_universe_20260629.py`.
- Added 20 FX pairs, 20 high-volume equities, S&P 500 (`SPX`), plus existing metals/crypto instruments: 45 library symbols total.
- Added dropdown/library and manual typed-symbol workflows.
- Refresh, one-click run payload, connector surfaces, Lunch refresh, and the Settings orchestrator now use the selected symbol instead of silently forcing EURUSD.
- A symbol change preserves the prior canonical snapshot for audit, clears only reconstructable symbol-specific presentation caches, refreshes the selected feed, and marks calculations as needing a new explicit run.

### Navigation, Settings, and application explanation

- Added a visible lightweight Home page.
- Added a Home shortcut that opens Settings with **Explain this App** expanded.
- The comprehensive explanation remains collapsed by default everywhere else.
- Moved **Twelve Data + MT5 Market Connector** directly below the Settings run controls.

### Broker-time synchronization

- Table 1 now uses the same shared broker-clock provider as other Lunch history tables.
- Added `Broker Candle Time`, `Completed Broker Candle`, and `Broker Candle` to the active Lunch history time-column authority.
- This also repairs regime interval compression when history is published under broker-candle column names.

### Lunch Field 1

- Preserved `ui/lunch_decision_table_20260626.py` byte-for-byte to satisfy its protected integrity hash.
- Added `ui/lunch_decision_table_bfd_wrapper_20260629.py` as a presentation-only wrapper.
- Added BFD and SFD to Table 1, overall history, and all factor-history tables.
- Output states are restricted to: `Wait Pullback`, `Hold and Protect`, `Allowed`, and `No Trade`.
- Refactored the AI Summary from metric cards into a dense text-based audit summary with identity, decision state, BFD/SFD, evidence counts, factor details, missing evidence, and ARERT reliability.

### Lunch Field 2

Added an additive, symbol-specific research layer built only during the explicit Settings run:

- Central Tendency path for +1H through +6H.
- GARCH-style recursive volatility forecasts and dynamically expanding upper/lower bands.
- Strong Trend Breakout Probability using candle body expansion, recent resistance/support break, ATR expansion, aligned momentum, volume pressure proxy, and Hurst trend memory.
- 25-day relationship history using Pearson/Spearman agreement, Relationship Trust Score, Absorb/Observe/Do Not Absorb status, definitive BUY/SELL/WAIT relationship decision, and Buy/Sell Relationship Ratio.
- Pie chart of BUY/SELL/NEUTRAL relationship weights.
- Dynamic Time Warping most-similar historical six-hour pattern, with historical Open/Close, subsequent six-hour Close, subsequent return, and an overlay chart of current 6H, matched 6H, and following 6H.
- The original protected prediction cache and production decision remain unchanged.

### Lunch Field 3

- Middle and Higher regime histories continue to use the existing 25-day publishers.
- Fixed broker-candle time recognition so the existing interval compressor now produces one row per consecutive regime episode with Regime Start, Regime End, duration, and observation count instead of hourly repetition.

### Dinner research history

- Added a bounded, newest-first, 25-broker-day research history quality view.
- Deduplicates by completed broker candle.
- Separates reliability, coverage, and uncertainty/conflict.
- Adds evidence status, search, compact display, and CSV export while preserving all original Dinner data and audit exports.

## Architecture and safety

- All new calculations are additive and presentation/research only.
- Existing production decisions, protected Table 3 logic, legacy prediction cache, canonical snapshots, and historical audit data are not overwritten.
- Heavy Field 2 upgrade calculations run only from the Settings calculation transaction; normal chart/expander interactions read the cached result.
