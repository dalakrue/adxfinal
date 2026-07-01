# Protected logic confirmation

The repair did not alter protected production decision calculations, Field 1 source-of-truth values, action rules, thresholds, Power BI central path, regime formulas, canonical identity semantics, historical outcomes, database records, model weights, TP/SL calculations, or broker-time rules. The only production-code change is defensive aggregation in the session projection statistics store: all-NaN evidence now returns the same unavailable `NaN` result without NumPy runtime warnings. Existing protected-file hash acceptance tests passed.
