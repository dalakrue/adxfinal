# Complete Test Report

## Automated suite

`PYTHONPATH=. pytest -q` completed with **155 passed**.

The new test module verifies:

- 25 broker days and up to 600 H1 rows.
- Required trust, regime, prediction, decision and protective-action columns.
- Every available trust score is between 0 and 10.
- H+h outcomes are not used before maturity.
- Truncating the future does not alter the same historical trust row.
- M1 evidence is not fabricated from H1.
- Mobile bounded views preserve exact values.
- Mobile mode changes presentation only.
- IMAP-RV weights sum to one, cleaned covariance is PSD, actions use the four permitted labels and same-candle cache reuse works.
- Protected Table 3 implementation hashes remain unchanged.

## Runtime and smoke tests

- `app.py`: Streamlit health `ok`; HTTP 200.
- `adx_dashpoard.py`: Streamlit health `ok`; HTTP 200.
- AppTest authentication page: zero exceptions for both entry files.
- Guest Settings: zero exceptions for both entry files.
- Lunch, Dinner and AI navigation: zero exceptions for both entry files.
- Full Settings run: zero exceptions; canonical run completion message displayed; Lunch opened.

## Expected no-key condition

The test environment did not include a Twelve Data key. The app explicitly displayed missing-connector and out-of-sync messages. This is correct: no fake candles were inserted.
