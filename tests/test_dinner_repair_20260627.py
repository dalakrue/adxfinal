import pandas as pd
from core.navigation_authority_20260625 import navigate_to
from ui.field4to9_collection_history_20260627 import build_field4to9_collection_history, build_self_calculated_field45_tables, _direction, _source_columns

def test_aliases_route_to_dinner():
    for alias in ["Field 4 to 9","Field 456+789","Field 456","Field 789"]:
        s={}; navigate_to(s,alias); assert s["active_page"]=="Dinner" and s["tab_choice"]=="Dinner"

def test_nested_field9_history_and_no_truncation():
    ts=pd.Timestamp('2026-06-27 10:00',tz='UTC')
    rec={"timestamp":ts,**{f"deep_decision_{i}":"BUY" for i in range(20)}}
    state={"field9_payload":{"a":{"b":{"rows":[rec]}}}}
    out=build_field4to9_collection_history(state,{"broker_candle_time":ts})
    assert len([c for c in out.columns if 'deep_decision_' in c])==20

def test_generated_sources_excluded_and_audited():
    ts=pd.Timestamp('2026-06-27 10:00',tz='UTC')
    state={"field4_original":pd.DataFrame([{"timestamp":ts,"technical_decision":"BUY","confidence":99}]),
           "field4_self_calculated_table_20260627":pd.DataFrame([{"timestamp":ts,"generated_decision":"SELL"}])}
    t4,t5,audit=build_self_calculated_field45_tables(state,{"broker_candle_time":ts})
    assert not audit["Source Column"].str.contains("generated",case=False).any()
    assert not audit["Source Column"].str.contains("confidence",case=False).any()
    assert t5.iloc[0]["Integrated Decision"]=="BUY"

def test_buy_sell_conflict_is_wait(): assert _direction("BUY and SELL conflict") == "WAIT"
def test_confidence_excluded():
    df=pd.DataFrame(columns=["Broker Candle Time","x confidence","x decision"])
    assert _source_columns(df)==["x decision"]

def test_broker_time_conversion():
    ts=pd.Timestamp('2026-06-27 00:00',tz='UTC')
    out=build_field4to9_collection_history({"field6":pd.DataFrame([{"timestamp":ts,"decision":"BUY"}])},{"broker_candle_time":ts})
    assert out.iloc[0]["Hour"]=="06:30"

def test_airllm_real_interface_and_lazy_import():
    import pathlib
    text=pathlib.Path('services/airllm_backend_20260626.py').read_text()
    assert 'from airllm import AutoModel' in text
    assert 'AutoModel.from_pretrained' in text
    assert text.index('from airllm import AutoModel') > text.index('def _load_model')
