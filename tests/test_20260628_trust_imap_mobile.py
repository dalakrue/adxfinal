from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd

from core.mobile_lite_mode_20260628 import bounded_frame, set_mobile_mode
from research_quant.imap_rv_20260628 import PROTECTIVE_ACTIONS, run_imap_rv
from ui.lunch_unified_trust_history_20260628 import (
    ALLOWED_PROTECTIVE_ACTIONS,
    build_unified_lunch_trust_history,
)


def _data(n: int = 840):
    idx = pd.date_range("2026-05-01", periods=n, freq="h", tz="UTC")
    rng = np.random.default_rng(20260628)
    returns = rng.normal(0.0, 0.00045, n) + np.sin(np.arange(n) / 45.0) * 0.00008
    close = 1.16 * np.cumprod(1.0 + returns)
    open_ = np.r_[close[0], close[:-1]]
    ohlc = pd.DataFrame(
        {
            "Time": idx,
            "Open": open_,
            "High": np.maximum(open_, close) + 0.0002,
            "Low": np.minimum(open_, close) - 0.0002,
            "Close": close,
            "Volume": rng.integers(100, 2000, n),
        }
    )
    decisions = pd.DataFrame(
        {
            "Broker Candle Time": idx,
            "Master Decision": np.where(returns >= 0, "BUY", "SELL"),
            "Direction Confirmation": np.where(pd.Series(returns).rolling(3, min_periods=1).mean() >= 0, "BUY", "SELL"),
        }
    )
    news_idx = idx[::12]
    news = pd.DataFrame(
        {
            "Time": news_idx,
            "Title": [f"ECB and Fed EURUSD event {i % 8}" for i in range(len(news_idx))],
            "Sentiment": rng.uniform(-1, 1, len(news_idx)),
            "Impact": rng.uniform(0, 100, len(news_idx)),
            "Source": np.where(np.arange(len(news_idx)) % 2, "A", "B"),
        }
    )
    canonical = {
        "run_id": "trust-run",
        "generation_id": "trust-generation",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "completed_broker_candle": idx[-1],
        "ohlc_df": ohlc,
        "source_snapshot_hash": "snapshot-test",
    }
    state = {
        "field1_table1_decision_history_20260628": decisions,
        "finnhub_ranked_news_20260626": news,
    }
    return idx, ohlc, state, canonical


def test_unified_table2_has_25_days_and_required_columns():
    _, ohlc, state, canonical = _data()
    result = build_unified_lunch_trust_history(state, canonical, ohlc, {})
    assert len(result) <= 600
    assert result["Broker Day"].nunique() == 25
    required = {
        "Blue Path Trust /10", "Red Path Trust /10", "H+1 Trust /10", "H+2 Trust /10",
        "H+3 Trust /10", "H+6 Trust /10", "Lower Trust /10", "Middle Trust /10",
        "Higher Trust /10", "Entry Trust /10", "Buy Pressure Trust /10",
        "Sell Pressure Trust /10", "Net Pressure Trust /10", "Pullback Trust /10",
        "M1 Trust /10", "Master Decision Trust /10", "Hold Safety Trust /10",
        "TP Quality Trust /10", "Direction Confirmation Trust /10",
        "Protective Action", "Original Production Direction",
    }
    assert required.issubset(result.columns)
    assert set(result["Protective Action"]).issubset(ALLOWED_PROTECTIVE_ACTIONS)
    assert result["Completed Broker Candle"].is_monotonic_decreasing


def test_trust_values_are_bounded_or_missing():
    _, ohlc, state, canonical = _data()
    result = build_unified_lunch_trust_history(state, canonical, ohlc, {})
    for column in [c for c in result.columns if c.endswith("Trust /10")]:
        values = pd.to_numeric(result[column], errors="coerce").dropna()
        assert ((values >= 0) & (values <= 10)).all(), column


