# Known Limitations

- Live Streamlit smoke launch and mobile-width browser rendering were not executable in the packaging container because Streamlit/browser tooling was absent.
- No trading-accuracy uplift is claimed. Session-shadow calibration requires matured out-of-sample outcomes for meaningful accuracy/coverage comparison.
- Existing legacy/inactive copy controls remain in legacy modules to avoid deleting potentially protected UI history; active Lunch controls use the current-only canonical exporter.
- Full production before/after timing requires the same connector data, secrets, and deployment runtime.
