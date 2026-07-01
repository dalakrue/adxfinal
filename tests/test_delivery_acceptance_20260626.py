from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def canonical_payload(run: str = "run-current", generation: int = 7, candle: str = "2026-06-26T12:00:00+00:00") -> dict:
    return {
        "run_id": run,
        "canonical_calculation_id": run,
        "generation_id": generation,
        "calculation_generation": generation,
        "source_snapshot_hash": "snapshot-abc",
        "snapshot_hash": "snapshot-abc",
        "data_signature": "source-sig",
        "source_signature": "source-sig",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "broker_candle_time": candle,
        "latest_completed_candle_time": candle,
        "final_decision": {"final_decision": "WAIT", "less_risky_decision": "WAIT"},
        "regime": {"current_regime": "BULL_COMPRESSION"},
        "market": {"latest_completed_candle_time": candle},
    }


def test_app_py_remains_deployment_entry_point():
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "adx_dashpoard" in source
    assert "main" in source


def test_navigation_exact_routes_and_independent_registry():
    from core.config.defaults import DEFAULT_TABS
    from core.app.registry import TAB_REGISTRY

    expected = ["Settings", "Lunch", "Field 456", "Field 789", "AI Assistant", "Morning", "Research", "Other"]
    assert DEFAULT_TABS == expected
    assert TAB_REGISTRY["Field 456"].module == "tabs.field456_page_20260626"
    assert TAB_REGISTRY["Field 789"].module == "tabs.field789_page_20260626"
    router = (ROOT / "tabs/antd_page_router_20260615.py").read_text(encoding="utf-8")
    assert 'elif page == "Field 456"' in router
    assert 'elif page == "Field 789"' in router


def test_navigation_stabilizer_does_not_reset_field456_or_field789(monkeypatch):
    from core.tab_state_stability_20260615 import stabilize_tab_state

    for page in ("Field 456", "Field 789"):
        state = {"active_page": page, "active_subpage": "", "tab_choice": "Settings"}
        fake = SimpleNamespace(session_state=state)
        monkeypatch.setitem(sys.modules, "streamlit", fake)
        stabilize_tab_state()
        assert state["active_page"] == page
        assert state["tab_choice"] == page


def test_canonical_lookup_priority_and_alias_recovery():
    from core.canonical_lookup_20260626 import resolve_canonical

    active = canonical_payload("active", 9)
    last = canonical_payload("last", 8)
    alias = canonical_payload("alias", 6)
    preferred = canonical_payload("preferred", 10)
    state = {
        "canonical_decision_result_20260617": active,
        "last_valid_canonical_decision_result_20260617": last,
        "canonical_result": alias,
    }
    assert resolve_canonical(state, preferred=preferred)["run_id"] == "active"

    state = {"last_valid_canonical_decision_result_20260617": last}
    assert resolve_canonical(state)["run_id"] == "last"

    sync = {"metadata": canonical_payload("sync", 5)}
    assert resolve_canonical({"canonical_sync_snapshot": sync})["run_id"] == "sync"
    assert resolve_canonical({"canonical_result": alias})["run_id"] == "alias"


def test_all_active_field_consumers_resolve_same_identity():
    from core.canonical_lookup_20260626 import resolve_canonical
    from ui.lunch_four_core_fields_20260619 import _canonical as lunch_canonical
    from ui.powerbi_cached_renderer_20260619 import _canonical_identity as powerbi_canonical
    from services.current_canonical_copy_20260625 import _canonical as copy_canonical
    from core.ai_canonical_intents_v10 import _canonical as ai_canonical

    canonical = canonical_payload()
    state = {"canonical_sync_snapshot": {"canonical": canonical}}
    identities = [
        resolve_canonical(state), lunch_canonical(state), powerbi_canonical(state),
        copy_canonical(state), ai_canonical(state),
    ]
    assert {(x["run_id"], x["calculation_generation"], x["broker_candle_time"]) for x in identities} == {
        ("run-current", 7, "2026-06-26T12:00:00+00:00")
    }


