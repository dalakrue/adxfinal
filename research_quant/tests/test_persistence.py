from __future__ import annotations

import sqlite3

from research_quant.persistence.research_store import (
    DDL,
    initialize_database,
    store_audit_row,
    store_canonical_snapshot,
    store_research_result,
)


def identity():
    return {
        "run_id": "run-persist-1",
        "generation_id": "gen-1",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "completed_broker_candle": "2026-06-27T10:00:00+00:00",
        "source_snapshot_hash": "hash-1",
        "source_signature": "sig-1",
    }


def test_empty_database_initializes_all_required_tables(tmp_path):
    path = initialize_database(tmp_path / "research.sqlite3")
    required = {
        "canonical_snapshots", "research_results", "research_model_registry",
        "research_validation_runs", "calibration_models", "drift_events",
        "prediction_intervals", "prediction_outcomes", "event_memory",
        "event_responses", "promotion_decisions", "research_audit",
    }
    with sqlite3.connect(path) as connection:
        observed = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert required <= observed
    assert len(DDL) == len(required)


def test_immutable_rows_are_idempotent(tmp_path):
    path = tmp_path / "research.sqlite3"
    base = identity()
    result = {
        **base,
        "model_name": "CRCEF-SV",
        "model_version": "1",
        "input_feature_hash": "feature-hash",
        "status": "RESEARCH_ONLY",
        "reason": "test",
        "sample_size": 1,
        "quality_flags": [],
        "payload": {"research_shadow_decision": "WAIT"},
        "created_at_broker_time": base["completed_broker_candle"],
    }
    audit = {
        "run_id": base["run_id"], "generation_id": base["generation_id"],
        "broker_candle": base["completed_broker_candle"], "module": "CRCEF-SV",
        "model_version": "1", "input_hash": "i", "output_hash": "o",
        "sample_size": 1, "status": "RESEARCH_ONLY", "warnings": [],
        "validation_status": "PENDING", "promotion_status": "RESEARCH_ONLY",
    }
    assert store_canonical_snapshot(base, {"decision": "WAIT"}, db_path=path) is True
    assert store_canonical_snapshot(base, {"decision": "BUY"}, db_path=path) is False
    assert store_research_result(result, db_path=path) is True
    assert store_research_result(result, db_path=path) is False
    assert store_audit_row(audit, db_path=path) is True
    assert store_audit_row(audit, db_path=path) is False
    with sqlite3.connect(path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM canonical_snapshots").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM research_results").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM research_audit").fetchone()[0] == 1
