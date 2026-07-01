from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_main_navigation_exposes_five_decision_surfaces():
    nav = text("ui/antd_navigation_20260615.py")
    assert '"Lunch", "Field 456", "Field 789"' in nav
    assert 'sac.MenuItem("Field 456"' in nav
    assert 'sac.MenuItem("Field 789"' in nav


def test_router_dispatches_independent_combined_pages():
    router = text("tabs/antd_page_router_20260615.py")
    assert 'page == "Field 456"' in router
    assert 'page == "Field 789"' in router
    assert "tabs.field456_page_20260626" in router
    assert "tabs.field789_page_20260626" in router


def test_field1_declares_exact_three_history_surfaces_and_decision_name():
    decision = text("ui/lunch_decision_table_20260626.py")
    lunch = text("ui/lunch_four_core_fields_20260619.py")
    assert "Table 1 of 3 — Decision History — Last 25 Days" in decision
    assert '"Decision Name","Final Decision"' in decision
    assert "Table 2 of 3 — Overall Full Metric History — Last 25 Days" in lunch
    assert "Table 3 of 3 — All 10 Decision Histories — Last 25 Days" in lunch


def test_field2_green_operational_prediction_path_remains_present():
    direction_ui = text("ui/lunch_one_hour_direction_20260626.py")
    assert "Prediction path (green)" in direction_ui
    assert "#20C997" in direction_ui


def test_copy_short_and_full_are_real_controls():
    copy_ui = text("ui/canonical_copy_export_20260619.py")
    assert "Copy Short" in copy_ui
    assert "Copy Full" in copy_ui
