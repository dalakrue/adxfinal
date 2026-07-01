# Performance Benchmark Report

## Environment

Deterministic synthetic completed-candle data: 840 source rows; generated Table 2: 600 rows × 126 columns across 25 broker days. Results are medians across repeated runs.

## Results

- Table 2 cold build: **1.1845 s**.
- Same-candle cached Table 2 request: **0.4232 s**, a measured **64.27%** reduction.
- IMAP-RV cold build: **0.5919 s**.
- IMAP-RV same-candle cache lookup: **0.00000471 s**, a measured **99.9992%** reduction.
- Mobile 10-row/13-column frame memory versus full 600-row/126-column frame: **99.85%** smaller.
- Serialized mobile payload versus full frame: **99.84%** smaller.
- Mobile serialization time versus full frame: **99.05%** lower.
- Mobile page and column changes invoked **0 heavy calculations** in the benchmark.

## Interpretation

The requested 50–70% target was met for repeated same-candle Table 2 work in this deterministic benchmark (64.27%). Payload/render proxies exceeded the target. This does **not** prove a 50–70% reduction in cold full-system calculation, browser CPU, battery use or physical phone temperature. Those require a real phone/browser measurement campaign. Raw results are in `PERFORMANCE_BENCHMARK_RAW.json`.
