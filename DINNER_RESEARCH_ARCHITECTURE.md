# Dinner Research Architecture

## Purpose

The project now separates the protected production decision system from an academic research layer.

- **Layer A — Protected Production:** the existing Lunch canonical snapshot and its price, OHLC, decisions, regimes, pressure, forecast, reliability, NLP, pattern, and session outputs.
- **Layer B — Dinner Research:** a read-only, reproducible ARERT laboratory that consumes one frozen completed-candle Layer A snapshot. It cannot overwrite Lunch values and is not a live trading-command generator.

## Runtime flow

1. The protected Settings run publishes the canonical production generation.
2. The user explicitly selects **Run Full Dinner Thesis Research + Open Dinner** or **Run Selected Dinner Research Module**.
3. `research_quant.arert_lab.build_context` resolves completed OHLC, timestamped production decisions, and timestamped news at or before the canonical candle.
4. Module dependencies are expanded, then selected modules run in numerical order.
5. Results are cached by completed candle, symbol, timeframe, module, ARERT version, parameter version, and snapshot hash.
6. `research_quant.arert_store` persists the result to a separate additive SQLite database.
7. `research_quant.ui.arert_dinner_lab` renders cached results in ten top-level fields. Expander changes never run models.

## Ten Dinner thesis fields

| Field | Laboratory | Modules |
|---|---|---|
| 1 | Research Snapshot and Data Integrity | canonical identity, freshness, quality, DB, benchmark |
| 2 | Multi-Scale Regime | 1–4 |
| 3 | Forecast and Uncertainty | 5–6 |
| 4 | Decision Reliability | 7–10 |
| 5 | Historical Analogue | 11–12 |
| 6 | Behavioral Finance and NLP | 13–15 |
| 7 | Model Ecology and Drift | 16 |
| 8 | Event Response | 17 |
| 9 | Evidence Information | 18 |
| 10 | Thesis Validation and ARERT | 19–20 |

Field 1 opens by default. Fields 2–10 are closed by default. There are no nested expanders inside these research fields.

## Data contracts

Every module result records: `run_id`, `generation_id`, symbol, timeframe, completed broker candle, research-model version, input-data version, calculation timestamp, sample period, sample size, data-quality status, input hash, output hash, runtime, and peak module memory.

Missing data produces an explicit incomplete status. No synthetic production result is substituted. Raw production values remain available in their original columns.

## Main files

- `research_quant/arert_lab.py` — context, modules, dependency expansion, caching, result envelope.
- `research_quant/arert_store.py` — isolated additive SQLite persistence.
- `research_quant/ui/arert_dinner_lab.py` — cached read-only ten-field renderer.
- `tabs/antd_page_router_20260615.py` — explicit Settings controls.
- `tabs/field456789_page_20260626.py` — Dinner integration.
- `scripts/benchmark_arert_20260628.py` — reproducible repeated-run benchmark.
