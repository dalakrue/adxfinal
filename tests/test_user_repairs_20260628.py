from __future__ import annotations

from pathlib import Path
import gzip

import cloudpickle
import pandas as pd


def _canonical() -> dict:
    candle = "2026-06-28T04:00:00+00:00"
    return {
        "run_id": "run-test",
        "calculation_generation": 7,
        "data_signature": "sig-test",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "source": "test",
        "latest_completed_candle_time": candle,
        "created_at": "2026-06-28T04:01:00+00:00",
        "expires_at": "2026-06-28T05:01:00+00:00",
        "schema_version": "1",
        "calculation_version": "test",
        "calculation_status": "COMPLETED",
        "market": {"latest_completed_candle_time": candle, "current_price": 1.17},
        "final_decision": {"final_decision": "BUY", "less_risky_decision": "WAIT PULLBACK"},
    }


def test_dinner_display_prunes_blank_and_single_value_columns():
    from ui.field4to9_collection_history_20260627 import compact_dinner_history_for_display

    frame = pd.DataFrame({
        "Broker Candle": pd.date_range("2026-06-01", periods=4, freq="h", tz="UTC"),
        "Production Master Decision": ["BUY", "BUY", "WAIT", "SELL"],
        "Technical Consensus": ["BUY", "BUY", "WAIT", "SELL"],
        "BUY Evidence": [2, 2, 0, 0],
        "SELL Evidence": [0, 0, 0, 2],
        "Conflict": [0, 0, 0, 0],
        "Coverage": [1, 1, 1, 1],
        "blank": [None, None, None, None],
        "one_row_only": [None, None, "x", None],
        "useful": ["a", "b", "c", "d"],
        **{f"wide_{i}": [i, i, i, i] for i in range(50)},
    })
    result = compact_dinner_history_for_display(frame, max_columns=28)
    assert "blank" not in result.columns
    assert "one_row_only" not in result.columns
    assert "useful" in result.columns
    assert len(result.columns) <= 28
    assert len(result.columns) <= (len(frame.columns) + 1) // 2


def test_medium_higher_regime_rows_become_change_intervals():
    from ui.lunch_four_core_fields_20260619 import compress_regime_change_intervals

    frame = pd.DataFrame({
        "Time": pd.date_range("2026-06-25 15:00", periods=8, freq="h", tz="UTC"),
        "Major Regime": ["BULL"] * 4 + ["BEAR"] * 3 + ["BULL"],
        "Reliability": [80, 81, 82, 83, 70, 72, 74, 65],
    })
    result = compress_regime_change_intervals(frame)
    assert len(result) == 3
    assert list(result["Major Regime"]) == ["BULL", "BEAR", "BULL"]
    assert set(result["Duration Hours"]) == {1.0, 3.0, 4.0}
    assert result.iloc[0]["Regime End"] > result.iloc[-1]["Regime End"]


def test_current_copy_excludes_previous_hour_rows_and_caps_short_at_100_lines():
    from services.current_canonical_copy_20260625 import build_current_full_payload, build_current_short_payload

    canonical = _canonical()
    times = pd.to_datetime(["2026-06-28T03:00:00Z", "2026-06-28T04:00:00Z"])
    state = {
        "canonical_decision_result_20260617": canonical,
        "full_metric_history_df_20260618": pd.DataFrame({
            "Time": times,
            "Decision": ["SELL_OLD_MARKER", "BUY"],
            "Net Pressure Decision": ["SELL", "BUY"],
        }),
    }
    short, short_stats = build_current_short_payload(state, canonical)
    full, _ = build_current_full_payload(state, canonical)
    assert short_stats.lines <= 100
    assert "SELL_OLD_MARKER" not in short
    assert "SELL_OLD_MARKER" not in full
    assert "Net Pressure Decision" in full
    assert "BUY" in full


def test_runtime_warm_cache_is_secret_free_and_restores_generation(tmp_path: Path):
    from core.runtime_state_cache_20260628 import restore_runtime_state, save_runtime_state

    cache = tmp_path / "runtime.pkl.gz"
    state = {
        "canonical_decision_result_20260617": _canonical(),
        "finnhub_api_key": "MUST_NOT_BE_STORED",
        "twelve_api_key_paste": "MUST_NOT_BE_STORED",
        "full_metric_history_df_20260618": pd.DataFrame({"Time": [pd.Timestamp("2026-06-28T04:00:00Z")], "Decision": ["BUY"]}),
    }
    report = save_runtime_state(state, status={"ok": True}, scope="FULL", path=cache)
    assert report["ok"] is True
    payload = cloudpickle.loads(gzip.decompress(cache.read_bytes()))
    serialized = repr(payload)
    assert "MUST_NOT_BE_STORED" not in serialized

    restored: dict = {}
    restore_report = restore_runtime_state(restored, path=cache)
    assert restore_report["ok"] is True
    assert restored["canonical_decision_result_20260617"]["run_id"] == "run-test"
    assert "finnhub_api_key" not in restored


def test_refresh_sync_does_not_import_or_call_settings_calculation():
    source = Path("ui/lunch_four_core_fields_20260619.py").read_text(encoding="utf-8")
    function = source.split("def _refresh_api_and_quick_sync", 1)[1].split("def render_lunch_top_copy_buttons", 1)[0]
    assert "run_settings_calculation" not in function
    assert "API_REFRESHED_AND_STAGED" in function


def test_powerbi_prefers_canonical_completed_ohlc_before_live_frames():
    source = Path("ui/powerbi_cached_renderer_20260619.py").read_text(encoding="utf-8")
    assert source.index('"canonical_completed_ohlc_df_20260617"') < source.index('"dv_pp_df"')
    assert source.index('"canonical_completed_ohlc_df_20260617"') < source.index('"last_df"')


def test_sklearn_class_mismatch_warning_is_filtered_centrally():
    source = Path("core/app/runner.py").read_text(encoding="utf-8")
    assert "y_pred contains classes not in y_true" in source
