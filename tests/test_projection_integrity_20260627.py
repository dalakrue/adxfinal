from __future__ import annotations

import pandas as pd
from core.canonical_identity_20260627 import CanonicalIntegrityError, parse_completed_broker_candle
from ui.powerbi_cached_renderer_20260619 import evaluate_projection_integrity


def canonical(stamp="2026-06-27T10:00:00+00:00"):
    return {
        "run_id": "run-1", "generation_id": "gen-1", "symbol": "EURUSD", "timeframe": "H1",
        "completed_broker_candle": stamp, "source_snapshot_hash": "hash-1", "source_signature": "sig-1",
    }


def bundle(stamp="2026-06-27T10:00:00+00:00"):
    identity = canonical(stamp)
    return {
        **identity,
        "summary": {**identity, "anchor_price": 1.17},
        "main": pd.DataFrame({"time": pd.to_datetime(["2026-06-27T11:00:00Z", "2026-06-27T12:00:00Z"]), "path": [1.171, 1.172]}),
    }


def market():
    return pd.DataFrame({"time": pd.to_datetime(["2026-06-27T09:00:00Z", "2026-06-27T10:00:00Z"]), "close": [1.16, 1.17]})


def test_valid_exact_run_projection():
    result = evaluate_projection_integrity({}, market(), bundle(), pd.DataFrame(), canonical())
    assert result["state"] == "VALID" and result["valid"] is True


def test_invalid_timestamp_is_not_valid():
    result = evaluate_projection_integrity({}, market(), bundle(), pd.DataFrame(), canonical("not-a-time"))
    assert result["state"] == "INVALID_TIMESTAMP" and result["valid"] is False


def test_nat_and_non_h1_rejected():
    for value in (pd.NaT, "2026-06-27T10:30:00+00:00"):
        try:
            parse_completed_broker_candle(value)
        except CanonicalIntegrityError:
            pass
        else:
            raise AssertionError("invalid completed candle was accepted")


def test_identity_mismatch_is_blocked_without_stale_fallback():
    item = bundle()
    item["run_id"] = "old-run"
    result = evaluate_projection_integrity({}, market(), item, pd.DataFrame(), canonical())
    assert result["state"] == "IDENTITY_MISMATCH"
    assert result["valid"] is False


def test_missing_central_path_is_path_unavailable():
    item = bundle()
    item["main"] = pd.DataFrame()
    result = evaluate_projection_integrity({}, market(), item, pd.DataFrame(), canonical())
    assert result["state"] == "PATH_UNAVAILABLE"


def test_project_broker_display_timestamp_is_valid_and_not_local_pc_time():
    stamp = parse_completed_broker_candle("2026-06-22 07:00:00 (Broker UTC+3)")
    assert stamp == pd.Timestamp("2026-06-22T04:00:00Z")


def test_invalid_project_broker_display_offset_is_rejected():
    try:
        parse_completed_broker_candle("2026-06-22 07:00:00 (Broker UTC+99)")
    except CanonicalIntegrityError:
        pass
    else:
        raise AssertionError("invalid broker offset was accepted")
