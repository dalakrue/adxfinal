# Detailed Master Implementation Command — 2026-06-28

Use this command when asking a coding agent to continue work on this project.

---

Inspect, repair, test and package the complete uploaded Streamlit project. Work on the actual files; do not provide only advice. Preserve protected Lunch trading calculations and Field 1 Table 3 as immutable production truth. Add performance, presentation, caching, validation and research layers around them.

## Source-of-truth and non-deletion rules

1. `app.py` is the recommended deployment entry; `adx_dashpoard.py` must remain a fully working compatibility entry. Both must call the same shared application shell.
2. Do not delete or rewrite protected decision formulas, existing source values, TP/SL logic, canonical snapshots, Field 1 Table 3, exports or audit data.
3. Display-only cleaning may omit blank, single-observation and audit-only columns, but full unpruned data must remain available in state/export.
4. Every renderer must use one frozen canonical identity: run ID, generation, symbol, timeframe, source snapshot hash/signature and completed broker candle.
5. No renderer may silently recalculate. Only Settings calculation controls may publish a new generation.
6. Never store API keys in code, logs, warm caches, ZIP evidence or test outputs.

## A. Dinner performance and layout

1. In `ui/field4to9_collection_history_20260627.py`:
   - scan only explicit Field 4/6/7/8/9 and Dinner publication roots;
   - cap traversal depth and rows;
   - precompute eligible columns and field routing once per generation, never inside every row loop;
   - cache by exact `(run_id, generation_id, source_snapshot_hash)`;
   - keep the full 25-day table for audit;
   - create a compact display retaining identity, production decision, consensus, evidence, Field biases/decisions and useful populated columns;
   - remove columns that are all blank/N/A or have fewer than two useful observations;
   - cap display at about half the original columns and no more than 28 by default.
2. In `tabs/field456789_page_20260626.py`:
   - show all current Field 4/6/7/8/9 metrics and compact current tables together in a flat, side-by-side overview;
   - load exactly one detailed field renderer at a time through an open/close selector;
   - preserve all original calculation functions;
   - show moved Morning session intelligence and one-hour exit-opportunity evidence in a Dinner expander.
3. Phone mode must use bounded research-validation windows and lazy detailed renderers. Protected production calculations are unchanged.
4. Performance acceptance:
   - synthetic 5-field × 600-H1-row Dinner aggregation cold time under 5 seconds on the test machine;
   - exact-generation cache hit under 0.1 seconds;
   - display columns at least 50% lower when the source is very wide;
   - state clearly that this does not guarantee a first full live calculation under every provider/network condition.

## B. Power BI and warning repair

1. In `ui/powerbi_cached_renderer_20260619.py`, prefer canonical completed OHLC frames before `dv_pp_df` or `last_df` live frames.
2. Reject a production chart when the selected OHLC completed candle differs from the canonical completed candle; never fabricate a replacement.
3. Preserve the exact-run green research path rule.
4. Centrally filter only the known harmless sklearn warning `y_pred contains classes not in y_true`; do not suppress all warnings.
5. Add regression tests confirming canonical source ordering and warning-filter presence.

## C. Lunch Field 1 consistency

1. Table 1:
   - use published Net Pressure when present;
   - otherwise use the existing self-contained completed-OHLC Data Mining bias only as a labeled display fallback;
   - never fabricate Decision Correct;
   - show unsettled rows as `PENDING — NEXT H1 NOT SETTLED` rather than a blank-looking N/A.
2. Table 2:
   - overlay current canonical Field 1 values;
   - align displayed decision/direction to the explicit production decision from Table 3 for the same completed H1;
   - preserve any old conflicting Table 2 value in an audit column;
   - publish a Table 2/Table 3 match flag.
3. Table 5:
   - enrich Table 1 before joining Table 4;
   - include Entry, BUY/SELL Pressure, M1 Confirmation, Outcome Status and Decision Correct from Table 1;
   - retain Table 4 columns;
   - never turn pending outcomes into correct/incorrect outcomes.
4. Quick Run and every Lunch navigation must open Lunch Field 1 first.

## D. Regime history and lifecycle

1. Put `Regime lifecycle, reliability and transition trust` in a closed-by-default expander that remains reopenable.
2. Lower standard may remain H1 history.
3. Medium and Higher tables must be change-only interval histories:
   - one row for each consecutive published regime episode;
   - Regime Start, Regime End, Duration Hours and observation count;
   - newest interval first;
   - include useful reliability/score fields;
   - preserve the underlying hourly publication outside this display.
