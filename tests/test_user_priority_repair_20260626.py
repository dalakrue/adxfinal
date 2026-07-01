from pathlib import Path

def test_table1_reuses_factor_histories():
    text=Path("core/decision_table_20260626.py").read_text()
    assert "_factor_history_fallback" in text
    assert "history_by_factor" in text

def test_table4_local_ohlc_fallback():
    text=Path("ui/lunch_next_hour_bias_history_20260626.py").read_text()
    assert "_local_h1_bias_frame" in text
    assert "LOCAL_COMPLETED_OHLC" in text

def test_copy_enabled_before_run():
    text=Path("ui/canonical_copy_export_20260619.py").read_text()
    assert "startup_short" in text
    assert "disabled=True" not in text[text.find("def render_direct_canonical_copy_buttons"):text.find("__all__")]

def test_combined_route_exists():
    assert '"Field 4 to 9"' in Path("core/app/registry.py").read_text()
