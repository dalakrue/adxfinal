# Final Field 1 / Field 4–9 / AIR-LLM Repair — 2026-06-27

## Implemented

1. Field 1 Table 1 now displays decision columns only. Score columns are deliberately omitted from the visible table, so unavailable score scales can no longer fill the table with `N/A`.
2. The decision diagnostics beneath Table 1 now count published BUY/SELL decisions and decision coverage; they no longer depend on missing scores and therefore do not incorrectly display `0.0` as evidence.
3. Field 1 Table 4 remains a 25-broker-day completed-H1 outer join of Technical, Regime, Session, Data Mining and NLP Sentiment bias.
4. Technical Bias reads Field 1 Table 3 Entry Strength history directly and can reuse the already-built Field 1 decision collection when legacy cache names differ.
5. Published-frame discovery now matches normalized words in paths and column names, improving recovery of Field 3 lower-standard Less Risky Bias, Research Data Mining labels and NLP Regime Direction.
6. Table 5 is now always visible and explicitly is not a fallback. It independently collects every real timestamped decision, bias, direction, label, action and priority publication from Fields 4–9 and Research for the latest 25 broker days.
7. The authoritative `Field 4 to 9` page and router branch are retained. It shows the collection history first, then Fields 4–6 and Fields 7–9 without merging or rerunning protected engines.
8. AIR-LLM status now reports the selected Open/Closed mode separately from server configuration. Open mode only attempts lazy model loading after a submitted question.

## Important data rule

The repair does not invent 25 days of rows. It outer-joins real published rows and retains partial rows. A missing source remains `MISSING` or blank rather than being rewritten as WAIT.

## Tests

- New user-contract tests: Table 1 no-score display, always-visible Table 5, AIR-LLM mode metric, authoritative Field 4–9 route.
- Existing priority and navigation tests retained.
- 13 focused tests passed.
- Python compile validation completed for changed modules.
