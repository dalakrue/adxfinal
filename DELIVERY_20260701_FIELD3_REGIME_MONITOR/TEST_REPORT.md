# Test Report

## Dedicated monitor tests

Command:

```powershell
python -m pytest -q tests/test_field3_regime_lifecycle_monitor_20260701.py
```

Result: **8 passed**.

Coverage includes:

- canonical identity and first-14-column order;
- required institutional schema;
- normalized full probability vector;
- separate trust components;
- chronological maturity-aware calibration metadata;
- 25-day daily validation schema;
- completed-candle and broker-time consistency;
- critical OHLC data-quality blocking;
- compressed SQLite round trip;
- cache reuse for an unchanged generation.

## Complete project regression suite

The inspection container does not include the Streamlit runtime package. A temporary import-compatible Streamlit test stub was used only to allow the existing unit modules to import; it was not added to the project or delivery.

Command:

```powershell
$env:PYTHONPATH="<temporary-streamlit-test-stub>;$PWD"
python -m pytest -q
```

Result: **175 passed**.

## Compile and static checks

- Changed Python modules compile successfully.
- No `datetime.now()`, `datetime.utcnow()` or `Timestamp.now()` is used by the new canonical monitor, store or renderer.
- The Lunch renderer contains no `.fit()` or training calls.
- No secret/API key fields were added to logs, tables or exports.
- No project file was deleted.

## Synthetic canonical run/render test

A 760-completed-H1 synthetic EURUSD run produced:

- status: `AVAILABLE`;
- main history: 600 rows;
- daily summary: 25 rows;
- timeline: 600 rows;
- regime calibration: anchored walk-forward isotonic;
- 3H switch calibration: anchored walk-forward isotonic;
- read-only Field 3 render: successful.

## Deployment validation still required

Real-provider validation must be performed after deployment with the project’s actual broker/API records. In particular, confirm provider spread units, real broker-time offset/session configuration and mature episode sample counts. The monitor fails safely and marks unavailable or low-sample evidence rather than fabricating values.
