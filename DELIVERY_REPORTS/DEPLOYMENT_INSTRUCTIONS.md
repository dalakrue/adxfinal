# Deployment instructions

## Streamlit Cloud

1. Upload/extract the project without changing its directory structure.
2. Set the main file path to `app.py`.
3. Use Python 3.12 (`runtime.txt` and `.python-version` are included).
4. Install `requirements.txt`.
5. Configure connector/API secrets through Streamlit secrets or environment variables as already supported by the project.
6. Start the app and run **Quick Run Fields 1–3 + Open Lunch** from Settings.

## Local

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Optional AirLLM server backend

Install `requirements-optional-heavy.txt` only on a measured server. Keep `ADX_ENABLE_AIRLLM=0` by default. To opt in, set `ADX_ENABLE_AIRLLM=1`, `ADX_AIRLLM_MODEL_ID` to a local model directory or approved model ID, and normally keep `ADX_AIRLLM_ALLOW_DOWNLOAD=0`. Output and input limits can be bounded with `ADX_AIRLLM_MAX_OUTPUT_TOKENS` and `ADX_AIRLLM_MAX_INPUT_TOKENS`. The lightweight grounded assistant remains the fallback.
