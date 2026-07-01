# Performance Before/After
V19 publishes once per Settings run and all requested renderers consume the saved compact sidecar. It reuses one outcome history and the saved V17 evidence, performs no model fitting during normal reruns, and retains no fitted heavy objects in session state.

A matched before/after production benchmark was not possible without the user's live connector data and Streamlit runtime. Therefore no unsupported percentage reduction is claimed. See `PERFORMANCE_BEFORE_AFTER_V19_20260624.json` for the local deterministic evaluation benchmark.
