# ADX Quant Pro — Repair and Quant Upgrade Command

## Implemented repairs

1. AirLLM Open mode is now the execution authority for the current Streamlit session. The answer path reads the same session state as the visible Open/Closed control. A model-ID/local-path input was added, and the backend receives `runtime_enabled=True` and the selected model ID. AirLLM remains lazy-loaded only after a submitted question.
2. `airllm==2.11.0` is included for supported Python 3.9–3.12 deployments. Use Python 3.12. AirLLM still requires a model ID, enough RAM/disk, and either a local model or explicitly permitted download.
3. Field 4 to 9 was added to the authoritative tab-stability page list and legacy Field 456/789/567 values now normalize to Field 4 to 9 instead of Settings.
4. Table 1 now enriches blank, N/A, missing, zero-string and negative-zero decision cells using reproducible completed-H1 OHLC evidence. This is display-only and never overwrites protected production calculations.
5. Table 4 now calculates technical, market-tone sentiment proxy, session, regime and data-mining evidence inside its own module from completed H1 OHLC. It does not depend on another tab being rendered first.
6. Table 5 is an always-visible self-contained calculated evidence table, not a fallback. It displays scores, decisions, timestamps and calculation source.
7. Missing OHLC is never silently converted into BUY/SELL/WAIT. The UI directs the user to Refresh Data/Run Calculation instead of fabricating evidence.

## Deployment

```powershell
cd "PATH_TO_THE_REPAIRED_PROJECT"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

For AirLLM, open the AI Assistant page, choose **Open**, enter a Hugging Face model ID or local model folder, then ask a question. For remote downloads, set `ADX_AIRLLM_ALLOW_DOWNLOAD=1` only on a server with adequate resources. A small instruct model should be used first; large models are not suitable for a low-memory free deployment.

## Acceptance checks

```powershell
pytest -q tests/test_20260627_user_table_contract.py tests/test_user_priority_repair_20260626.py tests/test_five_surface_navigation_20260626.py
python -m compileall -q .
```

Expected result: 13 tests pass and all changed Python modules compile.

## Detailed future implementation command

Inspect, repair and test the ADX Quant Pro Streamlit application while preserving every protected production rule, threshold, historical outcome, model weight, TP/SL rule, broker-time rule and canonical identity. Keep `app.py` as the entry point. Make the top-level Field 4 to 9 navigation route authoritative and immune to legacy state resetting. Make the visible AirLLM Open/Closed control and the inference execution path use one shared session-state key. Lazy-load AirLLM only after a submitted question; provide clear setup status for package, model ID, local/download availability and runtime errors. Ground every answer in the frozen canonical evidence contract and use the deterministic assistant only when AirLLM genuinely cannot execute.

For Field 1 Table 1, preserve collected published decisions first, then replace only invalid display cells (N/A, blank, unavailable, missing, zero-string or negative-zero) with explicitly labelled completed-OHLC derived evidence. Never rewrite stored production decisions. For Table 4 and Table 5, calculate their own timestamp-aligned technical, regime, session, data-mining and sentiment/market-tone evidence from the loaded completed EURUSD H1 frame so rendering other tabs is not a prerequisite. Use rolling calculations with strict shift-before-fit for historical estimates. Show source, coverage, scores, thresholds and timestamps. Never manufacture news sentiment; when no NLP headline exists, label the value as a market-tone proxy rather than NLP evidence. Keep the full 25-day history newest first. Add unit tests for navigation, AirLLM mode consistency, no invalid decision strings, 100% internally calculable Table 4 coverage when OHLC exists, Table 5 visibility and leakage-safe rolling calculations.
