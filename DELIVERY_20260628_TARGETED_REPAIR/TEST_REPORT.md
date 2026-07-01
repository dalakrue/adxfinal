# Test Report

## Automated tests

All **147 collected project tests passed** in deterministic batches:

| Batch | Scope | Result |
|---|---|---:|
| 1 | CRCEF persistence, table contract, new NA/regime/Dinner/Finder tests | 18 passed |
| 2a | ARCEF-SV | 17 passed |
| 2b | ARERT thesis repair | 15 passed |
| 2c | Combined display, delivery acceptance, Dinner repair | 30 passed |
| 3 | Field 1 publication, factor merge, navigation, projection integrity | 23 passed |
| 4 | Repair, requested acceptance, session warnings, upgrade, user repairs | 44 passed |
| **Total** |  | **147 passed** |

After the final Dinner-display and cache-optimization changes, the directly affected regression subset was rerun: **37 passed**.

## Exact regression coverage added

`tests/test_20260628_na_regime_dinner_finder_repairs.py` verifies:

- `pandas.NA` is accepted by ARERT decision labeling;
- ARERT context construction handles NA decision cells;
- mixed string/Timestamp regime history sorts safely newest-first;
- protective output is restricted to the four permitted labels and can produce all four;
- variable historical columns outrank constant snapshot columns;
- Finder source contains Table 5 and complete-copy integration;
- Dinner executes the flat published-results path rather than old nested detailed renderers.

## Compilation

`python -m compileall -q <project>` completed without syntax errors.

## Streamlit smoke tests

Both entry files started and returned a healthy Streamlit endpoint:

- `streamlit run app.py` → `/_stcore/health` returned `ok`.
- `streamlit run adx_dashpoard.py` → `/_stcore/health` returned `ok`.

Streamlit AppTest also executed both files with **zero uncaught exceptions**. For `app.py`, AppTest clicked **Continue as Guest**, loaded Settings, and observed zero exceptions/errors. It then opened Dinner and observed zero exceptions/errors and the single protective-history expander.

## Environment note

A one-process full-suite invocation occasionally printed the completed pytest summary but did not terminate cleanly in the container. Running the same collected tests in deterministic file batches produced the 147/147 pass result above. No test failure was hidden or skipped.
