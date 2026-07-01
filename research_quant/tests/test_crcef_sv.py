from __future__ import annotations

import copy
import pandas as pd

from research_quant.orchestrator import build_crcef_sv_result
from research_quant.validation.cpcv import combinatorial_purged_splits
from research_quant.validation.purging import information_intervals, leakage_free
from research_quant.fusion.crcef_sv import fuse_evidence, uncertainty_score
from research_quant.fusion.evidence_registry import Evidence
from research_quant.meta_labeling.primary_direction_adapter import production_direction


def _canonical(decision="WAIT PULLBACK"):
    return {
        "run_id": "run-1", "generation_id": "gen-1", "symbol": "EURUSD", "timeframe": "H1",
        "completed_broker_candle": "2026-06-27T10:00:00+00:00",
        "source_snapshot_hash": "hash-1", "source_signature": "sig-1",
        "final_decision": {"final_decision": decision},
        "market": {"ohlc_df": pd.DataFrame({"close": [1.10 + i / 10000 for i in range(80)]})},
        "regime": "BULL_NORMAL",
    }


def test_crcef_output_contract_and_production_immutability():
    canonical = _canonical()
    before = copy.deepcopy({k: v for k, v in canonical.items() if k != "market"})
    result = build_crcef_sv_result(canonical, {})
    assert result["run_id"] == "run-1"
    assert result["generation_id"] == "gen-1"
    assert result["model_name"].startswith("Canonical Regime-Calibrated")
    assert result["research_mode"] is True
    assert result["payload"]["production_decision"] == "WAIT PULLBACK"
    assert result["payload"]["research_shadow_decision"] == "WAIT PULLBACK"
    assert result["payload"]["production_decision_unchanged"] is True
    assert result["payload"]["promotion_status"] == "RESEARCH_ONLY"
    assert {k: v for k, v in canonical.items() if k != "market"} == before


def test_hold_is_not_converted_to_buy_or_sell():
    result = build_crcef_sv_result(_canonical("HOLD"), {})
    assert result["payload"]["production_decision"] == "HOLD"
    assert result["payload"]["research_shadow_decision"] == "HOLD"


def test_fusion_and_uncertainty_are_bounded():
    fused = fuse_evidence([Evidence("a", 3, 1), Evidence("b", -4, 1)])
    assert -1 <= fused["direction_fusion_score"] <= 1
    assert 0 <= fused["conflict"] <= 1
    assert 0 <= fused["coverage"] <= 1
    uncertainty = uncertainty_score(direction_probability=.5, conflict=1, drift_level=1, normalized_interval_width=1, coverage_error=1, missing_data_penalty=1)
    assert 0 <= uncertainty <= 100


def test_cpcv_purging_and_embargo_are_leakage_safe():
    starts = pd.date_range("2026-01-01", periods=60, freq="h", tz="UTC")
    ends = starts + pd.Timedelta(hours=2)
    intervals = information_intervals(starts, ends)
    splits = list(combinatorial_purged_splits(intervals, n_groups=6, test_groups_per_split=1, embargo_candles=2))
    assert splits
    for split in splits:
        assert leakage_free(split.train_indices, split.test_indices, intervals)
        assert not set(split.train_indices).intersection(split.test_indices)


def test_primary_text_taxonomy_is_preserved():
    for label in ("BUY", "SELL", "WAIT", "WAIT PULLBACK", "HOLD"):
        assert production_direction(_canonical(label)) == label
