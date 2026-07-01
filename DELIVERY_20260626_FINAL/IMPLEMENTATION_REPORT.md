# ADX Quant Pro — Final Repair and Verification Report

## Delivered architecture
Lunch exposes exactly five selectable display surfaces: Field 1, Field 2, Field 3, Field 456, and Field 789. Field 456 and Field 789 are display-only compositions; their original engines, caches, functions, tables and persistence paths remain independent. Only the selected field renderer is invoked.

Field 1 begins with **Decision History — Last 25 Days** and presents the requested columns in the requested order. It consumes immutable completed EURUSD H1 history, limits the view to the newest 25 broker dates, sorts newest first, and keeps unsettled correctness as `N/A`.

## Repairs made in this pass
1. Removed range-based score-scale guessing. A value outside 0–10 is converted only when the publisher supplies explicit `score_scales` metadata (`0-1` or `0-100`). Unknown scales remain `N/A`; missing data is never changed to zero.
2. Added canonical identity comparison support and a red **OUT-OF-SYNC** error path for run, generation, source hash, symbol, timeframe, or completed broker-candle mismatches.
3. Added a complete acceptance suite covering all 18 requested test categories.

## Production protection
No protected production calculation, decision threshold, Power BI central path, regime formula, canonical calculation module, historical outcome, or database record was modified. The decision table and research diagnostics remain read-only adapters. Shadow direction confirmation and abstention research do not overwrite production actions.

## Research gates
The project retains its chronological, purged and embargoed shadow validation components and one-hour direction-confirmation layer. Promotion remains evidence-gated; insufficient evidence retains the original protected threshold. No forced 50% HOLD/NO-TRADE reduction is applied.

## Verification summary
- 971 Python files passed AST parsing and byte-code compilation.
- 24 pytest checks passed: 18 requested acceptance categories plus 6 pre-existing upgrade tests.
- Key entrypoint and Lunch modules imported successfully.
- Streamlit started through `app.py`; `/_stcore/health` returned `ok`.
- Deployment remains pinned to Python 3.12. The inspection container itself used Python 3.13.5, so the exact Python 3.12 import run must be repeated in the deployment environment.

## Known evidence boundary
The synthetic tests prove schema, ordering, exclusion, N/A handling, identity mismatch detection and UI isolation. They do not manufacture real accuracy, reliability, uncertainty, settled outcomes, or threshold-promotion evidence. Live promotion remains blocked until enough genuine settled broker history exists.
