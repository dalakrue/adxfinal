# Security and Deployment Setup

## Immediate security action

An OpenRouter credential was pasted into the conversation. Treat it as exposed. Revoke it in OpenRouter and create a replacement before deployment. Do not put the replacement in Python source, screenshots, GitHub, or chat messages.

## Streamlit Secrets

Copy `.streamlit/secrets.example.toml` to the Streamlit Community Cloud Secrets editor and replace only the placeholder values:

```toml
[api_keys]
finnhub = "REPLACE_WITH_NEW_FINNHUB_KEY"
second_api = "REPLACE_WITH_TWELVE_DATA_KEY"
openrouter = "REPLACE_WITH_NEW_OPENROUTER_KEY"

[openrouter]
model = "openrouter/auto"

[automation]
auto_connect = true
auto_run_on_login = false
open_lunch_after_calculation = true
```

For local use, create `.streamlit/secrets.toml`. It is excluded by `.gitignore` and must remain uncommitted.

## OpenRouter connection behavior

- A secret key is detected automatically during Settings startup.
- It is validated once per session through the models endpoint.
- A temporary password-style field can replace it for only the current Streamlit session.
- The key is not persisted in the runtime warm cache.
- AI answers use the frozen canonical contract and bounded published history.
- Failure falls back to local deterministic evidence retrieval.

## Python version

Use Python 3.12. The included `.python-version` and `runtime.txt` both select Python 3.12.

The traceback in the original report came from Python 3.13. Base Streamlit can run there, but the project's optional AirLLM dependency is compatibility-locked below Python 3.13.

## Optional AirLLM installation on Windows

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install_airllm_windows.ps1
.\.venv-airllm\Scripts\python.exe -m streamlit run app.py
```

AirLLM is not required for OpenRouter or the built-in deterministic assistant.

## Standard Windows launch

```powershell
cd "PATH_TO_PROJECT"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Main-file answer

Use `app.py` as the preferred main file. `adx_dashpoard.py` is retained as a fully tested backward-compatible entry file.
