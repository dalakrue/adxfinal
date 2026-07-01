# Streamlit Deployment Runtime Fix — 2026-07-02

## Fixed

- Added `cloudpickle>=3.0,<4` to the Streamlit Cloud requirements.
- Added a standard-library `pickle` fallback so Settings can still open even if `cloudpickle` is unavailable.
- Removed direct deployment-critical `cloudpickle` imports from the runtime cache and multi-symbol controller.
- Decoupled the multi-symbol selector from the calculation-mode selector.
- Made all three calculation choices permanently visible on mobile and desktop:
  1. Quick — Fields 1–9 + AI
  2. Full — Fields 1–9 + thesis + AI
  3. Super Quick — Lunch Fields 1–3
- Preserved one main `Run Calculation + Open Lunch` trigger.
- Added a safe single-symbol fallback without exposing raw dependency errors to the user.

## Deployment entry point

Use `app.py` with Python 3.12 and the root `requirements.txt`.
