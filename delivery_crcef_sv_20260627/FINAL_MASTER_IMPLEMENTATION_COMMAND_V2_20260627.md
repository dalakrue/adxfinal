# FINAL MASTER IMPLEMENTATION COMMAND V2 — PRIORITY REPAIR OVERRIDE

Use this file together with the latest complete ADX Quant Pro project ZIP and the screenshots showing the defects.

The rules in this priority section override any conflicting lower-priority wording later in the document. The non-deletion, protected-source, immutable-canonical-snapshot, broker-time, no-fabrication, and no-future-leakage rules remain absolute.

## A. DELIVERY BOUNDARY

Do not claim that the project has been repaired merely from this requirements document.

Before editing, verify that the uploaded material includes the actual project files, including at minimum:

```text
app.py
adx_dashpoard.py or adx_dashboard.py
core/
ui/
tabs/
services/
tests/
requirements.txt
runtime.txt
.streamlit/config.toml
```

If only a text requirements file is present, return the implementation plan and exact missing-file list. Do not invent changed files, tests, screenshots, ZIPs, or execution results.

## B. OBSERVED FAILURE IDENTITY

The following values identify the observed failing published generation only:

```text
source_snapshot_hash: 98115b8a944ff3472a37
source_signature: 8ae056b2ce990a6ca938f7bf8d05f693d33ac1c42aad2ff4c372f8ee75e144b8
```

Do not hard-code these values. Use them only to locate logs, database rows, caches, and canonical publications associated with the failure.

The observed contradiction is:

```text
Power BI projection state: valid result
Projection integrity validation failed
Canonical latest completed H1 timestamp is invalid
Green path waiting for a valid exact-run central path
```

A generation must never be simultaneously published as `valid result` and `integrity validation failed`.

## C. ONE APPLICATION SHELL AND TWO COMPATIBLE ENTRY FILES

The supported command is:

```bash
streamlit run app.py
```

Do not use:

```bash
streamlit run app.pyb
```

`app.py` is the deployment entry point.

`adx_dashpoard.py` may remain as a backward-compatible alternative, but both files must call the same application shell, router, page registry, session-state schema, and renderer registry.

Required architecture:

```python
# app.py
from core.app_shell import run_app

if __name__ == "__main__":
    run_app()
```

```python
# adx_dashpoard.py
from core.app_shell import run_app

def main():
    run_app()

if __name__ == "__main__":
    main()
```

Do not maintain a second router or second menu definition inside either entry file.

Acceptance:

```text
streamlit run app.py
streamlit run adx_dashpoard.py
```

must display the same routes, including Dinner, and must use the same navigation state.

## D. NAVIGATION MUST BE INDEPENDENT OF LUNCH

Create one navigation state machine owned by the application shell, not by Lunch, Dinner, Settings, or a field renderer.

Use separate state keys:

```text
requested_page
active_page
active_lunch_field
active_dinner_field
menu_open
navigation_generation
```

Only the shell may commit `active_page`.

Page-local code may change only its own local selection, such as `active_lunch_field`.

Apply a navigation request before rendering the active page:

```python
def request_page(page_name: str) -> None:
    st.session_state["requested_page"] = page_name

def commit_requested_page(valid_pages: set[str]) -> None:
    requested = st.session_state.pop("requested_page", None)
    if requested in valid_pages:
        st.session_state["active_page"] = requested
        st.session_state["menu_open"] = False
        st.session_state["navigation_generation"] = (
            int(st.session_state.get("navigation_generation", 0)) + 1
        )
```

Execution order on every Streamlit rerun:

```text
1. Initialize navigation defaults.
2. Commit any requested route.
3. Render the floating menu.
4. Read active_page once.
5. Render exactly one page.
```

Do not allow Lunch code to run before route commitment.

Delete or disable every page-local fallback that performs behavior similar to:

```python
active_page = "Lunch"
active_page = "Settings"
st.session_state["active_page"] = default_page
```

unless the current route is genuinely invalid.

Do not use button return values after another part of the page has already rendered the Lunch route. Use `on_click=request_page` or a pre-render route transaction.

The floating menu must include direct buttons for at least:

```text
Settings
Lunch
Dinner
AI Assistant
Research
Other
```

Required Dinner button:

```python
st.button(
    "Dinner",
    key="floating_nav_dinner",
    on_click=request_page,
    args=("Dinner",),
    use_container_width=True,
)
```

The menu must remain clickable:

```text
- on first app load;
- before a calculation has run;
- after Quick Run;
- while Lunch is selected;
- after opening or closing any Lunch expander;
- after changing chart controls;
- after a Streamlit rerun;
- on desktop;
- on iPhone-sized layouts.
```

The menu must not be covered by Lunch CSS, chart overlays, fixed headers, invisible containers, or modal backdrops. Audit z-index, pointer-events, position, overflow, and viewport width.

Do not fix navigation by forcing multiple reruns. A click may cause one normal Streamlit rerun, but must not need a second click.

## E. DINNER IS A DIRECT TOP-LEVEL PAGE

Create a direct route:

```text
active_page = "Dinner"
```

Aliases may resolve to Dinner:

```text
Field 4 to 9
Field 456
Field 789
Field 456+789
Dinner Combined
```

The visible direct route name is `Dinner`.

Clicking Dinner must never redirect to Lunch or Settings.

Dinner must display original:

```text
Field 4
Field 6
Field 7
Field 8
Field 9
```

together in one read-only page.

Do not merge their production calculation engines merely because their outputs are displayed together.

Dinner rendering order:

```text
1. Canonical identity strip.
2. Dinner Combined History — Last 25 Broker Days.
3. Compact current consensus metrics.
4. Field 4 details, closed by default.
5. Field 6 details, closed by default.
6. Field 7 details, closed by default.
7. Field 8 details, closed by default.
8. Field 9 details, closed by default.
9. Research-only CRCEF-SV diagnostics, closed by default.
10. Audit evidence and exports.
```

## F. DINNER TOP HISTORY TABLE

At the absolute top of Dinner, after the identity strip, render:

```text
Dinner Combined History — Last 25 Broker Days
```

Use newest completed MetaTrader broker candle first.

Do not fabricate rows. A 25-day window means retain and show all genuinely available completed H1 rows whose broker dates fall within the most recent 25 broker days. It does not mean create 25 fake rows.

Recursively inspect the published outputs for Fields 4, 6, 7, 8, and 9. Collect only real decision-like and bias-like source columns, including nested structures where necessary.

Required columns where sources exist:

```text
Broker Candle
Broker Date
Weekday
Broker Hour
Symbol
Timeframe
Field 4 Bias
Field 4 Decision
Field 4 Source Column
Field 6 Bias
Field 6 Decision
Field 6 Source Column
Field 7 Bias
Field 7 Decision
Field 7 Source Column
Field 8 Bias
Field 8 Decision
Field 8 Source Column
Field 9 Bias
Field 9 Decision
Field 9 Source Column
Technical Consensus
NLP Event Bias
Regime Bias
Volatility State
Forecast Bias
BUY Evidence
SELL Evidence
Conflict
Coverage
Calibrated Probability
Actionability
Expected Utility
Uncertainty
Production Master Decision
Research Shadow Action
Research Reliability
Run ID
Generation ID
Source Snapshot Hash
Source Signature
```

Rules:

```text
- Preserve disagreements.
- Do not drop one field because another field disagrees.
- Calculate Conflict from disagreement; do not hide disagreement.
- Do not duplicate columns that have identical semantic meaning and identical provenance.
- Keep an audit mapping from each displayed column to its original field, object path, and source column.
- Detailed original Dinner tables remain available below.
```

## G. POWER BI PROJECTION INTEGRITY REPAIR

Repair the exact error:

```text
Canonical latest completed H1 timestamp is invalid.
```

### G1. Canonical timestamp contract

The canonical snapshot must contain one authoritative value:

```text
completed_broker_candle
```

It must be:

```text
- parseable;
- timezone-aware;
- aligned to H1;
- a completed candle, never the forming candle;
- expressed in the shared MetaTrader broker-candle clock;
- identical across Lunch Field 1, Power BI, Field 3, Dinner, AI grounding, histories, and exports.
```

Do not use `datetime.now()`, `datetime.utcnow()`, browser time, or local PC time as analytical candle time.

Implement or repair a strict parser:

```python
def parse_completed_broker_candle(value, broker_tz):
    ts = pd.Timestamp(value)
    if pd.isna(ts):
        raise CanonicalIntegrityError("completed_broker_candle is NaT")
    if ts.tzinfo is None:
        ts = ts.tz_localize(broker_tz)
    else:
        ts = ts.tz_convert(broker_tz)
    if ts.minute != 0 or ts.second != 0 or ts.microsecond != 0:
        raise CanonicalIntegrityError("completed_broker_candle is not H1 aligned")
    return ts
```

