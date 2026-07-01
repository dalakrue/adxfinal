# Deployment Instructions — 2026-06-22

## Local Windows PowerShell

```powershell
cd "<EXTRACTED_PROJECT_FOLDER>"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

`app.py` is the preferred entry point. `main.py` and `adx_dashpoard.py` remain compatible alternatives, but Streamlit Cloud should use `app.py`.

## Broker clock configuration

In Settings, configure either:

- the explicit manual MT5 broker-chart UTC offset, or
- a valid IANA broker timezone such as `Europe/Helsinki` when the broker clock follows that DST schedule.

The manual offset has precedence. After configuration, run the existing **Run Calculation + Open Lunch** action. Verify the top Lunch contract/sync status before relying on any history timestamp.

## Streamlit Cloud

1. Upload the complete project contents to the repository root.
2. Set Main file path to `app.py`.
3. Keep `runtime.txt` as `python-3.12`.
4. Install from the included `requirements.txt`.
5. Do not place API keys in copied payloads or source files; use Streamlit secrets only where an existing connector requires them.
6. After deployment, configure the broker clock in Settings and run one canonical calculation.

## Post-deployment checks

- Lunch top shows Copy Short and Copy Full before phone controls/field gates.
- Copy Short is no more than 100 lines.
- Field 1 sync panel shows the active completed broker candle, Field 1 latest candle, ID/generation/offset/source matches.
- Closed Fields 1–6 do not block AI Send/Analyze or copy generation.
- Field 6 exposes the preserved combined/readiness views plus eleven nested quantitative histories.
- Missing broker configuration shows the explicit unavailable message, never UTC under a broker label.
