# Field 6 Quantitative History Data Dictionary — 2026-06-22

All additions remain nested inside existing Lunch Field 6. They are read-only evidence/history tables, not prediction engines.

## Common identity/display columns

When applicable each rendered table leads with `event_time_utc`, `Broker Time`, `Myanmar Time`, `calculation_id`, `generation`, `symbol`, `timeframe`, `source`, `data_quality_status`, `synchronization_status`, `logic_version`, and `settled_status`. Storage retains canonical UTC and compact JSON payload metadata.

| # | Table | Purpose | Principal payload fields |
|---:|---|---|---|
| 1 | Broker-Time Synchronization Audit History | Watermark and broker-clock contract monitoring | watermark status, lag, clock availability/resolution, offset, timestamp source, contract version |
| 2 | Cross-Table Generation Consistency History | One-generation identity validation across Lunch data | status, table count, per-table timestamp/ID/generation/offset report |
| 3 | Forecast Coverage Calibration History | Read-only conformal coverage monitoring | recent coverage, target coverage, miscoverage, calibrated bands |
| 4 | Adaptive Coverage Controller History | Evidence-only adaptive feedback | recent/target coverage, controller adjustment/status |
| 5 | Market Change-Point and Drift History | Change-point and drift metadata | drift detected/status, change probability/time |
| 6 | Conditional Model Skill History | Conditional predictive ability evidence | conditional skill, sample size, benchmark |
| 7 | Research Rule SPA Validation History | Hansen SPA metadata and data-snooping warning | candidates, benchmark, statistic, p-value, evidence-only flag |
| 8 | Execution Cost and Trade Feasibility History | Cost versus expected move feasibility | spread points/pips, slippage, expected move/horizon, transaction cost, cost ratio, volatility, session, market quality, decision, GOOD/MARGINAL/AVOID reason |
| 9 | AI Evidence Retrieval and Answer Audit History | AI evidence provenance | intent, question hash, modules, identity, answer hash/status |
| 10 | AI Risk-Coverage and Abstention History | Selective-answer policy monitoring | evidence completeness, sync/quality, confidence, ANSWER/PARTIAL/ABSTAIN |
| 11 | Decision Outcome and Settlement History | Later result/settlement evidence | settlement status, decision outcome payload and horizon identity |

### Execution feasibility rule

No spread, slippage or transaction-cost input is invented. Missing required inputs produce `UNAVAILABLE`. Available cost-to-expected-move ratios map to `GOOD` (≤0.25), `MARGINAL` (>0.25 and ≤0.50), or `AVOID` (>0.50). This label is evidence only and does not modify protected decisions.
