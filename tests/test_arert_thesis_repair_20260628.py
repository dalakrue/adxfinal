from __future__ import annotations

import math
from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd

from core.time_safe_frame_20260628 import safe_sort_by_time
from research_quant.arert_lab import (
    MODULE_CATALOG,
    STATE_KEY,
    _expand_modules,
    build_context,
    run_arert_research,
)
from research_quant.arert_store import migrate_arert_database, persist_arert_envelope, table_counts
from services.current_canonical_copy_20260625 import _current_rows
from ui.field4to9_collection_history_20260627 import _add_protective_action_columns
from ui.lunch_next_hour_bias_history_20260626 import (
    _coalesce_table1_frames,
    _protective_display_action,
)


def _synthetic_context(n: int = 720):
    idx = pd.date_range("2026-05-01", periods=n, freq="h", tz="UTC")
    rng = np.random.default_rng(28)
    returns = rng.normal(0.0, 0.00055, n) + np.sin(np.arange(n) / 70.0) * 0.00008
    close = 1.15 * np.cumprod(1.0 + returns)
    open_ = np.r_[close[0], close[:-1]]
    ohlc = pd.DataFrame(
        {
            "Time": idx,
            "Open": open_,
            "High": np.maximum(open_, close) + rng.uniform(0.00005, 0.00035, n),
            "Low": np.minimum(open_, close) - rng.uniform(0.00005, 0.00035, n),
            "Close": close,
            "Volume": rng.integers(100, 2000, n),
        }
    )
    direction = np.where(pd.Series(returns).rolling(5, min_periods=1).mean() >= 0, "BUY", "SELL")
    decisions = pd.DataFrame(
        {
            "Broker Candle Time": idx,
            "Master Decision": direction,
            "Technical Bias": direction,
            "Pressure Decision": np.where(returns >= 0, "BUY", "SELL"),
            "Hold Safety Decision": np.where(np.abs(returns) < 0.00035, "WAIT FOR PULLBACK", "HOLD & PROTECT"),
        }
    )
    news_idx = idx[::8]
    news = pd.DataFrame(
        {
            "Time": news_idx,
            "Title": [f"event-{i}" for i in range(len(news_idx))],
            "Sentiment": rng.uniform(-1, 1, len(news_idx)),
            "Impact": rng.uniform(0, 100, len(news_idx)),
        }
    )
    canonical = {
        "run_id": "run-test",
        "generation_id": "generation-test",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "completed_broker_candle": idx[-1],
        "ohlc_df": ohlc,
        "snapshot_hash": "snapshot-test",
        "final_decision": {"final_decision": "BUY", "confidence": 72.0},
    }
    state = {
        "field1_table1_decision_history_20260628": decisions,
        "finnhub_ranked_news_20260626": news,
    }
    return state, canonical


def test_mixed_string_timestamp_sort_no_type_error():
    frame = pd.DataFrame(
        {
            "Broker Time": ["2026-06-01 01:00:00+00:00", pd.Timestamp("2026-06-01 03:00", tz="UTC"), "bad", pd.Timestamp("2026-06-01 02:00")],
            "value": [1, 3, 0, 2],
        }
    )
    result = safe_sort_by_time(frame, column="Broker Time", ascending=False)
    assert result["value"].tolist() == [3, 2, 1, 0]


def test_table1_coalescing_fills_only_blank_cells():
    t = pd.Timestamp("2026-06-28 10:00", tz="UTC")
    visible = pd.DataFrame({"Broker Candle Time": [t], "Master Decision": ["BUY"], "Pressure Decision": [pd.NA]})
    older = pd.DataFrame({"Broker Candle Time": [t], "Master Decision": ["SELL"], "Pressure Decision": ["WAIT"]})
    merged = _coalesce_table1_frames([visible, older])
    assert merged.loc[0, "Master Decision"] == "BUY"
    assert merged.loc[0, "Pressure Decision"] == "WAIT"


def test_protective_display_is_additive_not_directional():
    assert _protective_display_action("BUY") == "HOLD & PROTECT"
    assert _protective_display_action("SELL") == "HOLD & PROTECT"
    assert _protective_display_action("WAIT") == "WAIT FOR PULLBACK"
    assert _protective_display_action("WAIT FOR PULLBACK") == "WAIT FOR PULLBACK"


