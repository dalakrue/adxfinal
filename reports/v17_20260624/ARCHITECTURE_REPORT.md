# Architecture report — research-grade system v17

The implementation adds one unified, shadow-only sidecar consuming the completed canonical Field 1 snapshot. It binds Fields 2, 3, 8, 9 and grounded assistant answers to one `run_id`, `origin_id`, broker candle time and data cutoff.

The Settings one-click path is the only publication path. Lunch renderers read saved state only. The sidecar validates mixed run IDs, mixed broker times, future feature timestamps and future data cutoffs. A failed validation is rolled back and cannot appear as COMPLETE.

Field 2 stores immutable H1/H3/H6 origin forecasts, quantiles and intervals, separate MAE/CRPS, pinball loss, interval score, coverage, width, debt and directional accuracy. Field 3 adds BOCPD-style shadow transition evidence without replacing the production regime. Field 8 stores horizon-specific dynamic weights, model concentration/disagreement and bounded MCS membership. Field 9 evaluates BUY/SELL/WAIT gross/net values, saved costs, overlap/ESS, DR/DML-labelled estimates, robust stressed value, regret, SHAP-style surrogate groups and plausible flip thresholds.

The assistant contract is deterministic and evidence-bound. Unsupported questions are rejected; system values are never answered from general memory.
