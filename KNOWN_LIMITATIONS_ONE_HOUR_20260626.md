# Known Limitations

- No settled origin database was supplied, so walk-forward performance metrics cannot be estimated honestly.
- Conditional tails require at least 20 observations; before that, the hierarchy falls back to ATR/global/absolute emergency controls.
- Empirical interval coverage and session path MAE display as unavailable until settled path outcomes exist.
- The project may expose different Power BI path key names; the extractor supports common existing names and safely falls back to origin + raw endpoint.
- Threshold selection remains candidate-based until a sufficient chronological settled sample is available.
