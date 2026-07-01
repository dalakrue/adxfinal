"""Atomic warm-start cache and exact-source reuse guard.

This module is orchestration-only. It never calculates or changes a production
value. It persists a bounded, secret-free copy of the most recently completed
canonical generation so a Streamlit browser refresh can restore the last valid
published data. It also detects an unchanged completed OHLC source and reuses the
exact generation instead of recalculating it.
"""
from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from contextlib import contextmanager
from pathlib import Path
from typing import Any
import gzip
import os
import tempfile
import time

import pandas as pd

from core.serialization_compat_20260702 import dumps as serializer_dumps, loads as serializer_loads

CACHE_VERSION = "runtime-warm-cache-20260628-v1"
CACHE_PATH = Path(__file__).resolve().parents[1] / "data" / "latest_runtime_state_20260628.pkl.gz"
CACHE_STATE_KEY = "runtime_warm_cache_status_20260628"
SOURCE_SIGNATURE_KEY = "last_completed_source_signature_20260628"
SOURCE_SCOPE_KEY = "last_completed_calculation_scope_20260628"

# API credentials and widget values are deliberately excluded. Persistent API
# credentials belong in Streamlit Secrets, never in this cache.
_FORBIDDEN_KEY_PARTS = (
    "api_key", "apikey", "secret", "password", "passwd", "token", "credential",
    "finnhub_key_input", "twelve_api_key_paste", "bridge_token",
)

_EXACT_KEYS = {
    "canonical_decision_result_20260617", "canonical_decision_result",
    "last_valid_canonical_decision_result_20260617", "canonical_result_20260617",
    "canonical_run_snapshot_20260619", "successful_calculation_generation_20260617",
    "adx_shared_calc_result_20260615", "shared_calc_result",
    "canonical_priority_table_20260617", "adx_hourly_priority_calibrated_20260615",
    "three_center_priority_sorted_20260614", "reliability_dynamic_priority_table_20260614",
    "finder_readonly_priority_table_20260618", "lunch_quick_decision_merged_table_20260617",
    "full_metric_history_df_20260618", "full_metric_regime_history_df", "major_regime_history_df",
    "lunch_metric_result_cache", "full_metric_result_cache_20260618",
    "lunch_metric_result_published_20260618", "lunch_metric_result_20260619",
    "field1_factor_histories_20260626", "one_hour_direction_confirmation_20260626",
    "field1_table1_decision_history_20260628",
    "field1_table3_direction_confirmation_20260626",
    "field1_table4_current_20260627", "field1_table5_integrated_decision_collection_20260627",
    "canonical_completed_ohlc_df_20260617", "canonical_completed_ohlc_staging_20260617",
    "last_df", "dv_pp_df", "dv_pp_base_result", "dv_pp_predicted", "dv_pp_bt_hist",
    "dv_pp_bt_summary", "dv_pp_regime_summary", "dv_pp_regime_hist", "dv_pp_projection_history",
    "powerbi_calibrated_bundle_20260617", "powerbi_projection_result_20260619",
    "lunch_5layer_powerbi_df", "lunch_5layer_powerbi_result",
    "regime_standard_detail_tables_published_20260618", "regime_standard_detail_tables_20260617",
    "regime_standard_table_20260617", "regime_transition_trust_20260621",
    "field4to9_collection_history_full_20260628", "field4to9_collection_history_display_20260628",
    "field4to9_collection_history_20260627", "field4to9_collection_history_identity_20260628",
    "field7_research_result_20260626", "field7_shadow_v13",
    "field8_integrated_history_result_20260624", "field8_integrated_history_20260624",
    "field8_quant_research_v15_20260624", "field8_research_grade_v17_20260624",
    "field9_research_result_20260626", "field9_decision_impact_result_20260624",
    "field9_eurusd_h1_decision_impact", "field9_research_grade_v17_20260624",
    "arcef_sv", "arcef_sv_result", "crcef_sv_research_20260627",
    "quant_research_v3", "quant_research_v4", "quant_research_v7",
    "settings_run_status_20260617", "settings_run_complete_20260617",
    "system_wide_readiness_manifest_20260618", "position_sizing_plan_20260619",
    "compact_canonical_summary_20260619", "canonical_ai_fact_pack_20260619",
    "symbol", "timeframe", "source", "active_data_source", "connector_last_signature",
    "phone_mode", "active_page", "tab_choice", "active_lunch_field", "active_dinner_field",
    "lunch_active_field_selector_20260624", "active_subpage", "lunch_active_subpage",
    SOURCE_SIGNATURE_KEY, SOURCE_SCOPE_KEY,
}

_PREFIXES = (
    "canonical_", "full_metric_", "field1_", "field2_", "field3_", "field4_",
    "field6_", "field7_", "field8_", "field9_", "regime_", "powerbi_",
    "lunch_", "dinner_", "crcef_", "arcef_", "research_grade_",
)


def _forbidden(name: Any) -> bool:
    text = str(name).strip().lower()
    return any(part in text for part in _FORBIDDEN_KEY_PARTS)


