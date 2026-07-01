from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

import core.multi_symbol_field10_20260701 as ms


def _ohlc(rows: int = 2001) -> pd.DataFrame:
    time = pd.date_range("2026-04-01", periods=rows, freq="h", tz="UTC")
    close = pd.Series(range(rows), dtype=float) / 10000 + 1.1
    return pd.DataFrame({
        "time": time,
        "open": close,
        "high": close + 0.001,
        "low": close - 0.001,
        "close": close + 0.0002,
    })


def test_required_symbols_and_alias_resolution():
    required = {"EURUSD", "USDJPY", "AUDUSD", "GBPUSD", "USDCAD", "USDCHF", "EURJPY", "GBPJPY", "EURGBP", "NZDUSD", "XAUUSD", "BTCUSD", "NAS100", "US500"}
    assert required.issubset(set(ms.SUPPORTED_SYMBOLS))
    assert ms.normalize_symbol("USTEC") == "NAS100"
    assert ms.normalize_symbol("SPX500") == "US500"
    assert ms.resolve_provider_symbol("NAS100", "mt5", ["EURUSD", "USTEC"]) == "USTEC"
    assert ms.resolve_provider_symbol("US500", "twelve", ["SPX", "NDX"]) == "SPX"


def test_grade_boundaries():
    assert ms.grade_from_score(90) == "A"
    assert ms.grade_from_score(89.99) == "B"
    assert ms.grade_from_score(75) == "B"
    assert ms.grade_from_score(60) == "C"
    assert ms.grade_from_score(59.99) == "D"


def test_more_than_2000_candles_quality_is_supported():
    state = {
        "canonical_completed_ohlc_df_20260617": _ohlc(2001),
        "canonical_decision_result_20260617": {
            "run_id": "RUN-1", "symbol": "EURUSD", "timeframe": "H1", "source_id": "SRC-1",
        },
    }
    report = ms.assess_data_quality(state, state["canonical_decision_result_20260617"])
    assert report["rows"] == 2001
    assert report["invalid_timestamps"] == 0
    assert report["duplicates"] == 0
    assert report["missing_periods"] == 0
    assert report["grade"] == "A"


def test_duplicate_and_missing_candles_are_detected():
    frame = _ohlc(700)
    frame = pd.concat([frame.drop(index=[25]), frame.iloc[[40]]], ignore_index=True)
    state = {"canonical_completed_ohlc_df_20260617": frame}
    report = ms.assess_data_quality(state, {"run_id": "R", "symbol": "EURUSD", "timeframe": "H1", "source_id": "S"})
    assert report["duplicates"] >= 1
    assert report["missing_periods"] >= 1


