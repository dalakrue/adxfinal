"""Multi-symbol orchestration and Lunch Field 10 persistence.

This module is additive.  It reuses the existing single-symbol Settings-owned
calculation transaction, stores each completed symbol generation separately,
and exposes read-only cross-symbol quality/regime evidence to Lunch Field 10.
No protected calculation, decision, priority, BFP/SFP, or Field 1-9 formula is
replaced here.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping, Sequence
from contextlib import suppress
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
import gzip
import json
import os
import sqlite3
import time
import uuid

import numpy as np
import pandas as pd

from core.serialization_compat_20260702 import loads as serializer_loads

VERSION = "multi-symbol-field10-20260701-v1"
SUPPORTED_SYMBOLS: tuple[str, ...] = (
    "EURUSD", "USDJPY", "AUDUSD", "GBPUSD", "USDCAD", "USDCHF",
    "EURJPY", "GBPJPY", "EURGBP", "NZDUSD", "XAUUSD", "BTCUSD",
    "NAS100", "US500",
)

# Canonical names remain provider-neutral.  Provider aliases are resolved only
# at the connector boundary, so one provider's naming convention is never
# imposed on the rest of the application.
PROVIDER_ALIASES: Mapping[str, Mapping[str, tuple[str, ...]]] = {
    "canonical": {
        "BTCUSD": ("BTCUSD", "BTC/USD", "XBTUSD"),
        "XAUUSD": ("XAUUSD", "XAU/USD", "GOLD"),
        "NAS100": ("NAS100", "USTEC", "NDX", "US100", "NASDAQ100"),
        "US500": ("US500", "SPX500", "SPX", "SP500", "^GSPC", "GSPC"),
    },
    "twelve": {
        "BTCUSD": ("BTC/USD", "BTCUSD"),
        "XAUUSD": ("XAU/USD", "XAUUSD"),
        "NAS100": ("NDX", "NASDAQ100", "NAS100"),
        "US500": ("SPX", "GSPC", "US500"),
    },
    "finnhub": {
        "BTCUSD": ("BINANCE:BTCUSDT", "COINBASE:BTC-USD", "BTCUSD"),
        "XAUUSD": ("OANDA:XAU_USD", "XAUUSD"),
        "NAS100": ("^NDX", "NDX", "NAS100"),
        "US500": ("^GSPC", "SPX", "US500"),
    },
    "mt5": {
        "BTCUSD": ("BTCUSD", "BTCUSD.", "BTCUSDm", "BTCUSD.c"),
        "XAUUSD": ("XAUUSD", "GOLD", "XAUUSD.", "XAUUSDm"),
        "NAS100": ("NAS100", "USTEC", "US100", "NDX"),
        "US500": ("US500", "SPX500", "SP500", "SPX"),
    },
}

SELECTED_KEY = "multi_symbol_selected_20260701"
ACTIVE_KEY = "multi_symbol_active_20260701"
MANIFEST_KEY = "multi_symbol_manifest_20260701"
PROGRESS_KEY = "multi_symbol_progress_20260701"
CHILD_RUN_KEY = "multi_symbol_child_run_active_20260701"
PARENT_RUN_KEY = "multi_symbol_parent_run_id_20260701"
LAST_RESOURCE_KEY = "multi_symbol_resource_report_20260701"
RUNNING_KEY = "multi_symbol_run_in_progress_20260701"
FIELD10_SUMMARY_KEY = "field10_multi_symbol_summary_20260701"
FIELD10_DAILY_KEY = "field10_daily_higher_regime_20260701"
FIELD10_HOURLY_KEY = "field10_hourly_quality_20260701"

ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / "data" / "multi_symbol_runtime_20260701"
DB_PATH = ROOT / "data" / "multi_symbol_field10_20260701.sqlite3"

_UI_PRESERVE_KEYS = {
    "active_page", "tab_choice", "active_subpage", "phone_mode",
    "lunch_active_field_selector_20260624", "settings_calculation_scope_20260625",
    SELECTED_KEY, ACTIVE_KEY, MANIFEST_KEY, PROGRESS_KEY, CHILD_RUN_KEY,
    PARENT_RUN_KEY, LAST_RESOURCE_KEY, RUNNING_KEY, FIELD10_SUMMARY_KEY, FIELD10_DAILY_KEY,
    FIELD10_HOURLY_KEY,
}


def normalize_symbol(value: Any, default: str = "EURUSD") -> str:
    raw = str(value or default).strip().upper().replace("/", "").replace(" ", "")
    aliases = {
        "XBTUSD": "BTCUSD", "BTCUSDT": "BTCUSD", "GOLD": "XAUUSD",
        "USTEC": "NAS100", "US100": "NAS100", "NDX": "NAS100",
        "NASDAQ100": "NAS100", "SPX500": "US500", "SP500": "US500",
        "SPX": "US500", "GSPC": "US500", "^GSPC": "US500",
    }
    return aliases.get(raw, raw) or default


def normalize_selected(values: Any) -> list[str]:
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, Sequence):
        values = []
    seen: list[str] = []
    for value in values:
        symbol = normalize_symbol(value)
        if symbol in SUPPORTED_SYMBOLS and symbol not in seen:
            seen.append(symbol)
    return seen


def selected_symbols(state: Mapping[str, Any]) -> list[str]:
    selected = normalize_selected(state.get(SELECTED_KEY))
    if selected:
        return selected
    single = normalize_symbol(state.get("symbol") or "EURUSD")
    return [single] if single in SUPPORTED_SYMBOLS else ["EURUSD"]


def resolve_provider_symbol(symbol: Any, provider: Any, available_symbols: Sequence[str] | None = None) -> str:
    """Resolve a canonical instrument to the first provider-supported alias."""
    canonical = normalize_symbol(symbol)
    provider_name = str(provider or "canonical").strip().lower()
    aliases = list(PROVIDER_ALIASES.get(provider_name, {}).get(canonical, ()))
    aliases += list(PROVIDER_ALIASES["canonical"].get(canonical, (canonical,)))
    if canonical not in aliases:
        aliases.insert(0, canonical)
    if available_symbols:
        lookup = {str(item).strip().upper(): str(item) for item in available_symbols}
        for alias in aliases:
            match = lookup.get(str(alias).strip().upper())
            if match:
                return match
    return aliases[0]


def _cache_path(symbol: str) -> Path:
    return CACHE_DIR / f"{normalize_symbol(symbol)}.pkl.gz"


def _read_cache_payload(path: Path) -> Mapping[str, Any]:
    from core.runtime_state_cache_20260628 import CACHE_VERSION

    payload = serializer_loads(gzip.decompress(path.read_bytes()))
    if not isinstance(payload, Mapping) or payload.get("cache_version") != CACHE_VERSION:
        raise ValueError("Unsupported symbol runtime cache")
    return payload


def _managed_runtime_key(name: str) -> bool:
    from core.runtime_state_cache_20260628 import _EXACT_KEYS, _PREFIXES

    return name in _EXACT_KEYS or name.startswith(_PREFIXES)


def clear_active_symbol_results(state: MutableMapping[str, Any]) -> int:
    """Clear only reconstructable symbol-generation state before a fresh symbol."""
    removed = 0
    for key in list(state.keys()):
        name = str(key)
        if name in _UI_PRESERVE_KEYS or name.startswith("multi_symbol_"):
            continue
        if _managed_runtime_key(name):
            state.pop(key, None)
            removed += 1
    return removed


def activate_symbol_result(state: MutableMapping[str, Any], symbol: Any) -> dict[str, Any]:
    """Load one saved symbol generation without running calculations."""
    canonical = normalize_symbol(symbol)
    path = _cache_path(canonical)
    if not path.is_file():
        return {"ok": False, "status": "NO_SAVED_RESULT", "symbol": canonical, "path": str(path)}
    started = time.perf_counter()
    try:
        payload = _read_cache_payload(path)
        cached_state = payload.get("state")
        if not isinstance(cached_state, Mapping):
            raise ValueError("Symbol cache contains no state mapping")
        preserved = {key: state.get(key) for key in _UI_PRESERVE_KEYS if key in state}
        clear_active_symbol_results(state)
        restored = 0
        for key, value in cached_state.items():
            name = str(key)
            if any(part in name.lower() for part in ("api_key", "secret", "password", "token", "credential")):
                continue
            state[name] = value
            restored += 1
        state.update(preserved)
        state["symbol"] = canonical
        state["selected_symbol"] = canonical
        state["ws_symbol"] = canonical
        state[ACTIVE_KEY] = canonical
        state["selected_symbol_pending_run_20260629"] = False
        return {
            "ok": True, "status": "RESTORED", "symbol": canonical,
            "restored_keys": restored, "path": str(path),
            "seconds": round(time.perf_counter() - started, 4),
        }
    except Exception as exc:
        return {
            "ok": False, "status": "ERROR", "symbol": canonical, "path": str(path),
            "error": f"{type(exc).__name__}: {exc}",
        }


def _canonical(state: Mapping[str, Any]) -> Mapping[str, Any]:
    with suppress(Exception):
        from core.canonical_runtime_20260617 import get_canonical
        value = get_canonical(state)
        if isinstance(value, Mapping):
            return value
    for key in ("canonical_decision_result_20260617", "canonical_result_20260617", "last_valid_canonical_decision_result_20260617"):
        value = state.get(key)
        if isinstance(value, Mapping):
            return value
    return {}


def _source_frame(state: Mapping[str, Any]) -> pd.DataFrame:
    for key in ("canonical_completed_ohlc_df_20260617", "calculation_staging_ohlc_df_20260617", "last_df", "dv_pp_df"):
        value = state.get(key)
        if isinstance(value, pd.DataFrame) and not value.empty:
            return value
    return pd.DataFrame()


def _time_series(frame: pd.DataFrame) -> pd.Series:
    if frame.empty:
        return pd.Series(dtype="datetime64[ns, UTC]")
    normalized = {str(c).strip().lower().replace("_", " "): c for c in frame.columns}
    column = next((normalized.get(name) for name in ("broker candle time", "time", "datetime", "timestamp", "date") if normalized.get(name) is not None), None)
    if column is None:
        return pd.Series(pd.NaT, index=frame.index, dtype="datetime64[ns, UTC]")
    return pd.to_datetime(frame[column], errors="coerce", utc=True)


def grade_from_score(score: Any) -> str:
    try:
        value = float(score)
    except Exception:
        value = 0.0
    if value >= 90:
        return "A"
    if value >= 75:
        return "B"
    if value >= 60:
        return "C"
    return "D"


def assess_data_quality(state: Mapping[str, Any], canonical: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Transparent A-D quality score from existing data/validation evidence."""
    canonical = dict(canonical or _canonical(state))
    frame = _source_frame(state)
    score = 100.0
    reasons: list[str] = []
    if frame.empty:
        return {"score": 0.0, "grade": "D", "status": "FAILED", "reasons": ["completed OHLC unavailable"], "rows": 0}
    times = _time_series(frame)
    valid_times = times.dropna().sort_values()
    invalid_time_count = int(times.isna().sum())
    duplicate_count = int(valid_times.duplicated().sum())
    missing_periods = 0
    if len(valid_times) > 1:
        diff_hours = valid_times.drop_duplicates().diff().dt.total_seconds().div(3600)
        missing_periods = int(np.maximum(np.floor(diff_hours.fillna(1.0).to_numpy()) - 1, 0).sum())
    if invalid_time_count:
        score -= min(25.0, invalid_time_count * 2.0); reasons.append(f"invalid timestamps: {invalid_time_count}")
    if duplicate_count:
        score -= min(15.0, duplicate_count * 1.5); reasons.append(f"duplicate candles: {duplicate_count}")
    if missing_periods:
        score -= min(20.0, missing_periods * 0.35); reasons.append(f"missing H1 periods: {missing_periods}")
    if len(frame) < 600:
        score -= min(25.0, (600 - len(frame)) / 24.0); reasons.append(f"higher-standard history incomplete: {len(frame)}/600")

    normalized = {str(c).strip().lower(): c for c in frame.columns}
    required = [normalized.get(name) for name in ("open", "high", "low", "close")]
    invalid_ohlc = 0
    if all(column is not None for column in required):
        o, h, l, c = (pd.to_numeric(frame[column], errors="coerce") for column in required)
        invalid_ohlc = int((h.lt(pd.concat([o, c], axis=1).max(axis=1)) | l.gt(pd.concat([o, c], axis=1).min(axis=1)) | o.le(0) | h.le(0) | l.le(0) | c.le(0)).sum())
        if invalid_ohlc:
            score -= min(35.0, invalid_ohlc * 4.0); reasons.append(f"invalid OHLC rows: {invalid_ohlc}")
    else:
        score -= 20.0; reasons.append("required OHLC columns missing")

    identity_missing = [name for name in ("run_id", "symbol", "timeframe") if not canonical.get(name)]
    source_id = canonical.get("source_id") or canonical.get("data_source_id") or canonical.get("source_snapshot_hash") or canonical.get("snapshot_hash")
    if not source_id:
        score -= 8.0; reasons.append("source ID missing")
    if identity_missing:
        score -= 8.0; reasons.append("identity missing: " + ", ".join(identity_missing))
    field3 = state.get("field3_regime_lifecycle_monitor_20260701")
    if isinstance(field3, Mapping):
        reported = (field3.get("data_quality") or {}).get("score") if isinstance(field3.get("data_quality"), Mapping) else None
        if reported is not None:
            try:
                score = min(score, float(reported))
                reasons.append("capped by Field 3 data-quality gate")
            except Exception:
                pass
    score = round(max(0.0, min(100.0, score)), 2)
    return {
        "score": score, "grade": grade_from_score(score),
        "status": "PASS" if score >= 75 else ("WARN" if score >= 60 else "FAIL"),
        "reasons": reasons or ["all checked quality controls passed"],
        "rows": int(len(frame)), "invalid_timestamps": invalid_time_count,
        "duplicates": duplicate_count, "missing_periods": missing_periods,
        "invalid_ohlc": invalid_ohlc,
        "first_candle": valid_times.min().isoformat() if not valid_times.empty else None,
        "last_candle": valid_times.max().isoformat() if not valid_times.empty else None,
        "source_id": str(source_id or ""),
    }


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _first_number(*values: Any) -> float | None:
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if np.isfinite(number):
            return number
    return None


