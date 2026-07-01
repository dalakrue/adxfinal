# Deployment Instructions

1. Use Python 3.12, matching `.python-version` and the project deployment target.
2. Install `requirements.txt`. DuckDB and Streamlit are required for the full existing test/runtime path.
3. Set the Streamlit entry point to `app.py`.
4. Preserve the `data/` directory so immutable SQLite/DuckDB history survives restarts.
5. Start locally with `streamlit run app.py --server.headless true`.
6. In the application, use Settings → Run Calculation + Open Lunch. This publishes the canonical snapshot first and then the shadow sidecar.
7. Do not call `evaluate` or `publish` from a Lunch renderer. Renderers must read the saved session-state payload only.
8. API keys are optional. The no-key fallback was tested; live provider availability remains external to this ZIP.
9. To roll back this upgrade, remove only the unified sidecar module/service/UI additions and ignore/drop `rg17_*` tables. Field 1 and production files are unchanged.
