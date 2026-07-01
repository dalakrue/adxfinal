# Router Call Graph — Before and After

## Uploaded project

```text
streamlit run app.py
  -> app.py imports adx_dashpoard.main
     -> adx_dashpoard.main imports core.app_shell.run_app
        -> core.app.runner.run_app

streamlit run adx_dashpoard.py
  -> adx_dashpoard.main
     -> core.app_shell.run_app
        -> core.app.runner.run_app
```

The two entries reached the same eventual renderer but did not have the same direct entry contract. Several page-local/legacy controls also rewrote `active_page`, including Dinner-to-Settings/Lunch mappings.

## Repaired project

```text
streamlit run app.py
  -> core.app_shell.run_app
     -> core.app.runner.run_app
        -> initialize_navigation
        -> commit_requested_page
        -> render floating menu
        -> read active_page once
        -> render exactly one page

streamlit run adx_dashpoard.py
  -> core.app_shell.run_app
     -> the identical sequence above
```

```text
Floating Dinner click
  -> request_page("Dinner")
  -> normal Streamlit rerun
  -> commit_requested_page before page rendering
  -> active_page == "Dinner"
  -> tabs.field456789_page_20260626.show
```

Lunch, Dinner, fields, expanders, charts, and research renderers do not own top-level navigation.
