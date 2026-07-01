# Deployment Runtime and Three-Mode Run Fix

## User-visible issue repaired

The Settings page no longer loses the multi-symbol selector and calculation-mode controls when `cloudpickle` is unavailable. The raw deployment warning `No module named 'cloudpickle'` is prevented by both an explicit dependency and a standard-library fallback.

## Run calculation choices

Settings now always shows exactly three choices before the single run button:

1. Quick — Fields 1–9 + AI
2. Full — Fields 1–9 + thesis + AI
3. Super Quick — Lunch Fields 1–3

The choices are vertical so they remain readable on a phone. The main action remains one button: `Run Calculation + Open Lunch`.

## End-to-end resilience

- The multi-symbol selector and the three-mode selector render independently.
- A failure in the optional advanced selector cannot hide the calculation modes.
- A failure importing the multi-symbol controller falls back to running the active symbol rather than aborting the main calculation button.
- Runtime cache serialization prefers `cloudpickle` and safely falls back to standard `pickle`.
- `cloudpickle>=3.0,<4` is explicitly present in deployment requirements.
- The Latest Candle metric shows `Waiting for connected data` instead of a misleading green `No timestamp` delta before a feed is connected.
- Preferred Streamlit Cloud entry point remains `app.py` on Python 3.12.

## Verification completed

- Python compile check: passed.
- Full project test suite: **200 passed**.
- Local Streamlit health endpoint: **OK** on `app.py`.
- Startup log contained no `cloudpickle` error.

## Live deployment note

The package was validated locally in a Streamlit server. The actual Streamlit Cloud deployment still needs to rebuild from the updated root `requirements.txt` so the dependency layer is refreshed.
