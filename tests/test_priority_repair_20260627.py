from __future__ import annotations

from pathlib import Path
import copy
import pandas as pd

from core.navigation_state_20260627 import initialize_navigation, request_page, commit_requested_page
from core.navigation_authority_20260625 import navigate_to
from ui.field4to9_collection_history_20260627 import build_field4to9_collection_history


def test_app_and_legacy_entry_use_same_shell():
    app = Path("app.py").read_text()
    legacy = Path("adx_dashpoard.py").read_text()
    assert "from core.app_shell import run_app" in app
    assert "from core.app_shell import run_app" in legacy
    assert "run_app()" in app and "run_app()" in legacy


def test_floating_menu_route_transaction_works_first_load_and_after_run():
    state = {}
    assert initialize_navigation(state) == "Settings"
    request_page(state, "Dinner")
    assert commit_requested_page(state) == "Dinner"
    state["settings_run_status_20260617"] = {"ok": True}
    request_page(state, "Research")
    assert commit_requested_page(state) == "Research"
    request_page(state, "Dinner")
    assert commit_requested_page(state) == "Dinner"


def test_all_legacy_dinner_aliases_open_direct_dinner():
    for alias in ("Field 4 to 9", "Field 456+789", "Field 456", "Field 789", "Dinner Combined"):
        state = {}
        navigate_to(state, alias)
        assert state["active_page"] == "Dinner"
        assert state["tab_choice"] == "Dinner"


def test_lunch_code_cannot_remap_dinner():
    state = {"active_page": "Dinner", "tab_choice": "Dinner"}
    initialize_navigation(state)
    assert commit_requested_page(state) == "Dinner"


def test_dinner_page_declares_history_before_metrics_and_fields():
    source = Path("tabs/field456789_page_20260626.py").read_text()
    history = source.index("render_field4to9_collection_history")
    metrics = source.index("_render_compact_metrics(history")
    field4 = source.index('_lazy_section("Field 4')
    field9 = source.index('_lazy_section("Field 9')
    assert history < metrics < field4 < field9
    for number in (4, 6, 7, 8, 9):
        assert f"Field {number}" in source


def test_dinner_history_preserves_real_disagreement():
    stamp = pd.Timestamp("2026-06-27 10:00", tz="UTC")
    state = {
        "field4_payload": pd.DataFrame([{"timestamp": stamp, "technical_decision": "BUY"}]),
        "field6_payload": pd.DataFrame([{"timestamp": stamp, "decision": "SELL"}]),
        "field7_payload": pd.DataFrame([{"timestamp": stamp, "decision": "BUY"}]),
        "field8_payload": pd.DataFrame([{"timestamp": stamp, "decision": "WAIT"}]),
        "field9_payload": pd.DataFrame([{"timestamp": stamp, "decision": "SELL"}]),
    }
    table = build_field4to9_collection_history(state, {"broker_candle_time": stamp})
    row = table.iloc[0]
    assert row["Field 4 Decision"] == "BUY"
    assert row["Field 6 Decision"] == "SELL"
    assert float(row["Conflict"]) > 0


def test_fields_are_closed_first_and_no_active_quick_sync_button():
    lunch = Path("ui/lunch_four_core_fields_20260619.py").read_text()
    assert 'CLOSED_LUNCH_FIELD = "All Lunch fields closed"' in lunch
    assert "state.setdefault(selector_key, CLOSED_LUNCH_FIELD)" in lunch
    # Legacy wording may exist in comments, but there must be no button call.
    assert 'st.button("Refresh API Data + Quick Sync"' not in lunch


def test_settings_full_run_publishes_crcef_after_protected_run():
    source = Path("core/settings_run_orchestrator_20260617.py").read_text()
    assert "publish_crcef_sv_research" in source
    assert source.index("_v10_run_settings_calculation") < source.index("publish_crcef_sv_research")
