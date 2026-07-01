# ADX Quant Pro — Field 1/Table 4/AirLLM/Mobile Repair

## Implemented repair

1. Added `core/field1_publication_bridge_20260626.py`. After a successful Settings run, it checks the actual calculated Field 1 metric cache and completed OHLC frame. If legacy publication aliases are missing, it binds the existing outputs to one canonical identity. It performs no trading calculation and creates no historical trading row.
2. Settings Quick/Full run now invokes the bridge before `enforce_post_run_consistency`, so `run_id`, `generation_id`, symbol, timeframe, completed candle, snapshot hash, and source signature reach every Lunch renderer.
3. Table 1 now reads `lunch_metric_result_published_20260618`, both established metric caches, matrix outputs, and the published full-metric history. It joins the existing Table 3 factor histories by completed broker candle. When there is no archive yet, it displays only the genuine current published row as `PENDING`.
4. Table 4 now consumes both `ranked_news` and `articles` from Research/NLP publication objects, Finnhub retained cache, and canonical NLP/sentiment objects. Local H1 evidence is only the explicit fallback.
5. Field 789 already routes to the combined Field 4-to-9 workspace; the router and menu aliases were preserved. The workspace renders Field 456 and Field 789 together without merging their calculation engines.
6. AirLLM remains lazy, server-only, and canonical-grounded. It is enabled with `ADX_ENABLE_AIRLLM=1`, a local or explicitly downloadable model in `ADX_AIRLLM_MODEL_ID`, and the optional `requirements-airllm.txt`. The deterministic grounded assistant remains the safe fallback.

## Why Table 1 was blank

The renderer was read-only and correct to refuse invented data. The upstream run could produce Field 1/Table 3 objects yet fail to publish the complete identity aliases. Because Table 1 requires a completed canonical candle, its snapshot constructor failed and the fallback did not search every real publication key. The bridge repairs that producer-consumer contract.

## Why Table 4 stayed local-only

The renderer searched several news keys but omitted common `articles` outputs from the published NLP and Research packs. A connected Finnhub key alone does not create ranked rows; the fetch, NLP publication, and renderer must share the same state keys. Those keys are now covered.

## AirLLM deployment

Base Streamlit Cloud deployment intentionally excludes AirLLM because it is heavy for a phone-facing app. For a server with sufficient RAM/disk, install `requirements-airllm.txt`, set `ADX_ENABLE_AIRLLM=1`, set `ADX_AIRLLM_MODEL_ID` to a local model directory or model ID, and set `ADX_AIRLLM_ALLOW_DOWNLOAD=1` only when server downloads are acceptable. The iPhone runs only the browser UI; inference executes on the server.

## Ten research foundations and exact system use

1. **The Model Confidence Set** — Peter R. Hansen, Asger Lunde, James M. Nason (Econometrica, 2011). Belief: uncertain samples should retain a set of statistically indistinguishable best models instead of declaring one permanent winner. Theorem/concept: sequential equal-predictive-ability tests eliminate inferior models while controlling confidence. Use: maintain an MCS for Power BI path, regime, direction, and interval models by rolling loss; ensemble only surviving models.
2. **Strictly Proper Scoring Rules, Prediction, and Estimation** — Tilmann Gneiting and Adrian E. Raftery (JASA, 2007). Belief: a probability forecast must be rewarded for honesty, not merely direction accuracy. Theory: a strictly proper score has expected optimum at the true predictive distribution. Use: Brier/log score for BUY/SELL probabilities and CRPS/interval score for price paths; prevent overconfident reliability.
3. **Adaptive Conformal Inference Under Distribution Shift** — Isaac Gibbs and Emmanuel Candès (NeurIPS, 2021). Belief: fixed intervals lose coverage as markets drift. Theory: online adaptation of the conformal miscoverage parameter targets long-run coverage under changing distributions. Use: dynamically widen/narrow 1h/3h/6h bands using recent coverage error without altering the central prediction.
4. **Conformal Inference for Online Prediction with Arbitrary Distribution Shifts** — Isaac Gibbs and Emmanuel Candès (JMLR, 2024). Belief: adaptation must react on local time intervals, not only globally. Theory: online conformal procedures obtain local regret/coverage guarantees under arbitrary shifts. Use: separate calibrators for London, overlap, and Asian sessions and reset/accelerate after drift alarms.
5. **The Use of the Area Under the ROC Curve in the Evaluation of Machine Learning Algorithms** — Andrew P. Bradley (Pattern Recognition, 1997). Belief: threshold-free discrimination should be measured separately from probability calibration. Concept: ROC AUC estimates ranking probability across positive/negative classes. Use: evaluate direction-ranking quality, but never use AUC alone; combine with proper scores and trading utility.
6. **A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle** — James D. Hamilton (Econometrica, 1989). Belief: market behavior can switch among latent states with persistent transition probabilities. Theory: Markov-switching likelihood/filtering estimates state probabilities and transitions. Use: make Field 3 output probabilities, expected duration, and transition risk rather than one hard regime label.
7. **Multi-Scale Markov-Switching GARCH: Volatility Regime Detection and Forecasting for EUR/USD** (2026). Belief: EUR/USD volatility state differs across nested horizons and transition probabilities can vary over time. Concept: multi-timeframe MS-GARCH with time-varying transition probabilities. Use: combine 1-day, 5-day, and 25-day regime standards as independent state probabilities; use volatility state to scale intervals and TP/SL, not to overwrite direction.
8. **A Hidden Markov Model for Intraday Momentum Trading** — Hans Christensen and coauthors (2020). Belief: a latent momentum state can reduce lag around trend reversals and accept side information. Concept: offline HMM learning with fast online filtering. Use: add M1 confirmation and session/NLP features as emissions or side predictors; keep inference lightweight on each completed H1 candle.
9. **Continuous Inspection Schemes** — E. S. Page (Biometrika, 1954). Belief: small persistent changes should be detected through accumulated evidence. Theory: CUSUM/Page change detection signals when cumulative deviation crosses a threshold. Use: monitor Brier loss, interval misses, residual mean, and news-feature distribution; freeze model promotion and raise “DRIFT/WATCH” on alarm.
10. **Utility-Weighted Forecasting and Calibration for Risk-Adjusted Decision Systems** (2026 working paper). Belief: statistical accuracy is not the final objective when costs, risk limits, and capacity matter. Concept: optimize/calibrate forecasts against constrained decision utility. Use: keep protected BUY/SELL/WAIT rules, but evaluate candidate research models with spread/slippage-aware expected value, drawdown penalty, and abstention value before promotion.

## Recommended quant promotion order

First build an immutable walk-forward evaluation store. Second compute proper scores, interval coverage, and utility by session/regime. Third apply MCS to remove consistently inferior candidates. Fourth calibrate probabilities and intervals. Fifth add drift alarms. Sixth permit only shadow models that pass minimum sample size, leakage, stability, and economic-utility gates. Never promote from in-sample accuracy.

## Verification commands

```bash
python -m compileall -q .
PYTHONPATH=. pytest -q tests/test_field1_publication_bridge_20260626.py tests/test_user_priority_repair_20260626.py
streamlit run app.py
```

On the running app: add API keys in Settings, press Quick Run once, verify a non-empty canonical identity, verify Table 1 has the current row plus genuine retained history, verify Table 4 says `FINNHUB/NLP` when external news exists, open Field 789/Field 4 to 9, and test Refresh, Copy Short, Copy Full, all menu buttons, text-area paste, and chat input at a 375×812 viewport.