def _sanitize(value: Any, *, phone_mode: bool, depth: int = 0) -> Any:
    if depth > 8:
        return str(value)[:500]
    if isinstance(value, pd.DataFrame):
        row_limit = 900 if phone_mode else 3200
        frame = value.tail(row_limit).copy(deep=False) if len(value) > row_limit else value.copy(deep=False)
        # Keep all columns for canonical/history consistency; object values are
        # serialized by cloudpickle rather than converted into lossy strings.
        return frame
    if isinstance(value, pd.Series):
        limit = 1600 if phone_mode else 5000
        return value.tail(limit).copy(deep=False) if len(value) > limit else value.copy(deep=False)
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if _forbidden(key):
                continue
            try:
                result[str(key)] = _sanitize(item, phone_mode=phone_mode, depth=depth + 1)
            except Exception:
                continue
        return result
    if isinstance(value, tuple):
        return tuple(_sanitize(v, phone_mode=phone_mode, depth=depth + 1) for v in value[:5000])
    if isinstance(value, list):
        return [_sanitize(v, phone_mode=phone_mode, depth=depth + 1) for v in value[:5000]]
    if isinstance(value, set):
        return {_sanitize(v, phone_mode=phone_mode, depth=depth + 1) for v in list(value)[:5000]}
    if isinstance(value, (str, bytes, int, float, bool, type(None), pd.Timestamp)):
        return value
    # Preserve dataclasses and simple project objects when cloudpickle supports
    # them; otherwise fall back to a readable value.
    try:
        serializer_dumps(value, protocol=5)
        return value
    except Exception:
        return str(value)[:2000]


def _selected_state(state: Mapping[str, Any]) -> dict[str, Any]:
    phone_mode = bool(state.get("phone_mode", False))
    selected: dict[str, Any] = {}
    for key, value in state.items():
        name = str(key)
        if _forbidden(name):
            continue
        if name not in _EXACT_KEYS and not name.startswith(_PREFIXES):
            continue
        # Widget-only booleans/text are cheap but not needed unless explicitly
        # listed. This keeps the cache small and prevents stale UI controls.
        if name not in _EXACT_KEYS and not isinstance(value, (Mapping, list, tuple, pd.DataFrame, pd.Series)):
            continue
        try:
            selected[name] = _sanitize(value, phone_mode=phone_mode)
        except Exception:
            continue
    return selected


def build_source_signature(state: Mapping[str, Any]) -> dict[str, Any]:
    try:
        from core.canonical_runtime_20260617 import get_canonical
        canonical = get_canonical(state)
    except Exception:
        canonical = state.get("canonical_decision_result_20260617") or {}
    try:
        from core.quick_source_signature_20260626 import build_quick_source_signature
        return build_quick_source_signature(state, canonical if isinstance(canonical, Mapping) else {})
    except Exception:
        return {}


def save_runtime_state(
    state: MutableMapping[str, Any], *, status: Mapping[str, Any] | None = None,
    scope: str | None = None, path: Path | str = CACHE_PATH,
) -> dict[str, Any]:
    """Atomically save the last completed secret-free generation."""
    try:
        from core.canonical_runtime_20260617 import get_canonical
        canonical = get_canonical(state)
    except Exception:
        canonical = state.get("canonical_decision_result_20260617") or {}
    if not isinstance(canonical, Mapping) or not canonical:
        report = {"ok": False, "status": "SKIPPED", "reason": "No valid canonical generation"}
        state[CACHE_STATE_KEY] = report
        return report

    signature = build_source_signature(state)
    actual_scope = str(scope or state.get("settings_calculation_scope_20260625") or "FULL").upper()
    if signature:
        state[SOURCE_SIGNATURE_KEY] = signature
    state[SOURCE_SCOPE_KEY] = actual_scope
    payload = {
        "cache_version": CACHE_VERSION,
        "saved_at": pd.Timestamp.now(tz="UTC").isoformat(),
        "scope": actual_scope,
        "source_signature": signature,
        "status": _sanitize(dict(status or {}), phone_mode=bool(state.get("phone_mode", False))),
        "state": _selected_state(state),
    }
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    try:
        raw = serializer_dumps(payload, protocol=5)
        compressed = gzip.compress(raw, compresslevel=3)
        # Corrupt/accidental runaway cache protection.
        if len(compressed) > 180 * 1024 * 1024:
            raise ValueError(f"warm cache exceeds 180 MiB ({len(compressed)} bytes)")
        fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(compressed)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
        report = {
            "ok": True, "status": "SAVED", "path": str(path), "bytes": len(compressed),
            "keys": len(payload["state"]), "seconds": round(time.perf_counter() - started, 4),
            "scope": actual_scope, "source_signature": signature.get("source_signature"),
        }
    except Exception as exc:
        report = {"ok": False, "status": "ERROR", "error": f"{type(exc).__name__}: {exc}"}
    state[CACHE_STATE_KEY] = report
    return report


