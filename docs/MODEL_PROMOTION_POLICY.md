# Model Promotion Policy

Every new model starts as `RESEARCH_ONLY`.

Statuses:

```text
RESEARCH_ONLY
VALIDATION_FAILED
VALIDATION_PASSED
SHADOW_APPROVED
PRODUCTION_CANDIDATE
REJECTED
RETIRED
```

Promotion consideration requires all of:

- leakage tests passed;
- CPCV completed;
- PBO below the configured limit;
- minimum sample size met;
- Brier/ECE/log-loss limits met;
- interval coverage met where applicable;
- no material unresolved drift;
- stable expected utility after transaction costs;
- stable advantage over simple baseline;
- reproducible input/output hashes;
- successful rollback test.

`research_quant/drift/promotion_guard.py` enforces the mechanical gate. The application never automatically changes a production model or protected decision.
