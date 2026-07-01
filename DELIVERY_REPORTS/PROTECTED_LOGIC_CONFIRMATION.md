# Protected logic confirmation

- Verified protected-file hashes unchanged from the actual uploaded ZIP: **10/10**.
- No database file, prediction ledger, historical outcome store, model artifact, or persistence file differs from the upload.
- `app.py` remains the deployment entry point and is unchanged.
- The protected canonical runtime, canonical sync V9, decision product engine, Full Metric canonical adapter, and `lunch/field_01` protected files were not edited.
- No BUY/SELL/WAIT/HOLD/NO-TRADE threshold, Power BI central-path formula, regime formula, model weight, TP/SL calculation, or broker-time calculation was changed.
- Power BI renderer changes are identity lookup/display-only; the original protected path and session-conditioned shadow engine remain separate.
- Table 4 and AirLLM are display/assistant layers only and do not write production decisions or weights.

See `PROTECTED_LOGIC_HASH_VERIFICATION.json` for per-file SHA-256 evidence and `CHANGED_FILE_MANIFEST.json` for every modified/added source file.
