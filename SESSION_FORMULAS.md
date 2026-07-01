# Session Formulas

For each matured horizon, the shadow session correction is empirically shrunk:

`strength = n / (n + 30)`

`residual_bias = strength * session_bias + (1-strength) * global_bias`

A completed-H1 intraday prior is also shrunk:

`prior_strength = prior_n / (prior_n + 60)`

`combined_bias = residual_bias + prior_strength * relative_session_move`

The correction is capped to `±0.35 * ATR14`, and the adjusted value is clipped inside available lower/upper bounds. Weak evidence therefore converges to the protected central path.
