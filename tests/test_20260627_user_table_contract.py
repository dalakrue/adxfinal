from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def text(rel): return (ROOT/rel).read_text(encoding='utf-8')

def test_table1_display_has_no_score_columns():
    src=text('ui/lunch_decision_table_20260626.py')
    block=src[src.index('    preferred = ['):src.index('    shown = table.loc', src.index('    preferred = ['))]
    assert ' Score"' not in block
    assert 'Entry Strength Decision' in block
    assert 'Direction Confirmation Decision' in block

def test_table5_is_always_rendered_and_not_named_fallback():
    src=text('ui/lunch_next_hour_bias_history_20260626.py')
    assert 'def _render_table5' in src
    assert src.count('_render_table5(state, canonical)') >= 2
    assert 'It is not a fallback' in src

def test_airllm_metric_tracks_mode():
    src=text('ui/airllm_mobile_assistant_20260626.py')
    assert 'metric("AirLLM Mode", "OPEN" if mode == "Open" else "CLOSED")' in src

def test_field4to9_authoritative_route():
    src=text('tabs/antd_page_router_20260615.py')
    assert 'elif page == "Field 4 to 9":' in src
    assert 'field456789_page_20260626' in src
