# Deployment and Rollback

## Deploy
1. Keep repository root unchanged.
2. Deploy with `app.py` as the sole Streamlit entry point.
3. Preserve the existing `data/` directory if it contains production databases.
4. Run Settings → Quick Run Fields 1–3 + Open Lunch.
5. Verify Field 1 operational action, Field 2 dual path, Field 3 compatibility and Fields 8/9 history.

## Rollback
Restore these files from the prior ZIP:
- `core/one_hour_direction_confirmation_20260626.py`
- `ui/lunch_one_hour_direction_20260626.py`
- `lunch/field_01/renderer.py`
- `lunch/field_09/renderer.py`
- related test file

The additive ledger can remain; it does not overwrite protected production tables.
