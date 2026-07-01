# Deployment instructions

1. Use Python 3.12.
2. Install dependencies from the project requirements file.
3. Set Streamlit Cloud main file to `app.py`.
4. Preserve the `data/` directory for SQLite history.
5. Run `streamlit run app.py` locally.
6. In the application, use Settings → Run Calculation + Open Lunch. This publishes the canonical run first, then the shadow v17 sidecar.
7. Do not invoke research publishers from render paths.
