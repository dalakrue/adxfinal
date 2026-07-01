# QUICK Field 2 Root Cause

## Confirmed causes

1. QUICK reuse previously treated `powerbi_calibrated_bundle_20260617["ok"] == True` as sufficient. A partial or stale bundle could therefore be reused even when its central path was empty, non-finite, lacked time/value columns, or belonged to a different publication identity.
2. Session history classification used the legacy `ASIA_SYDNEY` bucket while the shared selector/detector emitted distinct `SYDNEY`, `TOKYO`, `TOKYO_SYDNEY_OVERLAP`, and `TOKYO_LONDON_OVERLAP` codes. This caused valid completed-candle evidence to be missed for manual session choices.
3. The QUICK source signature omitted session mode, selected session, session-layer version, and feature version, so a manual session change could reuse a shadow payload built under another session contract.

## Repair

- QUICK reuse now requires a non-empty finite main path, valid future timestamps, an anchor price, and compatible run/generation/snapshot identity.
- The vectorized completed-candle classifier now matches the exact priority and codes of `detect_session_from_utc`.
- The source signature now includes session mode, selected session, protected hash, session-layer version, and blue24/red120 feature version.
- Protected Field 1 calculations and the protected Power BI central calculation were not edited.
