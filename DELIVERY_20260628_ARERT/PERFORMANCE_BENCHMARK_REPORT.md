# Performance Benchmark Report — 2026-06-28

## Benchmark design

A deterministic synthetic 900-row EURUSD-like H1 series was used to run all 20 ARERT modules twice with the same completed candle, symbol, timeframe, source snapshot, model version, and parameter version.

This benchmark measures repeated same-candle research work. It is not a claim about live market accuracy or total device resource consumption.

## Results

| Measurement | First run | Same-candle cached run | Reduction |
|---|---:|---:|---:|
| Wall time | 5.140249 s | 0.418171 s | **91.86%** |
| Cache hits | 0 / 20 | 20 / 20 | all modules reused |
| Maximum measured module calculation peak | 44.5946 MB | 0.0 MB | 100% module-recalculation peak eliminated |

The cached run still reconstructs the bounded research context and persists the envelope, so it is not zero-cost.

## Implemented performance controls

- explicit-only research execution;
- per-module same-candle cache identity;
- no model execution on Dinner expander changes;
- one selected detailed legacy Dinner field at a time;
- compact display pruning without deleting stored data;
- current-copy payload cache by canonical identity;
- exact-candle payload filtering;
- vectorized feature calculations;
- additive indexed SQLite store;
- no repeated API request in the ARERT renderer.

## Honest interpretation

The measured repeated research time reduction exceeds the requested 30–50% target in this controlled benchmark. The result **does not prove** a 30–50% device-wide CPU or RAM reduction on every mobile phone. Physical device profiling is still required before making that broader claim.
