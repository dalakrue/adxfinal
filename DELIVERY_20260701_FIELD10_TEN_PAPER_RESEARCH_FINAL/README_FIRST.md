# Field 10 + Ten-Paper Research Upgrade — Read First

This delivery upgrades Lunch Field 10 into a lazy multi-symbol ranking, data-quality, broker-time, history and shadow-research workspace. It preserves the existing canonical calculation and keeps Field 3 and Field 10 separate.

## Main behavior

- Field 10 is inside the authoritative **Choose Lunch Field to Open** selector.
- All Lunch fields remain closed after the Settings run. The run still navigates to Lunch.
- Field 10 does not calculate or render while another field is selected.
- Opening Field 10 reads saved canonical symbol generations and computes only missing ten-paper shadow-validation rows.
- Reopening the same parent run uses the SQLite cache.
- Production decisions remain unchanged. Research action, permission, conflict and explanation are separate columns.
- Broker wall-clock date/hour are preserved instead of silently converting to UTC.
- Fields 1–9 have read-only post-run integrity checks using PASS, WARNING and FAIL.

## Important limitations

No live broker, Finnhub, Twelve Data or MT5 credential was available in the test container. Therefore, live-source accuracy and production Quick Run timing were not claimed. The full local test suite passed and the Streamlit server returned HTTP 200 during a local startup smoke test.