def _broker_wall_timestamp_value(value: Any) -> pd.Timestamp:
    """Parse a broker timestamp while preserving its displayed wall-clock hour."""
    try:
        stamp = pd.Timestamp(value)
    except Exception:
        return pd.NaT
    if pd.isna(stamp):
        return pd.NaT
    # tz_localize(None) removes the offset without converting the clock.  This is
    # intentional: Field 10 displays MetaTrader/broker candle time, not UTC.
    if stamp.tzinfo is not None:
        stamp = stamp.tz_localize(None)
    return stamp


def _broker_wall_series(values: Any) -> pd.Series:
    series = values if isinstance(values, pd.Series) else pd.Series(values)
    return series.map(_broker_wall_timestamp_value)


def _session_execution_context(state: Mapping[str, Any], canonical: Mapping[str, Any], broker_time: pd.Timestamp | None = None) -> dict[str, Any]:
    """Read published session/execution evidence without creating a new prediction."""
    contract = state.get("shared_fx_session_contract_20260625")
    contract = contract if isinstance(contract, Mapping) else {}
    if not contract:
        with suppress(Exception):
            from core.session_context_20260625 import normalize_session_selection, resolve_session_contract
            selection = normalize_session_selection(state.get("shared_fx_session_selection_20260625"))
            contract = resolve_session_contract(dict(state), dict(canonical), selection).to_dict()
    session = str(contract.get("selected_session") or contract.get("detected_session") or "UNAVAILABLE")
    priority_map = {
        "LONDON_NEW_YORK_OVERLAP": 100.0, "TOKYO_LONDON_OVERLAP": 90.0,
        "LONDON": 85.0, "NEW_YORK": 80.0, "TOKYO_SYDNEY_OVERLAP": 75.0,
        "TOKYO": 65.0, "SYDNEY": 55.0, "GLOBAL_FALLBACK": 40.0,
        "UNAVAILABLE": 0.0,
    }
    session_priority = _first_number(contract.get("session_priority"), contract.get("priority_score"))
    if session_priority is None:
        session_priority = priority_map.get(session.upper(), 50.0 if session != "UNAVAILABLE" else 0.0)

    execution = _mapping(canonical.get("execution"))
    market = _mapping(canonical.get("market"))
    spread = _first_number(
        execution.get("spread_pips"), execution.get("spread_points"),
        market.get("spread_pips"), market.get("spread"),
        canonical.get("spread_pips"), state.get("spread_pips"), state.get("estimated_spread_pips"),
    )
    published_quality = str(
        execution.get("spread_quality") or market.get("spread_quality")
        or canonical.get("spread_quality") or state.get("spread_quality") or ""
    ).upper().strip()
    if published_quality:
        spread_quality = published_quality
    elif spread is None:
        spread_quality = "UNAVAILABLE"
    elif spread <= 0.6:
        spread_quality = "LOW"
    elif spread <= 1.2:
        spread_quality = "AVERAGE"
    elif spread <= 2.0:
        spread_quality = "HIGH"
    else:
        spread_quality = "VERY HIGH"
    spread_score_map = {"LOW": 100.0, "GOOD": 90.0, "AVERAGE": 70.0, "MEDIUM": 65.0, "HIGH": 35.0, "VERY HIGH": 10.0, "UNAVAILABLE": 40.0}
    spread_score = spread_score_map.get(spread_quality, 50.0)

    final = _mapping(canonical.get("final_decision"))
    reliability = _mapping(canonical.get("reliability"))
    uncertainty = _first_number(
        final.get("uncertainty_pct"), canonical.get("uncertainty_pct"),
        reliability.get("uncertainty_pct"), reliability.get("uncertainty"),
    )
    error = _first_number(
        final.get("error_percentage"), canonical.get("error_percentage"),
        canonical.get("forecast_error_pct"), reliability.get("error_percentage"),
    )
    trade_permission = str(
        final.get("trade_permission") or canonical.get("trade_permission")
        or ("BLOCKED" if str(final.get("less_risky_decision") or "").upper() in {"WAIT", "NO TRADE"} else "CHECK")
    ).upper()
    final_action = str(
        final.get("final_decision") or final.get("less_risky_decision")
        or canonical.get("decision") or "WAIT"
    ).upper()
    return {
        "current_session": session, "session_priority": float(session_priority),
        "average_spread": spread, "spread_quality": spread_quality, "spread_score": spread_score,
        "uncertainty": uncertainty, "error_percentage": error,
        "trade_permission": trade_permission, "final_action": final_action,
    }


