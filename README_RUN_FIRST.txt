ADX Quant Pro — Super Quick + Multi-Selector Fixed Release (2026-07-22)

Windows launch:
1. Extract this ZIP.
2. Open Command Prompt in the extracted folder.
3. Install dependencies once:
   python -m pip install -r requirements.txt
4. Start the app:
   streamlit run app.py

Recommended workflow:
1. Open Settings and choose H4 (or your required timeframe).
2. Select symbols in any one, two, or all three selectors.
3. Click the corresponding selector load button, or Load All Selected (Top 20).
4. Successful symbols remain loaded even if a different symbol/provider fails.
5. Click Super Quick for only:
   - Regime Age Ranking — Candle After Regime Start Only
   - Higher Standard Summary
6. Click Quick for all deferred calculations and other sections.

Important:
- Super Quick makes zero new market API requests. It uses validated candles that
  were already loaded in Settings.
- Rank 1 in Regime Age Ranking means the most recent regime start (smallest
  Candle After Regime Start value), not the oldest regime.
