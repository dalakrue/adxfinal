# Protected Logic Equivalence

Changed code is limited to session UI/state wiring and tests.

Not changed:
- Field 1 production calculation or BUY/SELL/WAIT rules
- Existing thresholds and regime formulas
- Power BI central prediction path calculations
- KNN, Greedy, NLP, TP/SL, settlement, model weights, or protected hashes

The manual session choice remains a shadow/evidence-layer input. Exact numerical equivalence on a frozen live connector dataset was not executable in this sandbox; source-scope inspection found no edits to protected numerical functions.