Adapt this to the project's existing shared provider rather than creating a competing time engine.

### G2. Publication ordering

The Settings orchestration must publish in this order:

```text
1. Resolve broker-time configuration.
2. Fetch and normalize source candles once.
3. Select latest completed H1 candle once.
4. Freeze completed_broker_candle.
5. Run protected Lunch publishers.
6. Run protected Dinner publishers.
7. Run projection publisher from the same frozen inputs.
8. Run research shadow publishers.
9. Validate cross-output identity.
10. Atomically publish one canonical generation.
11. Navigate to Lunch.
```

A projection may not publish before `completed_broker_candle` is frozen.

### G3. Exact-run projection identity

A projection is valid only when all these values match the canonical snapshot:

```text
run_id
generation_id
symbol
timeframe
completed_broker_candle
source_snapshot_hash
source_signature
```

The central production path, displayed bands, and green less-risky path must reference that same identity.

Do not silently substitute a prior generation.

### G4. Single projection state

Replace contradictory state strings with one enum:

```text
VALID
INSUFFICIENT_DATA
STALE
IDENTITY_MISMATCH
INVALID_TIMESTAMP
PATH_UNAVAILABLE
PUBLICATION_INCOMPLETE
```

If the timestamp is invalid, state must be `INVALID_TIMESTAMP`, not `valid result`.

If the production path is valid but the optional green path is unavailable, keep the protected production chart visible and mark only the green research path as unavailable.

Do not remove or replace the production chart because a shadow path failed.

### G5. Projection tests

Add tests for:

```text
- valid timezone-aware completed H1 timestamp;
- naive timestamp localized through broker configuration;
- NaT rejection;
- malformed timestamp rejection;
- forming-candle rejection;
- H1 alignment rejection;
- projection/canonical run_id mismatch;
- generation_id mismatch;
- source hash mismatch;
- source signature mismatch;
- no stale fallback;
- protected chart remains visible when only green shadow path fails;
- one-button run produces a valid exact-run central path when source data is sufficient.
```

## H. DECISION LABEL TAXONOMY

Do not collapse these labels:

```text
BUY
SELL
WAIT
WAIT PULLBACK
HOLD
HOLD & PROTECT
```

Protected raw production text must remain available.

Use these two columns when user-facing wording differs:

```text
Production Decision Raw
Action Display Label
```

Mapping rules:

```text
BUY -> BUY
SELL -> SELL
WAIT PULLBACK -> WAIT PULLBACK
HOLD -> HOLD & PROTECT only when an existing-position state and protection logic are explicitly present
WAIT -> WAIT unless validated pullback criteria explicitly classify it as WAIT PULLBACK
```

Do not convert every WAIT into WAIT PULLBACK.

Do not convert HOLD into BUY or SELL.

Do not infer BUY or SELL from a positive or negative score alone.

Do not overwrite the canonical production decision to satisfy a display-label preference.

For the visible compact action summary, prefer:

```text
WAIT PULLBACK
HOLD & PROTECT
```

when those explicit conditions exist.

Store the original source label beside the display label for audit.

## I. LUNCH FIELD 1 — TABLE 1 SOURCE REPAIR

Table 3 remains protected and unchanged.

Table 1 must be a historical collection of Table 3 published decision columns, not a new re-computation.

For every row, map:

```text
Net Pressure Decision
Direction Confirmation Decision
```

from the exact Table 3 publication for the same:

```text
run_id
generation_id
symbol
timeframe
completed_broker_candle
```

Do not map by row number alone.

Required provenance:

```text
Net Pressure Source Object
Net Pressure Source Column
Direction Confirmation Source Object
Direction Confirmation Source Column
Master Decision Source Object
Master Decision Source Column
Source Run ID
Source Generation ID
Completed Broker Candle
Source Snapshot Hash
Source Signature
```

Preserve exact source labels:

```text
WAIT remains WAIT
WAIT PULLBACK remains WAIT PULLBACK
HOLD remains HOLD
BUY remains BUY
SELL remains SELL
```

If a user-facing display column is needed, add it separately without changing the source column.

The final production-decision column must never be blank when an explicit canonical master decision exists.

If no explicit source decision exists, show:

```text
N/A — source not published
```

Do not fabricate one.

Add row-level validation:

```text
table1.net_pressure_decision == table3.net_pressure_decision
table1.direction_confirmation_decision == table3.direction_confirmation_decision
table1.master_decision == canonical.production_master_decision
```

Any mismatch must display an audit error and fail the publication integrity gate.

## J. TABLE 4 THRESHOLD AUDIT

Preserve Table 4 production calculation and production thresholds.

The reported high WAIT frequency must be investigated, not “fixed” by arbitrarily halving a threshold.

Perform a shadow-only threshold study using completed, settled rows and leakage-safe validation.

Candidate thresholds may include:

```text
100%
90%
80%
70%
60%
50%
```

of the current threshold, but none may be promoted merely because it creates more BUY/SELL decisions.

Evaluate:

```text
CPCV result
PBO
net expected utility after spread/slippage
false BUY rate
false SELL rate
WAIT rate
WAIT PULLBACK rate
HOLD rate
decision turnover
maximum drawdown
expected shortfall
Brier score
ECE
coverage
regime stability
session stability
minimum sample size
```

Production remains unchanged unless an explicit promotion process passes.

## K. TABLE 5 REBUILD

Table 5 must not duplicate all of Field 1.

Rebuild it as:

```text
Table 5 — Integrated Decision Collection
```

It must join selected production columns from Table 1 and Table 4 by canonical identity.

Suggested production columns:

```text
Broker Candle
Net Pressure Decision
Direction Confirmation Decision
Table 1 Final Decision
Table 4 Technical Bias
Table 4 Entry Decision
Table 4 Reliability
Table 4 Conflict
Production Master Decision
Master Action
```

`Master Action` is the final production column.

Allowed Master Action values:

```text
BUY
SELL
WAIT
WAIT PULLBACK
HOLD
```

After the final production column, visibly separate research columns:

```text
Research Shadow Action
Research-Calibrated Probability
Actionability Probability
Expected Utility
Uncertainty
Research Reliability
Promotion Status
```

Do not use generated Table 5 columns as inputs to Table 5.

Do not feed Table 5 back into Table 1 or Table 4.

## L. FIRST-LOAD CLOSED STATE

On the first application load, and after a successful full Settings run opens Lunch:

```text
Field 1 closed
Field 2 closed
Field 3 closed
all nested Field 1 sections closed
all Field 3 sections closed
all Dinner field-detail sections closed
```

Opening an expander must never trigger a protected or heavy calculation.

Use state keys that are independent of navigation.

Do not initialize a widget key after the widget is instantiated.

## M. SINGLE SETTINGS RUN — NO QUICK SYNC

The only heavy action is:

```text
Quick Run All Fields 1–9 + AI + Open Lunch
```

It must run the complete dependency graph once and publish one generation.

Required outputs include:

```text
Lunch Fields 1, 2, and 3
all protected Lunch dependencies
Dinner Fields 4, 6, 7, 8, and 9
Dinner combined history
AI canonical grounding
all due outcome settlement
Power BI exact-run path
research shadow modules
audit rows
exports/copy payload caches
```

Remove, disable, or convert to read-only any Lunch button that performs a second:

```text
Quick Sync
Refresh API Data + Quick Sync
Publish Current Lunch
Rebuild Projection
```

The user may retain lightweight display refresh controls, but they must never calculate or publish a second canonical generation.

After publication:

```text
active_page = Lunch
all outputs share one identity
no second click is required
navigation remains usable
```

## N. TESTS THAT MUST FAIL BEFORE THE FIX AND PASS AFTER IT

Create targeted regression tests for the reported defects:

```text
test_app_and_legacy_entry_use_same_shell
test_floating_menu_works_on_first_load
test_floating_menu_works_after_full_run
test_lunch_cannot_overwrite_active_page
test_dinner_button_exists
test_dinner_click_opens_dinner
test_dinner_renders_fields_4_6_7_8_9
test_dinner_history_is_first_data_table
test_dinner_history_uses_completed_broker_candles
test_projection_state_not_valid_when_timestamp_invalid
test_projection_uses_exact_canonical_identity
test_green_shadow_failure_does_not_remove_production_path
test_table1_net_pressure_matches_table3
test_table1_direction_confirmation_matches_table3
test_table1_preserves_wait_pullback
test_table1_preserves_hold
test_table1_final_column_populated_from_explicit_source
test_table4_threshold_not_arbitrarily_halved
test_table5_is_selected_join_not_field1_duplicate
test_table5_master_action_is_final_production_column
test_one_settings_run_executes_all_publishers
test_no_second_quick_sync_required
test_fields_closed_on_first_load
test_opening_expanders_does_not_calculate
```