def test_forecast_maturity_and_no_future_dependency():
    idx, ohlc, state, canonical = _data()
    full = build_unified_lunch_trust_history(state, canonical, ohlc, {})
    target = idx[-72]
    truncated_ohlc = ohlc.loc[ohlc["Time"] <= target].copy()
    truncated_canonical = dict(canonical, completed_broker_candle=target, ohlc_df=truncated_ohlc)
    truncated = build_unified_lunch_trust_history(state, truncated_canonical, truncated_ohlc, {})
    full_row = full.loc[pd.to_datetime(full["Completed Broker Candle"], utc=True) == target].iloc[0]
    truncated_row = truncated.iloc[0]
    for column in ("H+1 Trust /10", "H+3 Trust /10", "H+6 Trust /10", "Lower Trust /10"):
        a = full_row[column]
        b = truncated_row[column]
        if pd.isna(a) and pd.isna(b):
            continue
        assert math.isclose(float(a), float(b), rel_tol=1e-10, abs_tol=1e-10), column
    assert pd.isna(truncated.iloc[0]["H+1 Actual Matured Price"])
    assert pd.isna(truncated.iloc[0]["H+6 Actual Matured Price"])


def test_m1_is_not_fabricated_from_h1():
    _, ohlc, state, canonical = _data()
    result = build_unified_lunch_trust_history(state, canonical, ohlc, {})
    assert result["M1 Confirmation"].isna().all()


def test_mobile_bounded_view_preserves_values():
    _, ohlc, state, canonical = _data()
    result = build_unified_lunch_trust_history(state, canonical, ohlc, {})
    view, meta = bounded_frame(result, mobile=True, page=1, page_size=10, columns=["Completed Broker Candle", "H+1 Trust /10"])
    assert len(view) == 10
    assert meta["total_rows"] == len(result)
    pd.testing.assert_series_equal(view["H+1 Trust /10"].reset_index(drop=True), result["H+1 Trust /10"].head(10).reset_index(drop=True), check_names=False)


def test_mobile_mode_changes_presentation_only():
    state = {"canonical_result": {"value": 123.45}}
    before = dict(state["canonical_result"])
    resolved = set_mobile_mode(state, "MOBILE LITE")
    assert resolved.enabled is True
    assert state["canonical_result"] == before
    resolved = set_mobile_mode(state, "FULL INTERFACE")
    assert resolved.enabled is False
    assert state["canonical_result"] == before


def test_imap_rv_invariants_and_cache(tmp_path, monkeypatch):
    _, _, state, canonical = _data()
    import research_quant.imap_rv_20260628 as module
    monkeypatch.setattr(module, "DB_PATH", tmp_path / "imap.sqlite3")
    envelope = run_imap_rv(state, canonical, force=True)
    assert envelope["production_values_modified"] is False
    assert envelope["protective_action"] in PROTECTIVE_ACTIONS
    decomposition = envelope["tables"]["imap_rv_reliability_decomposition"]
    available = decomposition.loc[decomposition["normalized value"].notna()]
    assert math.isclose(float(available["applied weight"].sum()), 1.0, rel_tol=1e-9)
    consensus = envelope["tables"]["diversity_weighted_consensus"]
    if not consensus.empty:
        assert math.isclose(float(consensus["diversity-adjusted weight"].sum()), 1.0, rel_tol=1e-9)
    cleaned = envelope["tables"]["cleaned_evidence_correlation"]
    if not cleaned.empty:
        eigenvalues = np.linalg.eigvalsh(cleaned.to_numpy(dtype=float))
        assert eigenvalues.min() >= -1e-8
    reused = run_imap_rv(state, canonical, force=False)
    assert reused["cache_status"] == "REUSED_SAME_COMPLETED_CANDLE"


def test_protected_table3_hashes_unchanged():
    expected = {
        "ui/lunch_decision_table_20260626.py": "d9f68a82e19c73efe2714a40781d9475cf826f9ce4c42007605336ebb5de89f2",
        "core/decision_table_20260626.py": "2c808100d6836689aa7f288c0fbd69cca21ce60b3e4d48b8ada81b06f3aa4b89",
    }
    for relative, digest in expected.items():
        assert hashlib.sha256(Path(relative).read_bytes()).hexdigest() == digest
