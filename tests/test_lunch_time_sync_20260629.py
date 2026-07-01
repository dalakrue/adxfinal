import pandas as pd

from core.shared_broker_time_20260622 import (
    frame_to_shared_broker_clock,
    shared_broker_time_provider,
)


def test_fresh_loaded_h1_overrides_stale_restored_canonical_clock():
    state = {
        "last_df": pd.DataFrame({
            "time": pd.date_range("2026-06-28 16:00", periods=5, freq="h", tz="UTC"),
            "close": [1.0, 1.1, 1.2, 1.3, 1.4],
        }),
        "manual_broker_utc_offset_hours_20260622": 0,
    }
    stale = {"latest_completed_candle_time": "2026-06-17T15:00:00Z", "run_id": "old"}
    contract = shared_broker_time_provider(state, canonical=stale)
    assert contract["latest_completed_h1_utc"] == "2026-06-28T20:00:00+00:00"
    assert contract["broker_date"] == "2026-06-28"
    assert contract["broker_hour"] == "20:00"
    assert contract["timestamp_source"].startswith("freshest_loaded_candle")


def test_all_visible_date_hour_columns_are_rebuilt_from_same_broker_timestamp():
    state = {
        "last_df": pd.DataFrame({
            "time": pd.date_range("2026-06-28 19:00", periods=2, freq="h", tz="UTC"),
            "close": [1.0, 1.1],
        }),
        "manual_broker_utc_offset_hours_20260622": 0,
    }
    stale = {"latest_completed_candle_time": "2026-06-17T15:00:00Z"}
    frame = pd.DataFrame({
        "time": pd.date_range("2026-06-28 19:00", periods=2, freq="h", tz="UTC"),
        "Date": ["2026-06-17", "2026-06-17"],
        "Hour": ["15:00", "18:00"],
    })
    shown = frame_to_shared_broker_clock(frame, state, canonical=stale)
    assert shown.iloc[-1]["Date"] == "2026-06-28"
    assert shown.iloc[-1]["Hour"] == "20:00"


def test_display_frame_itself_overrides_stale_canonical_without_last_df():
    state = {"manual_broker_utc_offset_hours_20260622": 3}
    stale = {"latest_completed_candle_time": "2026-06-17T15:00:00Z"}
    frame = pd.DataFrame({
        "Completed Broker Candle": ["2026-06-28T16:00:00Z", "2026-06-28T17:00:00Z"],
        "Date": ["2026-06-17", "2026-06-17"],
        "Hour": ["15:00", "18:00"],
    })
    shown = frame_to_shared_broker_clock(frame, state, canonical=stale)
    broker_col = next(column for column in shown.columns if str(column).startswith("Broker Time"))
    assert shown.iloc[-1][broker_col] == pd.Timestamp("2026-06-28 20:00:00")
    assert shown.iloc[-1]["Date"] == "2026-06-28"
    assert shown.iloc[-1]["Hour"] == "20:00"


def test_repeated_projection_cannot_leave_stale_date_or_hour_aliases():
    state = {"manual_broker_utc_offset_hours_20260622": 2}
    canonical = {"latest_completed_candle_time": "2026-06-28T18:00:00Z"}
    source = pd.DataFrame({
        "Broker Candle Time": ["2026-06-28T18:00:00Z"],
        "Date": ["2026-06-17"],
        "Weekday": ["Wednesday"],
        "Hour": ["15:00"],
    })
    once = frame_to_shared_broker_clock(source, state, canonical=canonical)
    twice = frame_to_shared_broker_clock(once, state, canonical=canonical)
    assert twice.loc[0, "Date"] == "2026-06-28"
    assert twice.loc[0, "Weekday"] == "Sunday"
    assert twice.loc[0, "Hour"] == "20:00"


def test_powerbi_plot_axis_uses_same_broker_hour_as_field1():
    from ui.powerbi_cached_renderer_20260619 import _plot_clock

    state = {
        "manual_broker_utc_offset_hours_20260622": 3,
        "last_df": pd.DataFrame({
            "time": [pd.Timestamp("2026-06-28T17:00:00Z")],
            "close": [1.17],
        }),
    }
    projected = _plot_clock(pd.Series([pd.Timestamp("2026-06-28T17:00:00Z")]), state)
    assert projected.iloc[0] == pd.Timestamp("2026-06-28 20:00:00")


def test_powerbi_history_table_rebuilds_stale_visible_aliases():
    from ui.powerbi_cached_renderer_20260619 import _broker_display_table

    state = {"manual_broker_utc_offset_hours_20260622": 3}
    canonical = {"latest_completed_candle_time": "2026-06-28T17:00:00Z"}
    history = pd.DataFrame({
        "target_time": ["2026-06-28T17:00:00Z"],
        "Date": ["2026-06-17"],
        "Hour": ["15:00"],
        "prediction": [1.17],
    })
    shown = _broker_display_table(history, state, canonical)
    assert shown.loc[0, "Date"] == "2026-06-28"
    assert shown.loc[0, "Hour"] == "20:00"