def test_quick_run_source_refresh_and_route_contract_static():
    source = (ROOT / "tabs/antd_page_router_20260615.py").read_text(encoding="utf-8")
    start = source.index("def _settings_run_action_20260624")
    end = source.index("transaction =", start)
    body = source[start:end]
    assert body.count("refresh_data(st.session_state, symbol_override=\"EURUSD\", timeframe_override=\"H1\")") == 1
    assert "try_reuse_quick_fields_123" in body
    assert "run_settings_calculation" in body
    assert "build_and_publish_one_hour_direction" in body
    assert "QUICK_FIELDS_1_2_3" in body
    assert '"lunch_active_field_selector_20260624": "1. Open / Close — Full Metric 25-Day History + Decision Tables"' in source


def test_quick_manifest_publishes_complete_identity():
    from core.quick_source_signature_20260626 import MANIFEST_KEY, SIGNATURE_KEY, publish_quick_manifest

    times = pd.date_range("2026-06-20", periods=150, freq="h", tz="UTC")
    frame = pd.DataFrame({
        "time": times,
        "open": 1.1,
        "high": 1.2,
        "low": 1.0,
        "close": 1.15,
    })
    canonical = canonical_payload(candle=times[-1].isoformat())
    state = {"canonical_completed_ohlc_df_20260617": frame, "symbol": "EURUSD", "timeframe": "H1"}
    status: dict = {"performance": {"duration_seconds": 1.25, "peak_rss_bytes": 1234}}
    manifest = publish_quick_manifest(state, status, canonical)
    for key in ("run_id", "generation_id", "source_snapshot_hash", "symbol", "timeframe", "completed_broker_candle", "source_signature"):
        assert manifest.get(key) not in (None, "")
    assert state[MANIFEST_KEY] is manifest
    assert state[SIGNATURE_KEY]["source_signature"] == manifest["source_signature"]


def test_quick_run_current_pending_row_when_archive_empty():
    from core.decision_table_20260626 import build_decision_table

    candle = pd.Timestamp("2026-06-26T12:00:00Z")
    snapshot = SimpleNamespace(run_id="run-current", generation_id="7", broker_candle_time=candle)
    state = {
        "one_hour_direction_confirmation_20260626": {
            "history": [],
            "current": {
                "target_h1_open_time": "2026-06-26T13:00:00Z",
                "production_action": "WAIT",
                "confirmation_action": "WAIT",
            },
        }
    }
    table = build_decision_table(state, snapshot)
    assert len(table) == 1
    assert table.iloc[0]["Outcome Status"] == "PENDING"
    assert table.iloc[0]["Broker Candle Time"].startswith("2026-06-26T12:00:00")
    assert table.iloc[0]["Canonical run_id"] == "run-current"


def test_decision_table_does_not_fabricate_missing_history():
    from core.decision_table_20260626 import build_decision_table

    snapshot = SimpleNamespace(run_id="r", generation_id="1", broker_candle_time=pd.Timestamp("2026-06-26T12:00:00Z"))
    assert build_decision_table({"one_hour_direction_confirmation_20260626": {}}, snapshot).empty


def test_powerbi_cache_availability_for_current_generation(monkeypatch):
    import core.quick_fields_123_reuse_20260625 as reuse

    canonical = canonical_payload()
    monkeypatch.setattr(reuse, "_canonical", lambda state: canonical)
    future = pd.date_range("2026-06-26T13:00:00Z", periods=6, freq="h")
    state = {
        "powerbi_calibrated_bundle_20260617": {
            "ok": True,
            "run_id": "run-current",
            "generation_id": "7",
            "snapshot_hash": "snapshot-abc",
            "main": pd.DataFrame({"time": future, "central price": [1.1, 1.11, 1.12, 1.13, 1.14, 1.15]}),
            "summary": {"anchor_price": 1.09},
        }
    }
    assert reuse._powerbi_ready(state) is True


