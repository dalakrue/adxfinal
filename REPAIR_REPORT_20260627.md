# ADX Quant Pro Repair — 2026-06-27

## Implemented

1. Added the missing authoritative router branch for `Field 4 to 9`, so the floating/menu choice no longer falls through to Settings.
2. Repaired Field 1 Table 3 factor-name/schema adaptation.
3. Added read-only recovery of missing Net Pressure and Direction Confirmation histories from already-published overall Field 1 history columns.
4. Rebuilt Field 1 Table 4 as a 25-day, completed-H1 aligned bias-history collection.
5. Table 4 now attempts these exact source contracts:
   - Technical: Field 1 Table 3 Entry Strength decision.
   - Regime: Field 3 lower-standard Less Risky Bias.
   - Session: published session history, with adaptive completed-OHLC fallback.
   - Data Mining: Historical Next 1 Hour Direction / Prescriptive Label from Random Forest + KNN priority publications.
   - Sentiment: Regime Direction from 25-Day Regime Prediction History + NLP publications.
6. Missing Table 4 sources remain marked `MISSING`; they are not silently rewritten as WAIT.
7. Added Available Sources, Coverage %, Directional Agreement, Combined Next-Hour Direction and Confirmation Strength columns.
8. Added explicit AirLLM Open / Closed mode to the independent AI Assistant tab. Closed mode never loads the model; Open mode still requires valid server configuration and lazy-loads only after a question.
9. Preserved protected production decisions and existing calculation engines. The new adapters are display/read-only except the requested adaptive session-bias fallback.

## Validation

- `python -m compileall -q core ui tabs lunch pages services app.py adx_dashpoard.py` — passed.
- Targeted pytest collection could not run in this repair container because Streamlit is not installed here (`ModuleNotFoundError: streamlit`). This is an environment dependency failure, not a Python syntax failure.

## Deployment entry point

Use `app.py` as the Streamlit entry point.

## Local commands

```powershell
cd "PATH_TO_EXTRACTED_PROJECT"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

## Streamlit Cloud

- Main file path: `app.py`
- Python: 3.12
- Add API keys only through Streamlit Secrets; never commit keys to Git.
- AirLLM remains optional. For a capable server set `ADX_ENABLE_AIRLLM=1` and `ADX_AIRLLM_MODEL_ID`; otherwise keep Closed mode.
