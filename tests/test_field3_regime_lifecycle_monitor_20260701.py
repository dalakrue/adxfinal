from __future__ import annotations

import sqlite3

import numpy as np
import pandas as pd
import pytest

from core.field3_regime_lifecycle_monitor_20260701 import (
    FIRST_14_COLUMNS,
    REGIMES,
    STATE_KEY,
    _data_quality,
    build_field3_regime_lifecycle_monitor,
)
from core.field3_regime_lifecycle_store_20260701 import load, save


@pytest.fixture(scope="module")
def monitor_bundle():
    n = 900
    rng = np.random.default_rng(20260701)
    times = pd.date_range("2026-04-01", periods=n, freq="h", tz="UTC")
    drift = np.zeros(n)
    drift[180:390] = 0.000035
    drift[390:590] = -0.000045
    volatility = np.full(n, 0.00018)
    volatility[590:710] = 0.00007
    volatility[710:830] = 0.00042
    returns = rng.normal(drift, volatility)
    close = 1.12 * np.exp(np.cumsum(returns))
    open_ = np.r_[close[0], close[:-1]]
    span = np.maximum(np.abs(close-open_), rng.uniform(0.00008, 0.00030, n))
    frame = pd.DataFrame({
        "time": times,
        "open": open_,
        "high": np.maximum(open_, close) + span * 0.65,
        "low": np.minimum(open_, close) - span * 0.65,
        "close": close,
        "spread": rng.uniform(0.00005, 0.00013, n),
        "volume": rng.integers(100, 1000, n),
    })
    snapshot = {
        "run_id": "FIELD3-TEST-RUN",
        "generation_id": "9",
        "source_snapshot_hash": "field3-test-hash",
        "snapshot_hash": "field3-test-hash",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "broker_candle_time": times[-1],
        "regime": "RANGE",
        "decision": "WAIT",
        "less_risky_decision": "WAIT",
    }
    state = {
        "canonical_completed_ohlc_df_20260617": frame,
        "canonical_result_20260617": snapshot,
        "manual_broker_utc_offset_hours_20260622": 2,
    }
    payload = build_field3_regime_lifecycle_monitor(snapshot, state, force=True)
    return payload, state, frame, snapshot


def test_monitor_keeps_required_identity_and_first_14_columns(monitor_bundle):
    payload, state, frame, snapshot = monitor_bundle
    assert payload["status"] == "AVAILABLE"
    assert payload["run_id"] == snapshot["run_id"]
    assert payload["snapshot_hash"] == snapshot["snapshot_hash"]
    assert payload["protected_regime_calculations_changed"] is False
    assert payload["production_decision_changed"] is False
    assert len(payload["history_25d"]) == 600
    assert list(payload["history_25d"][0])[:14] == FIRST_14_COLUMNS
    required = {
        "Existing KNN Priority", "Existing Greedy Priority", "Existing Score Out of 10",
        "Switch Probability Within 1H", "Switch Probability Within 3H", "Switch Probability Within 6H",
        "Model Disagreement Score", "Calibration Quality Score", "Final Action", "Invalidation Reason",
        "P(Net Positive 1H)", "P(Net Negative 3H)", "P(WAIT/Cost Zone 6H)",
    }
    assert required.issubset(payload["history_25d"][0])
    assert state[STATE_KEY]["cache_key"] == payload["cache_key"]


def test_full_probability_vector_is_retained_and_normalized(monitor_bundle):
    payload, *_ = monitor_bundle
    vector = payload["full_state_probability_vector"]
    assert set(vector) == set(REGIMES)
    assert sum(vector.values()) == pytest.approx(1.0, abs=1e-9)
    current = payload["current"]
    assert current["final_action"] in {"TRADE", "REDUCE", "WAIT", "BLOCK"}
    assert 0 <= current["selected_regime_posterior"] <= 0.99
    assert 0 <= current["change_point_probability"] <= 1
    assert {"model_agreement", "calibration_quality", "duration_confidence", "drift_risk"}.issubset(current)


def test_calibration_is_chronological_and_maturity_aware(monitor_bundle):
    payload, *_ = monitor_bundle
    regime = payload["calibration"]["regime_posterior"]
    assert regime["same_fit_sample"] is False
    assert regime["smoothed_probabilities_used_for_fit"] is False
    assert regime["label_maturity_hours"] == 3
    for horizon in ("H1", "H3", "H6"):
        item = payload["calibration"]["switch_probability"][horizon]
        assert item["same_fit_sample"] is False
        assert item["label_maturity_hours"] == int(horizon[1:])


def test_daily_summary_retains_requested_validation_schema(monitor_bundle):
    payload, *_ = monitor_bundle
    assert payload["daily_25d"]
    columns = set(payload["daily_25d"][0])
    assert {
        "Duration Prediction MAE", "50% Interval Coverage", "80% Interval Coverage",
        "Brier Score", "Multiclass Log Loss", "Expected Calibration Error",
        "False Switches", "Missed PELT Boundaries", "Best Session", "Worst Session",
    }.issubset(columns)


def test_completed_candle_and_broker_time_are_consistent(monitor_bundle):
    payload, _, frame, _ = monitor_bundle
    rows = pd.DataFrame(payload["history_25d"])
    event_time = pd.to_datetime(rows["event_time_utc"], utc=True)
    assert event_time.max() <= frame["time"].max()
    assert event_time.is_monotonic_decreasing
    assert rows["Run ID"].nunique() == 1
    assert rows["Snapshot Hash"].nunique() == 1
    assert rows["Broker Candle Time"].notna().all()


def test_critical_data_quality_blocks_invalid_ohlc():
    times = pd.date_range("2026-06-01", periods=500, freq="h", tz="UTC")
    frame = pd.DataFrame({
        "time": times,
        "open": 1.1,
        "high": 1.0,  # invalid: high below open/close
        "low": 1.2,   # invalid: low above open/close
        "close": 1.1,
    })
    report = _data_quality(frame, {"cutoff_utc": times[-1].isoformat(), "broker_clock_available": True}, {})
    assert report["critical"] is True
    assert report["status"] == "INVALID"
    assert any("invalid_ohlc" in reason for reason in report["reasons"])


def test_sqlite_store_roundtrip(monitor_bundle):
    payload, *_ = monitor_bundle
    with sqlite3.connect(":memory:") as conn:
        result = save(conn, payload)
        restored = load(conn, run_id=payload["run_id"], snapshot_hash=payload["snapshot_hash"])
    assert result["ok"] is True
    assert restored is not None
    assert restored["cache_key"] == payload["cache_key"]
    assert restored["current"]["current_canonical_regime"] == payload["current"]["current_canonical_regime"]


def test_repeated_build_reuses_exact_completed_generation(monitor_bundle):
    payload, state, _, snapshot = monitor_bundle
    reused = build_field3_regime_lifecycle_monitor(snapshot, state, force=False)
    assert reused["cache_key"] == payload["cache_key"]
    assert reused["performance"] == payload["performance"]