def test_daily_higher_result_is_immutable_before_23_and_reviewed_at_23(tmp_path: Path, monkeypatch):
    db = tmp_path / "field10.sqlite3"
    state = {"symbol": "EURUSD"}
    current = {
        "time": pd.Timestamp("2026-07-01 10:00:00", tz="UTC"),
        "regime": "BULL_NORMAL",
        "bias": "BUY",
        "quality": 92.0,
    }

    monkeypatch.setattr(ms, "_canonical", lambda _state: {
        "run_id": "RUN", "symbol": _state["symbol"], "timeframe": "H1", "source_id": "SRC",
        "latest_completed_candle_time": current["time"].isoformat(),
    })
    monkeypatch.setattr(ms, "_broker_timestamp", lambda canonical, _state: current["time"])
    monkeypatch.setattr(ms, "assess_data_quality", lambda _state, canonical=None: {
        "score": current["quality"], "grade": ms.grade_from_score(current["quality"]), "status": "PASS",
        "reasons": ["fixture"], "source_id": "SRC", "rows": 600,
    })
    monkeypatch.setattr(ms, "_daily_higher_snapshot", lambda _state, canonical: {
        "higher_regime": current["regime"], "less_risky_bias": current["bias"], "higher_reliability": 88,
        "higher_transition_risk": 12, "higher_alpha": 1, "higher_delta": 2, "sample_count": 600,
        "next_review_broker_time": "2026-07-01T23:00:00+00:00",
    })
    monkeypatch.setattr(ms, "_hourly_history", lambda _state, canonical, quality: pd.DataFrame([{
        "Broker Timestamp": current["time"], "Timeframe": "H1", "Data Quality": ms.grade_from_score(current["quality"]),
        "Data Quality Score": current["quality"], "Higher Standard Regime": current["regime"],
        "Less-Risky Bias": current["bias"], "Trust Score": 85, "Reliability": 88,
        "Validation Status": "PASS", "Quality Reason": "fixture", "Run ID": "RUN", "Source ID": "SRC",
    }]))

    def persist(parent: str):
        return ms._persist_symbol_evidence(
            state, parent_run_id=parent, child_run_id=parent + ":EURUSD", scope="QUICK",
            status={"ok": True}, elapsed=1, rss_delta_mb=1, cpu_seconds=1, path=db,
        )

    persist("P1")
    current.update(time=pd.Timestamp("2026-07-01 18:00:00", tz="UTC"), regime="BEAR_NORMAL", bias="SELL", quality=61)
    persist("P2")
    with sqlite3.connect(db) as conn:
        before = conn.execute("SELECT higher_standard_regime,less_risky_bias,data_quality_grade FROM field10_daily_higher_lock").fetchone()
    assert before == ("BULL_NORMAL", "BUY", "A")

    current.update(time=pd.Timestamp("2026-07-01 23:00:00", tz="UTC"), regime="BEAR_NORMAL", bias="SELL", quality=80)
    persist("P3")
    with sqlite3.connect(db) as conn:
        after = conn.execute("SELECT higher_standard_regime,less_risky_bias,data_quality_grade,lock_status FROM field10_daily_higher_lock").fetchone()
    assert after == ("BEAR_NORMAL", "SELL", "B", "DAY_END_REVIEW_23H")


