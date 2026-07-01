# ADX Quant Pro — Repair Implementation Report

Date: 2026-06-28  
Preferred entry point: `streamlit run app.py`  
Compatibility entry point: `streamlit run adx_dashpoard.py`  
Required deployment runtime: Python 3.12

## Executive result

The uploaded project was repaired in place without replacing the protected production decision logic. The work concentrated on publication identity, timestamp normalization, display integration, secure AI connectivity, calculation scope separation, runtime persistence, warning removal, and Windows event-loop compatibility.

The repaired package has:

- 125 passing automated tests.
- Successful byte-code compilation of the complete project.
- Successful Streamlit AppTest navigation through both entry files.
- Successful headless HTTP health checks through both entry files.
- No OpenRouter key pattern stored in project files.
- A new focused regression suite for the failures reported on 2026-06-28.

## Repairs completed

### 1. Windows `WinError 10054` event-loop noise

The Windows selector-event-loop compatibility policy is now installed before Streamlit/Tornado imports in all three entry paths: `app.py`, `adx_dashpoard.py`, and `main.py`.

This does not pretend that a remote provider can never reset a TCP connection. It prevents the common Proactor shutdown callback from becoming an unhandled transport traceback and keeps network errors inside the connector fallback path.

### 2. Scikit-learn single-label warnings

`core/nlp_event_response.py` now:

- Uses ordinary accuracy for the mathematically degenerate one-label balanced-accuracy case.
- Passes the complete production label universe (`BUY`, `SELL`, `WAIT`) to `confusion_matrix`.
- Produces a stable 3×3 matrix even when a short test slice contains only one class.

A regression test verifies that no single-label warning is emitted.

### 3. Pandas all-NA concatenation `FutureWarning`

The Field 1 current-row overlay now removes empty/all-NA fragments before concatenation and reindexes columns deliberately. This preserves the current behavior without relying on the deprecated dtype inference path.

### 4. `str` versus `Timestamp` comparison crash

All candidate latest-times used by Lunch field rendering are normalized into timezone-aware UTC `Timestamp` objects before ordering. This fixes:

`'<' not supported between instances of 'str' and 'Timestamp'`

The repair accepts legacy strings, pandas timestamps, index timestamps, and timezone-naive values.

### 5. Power BI stale canonical mismatch

The canonical publication bridge now compares three completed-H1 identities:

1. Loaded OHLC latest completed H1.
2. Existing canonical completed H1.
3. Newly published Field 1 metric history completed H1.

Rules:

- An exact or newer canonical may be reused.
- An older canonical cannot be silently reused for newer OHLC.
- If the freshly calculated metric reaches the newer H1 candle, the canonical identity is rebound to that calculated publication.
- If both canonical and metric are stale, the bridge returns `STALE_CANONICAL_RECALC_REQUIRED`; no synthetic or stale Power BI path is fabricated.

The runtime exact-source cache also reuses a generation only when its source signature exactly matches the currently loaded completed source.

### 6. Field 1 Table 1

The decision-table adapter now:

- Recovers Net Pressure Decision from already-published BUY/SELL pressure evidence when only the display alias is absent.
- Preserves the immutable correctness contract: an outcome that has not reached its next completed H1 remains unsettled.
- Displays `PENDING — NEXT H1 NOT SETTLED` rather than a visually blank `N/A` for unsettled correctness.
- Stores the exact visible Table 1 frame in a stable session/cache key for Table 5 and browser-refresh recovery.

No future outcome is guessed to remove `N/A`.

### 7. Field 1 Table 5 blank Table 1 columns

Table 5 now resolves the already-visible Table 1 first, including legacy cache aliases. It then:

- Detects common time-column names and Date+Hour forms.
- Converts both tables to UTC.
- Floors both sides to the completed H1 boundary.
- Normalizes legacy column names.
- Performs an outer one-to-one join by completed broker candle.
- Keeps partial rows honestly when one source is absent.
- Copies the production master decision only from an explicit production source.

This fixes the failure where Table 4 columns appeared but Table 1 columns stayed blank despite existing data.

### 8. Finder Table 3 fallback

Finder previously called `build_decision_table(state)` with a missing required snapshot argument. The fallback now resolves the published canonical identity, constructs a read-only display snapshot, and calls the existing builder correctly. It does not trigger a new trading calculation.

### 9. Browser refresh and state persistence

The secret-free warm cache now explicitly includes:

