# Leakage and chronology audit

- DMA updates require `matured=True` and are isolated by H1/H3/H6 state.
- Sequential conformal residual updates require the corresponding horizon to mature.
- Origin intervals are returned as standalone immutable values; later state updates do not mutate prior origin dictionaries.
- MCS consumes supplied out-of-sample loss vectors only and uses deterministic moving-block bootstrap indices.
- The Settings hook executes only after the existing canonical transaction and publishes shadow evidence under the completed canonical `run_id`.
- Lunch rendering reads the stored session payload and performs no fitting.
- No v15 method writes production BUY/SELL/WAIT values or protected weights.

Unverified: a full database replay against real historical origin records was not available in the supplied runtime data.
