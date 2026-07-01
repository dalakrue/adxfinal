# Regime Limitations

- The implementation is a practical bounded adaptation, not an exact reproduction of every cited academic estimator.
- Historical rows do not backfill unavailable point-in-time posterior values; they display N/A rather than fabricate evidence.
- Cross-market confirmation degrades gracefully because external market APIs were unavailable offline.
- Dynamic ensemble weights currently use bounded scale weights until enough settled walk-forward model-loss history is available.
- No claim of improved trading profitability or forecast accuracy is made without out-of-sample production evidence.
- The full repository test suite timed out at 56%; targeted affected and existing regime suites passed completely.