- Visible Field 1 Table 1.
- Published Field 1 Table 3.
- Table 4 and Table 5.
- Active page, subpage, Lunch field, and Dinner field.

API keys, passwords, tokens, and credential-like state remain excluded.

### 10. OpenRouter AI Assistant

A new secure backend was added in `services/openrouter_backend_20260628.py`.

Capabilities:

- Resolves OpenRouter from Streamlit Secrets, environment, or a temporary session replacement.
- One-click Save + Connect validation in Settings.
- Auto-validates a secret-configured key once per session.
- Uses `openrouter/auto` by default, with an optional configurable model.
- Sends a bounded, read-only canonical contract plus compact published Table 1/Table 4/Table 5/priority/news context.
- Never inserts the API key into prompts, history, runtime cache, logs, or visible status.
- Falls back to AirLLM when available, then to the existing deterministic canonical intent router if the API is unavailable.

The AI remains read-only and cannot rewrite protected calculations or decisions.

### 11. AirLLM setup

AirLLM is no longer force-installed by the base deployment requirements. The project now has:

- Base `requirements.txt` that runs without AirLLM.
- Separate `requirements-airllm.txt` restricted to compatible Python versions.
- `install_airllm_windows.ps1`, which creates a Python 3.12 virtual environment and installs the optional stack.
- Clear UI status when the app is running under Python 3.13: Python 3.12 is required for the compatibility-locked AirLLM environment.

OpenRouter and the deterministic assistant work independently of AirLLM.

### 12. Quick, Full, and Super Quick calculation scopes

The buttons now map to different scopes correctly:

- **Quick Run**: protected Fields 1–9 + AI; skips additive thesis-only rebuilds.
- **Full Run**: protected Fields 1–9 + all thesis/research publishers + AI.
- **Super Quick Lunch**: protected Lunch Fields 1–3 only; skips Fields 4–9 shadow publishers and thesis-only add-ons.

The underlying V9 implementation previously treated `QUICK` as the 1–3 scope. It now limits 1–3 only when the scope is `LUNCH_CORE`, matching the visible labels.

All successful modes navigate to Lunch and open Field 1 first.

### 13. Dinner and existing UI requirements verified

The uploaded project already contained and retained these requested behaviors:

- Dinner is a cached/read-only presentation path and does not rebuild the trading system when an expander or chart control changes.
- Dinner history removes empty/single-row late columns and compacts visible width.
- Fields 4, 6, 7, 8, and 9 use flattened metric/table presentation with lazy detail.
- Current Data Session Intelligence and the one-hour exit opportunity rule are rendered in Dinner.
- Copy Short, Copy Full, and independent Refresh + Sync controls remain available.
- Regime lifecycle is inside a user-openable expander that defaults closed.
- Medium/Higher regime history uses interval/change compression rather than repeating unchanged state every hour.
- Finnhub and the second market-data key retain one-click save/connect controls.

## Important performance statement

The repaired architecture removes redundant same-candle rebuilds and gives genuinely narrower calculation scopes. That is the correct mechanism for the requested 30–50% reduction. A percentage or universal “under five minutes” guarantee cannot be honestly certified without the user's live data volume, network latency, API rate limits, hardware, and model configuration. The included status records elapsed time and exact cache hits so the reduction can be measured on the deployment.

Dinner page opening itself is presentation-only and should not start its previous 15–390 minute rebuild behavior.

## Files materially added or changed

Added:

- `services/openrouter_backend_20260628.py`
- `tests/test_repair_20260628.py`
- `install_airllm_windows.ps1`
- `.streamlit/secrets.example.toml`
- `DELIVERY_20260628/*`

Principal modified files:

- `app.py`
- `adx_dashpoard.py`
- `main.py`
- `requirements.txt`
- `core/decision_table_20260626.py`
- `core/field1_publication_bridge_20260626.py`
- `core/nlp_event_response.py`
- `core/runtime_state_cache_20260628.py`
- `core/secure_api_startup_20260619.py`
- `core/settings_run_orchestrator_20260617.py`
- `core/settings_run_orchestrator_v9_parts/part_001.py`
- `pages/ai_assistant.py`
- `tabs/antd_page_router_20260615.py`
- `ui/airllm_mobile_assistant_20260626.py`
- `ui/finder_canonical_view_20260619.py`
- `ui/lunch_decision_table_20260626.py`
- `ui/lunch_four_core_fields_20260619.py`
- `ui/lunch_next_hour_bias_history_20260626.py`

## Recommended launch

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
