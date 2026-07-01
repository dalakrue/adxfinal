# Recommended Main Entry File

Use:

```bash
streamlit run app.py
```

`app.py` is explicitly documented as the preferred deployment entry and calls `core.app_shell.run_app()`.

`adx_dashpoard.py` is retained as a backward-compatible entry and uses the same application shell. Both were smoke-tested successfully, but Streamlit Cloud should point to **`app.py`**.
