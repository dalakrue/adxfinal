# Research Method Mapping

| Research concept | Implementation location | Operational use | Production influence |
|---|---|---|---|
| Giacomini & White — conditional predictive ability | `giacomini_white`, `_candidate_history`, `_forecast_layer` | Conditional shadow weight multiplier using regime/session/volatility/spread/changepoint instruments | None |
| Xu & Xie — EnbPI-style time-series conformal prediction | `_conformal` | Rolling matured residual pools with regime/session/volatility conditioning and documented fallback | None |
| Adams & MacKay — Bayesian online changepoint detection | `bayesian_online_changepoint` | Recursive run-length posterior and changepoint warning evidence | None |
| Hamilton — Markov switching | `hamilton_filter` | Three-state filtered regime posterior, persistence and transition probabilities | None |
| Niculescu-Mizil & Caruana — calibration | `chronological_calibration` and Platt/isotonic/beta helpers | Chronological selection and out-of-sample scoring for seven target families | None |
| Hansen, Lunde & Nason — Model Confidence Set | `model_confidence_set` | Dependence-aware block-bootstrap shadow membership for H1/H3/H6, regime, and after-cost value | None |
| Hansen — Superior Predictive Ability | `superior_predictive_ability` | Joint block-bootstrap test; superior label requires positive improvement and statistical evidence | None |
| Quaedvlieg — multi-horizon comparison | `_multi_horizon_comparison` | Joint summary without pooling H1/H3/H6 metrics | None |
| Lim, Arık, Loeff & Pfister — TFT-inspired fusion | `lightweight_tft_fusion` | Sparse feature-group gates, temporal importance, multi-horizon quantiles, CPU-safe fallback | None |
| Diebold & Mariano — forecast comparison | `diebold_mariano`, `_dm_breakdowns` | HAC comparison for all data, regimes, sessions, older block, and recent block | None |
