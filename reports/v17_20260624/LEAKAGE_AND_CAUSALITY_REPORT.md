# Leakage and causality report

Forecast records are keyed by origin and inserted with `INSERT OR IGNORE`, preventing historical interval rewrites. Contract validation rejects `feature_time > forecast_origin` and `data_cutoff_time > broker_candle_time`. Candidate evidence uses only supplied matured outcome rows; immature evidence is labelled rather than scored.

DML and doubly robust outputs are explicitly labelled shadow/associational unless identification assumptions hold. Strong conclusions are refused when overlap or effective sample size is inadequate. No sidecar output can modify the protected production action.