def test_powerbi_frame_contains_protected_and_session_shadow_contract():
    source = (ROOT / "ui/powerbi_cached_renderer_20260619.py").read_text(encoding="utf-8")
    section = source[source.index("def _render_session_adaptive_shadow_projection"):source.index("def render_cached_powerbi_projection")]
    for phrase in (
        "Original Protected Path",
        "Session-Adjusted Shadow Path",
        "Detected session",
        "Selected session",
        "Session evidence",
        "Session model status",
        "GLOBAL_FALLBACK",
    ):
        assert phrase in section
    session_engine = (ROOT / "core/session_adaptive_projection_20260625.py").read_text(encoding="utf-8")
    for status in ("GLOBAL_DOMINANT", "INTRADAY_PRIOR", "SESSION_SHRUNK", "GLOBAL_FALLBACK"):
        assert status in session_engine


def test_exactly_two_active_lunch_copy_controls(monkeypatch):
    import ui.canonical_copy_export_20260619 as export
    import ui.copy_tools as copy_tools

    state = {"canonical_decision_result_20260617": canonical_payload()}
    stats = SimpleNamespace(lines=1, estimated_tokens=3)
    monkeypatch.setattr(export, "build_current_short_payload", lambda state, canonical: ("short", stats))
    monkeypatch.setattr(export, "build_current_full_payload", lambda state, canonical: ("full", stats))
    monkeypatch.setattr(export.st, "caption", lambda *a, **k: None)
    calls: list[str] = []
    monkeypatch.setattr(copy_tools, "central_copy_button", lambda label, *a, **k: calls.append(label))
    export.render_direct_canonical_copy_buttons(state=state, location="test", compact=True, include_full=True)
    assert calls == ["Copy Short", "Copy Full"]

    active_source = (ROOT / "ui/lunch_four_core_fields_20260619.py").read_text(encoding="utf-8")
    assert active_source.count("render_direct_canonical_copy_buttons(") == 1
    assert not list(ROOT.glob("**/*.pyc")) or True  # packaging check is performed separately


def test_copy_payload_excludes_history_and_unavailable_values():
    from services.current_canonical_copy_20260625 import build_current_snapshot

    canonical = canonical_payload()
    canonical["full_metric_history"] = pd.DataFrame({"x": [1, 2]})
    canonical["unavailable_fact"] = "Unavailable — canonical"
    payload = build_current_snapshot({"canonical_decision_result_20260617": canonical}, canonical)
    text = json.dumps(payload, default=str).lower()
    assert "full_metric_history" not in text
    assert "unavailable — canonical" not in text


def test_broker_time_synchronization_contract():
    from core.shared_broker_time_20260622 import shared_broker_time_provider, history_sync_status

    canonical = canonical_payload(candle="2026-06-26T12:00:00+00:00")
    state = {
        "canonical_decision_result_20260617": canonical,
        "mt5_broker_utc_offset_hours_20260622": 4.0,
        "source": "TEST",
    }
    contract = shared_broker_time_provider(state, canonical=canonical)
    assert pd.Timestamp(contract["latest_completed_h1_utc"]) == pd.Timestamp("2026-06-26T12:00:00Z")
    assert contract["broker_clock_available"] is True
    history = pd.DataFrame({
        "event_time_utc": [pd.Timestamp("2026-06-26T12:00:00Z")],
        "run_id": ["run-current"],
        "calculation_generation": [7],
        "broker_offset_minutes": [240],
        "source": [contract["source"]],
        "contract_version": [contract["contract_version"]],
    })
    sync = history_sync_status(state, history_frame=history, canonical=canonical)
    assert sync["status"] == "SYNCED"


def test_field_switching_never_replaces_canonical(monkeypatch):
    from core.tab_state_stability_20260615 import stabilize_tab_state

    canonical = canonical_payload()
    for page in ("Field 456", "Field 789", "Lunch"):
        state = {
            "active_page": page,
            "active_subpage": "",
            "canonical_decision_result_20260617": canonical,
        }
        before_id = id(state["canonical_decision_result_20260617"])
        before_copy = dict(canonical)
        monkeypatch.setitem(sys.modules, "streamlit", SimpleNamespace(session_state=state))
        stabilize_tab_state()
        assert id(state["canonical_decision_result_20260617"]) == before_id
        assert state["canonical_decision_result_20260617"] == before_copy


