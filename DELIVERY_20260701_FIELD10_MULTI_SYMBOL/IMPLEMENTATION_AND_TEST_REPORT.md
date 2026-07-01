# Field 10 Multi-Symbol Implementation and Test Report

Date: 2026-07-01  
Application: ADX Quant Pro  
Delivery version: `multi-symbol-field10-20260701-v1`

## 1. Acceptance result

Field 10 did **not** exist in the active Lunch rendering path before this upgrade. It now exists as a real package under `lunch/field_10`, is mounted by the active Lunch root, and remains closed by default to keep normal Lunch rendering light.

The implementation adds:

- Multi-symbol selection in Settings.
- One main calculation button.
- Per-symbol reuse of the existing calculation transaction.
- Per-symbol saved state and error isolation.
- Hourly rank and A/B/C/D data-quality evidence.
- Today-only Higher-standard regime and less-risky bias lock.
- Cross-symbol tables and decision-useful visualizations.
- Always-visible Field 3 Middle/Higher raw history.
- Measured resource reporting.

## 2. Calculation flow

```text
Settings
  ├─ Searchable multi-select / checkbox list
  ├─ Mode: Quick | Full | Super Quick
  └─ Run Calculation + Open Lunch
          │
          ▼
Validate selected symbols and duplicate-run guard
          │
          ▼
Create parent run_id
          │
          ├─ Symbol 1 child ID
          │    ├─ Restore prior symbol cache when available
          │    ├─ Refresh selected source once
          │    ├─ Execute preserved Settings single-symbol pipeline
          │    ├─ Validate saved Field 1–9 objects
          │    ├─ Build Field 10 quality/regime evidence
          │    ├─ Commit SQLite evidence transaction
          │    └─ Compress symbol runtime state to disk
          │
          ├─ Symbol 2 child ID ...
          └─ Remaining selected symbols ...
          │
          ▼
Rank symbols by broker hour and broker day
          │
          ▼
Restore chosen active symbol from cache
          │
          ▼
Open Lunch automatically
          │
          ▼
Field 1–9 render saved canonical result only
Field 10 reads SQLite/cache only; no heavy recalculation
```

Symbols run sequentially. This intentionally avoids simultaneous large DataFrames and unsafe shared Streamlit state. A failed symbol is recorded and does not cancel completed symbols.

## 3. Canonical and multi-symbol schemas

### Existing canonical result

The existing canonical result remains the source of truth. Field 10 reads, but does not redefine, these identity fields when available:

```text
run_id
symbol
timeframe
source_id | data_source_id | snapshot_hash
latest_completed_candle_time
broker_candle_time
regime
final_decision
```

### Multi-symbol parent manifest

```text
parent_run_id
selection_fingerprint
selected_symbols[]
active_symbol
calculation_scope
status
completed_symbols
failed_symbols
elapsed_seconds
symbol_status{symbol -> status/progress/stage/error/child_run_id}
symbol_summaries{symbol -> quality/daily/hourly/field_validation}
resource_report
version
```

### Per-symbol cache

Each completed symbol is stored as a secret-free compressed runtime state:

```text
data/multi_symbol_runtime_20260701/<SYMBOL>.pkl.gz
```

The cache reuses the existing runtime-cache sanitizer. API keys, passwords, tokens, credentials, and secret widget values are excluded.

## 4. Field 10 database schema and migration

Runtime database:

```text
data/multi_symbol_field10_20260701.sqlite3
```

Tables:

### `multi_symbol_runs`

Primary key: `(parent_run_id, symbol)`

Stores child ID, symbol, timeframe, scope, status, elapsed time, RSS delta, CPU time, canonical run ID, source ID, completed candle, error, and creation time.

### `field10_hourly_quality`

Primary key: `(parent_run_id, symbol, broker_timestamp)`

Stores hourly rank, A/B/C/D grade, quality score, Higher-standard regime, less-risky bias, trust, reliability, validation status, reason, run ID, and source ID.

### `field10_daily_higher_lock`

Primary key: `(broker_day, symbol)`

Stores today’s rank, Higher-standard regime, less-risky bias, A/B/C/D grade, quality score, Higher reliability, transition risk, alpha, delta, sample count, lock status, lock/review timestamps, parent run ID, run ID, and source ID.