## O. REQUIRED IMPLEMENTATION EVIDENCE

At completion, provide actual evidence, not assertions:

```text
- changed-file list;
- before/after router call graph;
- exact entry-point code;
- exact navigation state transaction;
- projection integrity test output;
- Table 1/Table 3 row-level comparison sample;
- Table 5 source-column mapping;
- Dinner source-column mapping;
- pytest output;
- compile output;
- Streamlit smoke-test output;
- screenshots or textual AppTest evidence;
- packaged project ZIP;
- remaining limitations caused by unavailable live credentials or data.
```

Do not claim completion when only static inspection was possible.

---

# TEN VERIFIED RESEARCH-PAPER BLUEPRINTS

The following ten papers form the research foundation. Implement them as a separate, auditable shadow layer. A paper title is not permission to copy production logic or overwrite protected decisions.

## Paper 1 — The Probability of Backtest Overfitting

Authors:

```text
David H. Bailey
Jonathan M. Borwein
Marcos López de Prado
Qiji Jim Zhu
```

Research belief:

```text
The more strategies, thresholds, features, and parameter combinations that are tried,
the more likely the apparent winner is a statistical false discovery.
```

Core principle:

```text
Compare the in-sample ranking of candidate strategies with their out-of-sample ranking
across many combinatorial paths. Estimate how often the selected in-sample winner falls
below the out-of-sample median.
```

Key algorithm:

```text
1. Divide settled chronological observations into groups.
2. Form combinations of test groups.
3. Purge overlapping label intervals.
4. Apply an embargo.
5. Evaluate all candidates on every valid split.
6. Generate multiple out-of-sample paths.
7. Convert relative OOS performance into logit ranks.
8. Estimate PBO as the fraction of paths where the selected candidate underperforms.
```

System integration:

```text
Use CPCV/PBO before changing Table 4 thresholds, Table 5 policy,
calibration method, regime count, meta-label threshold, event-memory weighting,
or interval controller.
```

Benefit:

```text
Prevents a visually attractive threshold from being accepted because it was lucky
in one historical window.
```

Thesis extension:

```text
Develop regime-conditioned PBO and decision-class-conditioned PBO for
BUY, SELL, WAIT, WAIT PULLBACK, and HOLD.
```

## Paper 2 — Predicting Good Probabilities with Supervised Learning

Authors:

```text
Alexandru Niculescu-Mizil
Rich Caruana
```

Research belief:

```text
A classifier can rank examples well while producing badly distorted probabilities.
Trading decisions need reliable probabilities, not accuracy alone.
```

Core principle:

```text
Fit calibration only on predictions not used to fit the base model.
Compare Platt scaling, isotonic regression, beta calibration, and eligible
Venn-Abers methods using proper scoring rules.
```

Key equations:

```text
Brier = mean((p - y)^2)

LogLoss = -mean(y*log(p) + (1-y)*log(1-p))

ECE = sum_b (n_b / N) * abs(accuracy_b - confidence_b)

BrierSkill = 1 - Brier_model / Brier_reference
```

System integration:

```text
Create research-calibrated BUY and SELL probabilities by horizon, session,
and regime. Keep production confidence unchanged.
```

Benefit:

```text
Makes a displayed 70% research probability mean approximately 70% empirical
success in comparable historical cases, subject to sample and drift limits.
```

Thesis extension:

```text
Compare global calibration with regime-conditioned and session-conditioned calibration.
```

## Paper 3 — Meta-Labeling: Theory and Framework

Author:

```text
Jacques Joubert
```

Research belief:

```text
Direction and actionability are different questions.
A directional signal may be correct but still be a poor immediate trade because of
spread, timing, volatility, conflict, or weak expected utility.
```

Core principle:

```text
Primary model: preserve the production direction.
Secondary model: estimate whether acting on that direction is justified.
```

Meta-label:

```text
1 = actionable
0 = not actionable
```

Key algorithm:

```text
1. Read the protected production label.
2. Preserve BUY, SELL, WAIT, WAIT PULLBACK, and HOLD text.
3. Build actionability features from past-available data only.
4. Estimate actionability probability.
5. Estimate expected gain, expected loss, cost, and uncertainty penalty.
6. Return a research shadow action.
```

System integration:

```text
Use it to distinguish:
BUY
SELL
WAIT
WAIT PULLBACK
HOLD
```

Benefit:

```text
Reduces false entries without forcing the primary directional engine to change.
```

Thesis extension:

```text
Create a five-state selective-action policy with separate entry timing and
position-maintenance models.
```

## Paper 4 — Regime Changes and Financial Markets

Authors:

```text
Andrew Ang
Allan Timmermann
```

Research belief:

```text
Financial relationships are state-dependent and may change abruptly,
while each new state can persist.
```

Core principle:

```text
Represent the market as a latent Markov state with transition probabilities.
Estimate filtered probabilities for live use and reserve smoothed probabilities
for historical research.
```

Key equations:

```text
P_ij = P(S_t = j | S_(t-1) = i)

ExpectedDuration_j = 1 / (1 - P_jj)

EstimatedRemaining_j =
max(0, ExpectedDuration_j - CurrentRegimeAge_j)
```

System integration:

```text
Add research regime, agreement with production regime, age, expected duration,
remaining duration, and 1H/3H/6H transition risk to Field 3 and Dinner.
```

Benefit:

```text
Allows calibration, interval width, and actionability to adapt to the current state.
```

Thesis extension:

```text
Test whether regime-conditioned calibration and thresholds outperform global versions.
```

## Paper 5 — Regime-Switching and the Estimation of Multifractal Processes

Authors:

```text
Laurent E. Calvet
Adlai J. Fisher
```

Research belief:

```text
Volatility is generated by components operating at several persistence scales,
not by one homogeneous process.
```

Core model:

```text
sigma_t^2 = base_variance * product(M_k,t for k = 1..K)
```

Key algorithm:

```text
1. Estimate several latent volatility multipliers.
2. Give each multiplier a different switching persistence.
3. Combine components into forecast variance.
4. Produce horizon-specific expected moves.
5. Compare against GARCH, ATR, and rolling-volatility baselines.
```

System integration:

```text
Produce immediate, session, daily, persistent, jump, and residual volatility.
Use them in conformal width, WAIT PULLBACK diagnostics, and risk-capacity research.
```

Benefit:

```text
Distinguishes a short-lived spike from persistent high volatility.
```

Thesis extension:

```text
Design a EURUSD H1 multi-scale volatility-capacity score conditioned by session and regime.
```

## Paper 6 — Conformal Prediction for Time Series

Authors:

```text
Chen Xu
Yao Xie
```

Research belief:

```text
A point forecast without empirical interval coverage is incomplete.
Sequential residuals can produce adaptive uncertainty intervals without
assuming a fully correct parametric error distribution.
```

Core algorithm:

```text
1. Generate strictly out-of-sample residuals.
2. Maintain a rolling residual calibration set.
3. Compute the required residual quantile.
4. Add and subtract the quantile from each horizon forecast.
5. Update only after the outcome becomes available.
6. Track realized coverage and interval width.
```

Key equations:

```text
residual_t = abs(actual_t - prediction_t)

q_t = quantile(recent OOS residuals, 1 - alpha)

lower_t = prediction_t - q_t
upper_t = prediction_t + q_t
```

System integration:

```text
Add Research Conformal Lower and Research Conformal Upper for 1H, 3H, and 6H.
Do not replace production bands.
```

Benefit:

```text
Measures whether the displayed uncertainty interval actually covers realized prices.
```

Thesis extension:

```text
Compare global, regime-conditioned, and volatility-conditioned residual pools.
```

## Paper 7 — Bellman Conformal Inference: Calibrating Prediction Intervals for Time Series

Authors:

```text
Zitong Yang
Emmanuel Candès
Lihua Lei
```

Research belief:

```text
Intervals should not be widened blindly after every miss.
Coverage and sharpness can be treated as a sequential control problem.
```

Core principle:

```text
Use dynamic programming or a bounded approximation to select an interval-control
action that balances future coverage debt against interval length.
```

Suggested objective:

```text
Cost =
coverage_penalty
+ lambda_width * width
+ lambda_instability * abs(width_t - width_(t-1))
+ lambda_decision * decision_uncertainty
```

