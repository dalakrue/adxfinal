# Known Limitations — Quant Research V8

1. V8 does not guarantee forecast accuracy, profit or account survival. Kelly and risk-of-ruin outputs are explicitly shadow/advisory evidence.
2. Account, position, margin, spread, slippage and connector metrics remain `UNAVAILABLE` when no verified input is published; V8 does not invent them.
3. Conditioned conformal intervals, dynamic weights and trust labels remain `INSUFFICIENT EVIDENCE` or `NOT TESTABLE` until their settled-sample gates pass.
4. The ADWIN implementation is a compact bounded ADWIN-style monitor for the nine requested streams, not an unbounded feature-by-feature detector.
5. SPA, Reality Check and CSCV/PBO are bounded/sampled for Streamlit Cloud resource safety; promotion defaults to false.
6. The performance comparison is a cold-import benchmark. Live network latency, broker terminal behavior and long-running multi-user Streamlit memory require production telemetry.
7. A real Doo Bridge, MT5 terminal, API credentials and Streamlit Cloud deployment were unavailable for live integration testing. Headless local startup and failure-containment tests passed.
8. Old historical rows are retained after drift; V8 opens a new epoch and reduces/partially pools old influence rather than deleting data.
9. The protected legacy Doo account/risk/emergency workspace is still available and can be heavier when explicitly opened under Morning → Analysis.
