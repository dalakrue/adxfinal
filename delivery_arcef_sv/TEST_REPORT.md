# ARCEF-SV Test Report

- Python syntax/compile checks: **PASS**
- New ARCEF-SV unit/contract tests: see `arcef_tests.txt`
- Import checks for `app.py`, Settings orchestrator, Dinner renderer, and Lunch registry: **PASS**
- Streamlit startup smoke test using `streamlit run app.py --server.headless true`: **PASS**; server reached ready state on localhost.
- Dinner renderer contains the top synthesis, contribution ledger, and newest-first 25-record table: **PASS**
- One-click Settings orchestrator contains the post-canonical ARCEF-SV publication hook: **PASS**

The full legacy suite output is included in `full_pytest.txt`. Older tests may encode superseded UI assumptions, especially the former exact three-field Lunch count; these are retained as audit evidence rather than silently removed.
