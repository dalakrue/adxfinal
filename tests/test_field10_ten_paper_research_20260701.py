from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from research_quant.ten_paper_validation_20260701 import (
    adwin_drift,
    bai_perron_breaks,
    build_ten_paper_validation,
    diebold_mariano,
    hamilton_regime_validation,
    kalman_local_trend,
    ledoit_wolf_risk,
)
import core.field10_ten_paper_research_20260701 as lazy
import core.multi_symbol_field10_20260701 as multi


def _state(symbol: str, seed: int = 1, rows: int = 240):
    rng = np.random.default_rng(seed)
    times = pd.date_range("2026-01-01", periods=rows, freq="h", tz="UTC")
    close = 1.10 + np.cumsum(rng.normal(0, 0.0005, rows))
    ohlc = pd.DataFrame({
        "time": times, "open": close, "high": close + 0.001,
        "low": close - 0.001, "close": close,
    })
    regime = pd.DataFrame({
        "Broker Time": times,
        "Higher Standard Regime": ["BULL_NORMAL"] * (rows // 2) + ["RANGE"] * (rows - rows // 2),
    })
    outcomes = pd.DataFrame({
        "predicted_probability": np.clip(rng.normal(0.60, 0.10, rows), 0.01, 0.99),
        "outcome": rng.binomial(1, 0.58, rows),
        "absolute_error": np.abs(rng.normal(0, 0.001, rows)),
        "production_error": rng.normal(0, 0.0012, rows),
        "candidate_error": rng.normal(0, 0.0009, rows),
        "benchmark_loss": rng.random(rows),
        "candidate_loss_a": rng.random(rows),
        "candidate_loss_b": rng.random(rows),
    })
    canonical = {
        "run_id": f"RUN-{symbol}", "symbol": symbol, "timeframe": "H1", "source_id": f"SRC-{symbol}",
        "latest_completed_candle_time": times[-1].isoformat(),
        "final_decision": {"final_decision": "BUY"}, "predicted_1h_price": float(close[-1]),
    }
    return {
        "symbol": symbol, "timeframe": "H1",
        "canonical_decision_result_20260617": canonical,
        "canonical_completed_ohlc_df_20260617": ohlc,
        "field3_regime_lifecycle_monitor_20260701": {"history_25d": regime},
        "prediction_outcomes": outcomes,
    }


def test_hamilton_probabilities_and_duration_are_bounded():
    states = ["BULL"] * 50 + ["RANGE"] * 30 + ["BULL"] * 40
    result = hamilton_regime_validation(states)
    assert result["status"] == "VALID"
    assert 0 <= result["current_regime_probability"] <= 1
    assert 0 <= result["transition_risk_6h"] <= 1
    assert result["expected_duration_hours"] > 0


def test_bai_perron_style_break_detects_large_mean_shift():
    rng = np.random.default_rng(10)
    values = np.r_[rng.normal(0, 0.1, 120), rng.normal(1.0, 0.1, 120)]
    result = bai_perron_breaks(values)
    assert result["status"] == "BREAK"
    assert result["structural_break_detected"] is True
    assert result["break_count"] >= 1


def test_adwin_and_kalman_are_incremental_and_finite():
    rng = np.random.default_rng(2)
    values = np.r_[rng.normal(0, 0.05, 80), rng.normal(0.7, 0.05, 80)]
    drift = adwin_drift(values)
    filtered = kalman_local_trend(values)
    assert drift["drift_status"] in {"WARNING", "DRIFT"}
    assert filtered["status"] == "VALID"
    assert np.isfinite(filtered["filtered_state"])
    assert 0 <= filtered["state_stability"] <= 1


def test_dm_and_ledoit_wolf_validate_candidates_without_replacing_production():
    state = _state("EURUSD")
    dm = diebold_mariano(state)
    assert dm["status"] == "VALID"
    returns = {
        "EURUSD": state["canonical_completed_ohlc_df_20260617"]["close"].pct_change(),
        "GBPUSD": state["canonical_completed_ohlc_df_20260617"]["close"].pct_change() * 0.9,
    }
    lw = ledoit_wolf_risk("EURUSD", returns)
    assert lw["status"] == "VALID"
    assert 0 <= lw["shrinkage_intensity"] <= 1


def test_complete_validation_is_shadow_only_and_identity_linked():
    state = _state("EURUSD")
    result = build_ten_paper_validation(state)
    assert result["production_action"] == "BUY"
    assert result["production_action_unchanged"] is True
    assert result["research_recommended_action"] in {
        "BUY", "SELL", "WAIT", "WAIT FOR PULLBACK", "HOLD AND PROTECT", "NO TRADE", "TRADE ALLOWED"
    }
    assert result["canonical_run_id"] == "RUN-EURUSD"
    assert result["completed_candle_time"]
    assert result["result_hash"]


def test_lazy_field10_research_calculates_only_on_explicit_ensure(tmp_path: Path, monkeypatch):
    saved = {"EURUSD": _state("EURUSD", 1), "USDJPY": _state("USDJPY", 2)}
    state = {
        multi.MANIFEST_KEY: {
            "parent_run_id": "PARENT-1", "selected_symbols": ["EURUSD", "USDJPY"],
            "active_symbol": "EURUSD",
        },
        multi.SELECTED_KEY: ["EURUSD", "USDJPY"],
    }
    monkeypatch.setattr(lazy, "_saved_state", lambda symbol: saved.get(symbol))
    db = tmp_path / "research.sqlite3"
    first = lazy.ensure_field10_research_validation(state, path=db)
    second = lazy.ensure_field10_research_validation(state, path=db)
    tables = lazy.load_field10_research_tables(state, parent_run_id="PARENT-1", symbol="EURUSD", path=db)
    registries = lazy.load_research_registries(parent_run_id="PARENT-1", path=db)
    assert first["calculated_symbols"] == 2
    assert second["status"] == "CACHED"
    assert second["calculated_symbols"] == 0
    assert len(tables["current"]) == 2
    assert tables["current"]["Research Rank"].notna().all()
    assert len(registries["models"]) >= 1
    assert len(registries["experiments"]) == 2



def test_research_identity_preserves_broker_wall_clock():
    state = _state("EURUSD")
    state["canonical_decision_result_20260617"]["latest_completed_candle_time"] = "2026-07-01T23:00:00+04:00"
    result = build_ten_paper_validation(state)
    assert result["broker_date"] == "2026-07-01"
    assert result["broker_hour"] == 23
    assert result["completed_candle_time"].startswith("2026-07-01T23:00:00")

def test_field10_is_inside_authoritative_lunch_selector_and_not_bottom_toggle():
    source = Path("ui/lunch_four_core_fields_20260619.py").read_text(encoding="utf-8")
    wrapper = Path("tabs/final_lunch_upgrade_20260617.py").read_text(encoding="utf-8")
    assert "FIELD10_FIELD" in source
    assert "FIELD_LABELS = (\n    FULL_METRIC_FIELD, POWERBI_FIELD, REGIME_FIELD, FIELD10_FIELD" in source
    assert "elif selected_field == FIELD10_FIELD" in source
    assert "render_field10_content(state)" in source
    assert "render_field_10(st.session_state)" not in wrapper
