# Complete Test Report — 2026-06-28

## Automated suite

Command:

```bash
python -m compileall -q .
python -m pytest -q
```

Result:

- **140 passed**
- **0 failed**
- Runtime: **10.38 seconds**
- Compilation: passed

The baseline before this repair was 125 passing tests. Fifteen additional repair/ARERT tests were added.

## New acceptance coverage

Automated tests cover:

- mixed `str`/`Timestamp` Field 3 sorting;
- Table 1 coalescing that fills only blanks;
- protective-action mapping and raw-value preservation;
- exactly 20 Dinner protective audit columns;
- stale previous-hour copy rejection;
- future-row exclusion at the canonical cutoff;
- analogue current-row self-match prevention;
- ARERT dependency expansion;
- dynamic model weights summing to one;
- finite evidence-capital values;
- finite information-theoretic numeric outputs;
- ARERT score constrained to 0–100;
- same-candle module-cache reuse;
- additive research database migrations preserving an existing table;
- exact Settings button labels and ten-field layout;
- OpenRouter ARERT evidence context;
- one transient OpenRouter retry;
- deterministic local fallback source contract;
- protected Field 3 sorter integration.

## Entry-file smoke tests

Both entry files were launched headlessly and checked through Streamlit health endpoints.

| Entry | Port | Health | Startup result |
|---|---:|---|---|
| `app.py` | 8512 | `ok` | passed |
| `adx_dashpoard.py` | 8513 | `ok` | passed |

Logs are in `reports/smoke_20260628/`.

## Security scan

A pattern scan across source/configuration/documentation found **0 suspicious committed secrets**. Only placeholders remain in `.streamlit/secrets.example.toml`.

## Test limitations

- Smoke testing proves server startup and health, not every manual browser interaction on a physical phone.
- Live Finnhub, Twelve Data, MT5, and OpenRouter requests were not made with real user credentials.
- Mobile clipboard behavior has source and unit-level safeguards but should still be physically checked in the target browser because clipboard permission policies are browser-controlled.
