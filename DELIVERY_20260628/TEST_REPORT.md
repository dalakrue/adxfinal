# Test and Smoke-Test Report

Date: 2026-06-28

## Automated test suite

Command:

```bash
PYTHONPATH=. python -m pytest -q
```

Result:

- **125 passed**
- **0 failed**

The suite includes eight new regression tests covering:

1. Table 5 joins Table 1 and Table 4 by normalized UTC hour.
2. Single-label NLP evaluation emits no sklearn warning and yields a stable 3×3 matrix.
3. New OHLC plus old canonical/old metric is rejected as stale.
4. New OHLC plus fresh metric rebinds canonical identity.
5. OpenRouter validation and chat-completion calls work through a mocked HTTP transport.
6. AirLLM remains optional and Python is pinned to 3.12.
7. Browser warm-cache selection includes visible Table 1.
8. Super Quick alone maps to the Fields 1–3 protected scope, while Quick maps to Fields 1–9 + AI.

## Compilation

Command:

```bash
python -m compileall -q .
```

Result: **PASS**

## Streamlit AppTest

Both entry files were launched with Streamlit's test runner. For each entry, the test:

- Loaded the login page.
- Continued as Guest.
- Verified Settings rendered the OpenRouter one-click connector and Super Quick button.
- Opened Lunch.
- Opened Dinner.
- Opened AI Assistant.
- Confirmed no uncaught Streamlit exception.

Results:

- `app.py`: **PASS**
- `adx_dashpoard.py`: **PASS**

## Headless HTTP health smoke test

Both entry files were started as headless Streamlit servers and queried through `/_stcore/health`.

Results:

- `app.py`: **HEALTH PASS**
- `adx_dashpoard.py`: **HEALTH PASS**

## Security scan

A project-wide pattern scan found no stored OpenRouter-style secret.

Result: **PASS — no OpenRouter secret pattern found**

## Live testing boundary

No exposed user credential was used. OpenRouter behavior was tested with a deterministic mocked HTTP service. Live Finnhub, Twelve Data, MetaTrader, and OpenRouter results depend on credentials, provider availability, rate limits, internet access, and the user's installed MT5 terminal. The application now records those failures without corrupting the canonical generation.
