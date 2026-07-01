from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_removed_external_nlp_key_ui():
    text=(ROOT/'tabs/antd_page_router_20260615.py').read_text()
    assert 'Open / Close — NLP / AI Assistant API Key' not in text
    assert 'NLP API key — mobile paste box' not in text

def test_combined_page_and_no_embedded_field5():
    page=(ROOT/'tabs/field456789_page_20260626.py').read_text()
    assert 'render_field456_independent' in page and 'render_field789_independent' in page
    lunch=(ROOT/'ui/lunch_four_core_fields_20260619.py').read_text()
    assert '["Field 4 — Dinner Combined Intelligence", "Field 6 — Future Strategy Research History"]' in lunch

def test_post_run_consistency_publishes_current_row():
    import pandas as pd
    from core.post_run_consistency_20260626 import enforce_post_run_consistency
    c={'run_id':'r1','generation_id':'1','broker_candle_time':'2026-06-26T07:00:00Z','symbol':'EURUSD','timeframe':'H1','final_decision':{'final_decision':'WAIT'}}
    state={'canonical_decision_result_20260617':c}
    out=enforce_post_run_consistency(state,{})
    assert out['ok']
    assert state['one_hour_direction_confirmation_20260626']['current']['final_decision']=='WAIT'
    assert state['canonical_result']['run_id']=='r1'
