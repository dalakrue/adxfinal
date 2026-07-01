from __future__ import annotations

from pathlib import Path
import pandas as pd


def test_arert_decision_label_accepts_pandas_na():
    from research_quant.arert_lab import _decision_label
    assert _decision_label(pd.NA) is None
    assert _decision_label("BUY") == "BUY"


def test_arert_context_handles_na_decision_cells():
    from research_quant.arert_lab import build_context
    times = pd.date_range("2026-06-01", periods=40, freq="h", tz="UTC")
    ohlc = pd.DataFrame({"Time": times, "Open": 1.1, "High": 1.2, "Low": 1.0, "Close": 1.1 + pd.Series(range(40)).to_numpy() * 0.0001})
    decisions = pd.DataFrame({"Broker Candle Time": times, "Master Decision": [pd.NA] * 39 + ["BUY"]})
    canonical = {"completed_broker_candle": times[-1], "ohlc_df": ohlc, "run_id": "r", "generation_id": "g"}
    context = build_context({"field1_table1_decision_history_20260628": decisions}, canonical)
    assert not context.features.empty
    assert context.features["vote_mean"].notna().sum() >= 1


def test_mixed_string_timestamp_regime_history_is_safe():
    from ui.lunch_four_core_fields_20260619 import _history_25day
    frame = pd.DataFrame({
        "Time": ["2026-06-01T01:00:00Z", pd.Timestamp("2026-06-01 03:00", tz="UTC"), "bad", pd.Timestamp("2026-06-01 02:00")],
        "Major Regime": ["BULL", "BEAR", "RANGE", "BULL"],
    })
    result = _history_25day(frame, completed_h1=pd.Timestamp("2026-06-01 03:00", tz="UTC"))
    assert len(result) == 3
    assert pd.to_datetime(result["Time"], utc=True).is_monotonic_decreasing


def test_dinner_final_protective_vocabulary_has_four_allowed_labels():
    from ui.field4to9_collection_history_20260627 import _add_final_protective_result
    frame = pd.DataFrame({
        "Production Master Decision": ["BUY", "BUY", "WAIT", "SELL"],
        "Technical Consensus": ["BUY", "BUY", "WAIT", "SELL"],
        "Coverage": [1.0, 0.8, 1.0, 0.2],
        "Conflict": [0.0, 0.3, 0.0, 0.8],
        "Research Reliability": [85, 55, 80, 90],
        "Uncertainty": [15, 35, 20, 10],
    })
    result = _add_final_protective_result(frame)
    allowed = {"WAIT FOR PULLBACK", "HOLD AND PROTECT", "ALLOWED", "NO TRADE"}
    assert set(result["Protective Action"]).issubset(allowed)
    assert set(result["Protective Action"]) == allowed


def test_dinner_candidate_ranking_prefers_variable_history():
    from ui.field4to9_collection_history_20260627 import _rank_candidates
    frame = pd.DataFrame({"constant": ["BUY"] * 5, "history": ["BUY", "SELL", "BUY", "WAIT", "SELL"]})
    assert _rank_candidates(frame, ["constant", "history"])[0] == "history"


def test_finder_source_contains_table5_and_complete_copy():
    source = Path("ui/finder_canonical_view_20260619.py").read_text(encoding="utf-8")
    assert "Field 1 Table 5 integrated logic" in source
    assert "Copy Complete Finder Result" in source
    assert "FIELD 1 TABLE 5 INTEGRATED DECISION" in source


def test_dinner_page_uses_flat_published_results_without_running_nested_renderers():
    source = Path("tabs/field456789_page_20260626.py").read_text(encoding="utf-8")
    show = source.split("def show(runtime_context=None):", 1)[1]
    assert "_render_flat_published_dinner_tables(canonical)" in show
    assert "_render_selected_detail(selection)" not in show
