from __future__ import annotations

import numpy as np
import pandas as pd

from core.buy_sell_frequency_20260629 import enrich_bfd_sfd
from core.field2_quant_upgrade_20260629 import build_field2_quant_upgrade
from core.symbol_universe_20260629 import (
    EQUITY_SYMBOLS,
    FX_SYMBOLS,
    all_library_symbols,
    apply_symbol_selection,
    normalize_instrument,
)
from ui.dinner_research_history_upgrade_20260629 import build_research_history_view
from ui.lunch_four_core_fields_20260619 import compress_regime_change_intervals


def _ohlc(rows: int = 24 * 40) -> pd.DataFrame:
    rng = np.random.default_rng(29)
    returns = rng.normal(0.0, 0.00055, rows)
    close = 1.085 * np.exp(np.cumsum(returns))
    open_ = np.r_[close[0], close[:-1]]
    high = np.maximum(open_, close) * (1 + rng.uniform(0.0001, 0.0009, rows))
    low = np.minimum(open_, close) * (1 - rng.uniform(0.0001, 0.0009, rows))
    # Final candle is a clear bullish resistance breakout with a much larger body.
    open_[-1] = close[-2] * 0.999
    close[-1] = float(np.max(high[-22:-1])) * 1.003
    high[-1] = close[-1] * 1.001
    low[-1] = open_[-1] * 0.999
    return pd.DataFrame(
        {
            "time": pd.date_range("2026-05-01", periods=rows, freq="h", tz="UTC"),
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": rng.integers(100, 5000, rows),
        }
    )


def test_symbol_universe_and_global_state() -> None:
    assert len(FX_SYMBOLS) == 20
    assert len(EQUITY_SYMBOLS) == 20
    assert "SPX" in all_library_symbols()
    assert len(all_library_symbols()) >= 41
    assert normalize_instrument("S&P 500") == "SPX"
    assert normalize_instrument("eur/usd") == "EURUSD"
    state = {"symbol": "EURUSD"}
    result = apply_symbol_selection(state, "XAUUSD")
    assert result["changed"] is True
    assert state["symbol"] == state["selected_symbol"] == state["ws_symbol"] == "XAUUSD"
    assert state["selected_symbol_pending_run_20260629"] is True


def test_bfd_sfd_outputs_only_required_states() -> None:
    frame = pd.DataFrame(
        {
            "Hour": ["12", "11", "10", "09"],
            "Decision": ["BUY", "BUY", "SELL", "WAIT"],
            "BUY /10": [9.0, 8.0, 2.0, 5.0],
            "SELL /10": [1.0, 2.0, 9.0, 5.0],
            "Master Decision": ["BUY", "BUY", "SELL", "WAIT"],
        }
    )
    result = enrich_bfd_sfd(frame)
    allowed = {"Wait Pullback", "Hold and Protect", "Allowed", "No Trade"}
    assert set(result["BFD"]).issubset(allowed)
    assert set(result["SFD"]).issubset(allowed)
    assert {"BFD", "SFD"}.issubset(result.columns)


def test_field2_breakout_dynamic_bands_relationships_and_dtw() -> None:
    frame = _ohlc()
    state = {
        "last_df": frame,
        "symbol": "XAUUSD",
        "timeframe": "H1",
        "canonical_result_20260617": {
            "symbol": "XAUUSD",
            "timeframe": "H1",
            "run_id": "test-run",
            "generation_id": "test-generation",
            "latest_completed_candle_time": frame["time"].iloc[-1],
        },
    }
    result = build_field2_quant_upgrade(state, force=True)
    assert result["ok"] is True
    assert result["symbol"] == "XAUUSD"
    assert result["breakout"]["probability"] > 50
    path = result["prediction_path"]
    assert len(path) == 6
    assert (path["Dynamic Upper Band"] > path["Central Tendency"]).all()
    assert (path["Central Tendency"] > path["Dynamic Lower Band"]).all()
    assert path["Band Expansion Factor"].min() > 1
    relationships = result["relationship_history"]
    assert not relationships.empty
    assert {
        "Relationship Trust Score",
        "Absorb or Not",
        "Definitive Decision",
    }.issubset(relationships.columns)
    assert "buy_sell_relationship_ratio" in result["relationship_summary"]
    assert result["similar_day"]["ok"] is True
    assert result["similar_day"]["historical_open"] > 0
    assert result["similar_day"]["subsequent_close"] > 0


def test_regime_history_is_compressed_to_intervals() -> None:
    frame = pd.DataFrame(
        {
            "Broker Candle Time": pd.date_range("2026-06-01", periods=8, freq="h", tz="UTC"),
            "Regime": ["RANGE", "RANGE", "RANGE", "TREND", "TREND", "RANGE", "RANGE", "RANGE"],
            "Bias": ["WAIT", "WAIT", "WAIT", "BUY", "BUY", "WAIT", "WAIT", "WAIT"],
            "Reliability": [60, 61, 62, 75, 77, 64, 65, 66],
        }
    )
    result = compress_regime_change_intervals(frame)
    assert len(result) == 3
    assert {"Regime Start", "Regime End"}.issubset(result.columns)


def test_dinner_research_history_deduplicates_and_scores() -> None:
    times = pd.date_range("2026-06-20", periods=6, freq="h", tz="UTC")
    history = pd.DataFrame(
        {
            "Broker Candle Time": list(times) + [times[-1]],
            "Final Decision": ["BUY", "BUY", "WAIT", "SELL", "SELL", "WAIT", "WAIT"],
            "Research Reliability": [80, 82, 70, 65, 90, 55, 55],
            "Coverage": [90, 88, 80, 70, 95, 60, 60],
            "Conflict": [10, 12, 20, 30, 5, 45, 45],
            "Field 9 Decision Score": [7, 8, 6, 5, 9, 4, 4],
        }
    )
    view, summary = build_research_history_view(history)
    assert len(view) == 6
    assert summary["rows"] == 6
    assert "Evidence Status" in view.columns
    assert "Research Reliability %" in view.columns
