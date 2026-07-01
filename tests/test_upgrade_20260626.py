from pathlib import Path
from types import SimpleNamespace
import pandas as pd
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def test_exact_five_fields_static():
    text=(ROOT/'ui/lunch_four_core_fields_20260619.py').read_text()
    assert 'FIELD_LABELS = (' in text
    assert 'FULL_METRIC_FIELD, POWERBI_FIELD, REGIME_FIELD' in text
    assert 'render_field456_independent' in text
    assert 'render_field789_independent' in text
    assert 'Exactly 5 total surfaces' in text
    defaults=(ROOT/'core/config/defaults.py').read_text()
    assert '"Field 456"' in defaults and '"Field 789"' in defaults

def test_field1_three_groups_and_order_static():
    text=(ROOT/'ui/lunch_four_core_fields_20260619.py').read_text()
    a=text.index('render_field1_decision_history')
    b=text.index('Overall Full Metric History — Last 25 Days')
    c=text.index('All 10 Decision Histories — Last 25 Days')
    assert a < b < c

def test_copy_and_refresh_labels_static():
    text=(ROOT/'ui/canonical_copy_export_20260619.py').read_text()
    assert 'central_copy_button("Copy Short"' in text
    assert 'central_copy_button("Copy Full"' in text
    lunch=(ROOT/'ui/lunch_four_core_fields_20260619.py').read_text()
    assert 'Refresh API Data + Quick Sync' in lunch
    assert 'Exactly 5' in lunch

def test_decision_table_preserves_missing_and_genuine_percent_boundaries():
    from core.decision_table_20260626 import build_decision_table
    snap=SimpleNamespace(broker_candle_time=pd.Timestamp('2026-06-26T10:00:00Z'),run_id='r',generation_id='g',source_snapshot_hash='h',symbol='EURUSD',timeframe='H1',decision='WAIT',regime='R',created_at_utc=pd.Timestamp('2026-06-26T10:01:00Z'))
    hist=pd.DataFrame([{'broker_candle_time':'2026-06-26T10:00:00Z','decision_confidence':0,'uncertainty_percentage':100,'outcome_status':'PENDING'}])
    out=build_decision_table({'one_hour_direction_confirmation_20260626':{'history':hist}},snap)
    assert out.iloc[0]['Decision Confidence'] == 0
    assert out.iloc[0]['Uncertainty Percentage'] == 100
    assert out.iloc[0]['Decision Correct'] == 'N/A'
    assert out.iloc[0]['Entry Strength Score'] == 'N/A'

def test_shadow_threshold_retains_on_insufficient_data():
    from core.direction_confirmation_shadow_policy_20260626 import evaluate_shadow_policy
    out=evaluate_shadow_policy(pd.DataFrame({'direction_score':[1,2], 'actual_direction':['BUY','SELL']}), 5)
    assert out['status']=='RETAIN_PRODUCTION'
    assert out['promoted_threshold']==5

def test_state_taxonomy():
    from core.research_result_state_20260626 import classify_research_result
    assert classify_research_result(None)['state']=='missing source data'
    assert classify_research_result({'sample_size':3,'minimum_observations':20})['state']=='insufficient observations'
    assert classify_research_result({'outcome_status':'pending'})['state']=='unsettled future outcome'
    assert classify_research_result({'model_failure':True})['state']=='model failure'
    assert classify_research_result({'ok':True,'confidence':0.4})['state']=='valid but low-confidence result'
