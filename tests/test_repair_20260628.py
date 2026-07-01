from __future__ import annotations

import warnings
from pathlib import Path

import httpx
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_table5_joins_visible_table1_on_normalized_utc_hour():
    from ui.lunch_next_hour_bias_history_20260626 import build_integrated_decision_collection

    state = {
        "field1_table1_decision_history_20260628": pd.DataFrame(
            {
                "Completed Broker Candle": ["2026-06-28T05:42:19+00:00"],
                "net_pressure_decision": ["BUY"],
                "decision_correct": [pd.NA],
                "outcome_status": ["PENDING"],
                "production_decision_raw": ["WAIT"],
                "run_id": ["RUN-1"],
                "generation_id": ["GEN-1"],
            }
        )
    }
    table4 = pd.DataFrame(
        {
            "Broker Candle Time": [pd.Timestamp("2026-06-28T05:00:00Z")],
            "Technical Bias for Next H1": ["BUY"],
            "Combined Next-Hour Direction": ["BUY"],
            "Coverage %": [100.0],
        }
    )
    canonical = {
        "broker_candle_time": "2026-06-28T05:00:00Z",
        "final_decision": {"final_decision": "WAIT"},
    }

    result = build_integrated_decision_collection(state, canonical, table4)

    assert len(result) == 1
    assert result.loc[0, "Net Pressure Decision"] == "BUY"
    assert result.loc[0, "Technical Bias for Next H1"] == "BUY"
    assert result.loc[0, "Decision Correct"] == "PENDING — NEXT H1 NOT SETTLED"
    assert result.loc[0, "Production Master Decision"] == "WAIT"


def test_single_label_nlp_error_analysis_has_stable_matrix_without_warning():
    from core.nlp_event_response import error_analysis

    frame = pd.DataFrame(
        {"direction_label": ["WAIT"] * 5, "nlp_direction": ["WAIT"] * 5}
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = error_analysis(frame)

    assert result["ok"] is True
    assert result["confusion_matrix"].shape == (3, 3)
    assert not [w for w in caught if "single label" in str(w.message).lower()]


def _canonical(candle: str) -> dict:
    return {
        "run_id": "OLD-RUN",
        "generation_id": "OLD-GEN",
        "broker_candle_time": candle,
        "latest_completed_candle_time": candle,
        "symbol": "EURUSD",
        "timeframe": "H1",
    }


def test_field1_bridge_rejects_stale_canonical_when_metric_is_also_old():
    from core.field1_publication_bridge_20260626 import ensure_field1_publication

    state = {
        "canonical_decision_result_20260617": _canonical("2026-06-22T04:00:00Z"),
        "last_df": pd.DataFrame(
            {"time": [pd.Timestamp("2026-06-28T05:00:00Z")], "close": [1.17]}
        ),
        "lunch_metric_result_cache": {
            "ok": True,
            "history": pd.DataFrame(
                {"Broker Candle Time": [pd.Timestamp("2026-06-22T04:00:00Z")]}
            ),
        },
    }
    result = ensure_field1_publication(state)
    assert result["ok"] is False
    assert result["status"] == "STALE_CANONICAL_RECALC_REQUIRED"


def test_field1_bridge_rebinds_fresh_metric_to_new_source_candle():
    from core.field1_publication_bridge_20260626 import ensure_field1_publication

    newest = pd.Timestamp("2026-06-28T05:00:00Z")
    state = {
        "canonical_decision_result_20260617": _canonical("2026-06-22T04:00:00Z"),
        "last_df": pd.DataFrame({"time": [newest], "close": [1.17]}),
        "lunch_metric_result_cache": {
            "ok": True,
            "scores": {"Decision": "BUY"},
            "history": pd.DataFrame({"Broker Candle Time": [newest]}),
        },
    }
    result = ensure_field1_publication(state)
    assert result["ok"] is True
    assert result["repaired"] is True
    assert pd.Timestamp(result["canonical"]["broker_candle_time"]) == newest
    assert result["canonical"]["full_metric_direction"] == "BUY"


def test_openrouter_validate_and_chat_with_mock_transport(monkeypatch):
    from services import openrouter_backend_20260628 as backend

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-not-real")
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        assert request.headers["Authorization"] == "Bearer test-key-not-real"
        if request.url.path.endswith("/models"):
            return httpx.Response(200, json={"data": [{"id": "openrouter/auto"}]})
        assert request.url.path.endswith("/chat/completions")
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Grounded answer"}}]},
        )

    state = {}
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        validation = backend.validate_connection(state, client=client)
        answer = backend.generate_grounded_answer(
            "What is the current decision?",
            {"run_id": "R1", "generation_id": "G1", "final_decision": {"final_decision": "WAIT"}},
            state,
            client=client,
        )

    assert validation["ok"] is True
    assert answer["ok"] is True
    assert answer["answer"] == "Grounded answer"
    assert len(seen) == 2


def test_airllm_is_optional_and_python_version_is_pinned():
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    optional = (ROOT / "requirements-airllm.txt").read_text(encoding="utf-8")
    python_version = (ROOT / ".python-version").read_text(encoding="utf-8").strip()

    active_lines = [line.strip().lower() for line in requirements.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    assert not any(line.startswith("-r") and "requirements-airllm.txt" in line for line in active_lines)
    assert not any(line.startswith("airllm") for line in active_lines)
    assert "airllm" in optional.lower()
    assert python_version.startswith("3.12")


def test_runtime_refresh_cache_includes_visible_table1():
    from core.runtime_state_cache_20260628 import _selected_state

    frame = pd.DataFrame({"Broker Candle Time": [pd.Timestamp("2026-06-28T05:00:00Z")], "Decision": ["WAIT"]})
    selected = _selected_state({"field1_table1_decision_history_20260628": frame})
    assert "field1_table1_decision_history_20260628" in selected


def test_super_quick_is_the_only_scope_limited_to_fields_1_to_3():
    source = (ROOT / "core/settings_run_orchestrator_v9_parts/part_001.py").read_text(encoding="utf-8")
    assert 'quick_scope = requested_scope == "LUNCH_CORE"' in source
    assert '"QUICK_FIELDS_1_TO_9_PLUS_AI" if requested_scope == "QUICK"' in source
