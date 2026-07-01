# Rollback instructions

1. Stop the deployed app.
2. Restore the previous project ZIP or Git commit.
3. Preserve the existing database files before replacement; do not delete settled outcome history.
4. Restore only code/configuration unless a database migration explicitly failed.
5. Re-run protected-hash comparison and the acceptance tests.
6. Restart with `streamlit run app.py`.

The protected production threshold remains available and is never overwritten by the shadow candidate, so threshold rollback is immediate: disable candidate promotion and continue using the original protected threshold.