System integration:

```text
Wrap the base conformal intervals.
Store base width, controlled width, action, cost, and coverage debt.
```

Benefit:

```text
Targets adequate long-run coverage while avoiding permanently uninformative wide intervals.
```

Thesis extension:

```text
Add regime, session, spread, and actionability utility to the control state.
```

## Paper 8 — Learning from Time-Changing Data with Adaptive Windowing

Authors:

```text
Albert Bifet
Ricard Gavaldà
```

Research belief:

```text
A model trained on an old distribution should not be trusted indefinitely.
The useful historical window should shrink when statistically meaningful change occurs.
```

Core principle:

```text
ADWIN maintains an adaptive window and tests possible splits between older and newer data.
When their means differ beyond a confidence bound, the old portion is dropped and drift is declared.
```

Key algorithm:

```text
1. Add each new settled error or feature statistic.
2. Evaluate candidate splits in the adaptive window.
3. Compare older and newer means with a statistical bound.
4. Declare drift only when the bound is exceeded.
5. Preserve drift event, affected model, and prior model version.
```

System integration:

```text
Monitor directional error, Brier score, ECE, residuals, non-coverage,
volatility, regime probabilities, class balance, sentiment, and spread proxies.
```

Benefit:

```text
Blocks promotion or degrades research confidence when historical performance is no longer representative.
```

Thesis extension:

```text
Create a multi-stream drift severity index used by CRCEF-SV.
```

## Paper 9 — Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting

Authors:

```text
Bryan Lim
Sercan O. Arik
Nicolas Loeff
Tomas Pfister
```

Research belief:

```text
Multi-horizon forecasts can benefit from combining static, known-future,
and observed-history variables with feature selection and temporal attention.
```

Core architecture:

```text
- variable selection networks;
- gating;
- recurrent local processing;
- interpretable self-attention;
- quantile outputs.
```

Quantile loss:

```text
L_q =
q * max(y - y_hat, 0)
+ (1 - q) * max(y_hat - y, 0)
```

System integration:

```text
Research-only 1H, 3H, and 6H P10/P50/P90 forecasts.
Use lazy optional dependencies and CPU-safe inference.
Compare against previous close, zero return, rolling mean, and simpler models.
```

Benefit:

```text
Provides one coherent multi-horizon research forecast and feature-importance diagnostics.
```

Safeguard:

```text
Attention is not causal proof.
Reject TFT when it does not provide stable leakage-safe incremental value.
```

Thesis extension:

```text
Evaluate whether adding regime, event memory, and multi-scale volatility
improves quantile loss and expected utility.
```

## Paper 10 — FinBERT: Financial Sentiment Analysis with Pre-trained Language Models

Author:

```text
Dogu Araci
```

Research belief:

```text
Financial language is domain-specific, so generic sentiment models can
misread policy, inflation, employment, and market language.
```

Core principle:

```text
Use a finance-adapted language model for entity-level sentiment,
but do not treat sentiment alone as a trading decision.
```

Key event-memory algorithm:

```text
1. Deduplicate articles and event updates.
2. Extract EUR, USD, ECB, Federal Reserve, inflation, employment, GDP,
   PMI, rates, and geopolitical entities.
3. Estimate entity-level sentiment and EURUSD relevance.
4. Create event vectors with text, entities, topic, surprise, regime, and session.
5. Match only to historical events whose future outcomes were already settled.
6. Weight similar-event outcomes.
7. Produce 1H, 3H, and 6H expected responses with uncertainty and sample size.
```

Similarity weighting:

```text
weight_i =
exp(-distance_i / temperature)
/
sum_j exp(-distance_j / temperature)
```

Expected response:

```text
expected_response_h =
sum_i weight_i * historical_return_(i,h)
```

System integration:

```text
Dinner NLP event bias, Research page, AI grounding, and CRCEF-SV evidence.
```

Benefit:

```text
Uses historical market response to comparable events rather than trusting headline tone alone.
```

Thesis extension:

```text
Test event-response memory against sentiment-only and keyword-only baselines.
```

---

# ORIGINAL FULL REQUIREMENT BASELINE

The full original command follows. Apply the priority repair override above first, then implement the remaining requirements below unless they conflict with the override.

---

# MASTER IMPLEMENTATION COMMAND

## Advanced Quant Research Layer for Master’s and PhD Thesis

Inspect, repair, test, and upgrade the uploaded Streamlit quantitative-analysis project into a thesis-level quantitative research system.

The system analyzes EURUSD primarily on the H1 timeframe. Preserve the existing application, calculations, tables, navigation, APIs, exports, charts, history, and canonical data. Add the following 10 research frameworks as a separate, auditable research layer.

---

# 1. NON-DELETION AND SOURCE-OF-TRUTH RULES

You must obey all these rules.

1. Do not delete, rename, replace, simplify, hide permanently, or rewrite any existing:

   * Calculation
   * Production decision
   * Table
   * Column
   * History table
   * Chart
   * API connector
   * Export
   * Navigation item
   * AI feature
   * Regime output
   * Reliability metric
   * Canonical snapshot field

2. Do not modify the calculations or structure of Table 3 in Field 1 of the Lunch tab.

3. Treat Table 3 of Field 1 as a protected production source.

4. Preserve all Dinner data from Fields 4, 6, 7, 8, and 9.

5. Do not delete Dinner information merely because there is too much data.

6. Existing outputs must remain available as collapsible audit evidence.

7. Implement the research models as a separate shadow calculation layer.

8. Do not allow a research model to overwrite a production BUY, SELL, WAIT, WAIT PULLBACK, or HOLD decision.

9. Do not fabricate historical rows.

10. Do not convert missing values into invented results.

11. Do not use future information when calculating a historical row.

12. All calculations must use only information available at the completed broker candle being evaluated.

13. Every renderer must read one frozen canonical snapshot identified by:

```text
run_id
generation_id
symbol
timeframe
completed_broker_candle
source_snapshot_hash
source_signature
```

14. Use MetaTrader broker-candle time from one shared provider.

15. Never use local PC time, browser time, `datetime.now()`, or `datetime.utcnow()` as the analytical candle time.

16. Add or use one shared function similar to:

```python
shared_broker_time_provider()
```

17. Heavy calculations must run only from the Settings button:

```text
Quick Run All Fields 1–9 + AI + Open Lunch
```

18. That single button must:

* Fetch required source data.
* Complete all Lunch calculations.
* Complete all Dinner calculations.
* Run all Field 1–9 publishers.
* Run all research shadow models.
* Settle pending outcomes.
* Publish one complete canonical snapshot.
* Open the Lunch tab.
* Require no second Quick Sync click.

19. Opening a field, table, tab, expander, or history view must never start a heavy calculation.

20. Keep the system Streamlit Cloud compatible and mobile-friendly.

---

# 2. PRIMARY OBJECTIVE

Create a separate research framework called:

```text
Canonical Regime-Calibrated Evidence Fusion with Selective Validation
```

Abbreviation:

```text
CRCEF-SV
```

The research system must combine the outputs of the 10 research modules described below while preserving all production calculations.

The new framework must improve:

* Accuracy
* Probability reliability
* Decision consistency
* Uncertainty measurement
* Regime awareness
* Prediction-interval coverage
* Drift detection
* Historical validation
* Event-response analysis
* BUY/SELL actionability
* WAIT, WAIT PULLBACK, and HOLD classification
* Thesis auditability
* Computational efficiency

The research layer must produce recommendations, diagnostics, and shadow decisions. It must not directly change the protected production decisions.

---

# 3. REQUIRED ARCHITECTURE

Create a modular package similar to:

```text
research_quant/
    __init__.py
    config.py
    schemas.py
    canonical_adapter.py
    validation/
        cpcv.py
        purging.py
        embargo.py
        pbo.py
        metrics.py
    calibration/
        probability_calibration.py
        reliability_diagram.py
        calibration_metrics.py
    meta_labeling/
        primary_direction_adapter.py
        actionability_model.py
        action_policy.py
    regime/
        markov_switching.py
        regime_lifecycle.py
        transition_model.py
    multifractal/
        volatility_components.py
        msm_model.py
        volatility_capacity.py
    conformal/
        enbpi.py
        adaptive_intervals.py
        coverage_metrics.py
    bellman_conformal/
        interval_controller.py
        interval_policy.py
        interval_utility.py
    drift/
        adwin_monitor.py
        drift_registry.py
        promotion_guard.py
    forecasting/
        multi_horizon_dataset.py
        tft_adapter.py
        quantile_forecast.py
    nlp_event_memory/
        deduplication.py
        entity_sentiment.py
        event_embedding.py
        similarity_memory.py
        response_estimator.py
    fusion/
        evidence_registry.py
        crcef_sv.py
        selective_policy.py
        explanation.py
    persistence/
        research_store.py
        outcome_store.py
        model_registry.py
    ui/
        lunch_research.py
        dinner_research.py
        validation_dashboard.py
        audit_view.py
    tests/
```

