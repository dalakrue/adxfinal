# Data-Mining Architecture Report

## Current architecture used by this repair

1. **Canonical completed-candle layer**
   - Lunch publishes the protected production snapshot and identity.
   - Identity includes run/generation/candle/symbol/timeframe where available.

2. **Read-only historical projection**
   - `core/history_query_20260621.py` projects bounded completed-H1 history.
   - Timestamp parsing is normalized before comparison and sorting.

3. **Dinner publication discovery**
   - Already-published DataFrames are discovered from state/canonical roots.
   - No connector call, model training, or production recalculation occurs during Dinner rendering.
   - Mobile display is bounded; complete source tables remain in state/export.

4. **Research layer**
   - ARERT remains a separate research envelope with 20 modules, including HSMM persistence, Bayesian changepoints, conformal intervals, meta-labeling, selective prediction, dynamic Bayesian model averaging, event-response memory, and validity diagnostics.
   - Normal Settings reruns render cache only. Research execution requires an explicit button.

5. **Finder retrieval**
   - Finder reads disk/canonical published rows and the existing Table 5 integration builder.
   - Date/hour selection is display-only.

## Not newly completed in this repair

The broad requested universal cell-level analytics catalogue (SQL + vector + time-series retrieval over every tab/field/column) was not newly built. The existing project already contains canonical/history/database components, but a complete provenance catalogue with one record per result cell requires a separate schema migration, indexing design, backfill, and load test. See `INCOMPLETE_ITEMS.md`.