4. Do not force a fake 120H or 600H minimum duration. Explain that 5-day/25-day is the estimator window. Add diagnostics when observed transitions are unusually short.
5. Validate completed-candle-only construction and no future leakage.

## E. Finder/Morning and AI Assistant

1. Finder must include a read-only expander showing Lunch Field 1 Table 3 filtered by the selected date/hour. Whole-day selection shows all available rows for that day.
2. Remove Current Data Session Intelligence and One-hour Exit Opportunity Sound Rule from Morning display and render them in Dinner without deleting their calculation functions.
3. AirLLM model ID/path is optional. When absent or loading fails:
   - answer using the canonical evidence contract;
   - use deterministic intent classification, entity/metric extraction, semantic retrieval, data-mining summaries and financial NLP evidence;
   - clearly say when evidence is unavailable;
   - never claim a local LLM generated the answer.
4. Cache article hashes, embeddings and NLP outputs; enforce article publication-time leakage rules.

## F. API settings and refresh behavior

1. Twelve Data and Finnhub Settings expanders are open on first app load.
2. One button press must save, validate and connect. Do not require a second press caused by Streamlit rerun ordering.
3. Mask keys and keep them out of warm cache and logs.
4. `Refresh + Sync Current APIs` appears below Copy Full and is separate from calculation:
   - refresh/stage connector data;
   - reuse an exact cached generation when valid;
   - never call the Settings calculation orchestrator;
   - tell the user to run Settings only when a new completed H1 requires a new generation.

## G. Copy and persistent warm start

1. Copy Short contains up to 100 important lines from the current canonical Lunch generation.
2. Copy Full contains all available current-candle Lunch data and excludes previous-hour history rows.
3. On browser refresh, restore the newest valid secret-free generation from an atomic compressed cache.
4. Cache latest canonical, relevant tables, Power BI state, regimes and research publications, but exclude any key containing API key, secret, token, password or credentials.
5. Compute an exact source signature. Reuse a completed generation when source/candle/signature and requested scope match. A prior FULL may satisfy QUICK; QUICK may not satisfy a later FULL request.
6. Include a force-recalculate escape flag for deliberate same-candle reruns.

## H. Thesis research layer

Implement research modules as separate, shadow-only evidence using the ten-paper plan in `TEN_ADVANCED_QUANT_RESEARCH_RECOMMENDATIONS_20260628.md`:

- PBO and purged walk-forward validation;
- Deflated Sharpe Ratio;
- Hamilton Markov-switching state probabilities;
- Bayesian online change-point run length;
- ADWIN effective training window/drift;
- probability calibration with Brier/log loss/ECE;
- adaptive conformal bands by horizon;
- TFT-inspired horizon contribution analysis;
- FinBERT/entity/novelty/event-response NLP;
- prospect-theory behavioral risk audit.

Every experiment must store hypothesis, sample window, leakage controls, candidate count, seed, code/version hash, metrics, limitations and promotion/rejection status.

## I. Required testing and evidence

1. Compile all changed Python modules.
2. Run `PYTHONPATH=. pytest -q`; zero failures.
3. Add regression tests for:
   - Dinner blank/single-row column pruning and cap;
   - regime change intervals;
   - current-hour-only Copy Short/Full;
   - secret-free cache save/restore;
   - Refresh+Sync not importing/calling Settings calculation;
   - Power BI canonical frame precedence;
   - sklearn warning filter.
4. Smoke-test both:
   - `streamlit run app.py --server.headless true`
   - `streamlit run adx_dashpoard.py --server.headless true`
   Health endpoint must return OK and root page HTTP 200.
5. Live connector tests may be run only with user-supplied credentials. Redact credentials and URLs containing them. If the sandbox has no DNS/network, report `NOT VERIFIED — NETWORK UNAVAILABLE`, not `INVALID KEY`.
6. Produce:
   - test results;
   - performance benchmark;
   - redacted API test status;
   - changed-files hashes;
   - implementation report with DONE/PARTIAL/NOT TESTABLE for each item;
   - deployable ZIP.
7. Do not claim the first full live calculation is always under five minutes unless measured with the user’s real providers, data volume and device. Distinguish presentation/cached-reopen performance from first-generation model training.

---