Use the project’s current architecture where appropriate. Do not create duplicate canonical engines.

---

# 4. COMMON DATA CONTRACT

Create typed schemas for all research outputs.

At minimum, every research result must contain:

```python
{
    "run_id": str,
    "generation_id": str,
    "symbol": str,
    "timeframe": str,
    "completed_broker_candle": datetime,
    "model_name": str,
    "model_version": str,
    "research_mode": bool,
    "source_snapshot_hash": str,
    "input_feature_hash": str,
    "created_at_broker_time": datetime,
    "status": str,
    "reason": str,
    "sample_size": int,
    "quality_flags": list[str]
}
```

All research outputs must be immutable after publication for a given run.

Create explicit statuses:

```text
VALID
INSUFFICIENT_DATA
STALE
DRIFT_DETECTED
CALIBRATION_FAILED
COVERAGE_FAILED
LEAKAGE_RISK
MODEL_UNAVAILABLE
RESEARCH_ONLY
```

Do not silently replace errors with neutral scores.

---

# 5. RESEARCH MODULE 1

## Combinatorial Purged Cross-Validation and Probability of Backtest Overfitting

Implement a validation framework based on the research topic:

```text
Backtest Overfitting in the Machine Learning Era
```

### Required concept

Standard random K-fold cross-validation is not safe for overlapping financial labels.

Implement:

* Chronological groups
* Purging
* Embargo
* Combinatorial Purged Cross-Validation
* Multiple backtest paths
* Probability of Backtest Overfitting
* Deflated or adjusted performance analysis
* Stability measurement

### Required algorithm

1. Divide historical completed broker candles into chronological groups.
2. Select combinations of groups as test sets.
3. Remove training samples whose label intervals overlap test intervals.
4. Apply an embargo after each test interval.
5. Generate multiple valid out-of-sample paths.
6. Evaluate every candidate algorithm on every path.
7. Measure how often the in-sample winner underperforms out of sample.
8. Calculate a PBO estimate.
9. Block model promotion when overfitting risk exceeds the configured threshold.

### Required output columns

```text
Candidate Model
Validation Method
Number of Groups
Test Groups per Split
Number of Paths
Purge Count
Embargo Candles
In-Sample Score
Out-of-Sample Score
Score Degradation
Worst-Path Score
Median-Path Score
Path Stability
PBO
Leakage Check
Promotion Status
Reason
```

### Required tests

* No overlap between test labels and training information intervals.
* Embargo is applied correctly.
* Future data never enters the feature set.
* Identical inputs produce identical splits.
* Candidate ranking is calculated only from valid paths.

### Integration

Use this module to validate:

* Table 4 threshold changes
* Table 5 Master Action rules
* Regime thresholds
* NLP-event response models
* Calibration models
* Meta-label thresholds
* Prediction interval policies

Do not promote a new algorithm merely because it performs well in one historical split.

---

# 6. RESEARCH MODULE 2

## Probability Calibration

Implement probability calibration inspired by:

```text
Obtaining Calibrated Probabilities from Boosting
```

### Required concept

Classification accuracy is not enough. A predicted probability must correspond to its empirical outcome frequency.

Implement and compare:

* Uncalibrated probability
* Platt scaling
* Isotonic regression
* Beta calibration when available
* Venn-Abers when dependencies are available
* Calibration by regime
* Calibration by forecast horizon

### Required equations

Brier score:

```text
BS = mean((p - y)^2)
```

Log loss:

```text
LL = -mean(y*log(p) + (1-y)*log(1-p))
```

Expected Calibration Error:

```text
ECE = sum((bin_size / total_size) * abs(bin_accuracy - bin_confidence))
```

Brier Skill Score:

```text
BSS = 1 - BS_model / BS_reference
```

### Required algorithm

1. Train the base model only on the training data.
2. Generate predictions on a separate calibration period.
3. Fit every eligible calibration method.
4. Evaluate the calibrators on a separate untouched test set.
5. Choose the calibrator by:

   * Brier score
   * Log loss
   * ECE
   * Stability
   * Sample sufficiency
6. Do not choose by classification accuracy alone.
7. Store the selected calibrator with model version and training window.
8. Reuse the stored calibrator until drift or expiry requires reevaluation.

### Required output

```text
Raw BUY Probability
Calibrated BUY Probability
Raw SELL Probability
Calibrated SELL Probability
Selected Calibrator
Brier Score
Brier Skill Score
Log Loss
ECE
Maximum Calibration Error
Calibration Sample Size
Calibration Window
Regime-Specific Calibration
Reliability Status
```

### Required visual

Add a reliability diagram showing:

* Mean predicted probability by bin
* Actual outcome frequency by bin
* Perfect calibration diagonal
* Sample count per bin

### Integration

Use calibrated probabilities for research confidence, expected utility, and selective decision policies.

Do not overwrite any existing production confidence field. Label new values clearly as:

```text
Research-Calibrated Probability
```

---

# 7. RESEARCH MODULE 3

## Meta-Labeling and Actionability

Implement a two-stage decision model.

### Required concept

The first model determines direction. The second model decides whether acting on that direction is justified.

### Primary direction

Read the protected production direction without modifying it:

```text
BUY
SELL
WAIT
WAIT PULLBACK
HOLD
```

Where a numerical encoding is required, use:

```text
BUY = +1
SELL = -1
WAIT = 0
WAIT PULLBACK = 0
HOLD = 0
```

Do not lose the original text label.

### Required meta-label

```text
1 = primary directional signal was actionable
0 = primary directional signal was not actionable
```

### Required features

The meta-model may use:

* Calibrated direction probability
* Spread
* Volatility
* Regime probability
* Regime age
* Regime-transition risk
* Prediction-interval width
* Conflict score
* Data coverage
* Session
* Time until high-impact event
* M1 confirmation
* H1 trend capacity
* Drift status
* Recent calibration quality
* Historical similar-signal outcomes

### Required outputs

```text
Primary Direction
Primary Source
Actionability Probability
Meta-Label
Recommended Shadow Action
Entry Timing Status
Expected Gain
Expected Loss
Transaction Cost Estimate
Expected Utility
Reason for Action
Reason for Rejection
```

### Required decision distinctions

The research policy must distinguish:

```text
BUY
SELL
WAIT
WAIT PULLBACK
HOLD
```

Rules:

* BUY: positive direction and positive actionability utility.
* SELL: negative direction and positive actionability utility.
* WAIT PULLBACK: direction is strong, but current entry timing or price location is unfavorable.
* HOLD: an existing position remains valid and exit risk is acceptable.
* WAIT: no sufficiently reliable actionable direction exists.

### Important rule

Never change `WAIT PULLBACK` into BUY or SELL only because pressure is positive or negative.

Never change `HOLD` into BUY or SELL unless the underlying protected production source explicitly changes.

---

# 8. RESEARCH MODULE 4

## Markov-Switching Regime Lifecycle

Implement a regime model inspired by:

```text
Regime Changes and Financial Markets
```

### Required concepts

* Latent market state
* Transition matrix
* Filtered state probability
* Smoothed state probability for historical research only
* State persistence
* Regime age
* Expected regime duration
* Estimated remaining duration
* Transition probability by horizon

### Required equations

```text
P_ij = P(S_t = j | S_(t-1) = i)
```

```text
ExpectedDuration_j = 1 / (1 - P_jj)
```

```text
EstimatedRemaining_j =
max(0, ExpectedDuration_j - CurrentRegimeAge_j)
```

### Required states

Start with interpretable research states such as:

```text
BULL_NORMAL
BULL_COMPRESSION
BULL_EXPANSION
BEAR_NORMAL
BEAR_COMPRESSION
BEAR_EXPANSION
RANGE_LOW_VOLATILITY
RANGE_HIGH_VOLATILITY
TRANSITION
```

The exact fitted number of latent states must be selected through validation rather than forced.

### Required outputs

```text
Current Research Regime
Production Regime
Regime Agreement
Filtered Regime Probability
Second Most Likely Regime
Transition Risk
Regime Start Candle
Regime Age
Expected Duration
Estimated Remaining Duration
1H Transition Probability
3H Transition Probability
6H Transition Probability
Regime Reliability
Regime Sample Size
```

### Integration

Add the research regime result to:

