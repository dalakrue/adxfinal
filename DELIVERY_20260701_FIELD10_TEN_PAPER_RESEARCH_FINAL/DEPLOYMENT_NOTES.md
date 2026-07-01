# Deployment Notes

- Streamlit Community Cloud main file remains `app.py`.
- The project still targets the runtime declared by the existing project configuration.
- SQLite migrations are additive. Existing Field 10 databases receive new nullable columns/tables on first use.
- Back up the existing database before deployment.
- Deploy in shadow mode first and inspect research conflicts, data-quality grades, OOS verification and integrity warnings.
- Do not promote research thresholds or candidate models solely because a backtest looks better.
- Use real settled outcomes and explicit walk-forward/OOS markers before enabling any future promotion path.

## Local verification completed

- Full test suite passed.
- Streamlit startup smoke test returned HTTP 200.
- No live broker/API test was possible in the container.
