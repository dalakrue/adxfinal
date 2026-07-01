# CRCEF-SV Architecture

## Name

**Canonical Regime-Calibrated Evidence Fusion with Selective Validation (CRCEF-SV)**

## Original contribution

A canonical, regime-calibrated, uncertainty-aware evidence-fusion framework that separates directional prediction, actionability, entry timing, position maintenance, and abstention while enforcing leakage-safe validation and immutable broker-candle snapshots.

## Runtime boundary

CRCEF-SV is an additive shadow layer. Protected production values, including Field 1 Table 3, are read-only. The Settings full-run publishes all protected Fields 1–9 first, freezes one canonical identity, applies post-run identity checks, and only then calls `research_quant.orchestrator.publish_crcef_sv_research`.

The research result is stored under `crcef_sv_research_20260627`; it is not inserted into or used to overwrite the canonical production object.

## Canonical identity

Every output is keyed by:

- `run_id`
- `generation_id`
- `symbol`
- `timeframe`
- `completed_broker_candle`
- `source_snapshot_hash`
- `source_signature`

`core/canonical_identity_20260627.py` validates the identity and converts the broker candle to a timezone-aware, H1-aligned UTC timestamp without using local PC or browser time.

## Layers

1. **Canonical adapter** — validates and hashes exact-run inputs.
2. **Evidence registry** — bounds every directional value to [-1, +1] and quality to [0, 1].
3. **Research modules** — CPCV/PBO, calibration, meta-labeling, Markov lifecycle, multifractal volatility, EnbPI, Bellman control, ADWIN, optional TFT, and NLP event memory.
4. **Fusion** — softmax quality weights, directional fusion, conflict, coverage, uncertainty, expected utility, selective action.
5. **Promotion guard** — all models begin `RESEARCH_ONLY`; production promotion is impossible from a page render.
6. **Persistence and audit** — immutable SQLite rows and output hashes.
7. **UI** — closed-by-default Lunch, Dinner, validation, and audit views.

## Package map

```text
research_quant/
  canonical_adapter.py
  config.py
  schemas.py
  orchestrator.py
  validation/
  calibration/
  meta_labeling/
  regime/
  multifractal/
  conformal/
  bellman_conformal/
  drift/
  forecasting/
  nlp_event_memory/
  fusion/
  persistence/
  ui/
  tests/
```

## Decision separation

- `Production Decision Raw` preserves BUY, SELL, WAIT, WAIT PULLBACK, and HOLD.
- `Action Display Label` may show HOLD & PROTECT only when the source is explicitly HOLD and position-protection semantics exist.
- `Research Shadow Decision` is never a production input.
- WAIT PULLBACK and HOLD are never converted to BUY or SELL merely from score sign.