* Field 3
* Dinner top summary
* CRCEF-SV evidence fusion
* Prediction interval conditioning
* Calibration grouping
* Actionability model

Do not overwrite the existing production regime.

---

# 9. RESEARCH MODULE 5

## Multi-Scale Markov-Switching Multifractal Volatility

Implement a multi-scale volatility model based on Markov-switching multifractal concepts.

### Required concept

Represent volatility as several latent components with different persistence levels.

### Required equation

```text
sigma_t_squared =
base_variance * product(M_k_t for k in 1..K)
```

### Required volatility components

Create interpretable estimates for:

* Immediate H1 volatility
* Intraday/session volatility
* Daily volatility
* Multi-day volatility persistence
* Event-driven jump volatility
* Residual/unexplained volatility

### Required outputs

```text
Immediate Volatility
Session Volatility
Daily Volatility
Persistent Volatility
Jump Volatility
Combined Forecast Variance
Volatility Regime
Volatility Persistence
Expected Move 1H
Expected Move 3H
Expected Move 6H
Risk Capacity
Volatility Reliability
```

### Required risk capacity equation

```text
RiskCapacity =
ExpectedMove / sqrt(ForecastVariance)
```

### Integration

Use this research output to improve:

* Prediction interval width
* WAIT PULLBACK diagnostics
* Position-sizing research
* Trend-capacity research
* High-volatility warning
* Entry rejection during unstable volatility

Do not use the model to silently increase recommended leverage or lot size.

---

# 10. RESEARCH MODULE 6

## EnbPI and Adaptive Conformal Prediction

Implement conformal prediction inspired by:

```text
Conformal Prediction for Time Series
```

### Required concept

Produce distribution-free adaptive uncertainty intervals for sequential time-series forecasts.

### Required algorithm

1. Generate strictly out-of-sample residuals.
2. Maintain a rolling residual calibration window.
3. Calculate the required residual quantile.
4. Construct prediction intervals for:

   * 1H
   * 3H
   * 6H
5. Track realized coverage.
6. Adapt the residual window without using future observations.
7. Flag insufficient calibration data.

### Basic interval

```text
residual_t = abs(actual_t - predicted_t)
```

```text
q = quantile(recent_out_of_sample_residuals, 1 - alpha)
```

```text
lower = prediction - q
upper = prediction + q
```

### Required outputs

```text
Forecast Horizon
Point Prediction
Lower Bound
Upper Bound
Interval Width
Target Coverage
Realized Coverage
Coverage Error
Residual Sample Size
Residual Quantile
Interval Status
```

### Integration

Show the conformal bands in Power BI or the existing projection field without deleting existing bands.

Label them clearly:

```text
Research Conformal Lower
Research Conformal Upper
```

Do not represent the interval as a guaranteed future price range.

---

# 11. RESEARCH MODULE 7

## Bellman Conformal Interval Control

Implement an adaptive interval controller inspired by:

```text
Bellman Conformal Inference: Calibrating Prediction Intervals for Time Series
```

### Required objective

Balance:

* Interval coverage
* Interval width
* Coverage error persistence
* Market regime
* Volatility
* Decision usefulness

### Suggested objective

```text
Objective =
coverage_penalty
+ lambda_width * interval_width
+ lambda_instability * interval_change
+ lambda_decision * decision_uncertainty
```

### Required algorithm

1. Read the base conformal interval.
2. Read recent coverage errors.
3. Read regime and volatility state.
4. Adjust the interval control parameter.
5. Penalize unnecessarily wide intervals.
6. Penalize repeated undercoverage.
7. Keep adjustment limits bounded.
8. Store every interval-policy decision for audit.

### Required outputs

```text
Base Interval Width
Controlled Interval Width
Width Adjustment
Coverage Debt
Control Action
Control Cost
Coverage Penalty
Width Penalty
Decision Utility Penalty
Bellman Policy Status
```

### Integration

Use Bellman-controlled intervals as a research display and CRCEF-SV uncertainty input.

Do not overwrite production prediction bands.

---

# 12. RESEARCH MODULE 8

## ADWIN and Model Drift Detection

Implement adaptive drift detection based on ADWIN principles.

### Required monitored streams

Monitor drift separately for:

* Directional prediction error
* Brier score
* Calibration error
* Forecast residual
* Conformal non-coverage
* Feature distribution
* Volatility
* Regime probabilities
* BUY/SELL class balance
* NLP sentiment distribution
* Spread and liquidity proxies

### Required detection logic

Compare statistically different older and newer portions of the adaptive window.

A drift state must not depend on one unusual candle alone unless the configured statistical test supports it.

### Required outputs

```text
Monitor Name
Drift Status
Drift Magnitude
Drift Start Candle
Detection Candle
Old Window Mean
New Window Mean
Window Size Before
Window Size After
Affected Model
Retraining Recommended
Promotion Blocked
Reason
```

### Required system behavior

When meaningful drift is detected:

* Do not automatically retrain on a page render.
* Do not silently replace the model.
* Mark affected research outputs as degraded.
* Block model promotion where required.
* Reevaluate through the controlled Settings calculation.
* Preserve the previous model version for rollback.

---

# 13. RESEARCH MODULE 9

## Temporal Fusion Transformer Multi-Horizon Research Adapter

Implement a research-only multi-horizon forecasting adapter inspired by:

```text
Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting
```

### Important dependency rule

The Streamlit application must continue to run even when PyTorch, TensorFlow, or a TFT library is unavailable.

Use:

* Optional dependency guards
* Lazy loading
* Research-mode configuration
* Cached model loading
* CPU-safe inference
* Clear unavailable status

### Required forecast horizons

```text
1H
3H
6H
```

### Required inputs

Where available, use:

* H1 OHLC
* H1 returns
* M1 confirmation
* Session
* Broker candle hour
* Weekday
* Regime probabilities
* Multi-scale volatility
* Spread
* Trend capacity
* Economic-event timing
* Entity-level sentiment
* Event-response memory
* Existing technical factors
* Historical prediction errors

### Required quantiles

At minimum:

```text
0.10
0.50
0.90
```

### Quantile loss

```text
L_q =
q * max(y - prediction, 0)
+ (1 - q) * max(prediction - y, 0)
```

### Required outputs

```text
Horizon
P10 Forecast
P50 Forecast
P90 Forecast
Directional Probability
Expected Return
Expected Absolute Move
Forecast Agreement
Top Features
Attention Summary
Model Version
Training Window
Validation Status
```

### Required interpretation safeguards

* Do not claim that attention proves causality.
* Do not promote TFT until CPCV, calibration, and drift requirements pass.
* Compare the TFT with simple baselines.
* Reject it if it does not add stable out-of-sample value.

---

# 14. RESEARCH MODULE 10

## Financial NLP Event-Response Memory

Implement an entity-aware event-response research system inspired by FinBERT and financial event-memory research.

### Required functions

1. Collect or read the existing news data.
2. Deduplicate articles.
3. Extract entities.
4. Classify entity-level sentiment.
5. Calculate EURUSD relevance.
6. Create event embeddings.
7. Match current events with historical events.
8. Weight historical price responses.
9. Produce expected 1H, 3H, and 6H event responses.
10. Report sample size and uncertainty.

### Required entities

At minimum, identify:

```text
EUR
Eurozone
ECB
Germany
France
USD
United States
Federal Reserve
CPI
PCE
NFP
GDP
PMI
Interest Rate
Inflation
Employment
Geopolitical Risk
```

### Deduplication

Use:

* Exact title/text hash
* Normalized-title hash
* TF-IDF similarity or semantic-embedding similarity
* Source and timestamp analysis

Classify articles as:

```text
NEW
RELATED
DUPLICATE
UPDATED_EVENT
```

### Event similarity

Use a representation similar to:

```text
event_vector = [
    text_embedding,
    entity_features,
    topic_features,
    surprise_features,
    regime_features,
    session_features
]
```

Similarity weighting:

```text
weight_i =
exp(-distance(current_event, historical_event_i) / temperature)
/
sum_all_weights
```

Expected response:

```text
expected_response_h =
sum(weight_i * historical_return_i_h)
```

### Required outputs

```text
Event Time
Headline
Event Type
Primary Entity
EUR Sentiment
USD Sentiment
EURUSD Relevance
Novelty Score
Duplicate Status
Similar Event Count
Best Similarity
Weighted Response 1H
Weighted Response 3H
Weighted Response 6H
Event Direction
Event Reliability
Event Uncertainty
```

### Important rule

Do not use article sentiment alone as the final directional decision.

Event-response history must include regime, session, and sample sufficiency.

---

# 15. CRCEF-SV FUSION ENGINE