def _daily_higher_snapshot(state: MutableMapping[str, Any], canonical: Mapping[str, Any]) -> dict[str, Any]:
    locked: Mapping[str, Any] = {}
    with suppress(Exception):
        from core.daily_locked_regime_20260625 import ensure_daily_locked_regime
        locked = ensure_daily_locked_regime(state, canonical)
    higher = _mapping(locked.get("higher"))
    final = _mapping(canonical.get("final_decision"))
    regime = _mapping(canonical.get("regime"))
    higher_bias = str(higher.get("bias") or regime.get("higher_bias") or regime.get("bias") or "WAIT")
    less_risky_bias = str(final.get("less_risky_decision") or canonical.get("less_risky_decision") or higher_bias or "WAIT")
    return {
        "higher_regime": str(higher.get("regime") or regime.get("higher_regime") or regime.get("major_regime") or canonical.get("regime") or "UNKNOWN"),
        "higher_standard_bias": higher_bias,
        "less_risky_bias": less_risky_bias,
        "higher_reliability": float(higher.get("reliability") or regime.get("reliability") or 0.0),
        "higher_transition_risk": float(higher.get("transition_risk") or 0.0),
        "higher_alpha": float(higher.get("alpha") or 0.0),
        "higher_delta": float(higher.get("delta") or 0.0),
        "sample_count": int(higher.get("sample_count") or 0),
        "next_review_broker_time": locked.get("next_review_broker_time"),
        "locked_status": locked.get("status") or "UNAVAILABLE",
    }


def _hourly_history(state: Mapping[str, Any], canonical: Mapping[str, Any], quality: Mapping[str, Any]) -> pd.DataFrame:
    symbol = normalize_symbol(canonical.get("symbol") or state.get("symbol") or "EURUSD")
    run_id = str(canonical.get("run_id") or canonical.get("canonical_calculation_id") or "")
    source_id = str(canonical.get("source_id") or canonical.get("data_source_id") or canonical.get("source_snapshot_hash") or canonical.get("snapshot_hash") or "")
    monitor = state.get("field3_regime_lifecycle_monitor_20260701")
    if isinstance(monitor, Mapping):
        raw_history = monitor.get("history_25d")
        history = raw_history.copy(deep=False) if isinstance(raw_history, pd.DataFrame) else pd.DataFrame(raw_history or [])
    else:
        history = pd.DataFrame()
    if history.empty:
        details = state.get("regime_standard_detail_tables_published_20260618") or state.get("regime_standard_detail_tables_20260617")
        details = details if isinstance(details, Mapping) else {}
        higher = next((details.get(k) for k in ("higher", "high") if isinstance(details.get(k), pd.DataFrame)), None)
        history = higher.copy(deep=False) if isinstance(higher, pd.DataFrame) else pd.DataFrame()
    if history.empty:
        frame = _source_frame(state)
        history = pd.DataFrame({"event_time_utc": _time_series(frame)}) if not frame.empty else pd.DataFrame()
    if history.empty:
        return pd.DataFrame()

    def col(*tokens: str) -> str | None:
        for column in history.columns:
            lower = str(column).lower()
            if all(token in lower for token in tokens):
                return str(column)
        return None

    time_col = col("broker", "time") or col("event_time") or col("time") or col("date")
    times = _broker_wall_series(history[time_col]) if time_col else pd.Series(pd.NaT, index=history.index, dtype="datetime64[ns]")
    higher_col = col("existing higher regime") or col("higher", "regime") or col("regime")
    higher_bias_col = col("higher", "bias") or col("regime bias") or col("bias")
    less_risky_col = col("less-risky") or col("less risky") or col("final", "bias") or higher_bias_col or col("decision")
    dq_col = col("data quality score") or col("data quality")
    trust_col = col("calibrated trust score") or col("trust score") or col("trust")
    reliability_col = col("bias reliability score") or col("reliability")
    session_col = col("session")
    session_priority_col = col("session", "priority")
    spread_col = col("average", "spread") or col("spread", "pips") or col("spread")
    spread_quality_col = col("spread", "quality")
    uncertainty_col = col("uncertainty")
    error_col = col("error", "percentage") or col("error", "pct")
    permission_col = col("trade", "permission")
    action_col = col("final", "action")
    result = pd.DataFrame({
        "Broker Timestamp": times,
        "Symbol": symbol,
        "Timeframe": str(canonical.get("timeframe") or state.get("timeframe") or "H1"),
        "Higher Standard Regime": history[higher_col].astype(str).values if higher_col else "UNKNOWN",
        "Higher-Standard Bias": history[higher_bias_col].astype(str).values if higher_bias_col else "WAIT",
        "Less-Risky Bias": history[less_risky_col].astype(str).values if less_risky_col else "WAIT",
        "Data Quality Score": pd.to_numeric(history[dq_col], errors="coerce").values if dq_col else float(quality.get("score") or 0.0),
        "Trust Score": pd.to_numeric(history[trust_col], errors="coerce").values if trust_col else np.nan,
        "Reliability": pd.to_numeric(history[reliability_col], errors="coerce").values if reliability_col else np.nan,
        "Current Session": history[session_col].astype(str).values if session_col else "UNAVAILABLE",
        "Session Priority": pd.to_numeric(history[session_priority_col], errors="coerce").values if session_priority_col else np.nan,
        "Average Spread": pd.to_numeric(history[spread_col], errors="coerce").values if spread_col else np.nan,
        "Spread Quality": history[spread_quality_col].astype(str).values if spread_quality_col else "UNAVAILABLE",
        "Uncertainty": pd.to_numeric(history[uncertainty_col], errors="coerce").values if uncertainty_col else np.nan,
        "Error Percentage": pd.to_numeric(history[error_col], errors="coerce").values if error_col else np.nan,
        "Trade Permission": history[permission_col].astype(str).values if permission_col else "CHECK",
        "Final Action": history[action_col].astype(str).values if action_col else (history[less_risky_col].astype(str).values if less_risky_col else "WAIT"),
        "Run ID": run_id,
        "Source ID": source_id,
    })
    result = result.dropna(subset=["Broker Timestamp"]).sort_values("Broker Timestamp").drop_duplicates("Broker Timestamp", keep="last").tail(600)
    broker_wall = _broker_wall_series(result["Broker Timestamp"])
    result["Broker Timestamp"] = broker_wall
    result["Broker Date"] = broker_wall.dt.strftime("%Y-%m-%d")
    result["Broker Hour"] = broker_wall.dt.strftime("%H:%M")
    result["Data Quality Score"] = result["Data Quality Score"].fillna(float(quality.get("score") or 0.0)).clip(0, 100)
    result["Data Quality"] = result["Data Quality Score"].map(grade_from_score)
    result["Validation Status"] = str(quality.get("status") or "CHECK")
    result["Quality Reason"] = "; ".join(str(x) for x in list(quality.get("reasons") or [])[:4])
    # Only the newest row may use current exact-generation execution/session evidence.
    # Older rows stay UNAVAILABLE unless the historical source explicitly published it.
    if not result.empty:
        latest_index = result["Broker Timestamp"].idxmax()
        context = _session_execution_context(state, canonical, pd.Timestamp(result.loc[latest_index, "Broker Timestamp"]))
        if str(result.loc[latest_index, "Current Session"]).upper() in {"", "NAN", "UNAVAILABLE"}:
            result.loc[latest_index, "Current Session"] = context["current_session"]
        if pd.isna(result.loc[latest_index, "Session Priority"]):
            result.loc[latest_index, "Session Priority"] = context["session_priority"]
        if pd.isna(result.loc[latest_index, "Average Spread"]):
            result.loc[latest_index, "Average Spread"] = context["average_spread"]
        if str(result.loc[latest_index, "Spread Quality"]).upper() in {"", "NAN", "UNAVAILABLE"}:
            result.loc[latest_index, "Spread Quality"] = context["spread_quality"]
        if pd.isna(result.loc[latest_index, "Uncertainty"]):
            result.loc[latest_index, "Uncertainty"] = context["uncertainty"]
        if pd.isna(result.loc[latest_index, "Error Percentage"]):
            result.loc[latest_index, "Error Percentage"] = context["error_percentage"]
        if str(result.loc[latest_index, "Trade Permission"]).upper() in {"", "NAN", "CHECK"}:
            result.loc[latest_index, "Trade Permission"] = context["trade_permission"]
        if str(result.loc[latest_index, "Final Action"]).upper() in {"", "NAN"}:
            result.loc[latest_index, "Final Action"] = context["final_action"]
    return result.reset_index(drop=True)


