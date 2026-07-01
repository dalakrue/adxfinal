# Exact Test Commands

```bash
python -m compileall -q .
python - <<'PY'
# imported all 14 V14/integration modules; see IMPORT_SMOKE_OUTPUT_V14_20260623.txt
PY
pytest -q tests/test_lunch_v13_requested_fixes_20260623.py tests/test_quant_research_v14_20260623.py --disable-warnings
```

Observed output: `23 passed in 2.62s`. Dedicated V14 suite: `8 passed in 0.21s`.
