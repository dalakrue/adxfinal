# Verification Report

## Automated tests

- Full project test suite: **167 passed**
- Dedicated Lunch time-sync tests include:
  - stale 2026-06-17 canonical replaced by a newer 2026-06-28 completed-H1 frame;
  - stale `Date=2026-06-17`, `Hour=15:00/18:00` rebuilt as `Date=2026-06-28`, latest `Hour=20:00`;
  - a displayed frame can override a stale canonical even without `last_df`;
  - repeated rerenders cannot restore stale Date/Weekday/Hour aliases;
  - Field 2 Plotly axis uses the same broker hour as Field 1;
  - Field 2 history tables rebuild stale visible Date/Hour aliases;
  - newest metric and market publication wins over the first stale cache.

## Compilation

- `python -m compileall -q -f .`: **PASS**

## Entry-point smoke tests

- `python app.py`: **PASS**
- `python adx_dashpoard.py`: **PASS**
- `streamlit run app.py` health endpoint: **OK**
- `streamlit run adx_dashpoard.py` health endpoint: **OK**

## Data-integrity cleanup

Test-created SQLite output was removed and the pre-existing experiment registry was restored before packaging.