Migration uses `CREATE TABLE IF NOT EXISTS`, indexes, WAL journal mode, `BEGIN IMMEDIATE`, commit/rollback, and does not delete old rows.

## 5. Daily lock rule

- The broker timestamp is obtained from the shared broker-time provider or the canonical broker-candle timestamp.
- It is not silently converted to UTC for the broker-day/hour decision.
- The first valid row for `(broker_day, symbol)` is inserted with `TODAY_LOCKED_UNTIL_23H`.
- Before broker 23:00, later runs cannot overwrite that row.
- At or after broker 23:00, the row may be reviewed and updated with `DAY_END_REVIEW_23H`.
- A new broker day creates a new row.

This lock applies to the Field 10 today table only. It does not modify the protected Field 3 daily-lock calculation.

## 6. Rank and data-quality calculation

### Data-quality score

The additive score begins at 100 and transparently deducts for:

- Invalid timestamps.
- Exact duplicate candles.
- Missing H1 periods.
- Less than 600 rows for Higher-standard history.
- Missing or invalid OHLC columns/rows.
- Missing run/symbol/timeframe identity.
- Missing source ID.
- A lower Field 3 data-quality gate, when published.

Grades:

```text
A = score >= 90
B = score >= 75 and < 90
C = score >= 60 and < 75
D = score < 60
```

### Hourly rank

```text
composite = 0.70 × data_quality + 0.20 × trust + 0.10 × reliability
```

Symbols are ranked descending within the same broker timestamp using dense rank.

### Today rank

```text
composite = 0.75 × data_quality + 0.25 × Higher-standard reliability
```

The rank is decision support only. It does not replace an existing trading decision.

## 7. Field 1–9 integrity observer

For every completed symbol, Field 10 creates a read-only integrity table containing:

```text
Field
Status
Result Key
Object Type
Row Count
Column Count
Symbol
Timeframe
Run ID
Source ID
Validation Message
```

Statuses are `COMPLETED`, `PARTIAL`, `NOT_STARTED`, or `STALE`. Empty objects are not reported as completed, and no missing trading value is fabricated.

## 8. Symbol alias rules

Canonical application names remain provider-neutral. Connector-bound aliases include:

```text
BTCUSD -> BTC/USD, XBTUSD, provider exchange forms
XAUUSD -> XAU/USD, GOLD
NAS100 -> USTEC, US100, NDX, NASDAQ100
US500 -> SPX500, SP500, SPX, GSPC
```

Twelve Data receives slash-form FX symbols and index aliases (`NDX`, `SPX`). MT5 tries the canonical symbol, known provider aliases, and broker suffix/prefix variants returned from Market Watch. The exact available broker symbol still depends on the connected broker account.

## 9. API credential resolution

The existing secure resolver is preserved. Resolution order is server-side Streamlit Secrets, environment variable, then an optional temporary session replacement.

Supported canonical/compatible names include:

```toml
[api_keys]
second_api = "..."      # canonical Twelve Data name
twelve_data = "..."     # compatible alias
twelve = "..."          # compatible alias
finnhub = "..."
openrouter = "..."

[openrouter]
api_key = "..."         # compatible alias
```

Environment aliases include `TWELVE_DATA_API_KEY`, `TWELVE_API_KEY`, `FINNHUB_API_KEY`, and `OPENROUTER_API_KEY`. Secrets are not copied into Field 10 caches, tables, logs, exports, or UI values.

## 10. Session and time rules

- Existing shared broker-time and session detection remain authoritative.
- Field 10 uses canonical broker candle time for daily lock and display identity.
- Hourly history stores a timestamp per canonical row.
- Field 3 raw Middle/Higher tables continue through the existing broker-clock display adapter.
- Local phone/PC time is not used to identify a market candle.

## 11. Field 3 display repair

When Field 3 is open, the following now render before the existing compressed tables:

- Middle Standard Regime History — Raw Latest 25 Days.
- Higher Standard Regime History — Raw Latest 25 Days.

The renderer first uses the published canonical regime detail tables, then the saved Field 3 lifecycle history. When neither exists, it shows an explicit diagnostic row rather than a fake regime or bias. Existing interval-compressed Middle/Higher views remain intact.

## 12. Performance and resource report

Synthetic benchmark scope: 600 H1 rows per symbol, Field 10 validation, SQLite persistence, ranking, compressed state cache, and active-symbol restore. It excludes live API network latency and the protected model runtimes.

