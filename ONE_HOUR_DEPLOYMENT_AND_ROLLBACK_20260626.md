# Deployment Instructions

1. Use Python 3.12.
2. Install `requirements.txt`.
3. Keep `app.py` as the Streamlit entry point.
4. Run `streamlit run app.py`.
5. Use Settings → Quick Run Fields 1–3 + Open Lunch; the one-hour object publishes after the protected calculation.

# Rollback Instructions

Restore the files listed as MODIFIED in `ONE_HOUR_CHANGED_FILES_MANIFEST_20260626.md` from the prior ZIP and delete the three added modules plus `tests/test_one_hour_direction_confirmation_20260626.py`. The additive SQLite table may remain unused or be dropped as `one_hour_direction_ledger_20260626`; it is independent of protected production history.
