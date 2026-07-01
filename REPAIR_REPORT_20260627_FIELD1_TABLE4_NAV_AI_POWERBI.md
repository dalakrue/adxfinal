# ADX Quant Pro Repair — 2026-06-27

## Implemented

- Field 1 Table 1 now reads the same `history_by_factor` publisher used by Field 1 Table 3, across current and legacy cache names.
- It joins all ten factor histories by completed H1 broker candle, accepts common factor/title/time/score/decision column variations, keeps the newest completed candle first, and retains up to 25 distinct broker days.
- The one-row current direction-confirmation object is now only the final fallback when Table 3 has no history; it no longer takes priority over the richer Table 3 archive.
- Table 4 retains all directional rows but displays only every second WAIT/WEAK row in the lower-standard neutral view. It uses a published-evidence tie-break only where directional evidence exists. No protected production threshold, decision, weight, or stored row is changed.
- Field 4–9 menu aliases route to the combined `Field 4 to 9` workspace. The combined page renders existing Fields 4–6 and 7–9 results without recalculation.
- AI Assistant now has an explicit **Open / Close — AirLLM Mode** toggle. Closed mode always uses the lightweight canonical assistant. Open mode lazily attempts AirLLM after a submitted question and safely falls back when unavailable.
- Research opens directly after a full canonical generation exists. The old separate “Load Selected Research Workspace” gate is removed from the post-calculation path.
- Field 2 Power BI state lookup now checks the canonical object plus all known published/cache payload names before reporting missing source data.

## Verification

- Python compile check: passed for every changed Python module.
- Synthetic Table 3 integration test: 600 joined hourly rows with all ten decision columns populated.
- Existing acceptance test collection ran; failures were only because Streamlit is not installed in this repair container, not from syntax errors.

## Important boundary

The repair does not manufacture 25-day history. Table 1 can show 25 days only when Table 3 actually contains those published completed-candle rows. It now extracts those rows correctly instead of stopping at the one-row confirmation payload.
