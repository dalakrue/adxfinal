# Known limitations

- Exact dependency installation and imports were verified in this container on Python 3.13.5, not Python 3.12; deployment is correctly pinned to 3.12 and must rerun the same commands there.
- Synthetic history tests do not establish trading profitability or production promotion eligibility.
- Real Brier score, log loss, calibration slope, expectancy, drawdown, interval coverage and false-direction evidence require genuine settled observations.
- Missing source fields remain `N/A`; the repair intentionally does not fabricate them.
- MT5-specific Windows connectivity cannot be exercised in this Linux inspection environment.
