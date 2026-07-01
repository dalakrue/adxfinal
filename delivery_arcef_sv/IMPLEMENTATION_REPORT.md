# ARCEF-SV Implementation Report

## Scope
Added **Adaptive Regime-Calibrated Evidence Fusion with Statistical Validation (ARCEF-SV)** as an additive, shadow-only master-thesis calculation layer. The protected production calculation, Field 1 Table 3, canonical source values, existing Dinner renderers, and legacy audit evidence were not rewritten.

## Architecture
- New modular package: `core/thesis_engine/`
- Settings one-click orchestrator publishes ARCEF-SV only after the existing canonical generation is complete.
- The result is bound to `run_id`, `generation_id`, symbol, timeframe, and completed broker candle.
- Lunch adds a separate closed-by-default ARCEF-SV research field.
- Dinner places “Dinner Quantitative Master Synthesis” before existing synchronized Dinner evidence.
- Persistent append-only JSON stores record 25-run history and experiment versions under `data/arcef_sv/`.

## Implemented Research Components
Decision standardization; probability publication; Brier/log-loss utilities; conditional reliability shrinkage; recursive dynamic model averaging; probabilistic regime summary; changepoint/reset control; statistical-validation gate ledger; correlation penalty and effective independent model count; normalized final weights; evidence fusion; versioned master policy; experiment registry; ablation registry; and cached generation-bound publication.

## Scientific Limits
White Reality Check, SPA, Giacomini–White, MCS, CSCV/PBO, fitted Hamilton filtering, and full BOCPD require sufficient settled historical forecasts and outcomes. The implementation keeps these models visible and explicitly marks unavailable tests as `NOT_RUN`/shadow rather than fabricating p-values or claiming validation.

## Non-deletion Verification
No Field 1 Table 3 module was edited. Existing Dinner data remains accessible through the pre-existing closed gates below the new synthesis. The new code does not alter production decisions or source snapshot values.
