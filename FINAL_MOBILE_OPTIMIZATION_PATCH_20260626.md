# Final Mobile Optimization Patch — 2026-06-26

## Scope
This patch changes UI, orchestration, caching, packaging, and clipboard reliability only. It does not alter protected trading calculations, thresholds, BUY/SELL/WAIT rules, Field 1 source-of-truth logic, Power BI production path, or regime formulas.

## Changes made
- Hardened the central clipboard component against pointer-event and z-index interception.
- Added click, touch-end, and keyboard activation paths.
- Forced Copy Short and Copy Full into separate stacked rows to prevent overlapping component iframes on phones and narrow layouts.
- Preserved generation-scoped payload caching, current-generation-only filtering, and history/unavailable-value exclusion.
- Preserved the existing Lunch refresh button that refreshes EURUSD H1 once, republishes Quick Fields 1–3, invalidates copy payload caches, and reruns Lunch.
- Removed Python bytecode caches from the deployable package.

## Verified architecture
- Preferred deployment entry point: `app.py`.
- Quick Run scope: Fields 1–3 only, with exact same-completed-H1 reuse when source signature and caches match.
- Lunch reads the canonical published generation.
- Refresh invalidates stale Copy Short/Full payloads.

## Fresh validation
- Python compile validation: PASS for modified files and key entry/orchestration files.
- Architecture validator: PASS.
- Import smoke test: NOT EXECUTED because Streamlit is not installed in the repair container.
- Two older static validators fail because their expected page list/sidebar width no longer matches the current project; these failures are unrelated to this patch.

## Important audit finding
The project contains 962 Python files and many archived/versioned modules. Exact duplicate source deletion was intentionally not automated because many files are static-source contracts, split-module parts, or regression archives. Blind deletion could break dynamic imports or protected hash contracts. Runtime bytecode caches were safely removed.
