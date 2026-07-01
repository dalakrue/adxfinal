# Deployment
1. Deploy the ZIP unchanged with `app.py` as Streamlit main file.
2. Install `requirements.txt`.
3. Run `streamlit run app.py` locally or configure Streamlit Cloud main file as `app.py`.
4. The additive SQLite schema migrates automatically on first one-hour run.

# Rollback
Restore the files marked MODIFIED in `ONE_HOUR_V2_CHANGED_FILES_MANIFEST_20260626.md` from the prior ZIP and delete the ADDED v2 reports/migration. The additive one-hour table and columns may safely remain unused; they do not replace protected production tables.
