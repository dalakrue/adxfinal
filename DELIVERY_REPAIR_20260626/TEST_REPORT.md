# Test report

- `python -m pytest -q`: **50 passed**.
- `python -m compileall -q .`: passed.
- Navigation tests for Field 456 and Field 789: passed.
- Quick Run canonical publication and current PENDING-row tests: passed.
- Canonical identity consistency across Fields 1–3 consumers: passed.
- Power BI current-generation cache test: passed.
- Exactly two visible Lunch copy controls test: passed.
- Broker-time synchronization test: passed.
- Field-switching no-recalculation test: passed.
- AirLLM-disabled fallback/lazy-import test: passed.
- Table 4 empty-news and populated-news tests: passed.
- Streamlit smoke test: `/_stcore/health` returned `ok`.
- Warning regression: all-NaN interval coverage/width remains NaN and emits zero warnings.
