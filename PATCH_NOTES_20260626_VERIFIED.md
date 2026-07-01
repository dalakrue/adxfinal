# Patch Notes — Verified Fields 1–3 Package

- Preserved all protected production hashes.
- Kept `app.py` unchanged as the deployment entry point.
- Confirmed refresh-first Quick Run orchestration and immutable same-candle reuse.
- Confirmed QUICK skips Fields 4–9, AI, NLP, Similar-Day, and Full-only research.
- Confirmed current-only copy payloads for Fields 1–3.
- Confirmed shared Auto/Manual FX-session selector in Fields 1 and 2.
- Confirmed session adjustment is additive shadow logic and does not replace the Power BI central path.
- Confirmed broker-day lock for 120-candle Middle and 600-candle Higher regimes.
- Corrected one test to inspect the actual router integration instead of a protected compatibility wrapper.
- Compile validation passed.
- 659 pytest tests passed in two batches.
- Restored test-modified databases and removed generated caches/artifacts.
