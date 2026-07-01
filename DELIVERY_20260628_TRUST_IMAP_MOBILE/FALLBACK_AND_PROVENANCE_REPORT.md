# Fallback and Provenance Report

## Join/retrieval priority

1. Exact run ID, generation ID, completed broker candle, symbol and timeframe.
2. Exact completed candle from normalized published history.
3. Recalculation from stored completed OHLCV and already published features.
4. Explicit stale row only where permitted.
5. Otherwise preserve missingness and explain it.

## Permitted local fallback

The new Table 2 may derive returns, ATR, drift, forecast-error normalization, direction hits, interval coverage, pressure balance, trend persistence, rolling calibration and ranking from completed local OHLCV. These values are labelled `LOCAL FALLBACK RESEARCH` or mixed-source.

## Never fabricated

No missing broker candle, news item, M1 confirmation, external dependency, unpublished model prediction or future outcome is invented. M1 is explicitly missing in the deterministic test fixture.

## Provenance

Every history row includes run ID, generation ID, completed broker candle, symbol, timeframe, source version, source label, coverage, validation status and missingness reason.
