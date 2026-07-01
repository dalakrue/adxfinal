# ADX Quant Pro — CRCEF-SV Repair and Thesis Upgrade

Date: 2026-06-27  
Primary instrument/timeframe: EURUSD H1  
Priority source: `FINAL_MASTER_IMPLEMENTATION_COMMAND_V2_20260627.md`

## Delivery status

The attached project was edited, compiled, tested, smoke-tested through both Streamlit entry files, exercised with Streamlit AppTest, and packaged with rollback evidence.

All repository tests pass:

```text
110 passed, 0 failed
```

The package does **not** claim live-market validation. Live connector credentials and a newly fetched market generation were unavailable. Those limitations are explicit below and in `docs/LIMITATIONS_AND_ETHICS.md`.

## High-priority repairs

### One application shell

`app.py` and `adx_dashpoard.py` now call `core.app_shell.run_app` directly. The legacy entry remains usable but no longer owns a separate router or error-wrapper shell.

### Independent navigation

Top-level page state is owned by `core/navigation_state_20260627.py`. A route request is committed before page rendering. Lunch, Dinner, charts, fields, and expanders cannot overwrite the committed page.

The floating menu exposes:

```text
Settings · Lunch · Dinner · AI Assistant · Morning · Research · Other
```

Streamlit AppTest verified Dinner before a calculation and after the full Settings run, with zero exceptions.

### Direct Dinner page

Dinner now renders in this order:

1. canonical identity;
2. `Dinner Combined History — Last 25 Broker Days`;
3. compact current metrics;
4. closed Field 4;
5. closed Field 6;
6. closed Field 7;
7. closed Field 8;
8. closed Field 9;
9. closed CRCEF-SV diagnostics;
10. audit/export evidence.

The combined table recursively reads real published timestamped data and preserves field disagreements. It never creates a fake 25-day row.

### Canonical timestamp and Power BI integrity

`core/canonical_identity_20260627.py` accepts the project’s explicit broker-clock publication format, including:

```text
2026-06-22 07:00:00 (Broker UTC+3)
```

That value normalizes to `2026-06-22T04:00:00Z` without local-PC or browser time. NaT, malformed offsets, and non-H1 candles fail explicitly.

Power BI uses one state enum:

```text
VALID
INSUFFICIENT_DATA
STALE
IDENTITY_MISMATCH
INVALID_TIMESTAMP
PATH_UNAVAILABLE
PUBLICATION_INCOMPLETE
```

A projection is exact-run valid only when run ID, generation ID, symbol, timeframe, completed candle, source snapshot hash, and source signature match. No stale path is silently substituted. Failure of only the optional green path does not remove the protected chart.

### Table 1

Table 1 is a read-only collection of the exact Table 3 factor publications. It joins by completed broker candle and carries source paths, run/generation, snapshot hash, and source signature.

It does not infer BUY/SELL from score sign. Exact labels remain exact. Display-only behavior is separated:

```text
Production Decision Raw = HOLD
Action Display Label = HOLD & PROTECT
```

The deterministic Table 3 verification preserved `WAIT PULLBACK`, `HOLD`, and `SELL`, with all Net Pressure, Direction Confirmation, and Master labels matching and zero blank final decisions.

The disconnected cached AppTest run had no settled Table 3 history rows, so live row-by-row comparison was not claimed. A one-row pending production record remained visible without invented historical rows.

### Table 4

Production logic and thresholds were preserved. The requested lower WAIT standard was not implemented by arbitrary threshold halving. A closed research-only threshold audit evaluates candidate thresholds only when a continuous score and settled outcomes exist.

When completed OHLC is unavailable but real timestamped NLP rows exist, Table 4 may show a clearly labeled read-only published-news fallback. It does not disguise missing OHLC as a calculated trading result.

### Table 5

Table 5 is now `Integrated Decision Collection`. It selects and joins Table 1 and Table 4 columns by canonical candle identity.

`Master Action` is copied from an explicit production source and is the last production column. CRCEF-SV research columns follow it. The live cached verification produced 28 selected columns and did not duplicate all of Field 1.

### One Settings run

The full Settings button runs the protected pipeline first, performs post-run identity binding, runs additive research publishers, publishes CRCEF-SV, and opens Lunch. The UI no longer requires a second Lunch Quick Sync. All Lunch fields return closed.

In the disconnected AppTest run, the protected orchestrator reported overall data-source failure because no live connector was available, but it still reused the valid cached canonical `calc-7 / generation 7`, published CRCEF-SV as `RESEARCH_ONLY`, opened Lunch, and kept Dinner navigation functional. This is reported rather than misrepresented as a fresh live calculation.

