import pandas as pd
from core.field1_publication_bridge_20260626 import ensure_field1_publication
from core.decision_table_20260626 import build_decision_table
from types import SimpleNamespace

def test_bridge_rebinds_real_outputs_without_calculation():
    state={"symbol":"EURUSD","timeframe":"H1","last_df":pd.DataFrame({"time":["2026-06-26T10:00:00Z"],"close":[1.17]}),
           "lunch_metric_result_cache":{"ok":True,"scores":{"Decision":"BUY"}}}
    status={"run_id":"run-x","calculation_generation":7,"canonical":{"ok":True,"run_id":"run-x","calculation_generation":7}}
    result=ensure_field1_publication(state,status)
    assert result["ok"] and result["repaired"]
    assert state["canonical_decision_result_20260617"]["run_id"]=="run-x"

def test_table1_uses_current_publication_when_archive_empty():
    snap=SimpleNamespace(broker_candle_time=pd.Timestamp("2026-06-26T10:00:00Z"),run_id="r",generation_id="g")
    state={"one_hour_direction_confirmation_20260626":{"history":pd.DataFrame(),"current":{"broker_candle_time":"2026-06-26T10:00:00Z","final_decision":"BUY"}}}
    table=build_decision_table(state,snap)
    assert len(table)==1 and table.iloc[0]["Final Decision"]=="BUY"


def test_bridge_selects_newest_metric_and_market_candidates_not_first_cache():
    from core.field1_publication_bridge_20260626 import ensure_field1_publication

    stale = pd.Timestamp("2026-06-17T15:00:00Z")
    fresh = pd.Timestamp("2026-06-28T17:00:00Z")
    state = {
        "canonical_decision_result_20260617": {
            "run_id": "old", "generation_id": "old", "symbol": "EURUSD", "timeframe": "H1",
            "latest_completed_candle_time": stale,
        },
        "canonical_completed_ohlc_df_20260617": pd.DataFrame({"time": [stale], "close": [1.0]}),
        "last_df": pd.DataFrame({"time": [fresh], "close": [1.1]}),
        "lunch_metric_result_cache": {"ok": True, "history": pd.DataFrame({"Broker Candle Time": [stale]})},
        "full_metric_result_cache_20260618": {
            "ok": True,
            "scores": {"Decision": "BUY"},
            "history": pd.DataFrame({"Broker Candle Time": [fresh]}),
        },
    }
    result = ensure_field1_publication(state)
    assert result["ok"] is True
    assert result["repaired"] is True
    assert pd.Timestamp(result["canonical"]["latest_completed_candle_time"]) == fresh
    assert result["canonical"]["full_metric_direction"] == "BUY"
