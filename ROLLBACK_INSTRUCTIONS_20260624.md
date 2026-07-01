# Rollback Instructions

1. Restore `core/services/field8_service.py` and `core/field8_integrated_history_engine_20260624.py` from the supplied ZIP.
2. Delete `core/causal_accuracy_upgrade_20260624.py` and `tests/test_causal_accuracy_upgrade_20260624.py`.
3. Remove the optional session-state key `causal_accuracy_shadow_20260624` if present.
4. No database rollback is required because no destructive schema migration was made.