Create an evidence registry containing the research evidence families:

```text
Production Direction Adapter
Probability Calibration
Meta-Label Actionability
Regime Lifecycle
Multi-Scale Volatility
Conformal Coverage
Bellman Interval Control
Drift Status
Multi-Horizon Forecast
NLP Event-Response Memory
Historical Similarity
Data Coverage
Conflict
```

### Directional fusion score

Use a bounded score:

```text
Z_t =
sum(
    evidence_weight_k
    * calibration_quality_k
    * regime_relevance_k
    * directional_value_k
)
```

Normalize the weights:

```text
weight_k =
exp(quality_score_k / temperature)
/
sum(exp(quality_score_j / temperature))
```

Every directional value must be within:

```text
-1 to +1
```

### Uncertainty

Create an uncertainty score using:

```text
U_t =
lambda_entropy * direction_entropy
+ lambda_conflict * evidence_conflict
+ lambda_drift * drift_level
+ lambda_interval * normalized_interval_width
+ lambda_coverage * coverage_error
+ lambda_data * missing_data_penalty
```

Normalize uncertainty to:

```text
0 to 100 percent
```

### Expected utility

For each possible action:

```text
ExpectedUtility(action) =
probability_correct * expected_gain
- probability_wrong * expected_loss
- transaction_cost
- uncertainty_penalty
- regime_transition_penalty
```

### Selective action policy

Output one of:

```text
BUY
SELL
WAIT
WAIT PULLBACK
HOLD
```

Suggested logic:

```text
BUY:
Z_t exceeds BUY threshold,
calibrated BUY probability passes threshold,
meta-label actionability passes threshold,
expected utility is positive,
drift is acceptable,
coverage is acceptable.

SELL:
Z_t is below negative SELL threshold,
calibrated SELL probability passes threshold,
meta-label actionability passes threshold,
expected utility is positive,
drift is acceptable,
coverage is acceptable.

WAIT PULLBACK:
direction is strong,
but current entry location, volatility, spread,
or expected utility makes immediate entry unfavorable.

HOLD:
an existing position remains directionally valid,
exit risk is acceptable,
and no validated reversal exists.

WAIT:
evidence is weak, conflicting, poorly calibrated,
drifting, insufficient, or has negative expected utility.
```

### Required CRCEF-SV outputs

```text
Production Decision
Research Shadow Decision
Direction Fusion Score
BUY Evidence
SELL Evidence
Conflict
Coverage
Calibrated Direction Probability
Actionability Probability
Expected Utility
Uncertainty
Regime Relevance
Drift Penalty
Prediction Interval Width
NLP Event Contribution
Technical Contribution
Volatility Contribution
Decision Reason
Rejection Reason
Research Reliability
Promotion Eligibility
```

---

# 16. LUNCH TAB INTEGRATION

Do not modify Table 3 in Field 1.

Add the research layer to the Lunch tab as separate collapsible sections.

All fields must be closed by default on first system load.

## Field 1

Preserve all current tables.

### Table 1 correction

Verify that:

* Net Pressure Decision comes from the correct Table 3 factor publication.
* Direction Confirmation Decision comes from the correct Table 3 factor publication.
* `WAIT PULLBACK` remains `WAIT PULLBACK`.
* `HOLD` remains `HOLD`.
* `WAIT` remains `WAIT`.
* BUY and SELL are not inferred merely from the sign of a score.
* The final column is not blank.
* The final column reads the explicit canonical master or production decision.

Add provenance columns where appropriate:

```text
Net Pressure Source
Direction Confirmation Source
Master Decision Source
Source Run ID
Completed Broker Candle
```

### Table 4

Preserve the existing table and calculation.

Audit:

* Thresholds
* BUY/SELL symmetry
* WAIT frequency
* WAIT PULLBACK frequency
* HOLD frequency
* Missing-data handling
* Constant-output behavior
* Score diversity
* Leakage

Do not simply lower the WAIT threshold by an arbitrary amount.

Create a research comparison showing:

```text
Current Threshold
Research Candidate Threshold
CPCV Result
PBO
Expected Utility
Decision Turnover
False BUY Rate
False SELL Rate
WAIT Rate
Promotion Status
```

### Table 5

Table 5 must not duplicate all of Field 1.

It must be a combined decision-collection table containing selected columns from:

* Table 1
* Table 4

The last column must be:

```text
Master Action
```

The Master Action must use one of:

```text
BUY
SELL
WAIT
WAIT PULLBACK
HOLD
```

Add research columns after the preserved production columns:

```text
Research Shadow Action
Calibrated Probability
Actionability
Expected Utility
Uncertainty
Research Reliability
```

Clearly separate production and research outputs.

---

# 17. FIELD 3 INTEGRATION

Keep the entire Field 3 closed by default when the system first opens.

Add the research regime lifecycle outputs without deleting the existing regime tables.

Show:

* Existing production regime
* Research Markov regime
* Agreement
* Filtered probability
* Regime age
* Expected duration
* Estimated remaining duration
* 1H/3H/6H transition probabilities
* Regime reliability
* Drift warning

Do not recalculate merely because Field 3 is opened.

---

# 18. DINNER TAB INTEGRATION

Ensure the floating navigation contains a direct Dinner button.

Clicking Dinner must open the Dinner page.

The Dinner page must display together:

```text
Field 4
Field 6
Field 7
Field 8
Field 9
```

Do not delete their detailed data.

Keep detailed sections collapsible.

## Dinner top history table

At the top of Dinner, add a 25-day combined history table.

Use completed broker candles and newest-first order.

Combine the relevant bias and decision outputs from Fields 4, 6, 7, 8, and 9.

Suggested columns:

```text
Broker Candle
Symbol
Timeframe
Field 4 Bias
Field 4 Decision
Field 6 Bias
Field 6 Decision
Field 7 Bias
Field 7 Decision
Field 8 Bias
Field 8 Decision
Field 9 Bias
Field 9 Decision
Technical Consensus
NLP Event Bias
Regime Bias
Volatility State
Forecast Bias
BUY Evidence
SELL Evidence
Conflict
Coverage
Calibrated Probability
Actionability
Expected Utility
Uncertainty
Research Shadow Action
Production Master Decision
Research Reliability
Run ID
Generation ID
```

The top table must summarize existing detailed Dinner data. It must not replace or delete the detailed sections.

Avoid duplicated columns that have exactly the same meaning.

Where two fields disagree, preserve the disagreement and calculate conflict rather than hiding one value.

---

# 19. PERFORMANCE REQUIREMENTS

1. Use caching for immutable published snapshots.
2. Do not load heavy neural models until the Settings run requests them.
3. Use lazy imports for optional libraries.
4. Do not fit models during ordinary Streamlit reruns.
5. Store trained model artifacts with version metadata.
6. Reuse valid artifacts when:

   * Input schema matches.
   * Model has not expired.
   * Drift is acceptable.
   * Training configuration matches.
7. Use vectorized pandas or NumPy operations.
8. Avoid row-by-row Python loops where possible.
9. Limit UI rendering to required rows initially.
10. Keep all 25-day history available.
11. Make large tables collapsible.
12. Avoid repeatedly copying full DataFrames.
13. Add memory and runtime diagnostics.
14. Target a substantial RAM and CPU reduction without changing production logic.

---

# 20. PERSISTENCE REQUIREMENTS

Create or upgrade persistent tables for:

```text
canonical_snapshots
research_results
research_model_registry
research_validation_runs
calibration_models
drift_events
prediction_intervals
prediction_outcomes
event_memory
event_responses
promotion_decisions
```

Use migrations that safely create missing tables.

Do not assume an existing database contains every required table.

Do not delete old history.

Use uniqueness constraints based on appropriate combinations such as:

```text
run_id
generation_id
symbol
timeframe
completed_broker_candle
model_name
model_version
forecast_horizon
```

---

# 21. MODEL PROMOTION POLICY

All research models must initially have:

```text
RESEARCH_ONLY
```

A model becomes eligible for production consideration only when it passes:

* Leakage tests
* CPCV
* PBO limit
* Calibration limit
* Minimum sample size
* Prediction coverage
* Drift test
* Stability test
* Expected utility test
* Baseline comparison
* Reproducibility test

Create statuses:

```text
RESEARCH_ONLY
VALIDATION_FAILED
VALIDATION_PASSED
SHADOW_APPROVED
PRODUCTION_CANDIDATE
REJECTED
RETIRED
```

Do not automatically make any model a production model.

---

# 22. REQUIRED BASELINES

Every advanced model must be compared against simple baselines.

Include relevant baselines such as:

