# Recommended Main Entry File

Use `app.py`.

```powershell
streamlit run app.py
```

Reasons:

- Its module docstring explicitly identifies it as the preferred deployment entry.
- It installs Windows asyncio compatibility before Streamlit/Tornado startup.
- It calls the shared `core.app_shell.run_app` application shell directly.
- It passed the final Streamlit health smoke test.

`adx_dashpoard.py` remains supported for backward compatibility and also passed the smoke test, but new local and cloud deployments should select `app.py`.