def test_hourly_ranking_is_best_score_first(tmp_path: Path):
    db = tmp_path / "rank.sqlite3"
    ms.migrate_database(db)
    with sqlite3.connect(db) as conn:
        for symbol, quality, trust, reliability in [("EURUSD", 95, 90, 90), ("USDJPY", 70, 70, 70)]:
            conn.execute(
                """INSERT INTO field10_hourly_quality(parent_run_id,symbol,timeframe,broker_timestamp,rank,data_quality_grade,data_quality_score,higher_standard_regime,less_risky_bias,trust_score,reliability,validation_status,quality_reason,run_id,source_id,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                ("P", symbol, "H1", "2026-07-01T10:00:00+00:00", None, "A", quality, "RANGE", "WAIT", trust, reliability, "PASS", "ok", "R", "S", "now"),
            )
        conn.commit()
    ms._rank_persisted_rows("P", "2026-07-01", db)
    with sqlite3.connect(db) as conn:
        ranks = dict(conn.execute("SELECT symbol,rank FROM field10_hourly_quality").fetchall())
    assert ranks == {"EURUSD": 1, "USDJPY": 2}


def test_field10_is_integrated_and_only_one_main_run_button_remains():
    router = Path("tabs/antd_page_router_20260615.py").read_text(encoding="utf-8")
    lunch = Path("tabs/final_lunch_upgrade_20260617.py").read_text(encoding="utf-8")
    assert router.count('button(\n        "▶ Run Calculation + Open Lunch"') == 1
    assert "settings_quick_run_20260625" not in router
    assert "settings_super_quick_lunch_20260628" not in router
    assert "render_field_10" in lunch
    assert Path("lunch/field_10/renderer.py").is_file()


def test_field3_raw_middle_and_higher_tables_are_always_rendered():
    source = Path("ui/lunch_four_core_fields_20260619.py").read_text(encoding="utf-8")
    assert "_always_visible_middle_higher_history(state, canonical, details)" in source
    assert "Middle Standard Regime History — Raw Latest 25 Days" in source
    assert "Higher Standard Regime History — Raw Latest 25 Days" in source


def test_multi_symbol_runner_isolates_and_restores_saved_symbol_states(tmp_path: Path, monkeypatch):
    state = {ms.SELECTED_KEY: ["EURUSD", "USDJPY"], "timeframe": "H1"}
    calls: list[str] = []
    monkeypatch.setattr(ms, "_cache_path", lambda symbol: tmp_path / f"{symbol}.pkl.gz")
    monkeypatch.setattr(ms, "_persist_symbol_evidence", lambda state, **kwargs: {
        "symbol": state["symbol"], "status": "COMPLETED", "quality": {"grade": "A"},
        "broker_day": "2026-07-01", "run_id": f"RUN-{state['symbol']}", "source_id": f"SRC-{state['symbol']}",
    })
    monkeypatch.setattr(ms, "_rank_persisted_rows", lambda *args, **kwargs: None)
    monkeypatch.setattr(ms, "load_field10_tables", lambda *args, **kwargs: {
        "summary": pd.DataFrame(), "daily": pd.DataFrame(), "hourly": pd.DataFrame(),
    })
    import core.canonical_runtime_20260617 as canonical_runtime
    monkeypatch.setattr(canonical_runtime, "get_canonical", lambda current_state: current_state.get("canonical_decision_result_20260617") or {})

    def runner():
        symbol = state["symbol"]
        calls.append(symbol)
        state["canonical_decision_result_20260617"] = {
            "run_id": f"RUN-{symbol}", "symbol": symbol, "timeframe": "H1", "source_id": f"SRC-{symbol}",
            "latest_completed_candle_time": "2026-07-01T10:00:00+00:00",
        }
        state["canonical_completed_ohlc_df_20260617"] = _ohlc(650)
        return {"ok": True, "canonical": {"ok": True}}

    manifest = ms.run_selected_symbols(state, runner, scope="QUICK")
    assert calls == ["EURUSD", "USDJPY"]
    assert manifest["completed_symbols"] == 2
    assert (tmp_path / "EURUSD.pkl.gz").is_file()
    assert (tmp_path / "USDJPY.pkl.gz").is_file()
    assert ms.activate_symbol_result(state, "EURUSD")["ok"] is True
    assert state["canonical_decision_result_20260617"]["symbol"] == "EURUSD"
    assert ms.activate_symbol_result(state, "USDJPY")["ok"] is True
    assert state["canonical_decision_result_20260617"]["symbol"] == "USDJPY"


def test_broker_timestamp_preserves_broker_wall_hour():
    stamp = ms._broker_timestamp(
        {"broker_candle_time": "2026-07-01T23:00:00+04:00"},
        {},
    )
    assert stamp.hour == 23
    assert stamp.strftime("%Y-%m-%d") == "2026-07-01"


def test_connector_boundary_uses_provider_aliases(monkeypatch):
    import sys
    from unittest.mock import MagicMock
    streamlit_stub = MagicMock()
    streamlit_stub.session_state = {}
    monkeypatch.setitem(sys.modules, "streamlit", streamlit_stub)
    from core.connectors.data_parts.utils import _resolve_mt5_symbol, _twelve_symbol

    class FakeMT5:
        @staticmethod
        def symbol_select(name, enabled):
            return name == "USTEC"

        @staticmethod
        def symbols_get(pattern):
            return []

    resolved, ok, reason = _resolve_mt5_symbol(FakeMT5(), "NAS100")
    assert ok is True
    assert resolved == "USTEC"
    assert _twelve_symbol("US500") == "SPX"
    assert _twelve_symbol("EURJPY") == "EUR/JPY"


def test_field10_tables_publish_broker_date_session_spread_and_action_columns(tmp_path: Path):
    db = tmp_path / "enhanced.sqlite3"
    ms.migrate_database(db)
    with sqlite3.connect(db) as conn:
        conn.execute(
            """INSERT INTO multi_symbol_runs(
                parent_run_id,child_run_id,symbol,timeframe,scope,status,canonical_run_id,source_id,
                completed_candle,current_session,session_priority,average_spread,spread_quality,
                uncertainty,error_percentage,trade_permission,final_action,created_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            ("P", "P:EURUSD", "EURUSD", "H1", "QUICK", "COMPLETED", "R", "S",
             "2026-07-01T10:00:00+00:00", "LONDON", 90, 0.8, "LOW", 12, 4,
             "ALLOWED", "TRADE ALLOWED", "now"),
        )
        conn.execute(
            """INSERT INTO field10_hourly_quality(
                parent_run_id,symbol,timeframe,broker_date,broker_hour,broker_timestamp,
                data_quality_grade,data_quality_score,higher_standard_regime,less_risky_bias,
                current_session,session_priority,average_spread,spread_quality,uncertainty,
                error_percentage,trade_permission,final_action,trust_score,reliability,
                validation_status,quality_reason,run_id,source_id,created_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            ("P", "EURUSD", "H1", "2026-07-01", "10:00", "2026-07-01T10:00:00+00:00",
             "A", 94, "BULL_NORMAL", "BUY", "LONDON", 90, 0.8, "LOW", 12, 4,
             "ALLOWED", "TRADE ALLOWED", 90, 88, "PASS", "fixture", "R", "S", "now"),
        )
        conn.execute(
            """INSERT INTO field10_daily_higher_lock(
                broker_day,symbol,higher_standard_regime,less_risky_bias,
                data_quality_grade,data_quality_score,higher_reliability,current_session,
                session_priority,average_spread,spread_quality,uncertainty,error_percentage,
                trade_permission,final_action,lock_status,locked_at_broker_time,last_reviewed_broker_time,
                parent_run_id,run_id,source_id
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            ("2026-07-01", "EURUSD", "BULL_NORMAL", "BUY", "A", 94, 88,
             "LONDON", 90, 0.8, "LOW", 12, 4, "ALLOWED", "TRADE ALLOWED",
             "LOCKED_FIRST_VALID_RESULT", "2026-07-01T10:00:00+00:00",
             "2026-07-01T10:00:00+00:00", "P", "R", "S"),
        )
        conn.commit()
    ms._rank_persisted_rows("P", "2026-07-01", db)
    tables = ms.load_field10_tables({}, parent_run_id="P", symbol="EURUSD", path=db)
    required = {
        "Broker Date", "Broker Hour", "Current Session", "Session Priority", "Average Spread",
        "Spread Quality", "Uncertainty", "Error Percentage", "Trade Permission", "Final Action",
        "Rank Score", "Rank Reason",
    }
    assert required.issubset(set(tables["hourly"].columns))
    assert tables["hourly"].iloc[0]["Final Action"] == "TRADE ALLOWED"
    assert int(tables["hourly"].iloc[0]["Rank"]) == 1


def test_blocked_symbol_is_excluded_from_eligible_rank_pool(tmp_path: Path):
    db = tmp_path / "eligibility.sqlite3"
    ms.migrate_database(db)
    with sqlite3.connect(db) as conn:
        for symbol, permission, quality in [
            ("EURUSD", "ALLOWED", 85),
            ("USDJPY", "BLOCKED", 99),
        ]:
            conn.execute(
                """INSERT INTO field10_hourly_quality(
                    parent_run_id,symbol,timeframe,broker_timestamp,data_quality_grade,data_quality_score,
                    higher_standard_regime,less_risky_bias,trade_permission,trust_score,reliability,
                    validation_status,quality_reason,run_id,source_id,created_at
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                ("P", symbol, "H1", "2026-07-01T10:00:00+00:00", "A", quality,
                 "RANGE", "WAIT", permission, 90, 90, "PASS", "fixture", "R", "S", "now"),
            )
        conn.commit()
    ms._rank_persisted_rows("P", "2026-07-01", db)
    with sqlite3.connect(db) as conn:
        rows = dict(conn.execute("SELECT symbol,rank FROM field10_hourly_quality").fetchall())
        reason = conn.execute("SELECT rank_reason FROM field10_hourly_quality WHERE symbol='USDJPY'").fetchone()[0]
    assert rows["EURUSD"] == 1
    assert rows["USDJPY"] is None
    assert "UNRANKED" in reason