| Symbols | Hourly rows | Wall time | CPU time | RSS delta | Compressed cache | Heat proxy |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 600 | 0.1553 s | 0.14 s | 2.0312 MB | 0.0147 MB | LOW |
| 5 | 3,000 | 0.6322 s | 0.59 s | 2.2031 MB | 0.0734 MB | LOW |
| 10 | 6,000 | 1.2708 s | 1.18 s | 2.9727 MB | 0.1469 MB | LOW |

These numbers are from this sandbox and are not promises for live API/model execution. Actual total calculation time is approximately the sum of each selected symbol’s protected pipeline time plus network latency. Sequential execution reduces peak memory and CPU contention, but ten symbols naturally take longer than one.

“Heat” is a CPU-time proxy. Streamlit Cloud and this sandbox do not expose the user device’s physical temperature sensors.

## 13. Testing report

### Full project suite

```text
186 passed in 29.32s
```

The full suite was executed with a lightweight Streamlit import stub because the sandbox does not have the `streamlit` package installed. The stub allows non-browser unit tests to import UI modules; it is not used or included by the deployed application.

### Targeted regression suite

```text
25 passed in 11.18s
compileall: PASS
```

Coverage includes:

- Required symbols and aliases.
- MT5/Twelve connector-bound aliases.
- Grade boundaries.
- More than 2,000 candles.
- Duplicate and missing candles.
- Daily lock immutability before 23:00.
- Day-end update at 23:00.
- Broker wall-hour preservation.
- Hourly ranking.
- Multi-symbol isolation/cache restore.
- One main run button.
- Active Field 10 integration.
- Always-visible Field 3 Middle/Higher tables.
- Existing Field 3 lifecycle tests.
- Existing Lunch broker-time synchronization tests.
- Full Python compilation.

## 14. Mobile responsiveness

- Field 10 is closed by default.
- Only the active symbol’s hourly table is loaded into the visible view.
- Tables use Streamlit controlled scrolling.
- Selectors and buttons use full-width/touch-friendly controls.
- Charts use container width.
- Long evidence is placed in tables/expanders.
- Symbols calculate sequentially rather than displaying all full symbol states simultaneously.

Browser-level iPhone testing was not possible in this sandbox because Streamlit is not installed and no browser/device runner is available.

## 15. Unresolved limitations

1. Live MT5, Twelve Data, Finnhub, OpenRouter, reconnect behavior, and provider rate limits require the user’s credentials/network and were not exercised here.
2. Physical device temperature cannot be measured; only CPU-time-based heat proxy is reported.
3. Full protected model execution for 1/5/10 symbols was not benchmarked because it requires live project data and connected providers. The supplied benchmark measures the new orchestration/persistence overhead only.
4. Broker index names vary. MT5 dynamically searches aliases and suffixes, but the broker must expose the instrument in Market Watch.
5. Streamlit browser interactions were not run in this environment. The full non-browser suite and import/compilation checks passed.

## 16. Streamlit Cloud deployment

1. Upload the upgraded project contents to the existing GitHub repository root.
2. Do not upload `.streamlit/secrets.toml`, generated `*.sqlite3`, or `data/multi_symbol_runtime_20260701/`.
3. In Streamlit Cloud, set the main file to `app.py`.
4. Use Python 3.12, matching `.python-version` and the project deployment requirements.
5. Add server-side secrets in Streamlit Cloud **App → Settings → Secrets**, for example:

```toml
[api_keys]
second_api = "YOUR_TWELVE_DATA_KEY"
finnhub = "YOUR_FINNHUB_KEY"
openrouter = "YOUR_OPENROUTER_KEY"

[automation]
auto_connect = true
```

6. Deploy/reboot the app.
7. Open Settings.
8. Test the market connector and verify the active broker-time offset/timezone.
9. Select one symbol first and run **Run Calculation + Open Lunch**.
10. Verify Field 1–3 and Field 10.
11. Increase to five symbols, then ten symbols while watching the progress/resource report and provider rate limits.
12. Confirm that switching the active symbol in Field 10 restores saved data without a new calculation.
13. Confirm the daily Higher-standard row does not change before broker 23:00 and receives `DAY_END_REVIEW_23H` after the day-end review.