def migrate_database(path: Path | str = DB_PATH) -> dict[str, Any]:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(path), timeout=30) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS multi_symbol_runs (
                parent_run_id TEXT NOT NULL,
                child_run_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                scope TEXT NOT NULL,
                status TEXT NOT NULL,
                elapsed_seconds REAL NOT NULL DEFAULT 0,
                rss_delta_mb REAL NOT NULL DEFAULT 0,
                cpu_seconds REAL NOT NULL DEFAULT 0,
                canonical_run_id TEXT,
                source_id TEXT,
                completed_candle TEXT,
                current_session TEXT,
                session_priority REAL,
                average_spread REAL,
                spread_quality TEXT,
                uncertainty REAL,
                error_percentage REAL,
                trade_permission TEXT,
                final_action TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                PRIMARY KEY(parent_run_id, symbol)
            );
            CREATE TABLE IF NOT EXISTS field10_hourly_quality (
                parent_run_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                broker_timestamp TEXT NOT NULL,
                rank INTEGER,
                data_quality_grade TEXT NOT NULL,
                data_quality_score REAL NOT NULL,
                higher_standard_regime TEXT,
                higher_standard_bias TEXT,
                less_risky_bias TEXT,
                trust_score REAL,
                reliability REAL,
                validation_status TEXT,
                quality_reason TEXT,
                broker_date TEXT,
                broker_hour TEXT,
                current_session TEXT,
                session_priority REAL,
                average_spread REAL,
                spread_quality TEXT,
                uncertainty REAL,
                error_percentage REAL,
                trade_permission TEXT,
                final_action TEXT,
                rank_score REAL,
                rank_reason TEXT,
                run_id TEXT,
                source_id TEXT,
                created_at TEXT NOT NULL,
                PRIMARY KEY(parent_run_id, symbol, broker_timestamp)
            );
            CREATE INDEX IF NOT EXISTS idx_field10_hourly_latest
                ON field10_hourly_quality(symbol, broker_timestamp DESC);
            CREATE TABLE IF NOT EXISTS field10_daily_higher_lock (
                broker_day TEXT NOT NULL,
                symbol TEXT NOT NULL,
                rank INTEGER,
                higher_standard_regime TEXT NOT NULL,
                higher_standard_bias TEXT,
                less_risky_bias TEXT NOT NULL,
                data_quality_grade TEXT NOT NULL,
                data_quality_score REAL NOT NULL,
                higher_reliability REAL,
                higher_transition_risk REAL,
                higher_alpha REAL,
                higher_delta REAL,
                sample_count INTEGER,
                current_session TEXT,
                session_priority REAL,
                average_spread REAL,
                spread_quality TEXT,
                uncertainty REAL,
                error_percentage REAL,
                trade_permission TEXT,
                final_action TEXT,
                rank_score REAL,
                rank_reason TEXT,
                lock_status TEXT NOT NULL,
                locked_at_broker_time TEXT NOT NULL,
                last_reviewed_broker_time TEXT NOT NULL,
                next_review_broker_time TEXT,
                parent_run_id TEXT NOT NULL,
                run_id TEXT,
                source_id TEXT,
                PRIMARY KEY(broker_day, symbol)
            );
            CREATE INDEX IF NOT EXISTS idx_field10_daily_latest
                ON field10_daily_higher_lock(broker_day DESC, rank ASC);
            """
        )
        # Additive migrations for databases created by earlier Field 10 builds.
        additive_columns = {
            "multi_symbol_runs": {
                "current_session": "TEXT", "session_priority": "REAL", "average_spread": "REAL",
                "spread_quality": "TEXT", "uncertainty": "REAL", "error_percentage": "REAL",
                "trade_permission": "TEXT", "final_action": "TEXT",
            },
            "field10_hourly_quality": {
                "broker_date": "TEXT", "broker_hour": "TEXT", "current_session": "TEXT",
                "session_priority": "REAL", "average_spread": "REAL", "spread_quality": "TEXT",
                "uncertainty": "REAL", "error_percentage": "REAL", "trade_permission": "TEXT",
                "final_action": "TEXT", "rank_score": "REAL", "rank_reason": "TEXT",
                "higher_standard_bias": "TEXT",
            },
            "field10_daily_higher_lock": {
                "current_session": "TEXT", "session_priority": "REAL", "average_spread": "REAL",
                "spread_quality": "TEXT", "uncertainty": "REAL", "error_percentage": "REAL",
                "trade_permission": "TEXT", "final_action": "TEXT", "rank_score": "REAL",
                "rank_reason": "TEXT", "higher_standard_bias": "TEXT",
            },
        }
        for table, definitions in additive_columns.items():
            existing = {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
            for column, sql_type in definitions.items():
                if column not in existing:
                    conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {sql_type}")
        conn.commit()
    return {"ok": True, "path": str(path), "version": VERSION}


def _broker_timestamp(canonical: Mapping[str, Any], state: Mapping[str, Any]) -> pd.Timestamp:
    """Return the canonical broker-wall timestamp without silently converting it to UTC."""
    value: Any = None
    with suppress(Exception):
        from core.shared_broker_time_20260622 import shared_broker_time_provider
        contract = shared_broker_time_provider(state, canonical=dict(canonical))
        if bool(contract.get("broker_clock_available")):
            value = contract.get("broker_time") or contract.get("shared_broker_time")
    if value in (None, ""):
        value = canonical.get("broker_candle_time")
    if value in (None, ""):
        raise ValueError("Canonical broker candle timestamp is unavailable; Field 10 evidence was not fabricated")
    try:
        parsed = pd.Timestamp(value)
    except Exception as exc:
        raise ValueError(f"Canonical broker candle timestamp is invalid: {value!r}") from exc
    if pd.isna(parsed):
        raise ValueError("Canonical broker candle timestamp is invalid; Field 10 evidence was not fabricated")
    return parsed


def validate_fields_1_9(state: Mapping[str, Any], canonical: Mapping[str, Any] | None = None) -> list[dict[str, Any]]:
    """Read-only post-run integrity checks for Fields 1–9.

    The observer inspects already-published objects only.  It never imports a
    renderer, refreshes a connector, settles an outcome, or reruns a model.
    Status values are intentionally limited to PASS, WARNING, and FAIL.
    """
    canonical = dict(canonical or _canonical(state))
    expected_symbol = normalize_symbol(canonical.get("symbol") or state.get("symbol") or "EURUSD")
    expected_timeframe = str(canonical.get("timeframe") or state.get("timeframe") or "H1").upper()
    run_id = str(canonical.get("run_id") or canonical.get("canonical_calculation_id") or "")
    source_id = str(canonical.get("source_id") or canonical.get("data_source_id") or canonical.get("snapshot_hash") or "")
    canonical_candle_raw = canonical.get("broker_candle_time") or canonical.get("latest_completed_candle_time")
    canonical_candle = _broker_wall_timestamp_value(canonical_candle_raw)
    candidates: Mapping[int, tuple[str, ...]] = {
        1: ("lunch_metric_result_published_20260618", "full_metric_result_cache_20260618", "full_metric_history_df_20260618"),
        2: ("field2_quant_upgrade_20260629", "powerbi_projection_result_20260619", "powerbi_calibrated_bundle_20260617"),
        3: ("field3_regime_lifecycle_monitor_20260701", "regime_standard_detail_tables_published_20260618", "regime_standard_table_20260617"),
        4: ("field4to9_collection_history_full_20260628", "field4to9_collection_history_display_20260628"),
        5: ("canonical_ai_fact_pack_20260619", "compact_canonical_summary_20260619"),
        6: ("field6_quant_history_result_20260622", "field6_quant_history_20260622", "session_ai_field6_9_20260625"),
        7: ("field7_research_result_20260626", "field7_shadow_v13"),
        8: ("field8_integrated_history_result_20260624", "field8_integrated_history_20260624"),
        9: ("field9_research_result_20260626", "field9_decision_impact_result_20260624", "field9_eurusd_h1_decision_impact"),
    }

    def shape(value: Any) -> tuple[int, int, bool, str]:
        if isinstance(value, pd.DataFrame):
            return int(len(value)), int(len(value.columns)), not value.empty, "DataFrame"
        if isinstance(value, Mapping):
            ok_flag = value.get("ok")
            meaningful = any(v not in (None, "", [], {}) for k, v in value.items() if str(k).lower() not in {"ok", "status"})
            valid = bool(meaningful and ok_flag is not False)
            return int(value.get("rows") or len(value)), int(value.get("columns") or len(value)), valid, "Mapping"
        if isinstance(value, (list, tuple)):
            return len(value), 0, len(value) > 0, type(value).__name__
        return 0, 0, value not in (None, ""), type(value).__name__

    def first_value(mapping: Mapping[str, Any], names: tuple[str, ...]) -> Any:
        for name in names:
            if mapping.get(name) not in (None, ""):
                return mapping.get(name)
        return None

    rows: list[dict[str, Any]] = []
    for field, keys in candidates.items():
        selected_key = ""; selected_value: Any = None
        for key in keys:
            value = state.get(key)
            _, _, valid, _ = shape(value)
            if valid:
                selected_key, selected_value = key, value
                break
            if selected_value is None and value is not None:
                selected_key, selected_value = key, value
        row_count, column_count, valid, kind = shape(selected_value)
        failures: list[str] = []
        warnings: list[str] = []
        if not run_id:
            failures.append("canonical run_id missing")
        if not source_id:
            failures.append("canonical source/snapshot ID missing")
        if pd.isna(canonical_candle):
            failures.append("canonical completed broker candle missing or invalid")
        if not valid:
            failures.append("required saved result is empty or unavailable")

        published_symbol = expected_symbol
        published_timeframe = expected_timeframe
        if isinstance(selected_value, Mapping):
            published_symbol = normalize_symbol(first_value(selected_value, ("symbol", "identity.symbol")) or expected_symbol)
            published_timeframe = str(first_value(selected_value, ("timeframe", "identity.timeframe")) or expected_timeframe).upper()
            published_run = str(first_value(selected_value, ("run_id", "canonical_run_id", "identity.run_id")) or "")
            published_source = str(first_value(selected_value, ("source_id", "snapshot_hash", "source_snapshot_hash")) or "")
            published_candle_raw = first_value(selected_value, (
                "broker_candle_time", "latest_completed_candle_time", "completed_candle_time", "identity.latest_completed_candle",
            ))
            published_status = str(first_value(selected_value, ("calculation_status", "status")) or "").upper()
            if published_run and run_id and published_run != run_id:
                failures.append(f"run_id mismatch: {published_run}")
            if published_source and source_id and published_source != source_id:
                failures.append("source/snapshot mismatch")
            if published_candle_raw not in (None, "") and pd.notna(canonical_candle):
                published_candle = _broker_wall_timestamp_value(published_candle_raw)
                if pd.isna(published_candle):
                    warnings.append("published completed candle is invalid")
                elif published_candle != canonical_candle:
                    failures.append(f"completed-candle mismatch: {pd.Timestamp(published_candle).isoformat()}")
            if published_status in {"FAIL", "FAILED", "ERROR"}:
                failures.append(f"published calculation status={published_status}")
            elif published_status in {"PARTIAL", "WARNING", "STALE", "INSUFFICIENT_DATA"}:
                warnings.append(f"published calculation status={published_status}")

        if published_symbol != expected_symbol:
            failures.append(f"symbol mismatch: {published_symbol}")
        if published_timeframe != expected_timeframe:
            failures.append(f"timeframe mismatch: {published_timeframe}")

        if isinstance(selected_value, pd.DataFrame) and not selected_value.empty:
            time_column = next((column for column in selected_value.columns if any(token in str(column).lower() for token in ("broker time", "timestamp", "candle time"))), None)
            if time_column is not None:
                parsed = _broker_wall_series(selected_value[time_column])
                invalid_count = int(parsed.isna().sum())
                duplicate_count = int(parsed.dropna().duplicated().sum())
                if invalid_count:
                    warnings.append(f"{invalid_count} invalid timestamp row(s)")
                if duplicate_count:
                    warnings.append(f"{duplicate_count} duplicate timestamp row(s)")
            all_null = [str(column) for column in selected_value.columns if selected_value[column].isna().all()]
            if all_null:
                warnings.append(f"all-null columns: {', '.join(all_null[:4])}")

        status = "FAIL" if failures else ("WARNING" if warnings else "PASS")
        messages = failures + warnings
        rows.append({
            "Field": field, "Status": status, "Result Key": selected_key or "-",
            "Object Type": kind, "Row Count": row_count, "Column Count": column_count,
            "Symbol": expected_symbol, "Timeframe": expected_timeframe, "Run ID": run_id,
            "Source ID": source_id, "Completed Broker Candle": pd.Timestamp(canonical_candle).isoformat() if pd.notna(canonical_candle) else "",
            "Validation Message": "; ".join(messages) or "saved result is non-empty, identity-compatible, and linked to the canonical completed candle",
        })
    return rows


def _persist_symbol_evidence(
    state: MutableMapping[str, Any], *, parent_run_id: str, child_run_id: str,
    scope: str, status: Mapping[str, Any], elapsed: float, rss_delta_mb: float,
    cpu_seconds: float, path: Path | str = DB_PATH,
) -> dict[str, Any]:
    migrate_database(path)
    canonical = dict(_canonical(state))
    symbol = normalize_symbol(canonical.get("symbol") or state.get("symbol") or "EURUSD")
    quality = assess_data_quality(state, canonical)
    daily = _daily_higher_snapshot(state, canonical)
    hourly = _hourly_history(state, canonical, quality)
    broker_time = _broker_timestamp(canonical, state)
    broker_day = broker_time.strftime("%Y-%m-%d")
    current_hour = int(broker_time.hour)
    execution_context = _session_execution_context(state, canonical, broker_time)
    source_id = str(quality.get("source_id") or "")
    run_id = str(canonical.get("run_id") or canonical.get("canonical_calculation_id") or "")
    child_status = "COMPLETED" if bool((status.get("canonical") or {}).get("ok") or status.get("ok") or canonical) else "PARTIAL"
    created = pd.Timestamp.now(tz="UTC").isoformat()

    with sqlite3.connect(str(path), timeout=30) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute(
                """INSERT OR REPLACE INTO multi_symbol_runs(
                    parent_run_id,child_run_id,symbol,timeframe,scope,status,elapsed_seconds,
                    rss_delta_mb,cpu_seconds,canonical_run_id,source_id,completed_candle,
                    current_session,session_priority,average_spread,spread_quality,uncertainty,error_percentage,
                    trade_permission,final_action,error,created_at
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (parent_run_id, child_run_id, symbol, str(canonical.get("timeframe") or "H1"), scope,
                 child_status, float(elapsed), float(rss_delta_mb), float(cpu_seconds), run_id,
                 source_id, str(canonical.get("latest_completed_candle_time") or canonical.get("broker_candle_time") or ""),
                 str(execution_context.get("current_session") or "UNAVAILABLE"),
                 float(execution_context.get("session_priority") or 0.0),
                 execution_context.get("average_spread"), str(execution_context.get("spread_quality") or "UNAVAILABLE"),
                 execution_context.get("uncertainty"), execution_context.get("error_percentage"),
                 str(execution_context.get("trade_permission") or "CHECK"),
                 str(execution_context.get("final_action") or "WAIT"),
                 str(status.get("error") or ""), created),
            )
            for row in hourly.to_dict("records"):
                ts = _broker_wall_timestamp_value(row.get("Broker Timestamp"))
                if pd.isna(ts):
                    continue
                conn.execute(
                    """INSERT OR REPLACE INTO field10_hourly_quality(
                        parent_run_id,symbol,timeframe,broker_timestamp,rank,data_quality_grade,
                        data_quality_score,higher_standard_regime,higher_standard_bias,less_risky_bias,trust_score,
                        reliability,validation_status,quality_reason,broker_date,broker_hour,current_session,
                        session_priority,average_spread,spread_quality,uncertainty,error_percentage,
                        trade_permission,final_action,rank_score,rank_reason,run_id,source_id,created_at
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (parent_run_id, symbol, str(row.get("Timeframe") or "H1"), pd.Timestamp(ts).isoformat(), None,
                     str(row.get("Data Quality") or "D"), float(row.get("Data Quality Score") or 0),
                     str(row.get("Higher Standard Regime") or "UNKNOWN"), str(row.get("Higher-Standard Bias") or "WAIT"),
                     str(row.get("Less-Risky Bias") or "WAIT"),
                     None if pd.isna(row.get("Trust Score")) else float(row.get("Trust Score")),
                     None if pd.isna(row.get("Reliability")) else float(row.get("Reliability")),
                     str(row.get("Validation Status") or "CHECK"), str(row.get("Quality Reason") or ""),
                     str(row.get("Broker Date") or pd.Timestamp(ts).strftime("%Y-%m-%d")),
                     str(row.get("Broker Hour") or pd.Timestamp(ts).strftime("%H:%M")),
                     str(row.get("Current Session") or "UNAVAILABLE"),
                     None if pd.isna(row.get("Session Priority")) else float(row.get("Session Priority")),
                     None if pd.isna(row.get("Average Spread")) else float(row.get("Average Spread")),
                     str(row.get("Spread Quality") or "UNAVAILABLE"),
                     None if pd.isna(row.get("Uncertainty")) else float(row.get("Uncertainty")),
                     None if pd.isna(row.get("Error Percentage")) else float(row.get("Error Percentage")),
                     str(row.get("Trade Permission") or "CHECK"), str(row.get("Final Action") or "WAIT"),
                     None, "pending deterministic rank",
                     str(row.get("Run ID") or run_id), str(row.get("Source ID") or source_id), created),
                )

            existing = conn.execute(
                "SELECT locked_at_broker_time FROM field10_daily_higher_lock WHERE broker_day=? AND symbol=?",
                (broker_day, symbol),
            ).fetchone()
            # Before broker 23:00, today's first published value remains immutable.
            # At/after 23:00 the day-end review may update it from the final completed H1 evidence.
            may_write = existing is None or current_hour >= 23
            if may_write:
                lock_status = "DAY_END_REVIEW_23H" if current_hour >= 23 else "TODAY_LOCKED_UNTIL_23H"
                locked_at = existing[0] if existing else broker_time.isoformat()
                conn.execute(
                    """INSERT OR REPLACE INTO field10_daily_higher_lock(
                        broker_day,symbol,rank,higher_standard_regime,higher_standard_bias,less_risky_bias,
                        data_quality_grade,data_quality_score,higher_reliability,
                        higher_transition_risk,higher_alpha,higher_delta,sample_count,
                        current_session,session_priority,average_spread,spread_quality,uncertainty,error_percentage,
                        trade_permission,final_action,rank_score,rank_reason,
                        lock_status,locked_at_broker_time,last_reviewed_broker_time,
                        next_review_broker_time,parent_run_id,run_id,source_id
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (broker_day, symbol, None, str(daily.get("higher_regime") or "UNKNOWN"),
                     str(daily.get("higher_standard_bias") or "WAIT"), str(daily.get("less_risky_bias") or "WAIT"),
                     str(quality.get("grade") or "D"),
                     float(quality.get("score") or 0), float(daily.get("higher_reliability") or 0),
                     float(daily.get("higher_transition_risk") or 0), float(daily.get("higher_alpha") or 0),
                     float(daily.get("higher_delta") or 0), int(daily.get("sample_count") or 0),
                     str(execution_context.get("current_session") or "UNAVAILABLE"),
                     float(execution_context.get("session_priority") or 0.0),
                     execution_context.get("average_spread"), str(execution_context.get("spread_quality") or "UNAVAILABLE"),
                     execution_context.get("uncertainty"), execution_context.get("error_percentage"),
                     str(execution_context.get("trade_permission") or "CHECK"),
                     str(execution_context.get("final_action") or daily.get("less_risky_bias") or "WAIT"),
                     None, "pending deterministic rank",
                     lock_status, locked_at, broker_time.isoformat(), str(daily.get("next_review_broker_time") or ""),
                     parent_run_id, run_id, source_id),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    return {
        "symbol": symbol, "status": child_status, "quality": quality, "daily": daily,
        "hourly_rows": int(len(hourly)), "broker_day": broker_day,
        "broker_time": broker_time.isoformat(), "run_id": run_id, "source_id": source_id,
        "field_validation": validate_fields_1_9(state, canonical),
    }


def _rank_persisted_rows(parent_run_id: str, broker_day: str, path: Path | str = DB_PATH) -> None:
    """Apply deterministic eligibility-first ranking to persisted Field 10 rows."""
    with sqlite3.connect(str(path), timeout=30) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            rows = conn.execute(
                """SELECT symbol,broker_timestamp,data_quality_score,COALESCE(trust_score,0),
                          COALESCE(reliability,0),COALESCE(session_priority,0),
                          COALESCE(spread_quality,'UNAVAILABLE'),COALESCE(uncertainty,0),
                          COALESCE(error_percentage,0),COALESCE(trade_permission,'CHECK')
                   FROM field10_hourly_quality WHERE parent_run_id=?""",
                (parent_run_id,),
            ).fetchall()
            if rows:
                frame = pd.DataFrame(rows, columns=[
                    "symbol", "broker_timestamp", "quality", "trust", "reliability",
                    "session_priority", "spread_quality", "uncertainty", "error", "permission",
                ])
                for column in ("quality", "trust", "reliability", "session_priority", "uncertainty", "error"):
                    frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
                for column in ("trust", "reliability", "session_priority", "uncertainty", "error"):
                    mask = frame[column].abs().le(1.0) & frame[column].ne(0)
                    frame.loc[mask, column] = frame.loc[mask, column] * 100.0
                spread_scores = {"LOW": 100.0, "GOOD": 90.0, "AVERAGE": 70.0, "MEDIUM": 65.0, "HIGH": 35.0, "VERY HIGH": 10.0, "UNAVAILABLE": 40.0}
                frame["spread_score"] = frame["spread_quality"].astype(str).str.upper().map(spread_scores).fillna(50.0)
                permission_scores = {"ALLOWED": 2.0, "TRADE ALLOWED": 2.0, "CAUTION": 1.0, "CHECK": 1.0, "BLOCKED": 0.0, "NO TRADE": 0.0}
                frame["eligibility"] = frame["permission"].astype(str).str.upper().map(permission_scores).fillna(1.0)
                frame["rank_score"] = (
                    frame["quality"] * 0.35 + frame["trust"] * 0.15 + frame["reliability"] * 0.20
                    + frame["session_priority"] * 0.15 + frame["spread_score"] * 0.15
                    - frame["uncertainty"].clip(lower=0) * 0.05 - frame["error"].clip(lower=0) * 0.05
                ).clip(0.0, 100.0)
                frame = frame.sort_values(
                    ["broker_timestamp", "eligibility", "rank_score", "quality", "reliability", "uncertainty", "symbol"],
                    ascending=[True, False, False, False, False, True, True], kind="mergesort",
                )
                frame["rank"] = np.nan
                eligible_mask = frame["eligibility"].gt(0.0)
                frame.loc[eligible_mask, "rank"] = (
                    frame.loc[eligible_mask].groupby("broker_timestamp", sort=False).cumcount() + 1
                )
                for row in frame.itertuples(index=False):
                    is_ranked = pd.notna(row.rank)
                    reason = (
                        f"eligibility={row.permission}; quality={row.quality:.1f}; reliability={row.reliability:.1f}; "
                        f"session={row.session_priority:.1f}; spread={row.spread_quality}; "
                        f"uncertainty={row.uncertainty:.1f}; error={row.error:.1f}"
                    )
                    if not is_ranked:
                        reason = "UNRANKED — failed or blocked symbols are excluded from the eligible rank pool; " + reason
                    conn.execute(
                        "UPDATE field10_hourly_quality SET rank=?,rank_score=?,rank_reason=? WHERE parent_run_id=? AND symbol=? AND broker_timestamp=?",
                        (int(row.rank) if is_ranked else None, float(row.rank_score), reason, parent_run_id, str(row.symbol), str(row.broker_timestamp)),
                    )
            daily = conn.execute(
                """SELECT symbol,data_quality_score,COALESCE(higher_reliability,0),
                          COALESCE(session_priority,0),COALESCE(spread_quality,'UNAVAILABLE'),
                          COALESCE(uncertainty,0),COALESCE(error_percentage,0),COALESCE(trade_permission,'CHECK')
                   FROM field10_daily_higher_lock WHERE broker_day=?""",
                (broker_day,),
            ).fetchall()
            if daily:
                d = pd.DataFrame(daily, columns=[
                    "symbol", "quality", "reliability", "session_priority", "spread_quality",
                    "uncertainty", "error", "permission",
                ])
                for column in ("quality", "reliability", "session_priority", "uncertainty", "error"):
                    d[column] = pd.to_numeric(d[column], errors="coerce").fillna(0.0)
                for column in ("reliability", "session_priority", "uncertainty", "error"):
                    mask = d[column].abs().le(1.0) & d[column].ne(0)
                    d.loc[mask, column] = d.loc[mask, column] * 100.0
                spread_scores = {"LOW": 100.0, "GOOD": 90.0, "AVERAGE": 70.0, "MEDIUM": 65.0, "HIGH": 35.0, "VERY HIGH": 10.0, "UNAVAILABLE": 40.0}
                permission_scores = {"ALLOWED": 2.0, "TRADE ALLOWED": 2.0, "CAUTION": 1.0, "CHECK": 1.0, "BLOCKED": 0.0, "NO TRADE": 0.0}
                d["spread_score"] = d["spread_quality"].astype(str).str.upper().map(spread_scores).fillna(50.0)
                d["eligibility"] = d["permission"].astype(str).str.upper().map(permission_scores).fillna(1.0)
                d["rank_score"] = (
                    d["quality"] * 0.40 + d["reliability"] * 0.25
                    + d["session_priority"] * 0.15 + d["spread_score"] * 0.20
                    - d["uncertainty"] * 0.05 - d["error"] * 0.05
                ).clip(0.0, 100.0)
                d = d.sort_values(
                    ["eligibility", "rank_score", "quality", "reliability", "uncertainty", "symbol"],
                    ascending=[False, False, False, False, True, True], kind="mergesort",
                ).reset_index(drop=True)
                d["rank"] = np.nan
                eligible_mask = d["eligibility"].gt(0.0)
                d.loc[eligible_mask, "rank"] = np.arange(1, int(eligible_mask.sum()) + 1)
                for row in d.itertuples(index=False):
                    is_ranked = pd.notna(row.rank)
                    reason = (
                        f"eligibility={row.permission}; quality={row.quality:.1f}; reliability={row.reliability:.1f}; "
                        f"session={row.session_priority:.1f}; spread={row.spread_quality}"
                    )
                    if not is_ranked:
                        reason = "UNRANKED — failed or blocked symbols are excluded from the eligible rank pool; " + reason
                    conn.execute(
                        "UPDATE field10_daily_higher_lock SET rank=?,rank_score=?,rank_reason=? WHERE broker_day=? AND symbol=?",
                        (int(row.rank) if is_ranked else None, float(row.rank_score), reason, broker_day, str(row.symbol)),
                    )
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def load_field10_tables(
    state: MutableMapping[str, Any] | None = None, *, parent_run_id: str | None = None,
    symbol: str | None = None, path: Path | str = DB_PATH,
) -> dict[str, pd.DataFrame]:
    migrate_database(path)
    state = state if state is not None else {}
    manifest = state.get(MANIFEST_KEY) if isinstance(state.get(MANIFEST_KEY), Mapping) else {}
    parent_run_id = str(parent_run_id or manifest.get("parent_run_id") or state.get(PARENT_RUN_KEY) or "")
    symbol = normalize_symbol(symbol or state.get(ACTIVE_KEY) or state.get("symbol") or "EURUSD")
    with sqlite3.connect(str(path), timeout=30) as conn:
        if parent_run_id:
            summary = pd.read_sql_query(
                """SELECT symbol AS Symbol,timeframe AS Timeframe,status AS Status,status AS [Calculation Status],elapsed_seconds AS [Elapsed Seconds],
                rss_delta_mb AS [RSS Delta MB],cpu_seconds AS [CPU Seconds],canonical_run_id AS [Run ID],canonical_run_id AS [Canonical Run ID],
                source_id AS [Source ID],completed_candle AS [Completed Candle],
                current_session AS [Current Session],session_priority AS [Session Priority],
                average_spread AS [Average Spread],spread_quality AS [Spread Quality],
                uncertainty AS Uncertainty,error_percentage AS [Error Percentage],
                trade_permission AS [Trade Permission],final_action AS [Final Action],error AS Error
                FROM multi_symbol_runs WHERE parent_run_id=? ORDER BY status DESC,symbol""",
                conn, params=(parent_run_id,),
            )
            hourly = pd.read_sql_query(
                """SELECT broker_date AS [Broker Date],broker_hour AS [Broker Hour],
                broker_timestamp AS [Broker Timestamp],rank AS Rank,rank_score AS [Rank Score],symbol AS Symbol,
                data_quality_grade AS [Data Quality],data_quality_score AS [Data Quality Score],
                higher_standard_regime AS [Higher Standard Regime],higher_standard_bias AS [Higher-Standard Bias],less_risky_bias AS [Less-Risky Bias],
                current_session AS [Current Session],session_priority AS [Session Priority],
                average_spread AS [Average Spread],spread_quality AS [Spread Quality],
                uncertainty AS Uncertainty,error_percentage AS [Error Percentage],
                trade_permission AS [Trade Permission],final_action AS [Final Action],
                trust_score AS [Trust Score],reliability AS Reliability,validation_status AS [Validation Status],
                quality_reason AS [Quality Reason],rank_reason AS [Rank Reason],run_id AS [Run ID],source_id AS [Source ID]
                FROM field10_hourly_quality WHERE parent_run_id=? AND symbol=?
                ORDER BY broker_timestamp DESC LIMIT 600""",
                conn, params=(parent_run_id, symbol),
            )
        else:
            summary = pd.DataFrame(); hourly = pd.DataFrame()
        latest_day_row = conn.execute("SELECT MAX(broker_day) FROM field10_daily_higher_lock").fetchone()
        latest_day = str(latest_day_row[0] or "") if latest_day_row else ""
        daily = pd.read_sql_query(
            """SELECT broker_day AS [Broker Day],rank AS Rank,rank_score AS [Rank Score],symbol AS Symbol,
            higher_standard_regime AS [Higher Standard Regime],higher_standard_bias AS [Higher-Standard Bias],less_risky_bias AS [Less-Risky Bias],
            data_quality_grade AS [Data Quality],data_quality_score AS [Data Quality Score],
            higher_reliability AS [Higher Reliability],higher_transition_risk AS [Transition Risk],
            higher_alpha AS Alpha,higher_delta AS Delta,sample_count AS [Sample Count],
            current_session AS [Current Session],session_priority AS [Session Priority],
            average_spread AS [Average Spread],spread_quality AS [Spread Quality],
            uncertainty AS Uncertainty,error_percentage AS [Error Percentage],
            trade_permission AS [Trade Permission],final_action AS [Final Action],rank_reason AS [Rank Reason],
            lock_status AS [Lock Status],locked_at_broker_time AS [Locked At],
            last_reviewed_broker_time AS [Last Reviewed],next_review_broker_time AS [Next Review],
            run_id AS [Run ID],source_id AS [Source ID]
            FROM field10_daily_higher_lock WHERE broker_day=? ORDER BY rank ASC,symbol""",
            conn, params=(latest_day,),
        ) if latest_day else pd.DataFrame()
    if not summary.empty and not daily.empty:
        merge_columns = [
            "Symbol", "Rank", "Rank Score", "Data Quality", "Data Quality Score",
            "Higher Standard Regime", "Higher-Standard Bias", "Less-Risky Bias", "Higher Reliability",
            "Current Session", "Session Priority", "Average Spread", "Spread Quality",
            "Uncertainty", "Error Percentage", "Trade Permission", "Final Action", "Rank Reason",
        ]
        # Prefer the daily locked table for rank/regime; keep run-level execution columns when duplicate.
        summary = summary.drop(columns=[c for c in merge_columns if c != "Symbol" and c in summary.columns], errors="ignore")
        summary = summary.merge(daily[[c for c in merge_columns if c in daily.columns]], on="Symbol", how="left")
        first = [
            "Rank", "Rank Score", "Symbol", "Status", "Data Quality", "Data Quality Score",
            "Higher Standard Regime", "Higher-Standard Bias", "Less-Risky Bias", "Final Action", "Trade Permission",
            "Current Session", "Session Priority", "Average Spread", "Spread Quality",
            "Higher Reliability", "Uncertainty", "Error Percentage",
        ]
        summary = summary[[c for c in first if c in summary] + [c for c in summary.columns if c not in first]]
    for frame in (summary, daily, hourly):
        if not frame.empty and "Rank Score" in frame.columns:
            score = pd.to_numeric(frame["Rank Score"], errors="coerce")
            permission = frame["Trade Permission"].astype(str).str.upper() if "Trade Permission" in frame.columns else pd.Series("CHECK", index=frame.index)
            frame["Rank Grade"] = np.select(
                [permission.isin(["BLOCKED", "NO TRADE"]), score.ge(90), score.ge(75), score.ge(60)],
                ["UNRANKED", "A", "B", "C"], default="D",
            )
    if not summary.empty and "Completed Candle" in summary.columns:
        completed = _broker_wall_series(summary["Completed Candle"])
        summary.insert(min(2, len(summary.columns)), "Date", completed.dt.strftime("%Y-%m-%d"))
        summary.insert(min(3, len(summary.columns)), "Broker Candle Time", completed.dt.strftime("%H:%M"))
    if state is not None:
        state[FIELD10_SUMMARY_KEY] = summary
        state[FIELD10_DAILY_KEY] = daily
        state[FIELD10_HOURLY_KEY] = hourly
    return {"summary": summary, "daily": daily, "hourly": hourly}


def _progress_snapshot(parent_run_id: str, selected: Sequence[str], statuses: Mapping[str, Mapping[str, Any]], current: str = "", stage: str = "") -> dict[str, Any]:
    completed = sum(1 for item in statuses.values() if item.get("status") == "COMPLETED")
    failed = sum(1 for item in statuses.values() if item.get("status") == "FAILED")
    total = max(1, len(selected))
    return {
        "parent_run_id": parent_run_id, "selected_symbols": list(selected),
        "overall_percent": round(100 * (completed + failed) / total, 1),
        "current_symbol": current, "current_stage": stage,
        "completed_symbols": completed, "failed_symbols": failed,
        "remaining_symbols": max(0, total - completed - failed),
        "symbols": {key: dict(value) for key, value in statuses.items()},
        "updated_at": pd.Timestamp.now(tz="UTC").isoformat(),
    }


def _run_selected_symbols_impl(
    state: MutableMapping[str, Any], single_symbol_runner: Callable[[], Mapping[str, Any]], *,
    scope: str = "FULL", progress_callback: Callable[[Mapping[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Implementation for the guarded public multi-symbol transaction."""
    selected = selected_symbols(state)
    if not selected:
        return {"ok": False, "status": "NO_SYMBOLS_SELECTED", "error": "Select at least one instrument."}
    scope = str(scope or "FULL").upper()
    fingerprint = sha256((scope + "|" + "|".join(selected)).encode()).hexdigest()[:16]
    previous_manifest = state.get(MANIFEST_KEY)

    parent_run_id = f"MS-{pd.Timestamp.now(tz='UTC').strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    state[PARENT_RUN_KEY] = parent_run_id
    started = time.perf_counter()
    process = None
    with suppress(Exception):
        import psutil
        process = psutil.Process(os.getpid())
    original_rss = float(process.memory_info().rss) if process else 0.0
    original_cpu = float(sum(process.cpu_times()[:2])) if process else 0.0
    statuses: dict[str, dict[str, Any]] = {symbol: {"status": "WAITING", "percent": 0, "stage": "Queued"} for symbol in selected}
    resource_rows: list[dict[str, Any]] = []
    summaries: dict[str, Any] = {}
    last_status: dict[str, Any] = {}
    latest_broker_day = ""

    def publish(current: str = "", stage: str = "") -> None:
        snapshot = _progress_snapshot(parent_run_id, selected, statuses, current, stage)
        elapsed_now = time.perf_counter() - started
        processed = int(snapshot.get("completed_symbols") or 0) + int(snapshot.get("failed_symbols") or 0)
        remaining = int(snapshot.get("remaining_symbols") or 0)
        eta = (elapsed_now / processed * remaining) if processed > 0 else None
        snapshot["elapsed_seconds"] = round(elapsed_now, 2)
        snapshot["estimated_remaining_seconds"] = round(eta, 2) if eta is not None else None
        state[PROGRESS_KEY] = snapshot
        if progress_callback:
            progress_callback(snapshot)

    publish(stage="Validating selected instruments")
    for index, symbol in enumerate(selected, start=1):
        child_started = time.perf_counter()
        child_rss = float(process.memory_info().rss) if process else 0.0
        child_cpu = float(sum(process.cpu_times()[:2])) if process else 0.0
        child_id = f"{parent_run_id}:{symbol}"
        statuses[symbol] = {"status": "RUNNING", "percent": 5, "stage": "Loading symbol context", "child_run_id": child_id}
        publish(symbol, "Loading symbol context")
        try:
            cached = activate_symbol_result(state, symbol)
            if not cached.get("ok"):
                clear_active_symbol_results(state)
                state["symbol"] = symbol; state["selected_symbol"] = symbol; state["ws_symbol"] = symbol
            state[CHILD_RUN_KEY] = True
            state["multi_symbol_current_child_id_20260701"] = child_id
            state["multi_symbol_current_index_20260701"] = index
            state["multi_symbol_current_total_20260701"] = len(selected)
            statuses[symbol].update({"percent": 20, "stage": "Refreshing source and running Fields 1-9"})
            publish(symbol, "Refreshing source and running Fields 1-9")
            result = single_symbol_runner()
            result = dict(result) if isinstance(result, Mapping) else {"ok": False, "error": "Single-symbol runner returned no status"}
            last_status = result
            statuses[symbol].update({"percent": 88, "stage": "Validating and publishing Field 10"})
            publish(symbol, "Validating and publishing Field 10")
            elapsed = time.perf_counter() - child_started
            rss_delta = ((float(process.memory_info().rss) if process else child_rss) - child_rss) / (1024 * 1024)
            cpu_delta = (float(sum(process.cpu_times()[:2])) if process else child_cpu) - child_cpu
            evidence = _persist_symbol_evidence(
                state, parent_run_id=parent_run_id, child_run_id=child_id, scope=scope,
                status=result, elapsed=elapsed, rss_delta_mb=rss_delta, cpu_seconds=cpu_delta,
            )
            latest_broker_day = str(evidence.get("broker_day") or latest_broker_day)
            summaries[symbol] = evidence
            from core.runtime_state_cache_20260628 import save_runtime_state
            cache_report = save_runtime_state(state, status=result, scope=scope, path=_cache_path(symbol))
            completed = evidence.get("status") == "COMPLETED" and bool(cache_report.get("ok"))
            statuses[symbol].update({
                "status": "COMPLETED" if completed else "PARTIAL",
                "percent": 100, "stage": "Completed" if completed else "Saved with validation warnings",
                "elapsed_seconds": round(elapsed, 3), "data_quality": evidence.get("quality", {}).get("grade"),
                "cache_bytes": cache_report.get("bytes", 0),
            })
            resource_rows.append({
                "Symbol": symbol, "Elapsed Seconds": round(elapsed, 3),
                "RSS Delta MB": round(rss_delta, 3), "CPU Seconds": round(cpu_delta, 3),
                "Cache MB": round(float(cache_report.get("bytes") or 0) / (1024 * 1024), 3),
                "Status": statuses[symbol]["status"],
            })
        except Exception as exc:
            elapsed = time.perf_counter() - child_started
            statuses[symbol].update({
                "status": "FAILED", "percent": 100, "stage": "Failed",
                "elapsed_seconds": round(elapsed, 3), "error": f"{type(exc).__name__}: {exc}",
            })
            resource_rows.append({"Symbol": symbol, "Elapsed Seconds": round(elapsed, 3), "RSS Delta MB": 0.0, "CPU Seconds": 0.0, "Cache MB": 0.0, "Status": "FAILED"})
        finally:
            state.pop(CHILD_RUN_KEY, None)
            publish(symbol, statuses[symbol].get("stage", "Complete"))

    if latest_broker_day:
        with suppress(Exception):
            _rank_persisted_rows(parent_run_id, latest_broker_day)
    active = normalize_symbol(state.get(ACTIVE_KEY) or state.get("symbol") or selected[0])
    if active not in selected or statuses.get(active, {}).get("status") == "FAILED":
        active = next((symbol for symbol in selected if statuses.get(symbol, {}).get("status") in {"COMPLETED", "PARTIAL"}), selected[0])
    activation = activate_symbol_result(state, active)
    tables = load_field10_tables(state, parent_run_id=parent_run_id, symbol=active)
    elapsed_total = time.perf_counter() - started
    final_rss = float(process.memory_info().rss) if process else original_rss
    final_cpu = float(sum(process.cpu_times()[:2])) if process else original_cpu
    resource_report = {
        "rows": resource_rows,
        "total_elapsed_seconds": round(elapsed_total, 3),
        "rss_delta_mb": round((final_rss - original_rss) / (1024 * 1024), 3),
        "cpu_seconds": round(final_cpu - original_cpu, 3),
        "symbols": len(selected),
        "heat_proxy": "HIGH" if (final_cpu - original_cpu) > 180 else ("MODERATE" if (final_cpu - original_cpu) > 45 else "LOW"),
        "heat_proxy_note": "CPU-time proxy only; the application cannot read device temperature sensors on Streamlit Cloud.",
    }
    state[LAST_RESOURCE_KEY] = resource_report
    completed = sum(1 for item in statuses.values() if item.get("status") == "COMPLETED")
    failed = sum(1 for item in statuses.values() if item.get("status") == "FAILED")
    manifest = {
        **last_status,
        "ok": completed > 0,
        "status": "COMPLETED" if failed == 0 and completed == len(selected) else ("PARTIAL" if completed else "FAILED"),
        "parent_run_id": parent_run_id,
        "selection_fingerprint": fingerprint,
        "selected_symbols": selected,
        "active_symbol": active,
        "symbol_status": statuses,
        "symbol_summaries": summaries,
        "completed_symbols": completed,
        "failed_symbols": failed,
        "calculation_scope": scope,
        "elapsed_seconds": round(elapsed_total, 3),
        "activation": activation,
        "field10_rows": {name: int(len(frame)) for name, frame in tables.items()},
        "resource_report": resource_report,
        "version": VERSION,
    }
    state[MANIFEST_KEY] = manifest
    state[PROGRESS_KEY] = {**_progress_snapshot(parent_run_id, selected, statuses, active, "Completed"), "elapsed_seconds": round(elapsed_total, 2)}
    return manifest


def run_selected_symbols(
    state: MutableMapping[str, Any], single_symbol_runner: Callable[[], Mapping[str, Any]], *,
    scope: str = "FULL", progress_callback: Callable[[Mapping[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Run selected symbols once with duplicate-click and cleanup protection."""
    previous_manifest = state.get(MANIFEST_KEY)
    if bool(state.get(RUNNING_KEY)):
        if isinstance(previous_manifest, Mapping):
            return {**dict(previous_manifest), "duplicate_click_ignored": True}
        return {"ok": False, "status": "ALREADY_RUNNING", "duplicate_click_ignored": True}
    state[RUNNING_KEY] = True
    try:
        return _run_selected_symbols_impl(
            state, single_symbol_runner, scope=scope, progress_callback=progress_callback
        )
    finally:
        state.pop(RUNNING_KEY, None)


__all__ = [
    "VERSION", "SUPPORTED_SYMBOLS", "PROVIDER_ALIASES", "SELECTED_KEY", "ACTIVE_KEY",
    "MANIFEST_KEY", "PROGRESS_KEY", "CHILD_RUN_KEY", "PARENT_RUN_KEY",
    "LAST_RESOURCE_KEY", "RUNNING_KEY", "FIELD10_SUMMARY_KEY", "FIELD10_DAILY_KEY", "FIELD10_HOURLY_KEY",
    "DB_PATH", "normalize_symbol", "normalize_selected", "selected_symbols",
    "resolve_provider_symbol", "grade_from_score", "assess_data_quality", "validate_fields_1_9",
    "activate_symbol_result", "clear_active_symbol_results", "migrate_database",
    "load_field10_tables", "run_selected_symbols",
]
