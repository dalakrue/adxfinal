# Test Report — 2026-06-29

## Automated tests

Command:

```text
python -m pytest -q tests
```

Result:

```text
153 passed in 19.09s
```

The new focused suite verifies:

- 20 FX + 20 equities + S&P 500 symbol-library contract.
- Alias normalization and global symbol-state publication.
- BFD/SFD outputs are limited to the four required action states.
- Strong breakout probability reacts to a synthetic large resistance-breaking candle.
- Dynamic bands remain above/below central tendency and expand with volatility/breakout evidence.
- Relationship table publishes trust, absorb status, decisions, and Buy/Sell ratio.
- DTW similar-day output includes historical and subsequent six-hour evidence.
- Regime history compresses repeated hourly states into start/end intervals.
- Dinner research history deduplicates broker candles and publishes reliability status.

## Compilation

Command:

```text
python -m compileall -q core ui tabs pages research_quant app.py adx_dashpoard.py
```

Result: exit code `0`.

## Streamlit execution smoke tests

`streamlit.testing.v1.AppTest` executed both entry files:

```text
app.py             exceptions=0
adx_dashpoard.py   exceptions=0
```

Headless server health checks also returned `ok` for both entry files.

## Environment note

Streamlit 1.58.0 was used for the sandbox smoke test. The project requirement remains `streamlit>=1.35,<2`. Live Twelve Data, Finnhub, and local MT5 provider calls were not executed because deployment credentials/terminal connectivity were not used in this sandbox test. Provider-specific symbol availability still depends on the selected connector and its symbol naming rules.
