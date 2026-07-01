# Evidence — Field 1 Cross-Table Identity and Completed H1

Field 1 normalization uses `event_time_utc` as its authoritative timestamp, accepts timezone-aware normalized UTC values, removes invalid times, rejects rows after the canonical completed-H1 watermark, rejects duplicate event identities, sorts chronologically for validation, detects unexpected H1 gaps and finally presents newest-first data.

Visible Date, Hour and Weekday are rebuilt only after conversion through `core/shared_broker_time_20260622.py`. UTC remains available to the audit contract. `validate_field1_identity()` checks latest timestamp, calculation ID, generation, symbol, timeframe, broker offset, broker-time contract version and data-quality PASS. The UI says SYNCED only when every check passes and never fabricates a current row.

A synthetic integrated publication test used calculation ID `CALC-8`, generation `8`, EURUSD/H1 and the same completed H1 for canonical and Field 1. It passed with `field1_sync.status == SYNCED`, raw paths preserved and production influence false. Separate tests proved generation mismatch becomes NOT SYNCED and future/duplicate rows cannot produce PASS.
