# Dinner Navigation + Full Run Repair — 2026-06-27

## Entry point
Use `streamlit run app.py`. `app.py` is the preferred wrapper and calls the same `adx_dashpoard.main()` function, so both commands now enter the same application shell.

## Implemented repairs
- Replaced visible legacy `Field 456` / `Field 789` menu routes with one authoritative `Dinner` route.
- The floating menu Dinner button now writes `active_page=Dinner`; it is no longer normalized back to Lunch.
- Dinner renders the combined Fields 4–9 workspace and places the 25-broker-day Field 4–9 bias/decision collection at the top.
- Kept legacy names as aliases so saved sessions still open Dinner.
- Changed Settings Quick Run to execute the complete Fields 1–9 + AI publication path from one canonical snapshot.
- Removed the partial Quick-Run reuse branch and removed Field 7–9/AI skip behavior from the visible Quick Run action.
- After a Settings run, Lunch opens with Fields 1–6 closed on both phone and desktop.
- Field 1 Table 1 now rejects blank strings as values and fills blank canonical run/generation IDs from the frozen snapshot.
- Field 1 Table 5 is now an integrated Table 1 + Table 4 collection, with a final transparent `Master Action` of BUY, SELL, WAIT PULLBACK, or HOLD.

## Decision-column interpretation
`Net Pressure Decision` and `Direction Confirmation Decision` are copied from their matching Table 3 factor-history publishers. They are not recalculated from unrelated columns. Table 5 preserves the source decisions and adds a separate integrated Master Action, preventing source labels such as HOLD or WAIT PULLBACK from being silently rewritten as BUY/SELL.

## Validation performed
- Python compile validation passed for all modified modules and full `core`, `ui`, and `tabs` trees.
- Static route checks confirm Dinner exists in the defaults, drawer, Ant Design page list, and registry.
- Runtime browser validation was not possible in this container because Streamlit is not installed in the execution environment; install `requirements.txt` before local launch.