## CRCEF-SV research package

The new `research_quant/` package contains:

- immutable schemas and canonical adapter;
- CPCV, purging, embargo, PBO, and metrics;
- probability calibration and reliability diagrams;
- direction/actionability meta-labeling;
- Markov regime lifecycle and transitions;
- multi-scale multifractal volatility diagnostics;
- EnbPI adaptive conformal intervals;
- Bellman interval control;
- ADWIN-style drift monitoring and promotion guard;
- optional lazy TFT multi-horizon adapter;
- entity-aware NLP event-response memory;
- evidence registry, selective policy, explanations, and CRCEF-SV fusion;
- additive SQLite persistence and audit UI.

The complete file-by-file description is in `NEW_MODULE_CATALOG.md`. Paper-to-code mapping is in `docs/RESEARCH_PAPER_IMPLEMENTATION_MAP.md`; equations are mapped in `docs/MATHEMATICAL_DEFINITIONS.md`.

The cached verification publication had:

```text
run_id: calc-7
generation_id: 7
status: RESEARCH_ONLY
production_decision_unchanged: true
runtime: approximately 0.022 seconds
peak CRCEF-SV traced memory: approximately 0.036 MB
```

These runtime figures measure only the additive CRCEF-SV publisher in that cached run, not the whole application, and are not presented as a 30–50% whole-system benchmark.

## Persistence

The initialization command creates 12 additive tables:

```text
canonical_snapshots
research_results
research_model_registry
research_validation_runs
calibration_models
drift_events
prediction_intervals
prediction_outcomes
event_memory
event_responses
promotion_decisions
research_audit
```

Automated tests verify empty-state migration and duplicate-run idempotence.

## Test and smoke evidence

- `COMPILE_OUTPUT.txt`: compile-all exit 0.
- `FULL_PYTEST_OUTPUT.txt`: 110 passed.
- `TARGETED_PYTEST_OUTPUT.txt`: priority/projection/research/persistence tests passed.
- `SMOKE_app_py.log`: health `ok`.
- `SMOKE_adx_dashpoard_py.log`: health `ok`.
- `APPTEST_ENTRY_PARITY.txt`: same menu and zero exceptions through both entries.
- `APPTEST_UI_EVIDENCE.txt`: direct Dinner, closed Lunch, Field 1, Field 3, Dinner-after-run.
- `APPTEST_CANONICAL_INSPECTION.txt`: exact cached identity and successful CRCEF-SV publication.
- `TABLE1_TABLE3_SYNTHETIC_EXACT_LABEL_VERIFICATION.csv`: exact label mapping evidence.
- `TABLE1_TABLE5_VERIFICATION.json`: Table 5 production/research boundary and final-column ordering.
- `DATABASE_INITIALIZATION_OUTPUT.txt`: all 12 tables created.

## Source and data preservation

No original file was deleted. No original history/data file remains modified after testing. Test-created runtime databases were removed from the project data directory.

Protected Table 3 calculation/publisher files remained byte-identical, including the canonical sync, Field 1 publication bridge, full-metric adapters, EURUSD H1 matrix, and original renderer. Only read-only Table 1/Table 4/Table 5 adapters and presentation code were changed.

## Commands

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Backward-compatible entry:

```bash
streamlit run adx_dashpoard.py
```

Database initialization:

```bash
python -m research_quant.persistence.research_store --db data/crcef_sv_research.sqlite3
```

Verification:

```bash
python -m compileall -q .
PYTHONPATH=. pytest -q
```

No separate training command is applicable to this delivery. No model was trained or promoted from unavailable live credentials or unsettled history. Optional TFT remains lazy and unavailable until a validated artifact is supplied.

## Safe rollback

From the project root:

```bash
python delivery_crcef_sv_20260627/rollback_repair_20260627.py --project-root .
```

The rollback archive restores only modified original source/config files and removes only source/document/test files that were absent from the uploaded ZIP. It does not erase user history/data.

## Remaining limitations

1. Twelve Data, MT5/Doo Prime, and Finnhub live credentials were not available.
2. A newly fetched exact-run Power BI market path could not be exercised; strict identity, timestamp, mismatch, and no-stale-fallback behavior passed automated tests.
3. The cached run reused the uploaded project’s June 22, 2026 completed broker candle. This is clearly marked as cached, not current live market data.
4. Long-window validation, calibration, conformal coverage, drift conclusions, NLP event outcomes, and ablations require settled samples. Modules return pending/insufficient statuses instead of invented statistics.
5. Optional TFT libraries/artifacts were unavailable. The base Streamlit app remains functional without them.

See `VERIFICATION_MATRIX.md` for the itemized checklist.
