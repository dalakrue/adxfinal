# Deployment instructions

1. Extract the ZIP without nesting an additional project folder.
2. Use Python 3.12 (`runtime.txt` and `.python-version` are included).
3. Install: `pip install -r requirements.txt`.
4. Start locally: `streamlit run app.py`.
5. On Streamlit Cloud, set the main file path to `app.py`.
6. Configure optional API secrets in Streamlit secrets/environment; do not commit credentials.
7. AirLLM stays disabled unless explicitly enabled with `ADX_ENABLE_AIRLLM=1` and a model ID is supplied through `ADX_AIRLLM_MODEL_ID`. Install `requirements-optional-heavy.txt` only on a measured server suitable for that workload.
