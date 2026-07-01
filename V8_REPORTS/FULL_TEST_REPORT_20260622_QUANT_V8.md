# Full Test Report — Quant Research V8

## Final result

- Collected tests: **524**
- Passed: **524**
- Failed: **0**
- Skipped: **0** after installing the dependencies already declared in `requirements.txt` (`duckdb` and `streamlit`) and rerunning the three previously skipped startup/dependency checks.
- Unverified automated tests: **0**

The suite was executed in bounded batches because the execution environment imposes a per-command runtime cap. Every collected node was accounted for and passed at least once in the final validation. A 71-test final regression subset covering all changed integration areas also passed after the last code patch.

## V8-specific coverage

The new suite validates CQR ordering/coverage, adaptive widening, future/same-row leakage rejection, Fixed-Share bounds, Bates–Granger singular fallback, conditional trust small-sample behavior, deterministic SPA/Reality Check/PBO, ADWIN stable/shifted streams, all migrations, idempotency, secret redaction, UTC/broker/Myanmar time, DST, invalid offsets, Field 1 filtering/identity, no calculation on display opens/tab switches, Save+Connect debounce, Settings→Lunch Field 1 navigation, Python 3.12/startup, mobile-width controls, and last-valid-generation preservation.

## Non-failing warnings

Recorded warning summaries include legacy sklearn and pandas deprecation warnings in V4/V7 research modules. They do not change test outcomes and were not introduced as production influence by V8.

## Live-environment validation boundary

Headless Streamlit startup passed. A real Streamlit Cloud deployment, real Doo Bridge timestamp, live MT5 terminal and live API credentials were not available in this container; those operational checks remain environment-dependent rather than failed tests.
