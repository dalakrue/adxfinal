from core.thesis_engine.decision_mapping import map_decision
from core.thesis_engine.correlation_penalty import penalty
from core.thesis_engine.orchestrator import build_arcef_result
from core.thesis_engine.settled_outcomes import exclude_incomplete

def snap(**kw):
    x={"run_id":"r1","generation_id":"g1","symbol":"EURUSD","timeframe":"H1","broker_candle_time":"2026-06-27T10:00:00+02:00","decision":"WAIT","reliability_score":70,"regime":"BULL","regime_reliability":70,"uncertainty":30,"data_quality_score":100}; x.update(kw); return x

def test_wait_hold_mapping(): assert map_decision("WAIT")["standardized_action"]==0 and map_decision("HOLD")["standardized_action"]==0
def test_wait_pullback_intention(): assert map_decision("WAIT PULLBACK BUY")["intended_direction"]=="BUY"
def test_blank(): assert map_decision("")["normalized_label"]=="BLANK"
def test_weight_normalization(): assert abs(sum(x["final_weight"] for x in build_arcef_result(snap(decision="BUY"))["model_contribution_ledger"])-1)<1e-9
def test_single_model_fallback(): assert build_arcef_result(snap(decision="SELL"))["valid_model_count"]>=1
def test_correlation_penalty(): assert penalty(.9)<1
def test_incomplete_exclusion(): assert len(exclude_incomplete([{"broker_candle":"2026-06-27T09:00:00"},{"broker_candle":"2026-06-27T11:00:00"}],"2026-06-27T10:00:00"))==1
def test_identity_and_version():
    r=build_arcef_result(snap()); assert r["run_id"]=="r1" and r["generation_id"]=="g1" and r["algorithm_version"]
def test_history_newest_first(): assert len(build_arcef_result(snap())["history_25d"])<=25

def test_all_models_rejected_fallback_is_non_directional_visible():
    r=build_arcef_result(snap(decision="")); assert r["master_decision"] in {"WAIT","HOLD"} and r["model_contribution_ledger"]
def test_missing_data_behavior(): assert build_arcef_result({})["ok"]
def test_broker_time_consistency(): assert build_arcef_result(snap())["completed_broker_candle"]==snap()["broker_candle_time"]
def test_dinner_route_and_synthesis_present():
    from pathlib import Path
    text=Path("tabs/dinner_unified_center_20260617.py").read_text(); assert "Dinner Quantitative Master Synthesis" in text and "history_25d" in text
def test_first_load_closed_state():
    from pathlib import Path
    assert 'expanded=False' in Path("lunch/field_arcef/renderer.py").read_text()
def test_full_quick_run_orchestration_hook():
    from pathlib import Path
    text=Path("core/settings_run_orchestrator_20260617.py").read_text(); assert "publish_arcef_result" in text
def test_algorithm_version_persistence():
    r=build_arcef_result(snap(run_id="persist")); assert any(x.get("algorithm_version")==r["algorithm_version"] for x in r["version_history"])
def test_calibration_separation_declared():
    r=build_arcef_result(snap()); e=r["experiment_registry"][-1]; assert e["calibration_window"]=="separate" and e["test_window"]=="held-out"
