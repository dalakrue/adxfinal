# Test report

## Results

- `python -m compileall -q .`: **PASS**
- Full pytest suite (working tree): **49 passed** in 8.97 seconds
- Full pytest suite (clean staged deployment): **49 passed** in 10.34 seconds
- Delivery acceptance suite: **20 passed** in 2.27 seconds
- Protected upload hash verification: **10/10 PASS**
- Streamlit live smoke test (`app.py`, health endpoint and index): **PASS**
- Streamlit health response: `ok`; index response: 1,522 bytes

## Acceptance coverage

The automated suite covers independent Field 456/789 routes, navigation-state stability, Quick Run single-refresh architecture, complete Quick manifest identity, immediate one-row PENDING Table 1 behavior, no fabricated archive rows, canonical fallback priority, cross-consumer identity consistency, Power BI current-generation cache, original/session-shadow display contract, exactly two active Lunch copy controls, current-only copy serialization, broker-time synchronization, no recalculation during field switching, AirLLM-disabled lazy fallback, Table 4 empty/populated cases, requested table headings, optional-dependency isolation, and unchanged protected hashes.

## Not executed

A live broker/API-backed Quick Run was not executed because no MT5/Twelve Data/Finnhub credentials or live terminal were supplied. Tests used deterministic in-memory frames and published-canonical fixtures. No AirLLM model was downloaded or inferred.
