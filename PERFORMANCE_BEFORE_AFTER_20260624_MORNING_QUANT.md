# Performance Before/After — 20260624 Morning Quant Upgrade

Measured in this container:
- New focused pytest suite: 8 tests in 0.57 seconds.
- Full project compileall: PASS.

Performance design changes:
- immutable ledger settles only newly matured pending origin rows;
- CRPS/sample calculations are vectorized or bounded O(n log n) for samples;
- Morning renders saved state/ledger evidence only and does not calculate heavy models;
- large historical query/display remains lazy in the existing Morning V8 renderer;
- one-click controller prevents duplicate heavy runs from double clicks/reruns.

No unverified 30–50% runtime/RAM improvement is claimed. The code records a performance-safe design and keeps the existing project measurement/reporting files intact.
