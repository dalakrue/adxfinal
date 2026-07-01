# Priority Repair Report — 2026-06-26

## Implemented
- Table 1 now falls back to the already-calculated Field 1 Table 3 `history_by_factor` evidence and joins the ten factor histories by completed broker candle.
- Table 4 now has a deterministic completed-H1 OHLC fallback when external NLP/news is absent. These rows are explicitly labeled `LOCAL_TECHNICAL` and `LOCAL_COMPLETED_OHLC`.
- Copy Short and Copy Full are clickable from first system open. Before any run they copy a truthful startup/status payload; after Quick Run they copy the current canonical payload.
- Main navigation now exposes one visible `Field 4 to 9` route. Legacy Field 456 and Field 789 names are retained as aliases for saved sessions.
- Original Fields 4–9 calculation modules remain independent. The combined route integrates their display and avoids starting calculations during rendering.

## Safety
- No protected BUY/SELL/WAIT/HOLD/NO-TRADE threshold was changed.
- No historical outcome, news headline, accuracy, or reliability was fabricated.
- Local Table 4 fallback is display-only and cannot overwrite production weights.

## Performance design
- Table 1 reuses existing factor frames instead of recalculating decisions.
- Table 4 uses vectorized pandas operations on a bounded 25-day H1 window.
- Copy payloads remain cached by canonical generation.
- Combined Field 4–9 rendering reuses published stores and does not trigger engines.

A precise 30–50% RAM/CPU reduction cannot be guaranteed without profiling the user's production data, connector latency, and Streamlit Cloud instance. The changes remove duplicate work in the repaired paths and bound local computation.