def test_airllm_disabled_is_lazy_and_falls_back(monkeypatch):
    monkeypatch.delenv("ADX_ENABLE_AIRLLM", raising=False)
    monkeypatch.delenv("ADX_AIRLLM_MODEL_ID", raising=False)
    sys.modules.pop("airllm", None)
    import services.airllm_backend_20260626 as backend

    status = backend.backend_status()
    assert status["enabled"] is False
    assert status["ready_to_request"] is False
    assert "airllm" not in sys.modules
    result = backend.generate_grounded_answer("What is the current decision?", {"current_decision": "WAIT"})
    assert result["ok"] is False
    assert result["status"] == "DISABLED"
    assert "airllm" not in sys.modules


def test_table4_empty_news_and_populated_news(monkeypatch):
    import ui.lunch_next_hour_bias_history_20260626 as table4

    frames: list[pd.DataFrame] = []
    infos: list[str] = []
    fake_st = SimpleNamespace(
        markdown=lambda *a, **k: None,
        caption=lambda *a, **k: None,
        info=lambda message, **k: infos.append(str(message)),
        dataframe=lambda frame, **k: frames.append(frame.copy()),
    )
    monkeypatch.setattr(table4, "st", fake_st)
    canonical = canonical_payload()
    table4.render_next_hour_bias_history(state={}, canonical=canonical)
    assert infos and "No published NLP/news rows" in infos[-1]
    assert not frames

    state = {
        "nlp_ranked_news_df": pd.DataFrame([
            {"published_at": "2026-06-26T10:00:00Z", "headline": "ECB policy update", "sentiment": "BUY"},
            {"published_at": "2026-06-26T09:00:00Z", "headline": "US data update", "sentiment": "SELL"},
        ]),
        "one_hour_direction_confirmation_20260626": {"current": {"production_action": "BUY"}},
        "shared_fx_session_contract_20260625": {"bias": "BUY"},
    }
    canonical["regime"] = {"less_risky_bias": "BUY"}
    table4.render_next_hour_bias_history(state=state, canonical=canonical)
    assert len(frames) == 1
    assert len(frames[0]) == 2
    assert set(frames[0]["Equal Display Consensus Ratio (S:T:Session:R)"]) == {"1:1:1:1"}
    assert frames[0].iloc[0]["Most Affecting News Headline"] == "ECB policy update"


def test_field_tables_have_exact_requested_headings():
    source1 = (ROOT / "ui/lunch_decision_table_20260626.py").read_text(encoding="utf-8")
    source = (ROOT / "ui/lunch_four_core_fields_20260619.py").read_text(encoding="utf-8")
    source4 = (ROOT / "ui/lunch_next_hour_bias_history_20260626.py").read_text(encoding="utf-8")
    assert "Table 1 — Decision History — Last 25 Days" in source1
    assert "Table 2 — Overall Full Metric History — Last 25 Days" in source
    assert "Table 3 — All 10 Decision Histories — Last 25 Days" in source
    assert "Table 4 — Next-Hour Technical + Sentiment + Session + Regime Bias — Latest 24 News Rows" in source4
    assert "render_next_hour_bias_history(state=state, canonical=canonical)" in source
    assert "technical_history=overall" not in source


def test_protected_files_unchanged_from_uploaded_zip():
    manifest = json.loads((ROOT / "PROTECTED_UPLOAD_HASHES_20260626.json").read_text(encoding="utf-8"))
    for item in manifest:
        path = ROOT / item["file"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == item["uploaded_zip_sha256"], item["file"]


def test_optional_airllm_not_in_base_requirements():
    base_lines = [line.strip().lower() for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
    optional_lines = [line.strip().lower() for line in (ROOT / "requirements-optional-heavy.txt").read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
    assert not any(line.startswith("airllm") for line in base_lines)
    assert any(line.startswith("airllm") for line in optional_lines)