* Previous close
* Zero-return forecast
* Historical mean
* Rolling mean
* Logistic regression
* Simple calibrated classifier
* Existing production decision
* ATR interval
* Fixed-width interval
* Majority-class classifier
* Simple sentiment score

Reject an advanced model when it is not stably better than its baseline after costs and uncertainty.

---

# 23. REQUIRED TESTS

Create automated tests for:

## Navigation

* `streamlit run app.py` uses the correct application shell.
* `streamlit run adx_dashpoard.py` uses the same shell.
* Dinner button exists.
* Clicking Dinner selects Dinner.
* Dinner renders Fields 4, 6, 7, 8, and 9.
* Settings run opens Lunch.

## Single-run orchestration

* One Settings run executes every required publisher.
* No second Quick Sync action is required.
* All outputs share one `run_id`.
* All outputs share one completed broker candle.
* Opening fields does not recalculate.

## Time

* All history uses shared broker time.
* No analytical renderer uses local PC time.
* No future candle appears in a historical row.

## Table 1

* Net Pressure Decision matches its Table 3 source.
* Direction Confirmation Decision matches its Table 3 source.
* Text labels are preserved.
* Last column is populated.
* Missing values are not fabricated.

## Table 5

* It combines selected Table 1 and Table 4 columns.
* It is not a full duplicate.
* Master Action is the final production column.
* Research outputs are clearly separate.

## Research modules

* CPCV purging works.
* Embargo works.
* Calibration uses separate data.
* Meta-labels use only past information.
* Regime probabilities sum correctly.
* Prediction intervals use out-of-sample residuals.
* Drift events are reproducible.
* Event matching excludes future outcomes.
* CRCEF-SV output stays bounded.
* Production decisions are never overwritten.

## Persistence

* Database initializes from an empty state.
* Duplicate runs do not duplicate immutable rows.
* Model versions can be rolled back.
* Historical research outputs remain available.

---

# 24. REQUIRED AUDIT TABLE

Create an audit table containing:

```text
Run ID
Generation ID
Broker Candle
Module
Model Version
Input Hash
Output Hash
Data Window
Sample Size
Status
Warnings
Runtime
Peak Memory
Validation Status
Promotion Status
```

Add copy and export functionality without removing existing exports.

---

# 25. REQUIRED THESIS DOCUMENTATION

Create documentation files:

```text
docs/CRCEF_SV_ARCHITECTURE.md
docs/RESEARCH_METHODOLOGY.md
docs/MATHEMATICAL_DEFINITIONS.md
docs/VALIDATION_AND_LEAKAGE_CONTROL.md
docs/MODEL_PROMOTION_POLICY.md
docs/LUNCH_INTEGRATION.md
docs/DINNER_INTEGRATION.md
docs/EXPERIMENT_PLAN.md
docs/ABLATION_STUDY_PLAN.md
docs/THESIS_CONTRIBUTIONS.md
docs/LIMITATIONS_AND_ETHICS.md
```

## Thesis contribution proposal

Document the original contribution as:

```text
A canonical, regime-calibrated, uncertainty-aware evidence-fusion
framework that separates directional prediction, actionability,
entry timing, position maintenance, and abstention while enforcing
leakage-safe validation and immutable broker-candle snapshots.
```

## Required research questions

Include at least:

1. Does calibrated selective prediction improve EURUSD H1 decision reliability?
2. Does regime-conditioned calibration outperform global calibration?
3. Does meta-labeling reduce false BUY and false SELL actions?
4. Do adaptive conformal intervals improve empirical coverage?
5. Does Bellman interval control reduce width without damaging coverage?
6. Does multi-scale volatility improve WAIT PULLBACK classification?
7. Does event-response memory outperform plain sentiment?
8. Does CRCEF-SV outperform each individual evidence family?
9. Does drift-aware model blocking improve out-of-sample stability?
10. Does the complete framework remain effective after transaction costs?

## Required hypotheses

Example:

```text
H1:
CRCEF-SV produces a lower Brier score than the uncalibrated baseline.

H2:
The meta-labeling layer reduces false actionable signals without
materially reducing profitable-signal recall.

H3:
Regime-conditioned conformal intervals achieve coverage closer to
the target than fixed-width prediction intervals.

H4:
The combined framework produces higher leakage-safe expected utility
than any individual research module.
```

---

# 26. REQUIRED EXPERIMENTS

Implement an experiment registry and support:

1. Baseline versus calibrated probabilities.
2. Global versus regime-specific calibration.
3. Production direction versus meta-labeled action.
4. Fixed threshold versus dynamic threshold.
5. Fixed interval versus EnbPI.
6. EnbPI versus Bellman-controlled intervals.
7. Single-scale versus multi-scale volatility.
8. Sentiment-only versus event-response memory.
9. Individual module versus CRCEF-SV.
10. CRCEF-SV with and without drift protection.

For every experiment report:

```text
Experiment ID
Dataset Window
Training Window
Calibration Window
Test Window
CPCV Configuration
Costs
Brier Score
ECE
Log Loss
Accuracy
Precision
Recall
F1
Coverage
Interval Width
Expected Utility
Maximum Drawdown
Decision Turnover
BUY Rate
SELL Rate
WAIT Rate
WAIT PULLBACK Rate
HOLD Rate
PBO
Statistical Test
Confidence Interval
Conclusion
```

---

# 27. REQUIRED ABLATION STUDY

Test CRCEF-SV after removing each component:

```text
Without Calibration
Without Meta-Labeling
Without Regime
Without Multi-Scale Volatility
Without Conformal Intervals
Without Bellman Control
Without Drift Detection
Without TFT
Without NLP Event Memory
Without Similarity Weighting
```

Measure whether each component creates genuine incremental value.

Do not claim that a component is beneficial without an out-of-sample ablation result.

---

# 28. REQUIRED OUTPUT AT COMPLETION

After implementation, provide:

1. The repaired project ZIP.
2. A changed-files list.
3. A description of every new module.
4. A description of every changed existing module.
5. Test results.
6. Remaining warnings.
7. Exact Streamlit run command.
8. Exact dependency-installation command.
9. Exact database-initialization command if required.
10. Exact model-training command if training is separate.
11. Exact safe rollback instructions.
12. A mapping between each research paper and implemented code.
13. A mapping between each thesis equation and its implementation.
14. Screenshots or textual verification of:

    * Lunch
    * Field 1
    * Field 3
    * Dinner
    * Dinner top history
    * Research validation dashboard
15. A statement identifying anything that could not be tested because of unavailable live credentials or market data.

---

# 29. FINAL ACCEPTANCE CHECKLIST

Before delivering the repaired project, verify every item.

## Application

* [ ] `streamlit run app.py` works.
* [ ] `streamlit run adx_dashpoard.py` loads the same shell.
* [ ] Settings opens first after login.
* [ ] One Settings run calculates everything.
* [ ] Lunch opens automatically.
* [ ] No second Quick Sync is required.

## Lunch

* [ ] All fields are closed initially.
* [ ] Table 3 remains unchanged.
* [ ] Table 1 decisions match Table 3 sources.
* [ ] Table 1 final column is populated.
* [ ] Table 4 is audited without arbitrary threshold reduction.
* [ ] Table 5 is not a duplicate.
* [ ] Table 5 ends with Master Action.
* [ ] Research results are clearly separated.

## Dinner

* [ ] Dinner button exists in the floating menu.
* [ ] Dinner button opens Dinner.
* [ ] Fields 4, 6, 7, 8, and 9 are displayed.
* [ ] Dinner has a 25-day combined table at the top.
* [ ] Detailed Dinner data remains available.
* [ ] The combined table includes production and research decisions.

## Research

* [ ] CPCV is implemented.
* [ ] Purging is implemented.
* [ ] Embargo is implemented.
* [ ] PBO is reported.
* [ ] Calibration is leakage-safe.
* [ ] Meta-labeling is implemented.
* [ ] Regime lifecycle is implemented.
* [ ] Multi-scale volatility is implemented.
* [ ] EnbPI is implemented.
* [ ] Bellman interval control is implemented.
* [ ] ADWIN drift monitoring is implemented.
* [ ] TFT is optional and lazy-loaded.
* [ ] NLP event memory is implemented.
* [ ] CRCEF-SV fusion is implemented.
* [ ] No research output overwrites production.

## Validation

* [ ] Baselines are included.
* [ ] Transaction costs are included.
* [ ] Ablation studies are supported.
* [ ] Model promotion is guarded.
* [ ] Results are reproducible.
* [ ] No historical future leakage exists.

Do not report that the project is complete until all applicable checklist items pass. If any item cannot pass, explain the exact file, function, error, cause, and remaining corrective action.
