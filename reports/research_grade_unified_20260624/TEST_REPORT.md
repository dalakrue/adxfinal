# Executed Test Report

## Result

- **609 tests passed** across all 65 project test files, executed in five complete batches.
- All Python files compiled successfully.
- Import smoke passed for the unified core, Settings service, read-only UI module, and `app`.
- Live Streamlit startup passed; `/_stcore/health` returned `ok` on port 8766.
- Protected Field 1/production comparison passed for 17 files; every before/after hash is identical and matches the supplied baseline.

## Required checks

| Required check | Result |
|---|---|
| ZIP extraction and inventory | PASS |
| Protected hash baseline | PASS |
| Python compilation | PASS |
| Import smoke | PASS |
| Streamlit startup smoke | PASS |
| Additive DB migration | PASS |
| Idempotent rerun | PASS |
| Canonical snapshot consistency | PASS |
| Broker-time consistency | PASS |
| Origin-time leakage guard | PASS |
| Independent H1/H3/H6 settlement | PASS |
| Conformal historical immutability | PASS |
| Probability calibration separation | PASS |
| CRPS correctness | PASS |
| Regime posterior normalization | PASS |
| Changepoint recursive update | PASS |
| Model Confidence Set | PASS |
| SPA block bootstrap | PASS |
| DM overlapping horizon | PASS |
| Field 1 before/after hashes | PASS |
| Ordinary rerun no-heavy-work guard | PASS |
| Settings one-click + Lunch navigation | PASS |
| Mobile static/lazy-render smoke | PASS |
| Missing optional full model | PASS |
| No-API-key fallback | PASS |

The first monolithic `pytest -q` invocation exceeded the execution time limit after progressing without failures. The final code state was therefore validated by executing the same 65 files in five exhaustive batches: 173 + 109 + 142 + 181 + 4 = 609 passed. A combined shell wrapper also timed out between batches, but each batch was completed separately. No test file was omitted.