def test_dinner_adds_exactly_twenty_protective_columns_and_preserves_raw():
    frame = pd.DataFrame(
        {
            "Broker Candle Time": [pd.Timestamp("2026-06-28 10:00", tz="UTC")],
            "Field 4 Bias": ["BUY"],
            "Field 4 Decision": ["SELL"],
            "Production Master Decision": ["WAIT"],
            "Technical Consensus": ["BUY"],
        }
    )
    output = _add_protective_action_columns(frame)
    actions = [c for c in output.columns if c.startswith("Action ")]
    assert len(actions) == 20
    assert output.loc[0, "Field 4 Bias"] == "BUY"
    populated = output[actions].stack().dropna().astype(str)
    assert set(populated).issubset({"HOLD & PROTECT", "WAIT FOR PULLBACK"})


def test_current_copy_rejects_stale_rows():
    frame = pd.DataFrame({"Time": [pd.Timestamp("2026-06-28 09:00", tz="UTC")], "Decision": ["BUY"]})
    assert _current_rows(frame, target_candle=pd.Timestamp("2026-06-28 10:00", tz="UTC")) == []


def test_arert_context_prevents_future_rows():
    state, canonical = _synthetic_context(200)
    future = pd.Timestamp(canonical["completed_broker_candle"]) + pd.Timedelta(hours=1)
    state["field1_table1_decision_history_20260628"] = pd.concat(
        [state["field1_table1_decision_history_20260628"], pd.DataFrame({"Broker Candle Time": [future], "Master Decision": ["SELL"]})],
        ignore_index=True,
    )
    context = build_context(state, canonical)
    assert context.market["time"].max() <= canonical["completed_broker_candle"]
    assert context.decisions["time"].max() <= canonical["completed_broker_candle"]
    assert context.news.empty or context.news["time"].max() <= canonical["completed_broker_candle"]


def test_arert_dependency_expansion_for_final_score():
    selected = _expand_modules([20])
    assert 20 in selected
    assert {1, 5, 7, 9, 11, 13, 14, 16, 18, 19}.issubset(selected)


def test_arert_all_modules_safe_and_core_invariants(tmp_path, monkeypatch):
    state, canonical = _synthetic_context()
    monkeypatch.setenv("ARERT_RESEARCH_DB_PATH", str(tmp_path / "arert.sqlite3"))
    # The module constant is import-time; pass a temporary path directly through a patched persist wrapper.
    import research_quant.arert_store as store
    original = store.persist_arert_envelope
    monkeypatch.setattr(store, "persist_arert_envelope", lambda envelope: original(envelope, tmp_path / "arert.sqlite3"))
    envelope = run_arert_research(state, canonical, MODULE_CATALOG.keys())
    assert envelope["production_values_modified"] is False
    assert set(envelope["selected_modules"]) == set(MODULE_CATALOG)
    assert envelope["database"]["ok"] is True
    assert state[STATE_KEY] is envelope

    module9 = envelope["modules"]["9"]
    if module9["status"].startswith("RESEARCH"):
        weights = pd.DataFrame(module9["tables"]["dynamic_model_weights"])
        assert math.isclose(float(weights["current_weight"].sum()), 1.0, rel_tol=1e-8, abs_tol=1e-8)

    module10 = envelope["modules"]["10"]
    if module10["status"].startswith("RESEARCH"):
        capital = pd.DataFrame(module10["tables"]["evidence_capital_agents"]).select_dtypes(include="number")
        assert np.isfinite(capital.to_numpy()).all()

    module11 = envelope["modules"]["11"]
    if module11["status"].startswith("RESEARCH"):
        analogues = pd.DataFrame(module11["tables"]["top_historical_analogues"])
        current = pd.Timestamp(canonical["completed_broker_candle"])
        assert not pd.to_datetime(analogues["time"], utc=True).eq(current).any()

    module18 = envelope["modules"]["18"]
    if module18["status"].startswith("RESEARCH"):
        info = pd.DataFrame(module18["tables"]["information_scores"]).select_dtypes(include="number")
        assert np.isfinite(info.to_numpy()).all()

    module20 = envelope["modules"]["20"]
    if module20["status"].startswith("RESEARCH"):
        score = float(module20["summary"]["final_arert_score"])
        assert 0.0 <= score <= 100.0
        assert module20["summary"]["live_trading_command"] is False