def restore_runtime_state(
    state: MutableMapping[str, Any], *, path: Path | str = CACHE_PATH,
    max_age_days: int = 35,
) -> dict[str, Any]:
    """Restore the newest completed generation without recalculating it."""
    if state.get("canonical_decision_result_20260617"):
        return {"ok": True, "status": "ALREADY_PRESENT", "restored": 0}
    path = Path(path)
    if not path.is_file():
        report = {"ok": False, "status": "NO_CACHE", "restored": 0}
        state[CACHE_STATE_KEY] = report
        return report
    started = time.perf_counter()
    try:
        payload = serializer_loads(gzip.decompress(path.read_bytes()))
        if not isinstance(payload, Mapping) or payload.get("cache_version") != CACHE_VERSION:
            raise ValueError("unsupported warm-cache version")
        saved = pd.to_datetime(payload.get("saved_at"), errors="coerce", utc=True)
        if pd.isna(saved) or (pd.Timestamp.now(tz="UTC") - saved) > pd.Timedelta(days=max_age_days):
            report = {"ok": False, "status": "EXPIRED", "restored": 0, "saved_at": str(saved)}
            state[CACHE_STATE_KEY] = report
            return report
        cached_state = payload.get("state")
        if not isinstance(cached_state, Mapping):
            raise ValueError("cache has no state mapping")
        restored = 0
        for key, value in cached_state.items():
            if _forbidden(key):
                continue
            # Current-session values always win; startup defaults such as blank
            # frames may be replaced only when no published canonical exists.
            if key in state and state.get(key) not in (None, "", False):
                if key not in _EXACT_KEYS:
                    continue
            state[key] = value
            restored += 1
        if isinstance(payload.get("source_signature"), Mapping):
            state[SOURCE_SIGNATURE_KEY] = dict(payload["source_signature"])
        state[SOURCE_SCOPE_KEY] = str(payload.get("scope") or "FULL").upper()
        state["runtime_cache_restored_20260628"] = True
        state["runtime_cache_restored_at_20260628"] = pd.Timestamp.now(tz="UTC").isoformat()
        report = {
            "ok": True, "status": "RESTORED", "restored": restored,
            "saved_at": payload.get("saved_at"), "scope": payload.get("scope"),
            "seconds": round(time.perf_counter() - started, 4), "path": str(path),
        }
    except Exception as exc:
        report = {"ok": False, "status": "ERROR", "restored": 0, "error": f"{type(exc).__name__}: {exc}"}
    state[CACHE_STATE_KEY] = report
    return report


def reusable_completed_generation(state: MutableMapping[str, Any], requested_scope: str) -> dict[str, Any]:
    """Return a reuse status only when the exact completed OHLC source matches."""
    if bool(state.get("force_recalculate_same_candle_20260628", False)):
        return {}
    try:
        from core.canonical_runtime_20260617 import get_canonical
        canonical = get_canonical(state)
    except Exception:
        canonical = state.get("canonical_decision_result_20260617") or {}
    if not isinstance(canonical, Mapping) or not canonical:
        return {}
    previous = state.get(SOURCE_SIGNATURE_KEY)
    if not isinstance(previous, Mapping) or not previous.get("source_signature"):
        return {}
    current = build_source_signature(state)
    if not current or current.get("source_signature") != previous.get("source_signature"):
        return {}
    requested = str(requested_scope or "FULL").upper()
    prior_scope = str(state.get(SOURCE_SCOPE_KEY) or "FULL").upper()
    # A prior FULL generation satisfies QUICK; a prior QUICK generation does not
    # satisfy a later FULL thesis/research request.
    if requested == "FULL" and prior_scope != "FULL":
        return {}
    prior_status = state.get("settings_run_status_20260617")
    result = dict(prior_status) if isinstance(prior_status, Mapping) else {}
    result.update({
        "ok": True,
        "reused_completed_generation": True,
        "cache_status": "EXACT_SOURCE_HIT",
        "calculation_scope": requested,
        "source_signature": current,
        "message": "Exact completed-candle generation reused; no protected or research calculation was rebuilt.",
        "elapsed_seconds": 0.0,
    })
    state["settings_run_status_20260617"] = result
    state["settings_run_complete_20260617"] = True
    state["runtime_exact_generation_reuse_20260628"] = {
        "at": pd.Timestamp.now(tz="UTC").isoformat(),
        "scope": requested,
        "source_signature": current.get("source_signature"),
    }
    return result


@contextmanager
def phone_research_profile(state: Mapping[str, Any]):
    """Use bounded research-validation windows on phone; production core is untouched."""
    previous = os.environ.get("ADX_TEST_PROFILE")
    changed = bool(state.get("phone_mode", False))
    if changed:
        os.environ["ADX_TEST_PROFILE"] = "fast"
    try:
        yield
    finally:
        if changed:
            if previous is None:
                os.environ.pop("ADX_TEST_PROFILE", None)
            else:
                os.environ["ADX_TEST_PROFILE"] = previous


__all__ = [
    "CACHE_PATH", "CACHE_STATE_KEY", "SOURCE_SIGNATURE_KEY", "SOURCE_SCOPE_KEY",
    "build_source_signature", "save_runtime_state", "restore_runtime_state",
    "reusable_completed_generation", "phone_research_profile",
]