def test_arert_same_candle_second_run_uses_module_cache(tmp_path, monkeypatch):
    state, canonical = _synthetic_context(300)
    import research_quant.arert_store as store
    original = store.persist_arert_envelope
    monkeypatch.setattr(store, "persist_arert_envelope", lambda envelope: original(envelope, tmp_path / "cache.sqlite3"))
    run_arert_research(state, canonical, [1, 3, 5])
    second = run_arert_research(state, canonical, [1, 3, 5])
    assert all(row["cache_hit"] for row in second["benchmarks"])


def test_database_migration_preserves_existing_table(tmp_path):
    path = tmp_path / "research.sqlite3"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE protected_production_table (id INTEGER PRIMARY KEY, value TEXT)")
    conn.execute("INSERT INTO protected_production_table(value) VALUES ('unchanged')")
    conn.commit()
    conn.close()
    result = migrate_arert_database(path)
    assert result["ok"] is True
    conn = sqlite3.connect(path)
    assert conn.execute("SELECT value FROM protected_production_table").fetchone()[0] == "unchanged"
    conn.close()
    counts = table_counts(path)
    assert "research_arert_scores" in counts


def test_settings_and_dinner_source_contracts_present():
    settings = Path("tabs/antd_page_router_20260615.py").read_text(encoding="utf-8")
    dinner = Path("research_quant/ui/arert_dinner_lab.py").read_text(encoding="utf-8")
    assert "Run Full Dinner Thesis Research + Open Dinner" in settings
    assert "Run Selected Dinner Research Module" in settings
    for field in range(1, 11):
        assert f"{field}: (" in dinner
    assert "expanded=(field_number == 1)" in dinner


def test_field3_uses_safe_timestamp_sorter():
    source = Path("ui/lunch_field3_regime_matrix_v13.py").read_text(encoding="utf-8")
    assert "safe_sort_by_time" in source
    assert '.sort_values("Broker Time"' not in source


def test_openrouter_context_contains_bounded_arert_research():
    from services.openrouter_backend_20260628 import compact_history_context
    state = {
        STATE_KEY: {
            "metadata": {"run_id": "R", "generation_id": "G"},
            "model_version": "V",
            "parameter_version": "P",
            "selected_modules": [20],
            "modules": {
                "20": {
                    "module_name": "ARERT Reliability Decomposition",
                    "status": "RESEARCH_PROTOTYPE_COMPLETE_EQUAL_WEIGHT_BASELINE",
                    "summary": {"final_arert_score": 66.0},
                    "limitations": ["walk-forward weights incomplete"],
                    "production_influence_enabled": False,
                }
            },
        }
    }
    context = compact_history_context(state)
    assert context["arert_dinner_research"]["modules"]["20"]["summary"]["final_arert_score"] == 66.0
    assert context["arert_dinner_research"]["modules"]["20"]["production_influence_enabled"] is False


def test_openrouter_retries_one_transient_failure(monkeypatch):
    import httpx
    from services import openrouter_backend_20260628 as backend

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-not-real")
    monkeypatch.setattr(backend.time, "sleep", lambda _seconds: None)
    calls = {"count": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["count"] += 1
        if calls["count"] == 1:
            return httpx.Response(503, json={"error": {"message": "temporary"}})
        return httpx.Response(200, json={"choices": [{"message": {"content": "Recovered grounded answer"}}]})

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        result = backend.generate_grounded_answer("Explain ARERT", {"run_id": "R"}, {}, client=client)
    assert result["ok"] is True
    assert result["attempts"] == 2
    assert calls["count"] == 2


def test_ai_assistant_source_has_deterministic_openrouter_fallback():
    source = Path("tabs/ai_assistant_compact_20260619.py").read_text(encoding="utf-8")
    assert "OPENROUTER_GROUNDED" in source
    assert "openrouter_fallback" in source
    assert "answer_question(question" in source
