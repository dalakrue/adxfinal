# Protected Field 1 hash comparison

Protected scope: every Python file under `lunch/field_01/`.

- Baseline: the supplied project's existing `reports/v15_20260624/FIELD1_HASH_BEFORE.sha256`.
- After: `reports/v17_20260624/FIELD1_HASH_AFTER.sha256`.
- Result: **IDENTICAL** (`cmp` exit code 0).

No Field 1 source file was modified. The upgrade reads the completed canonical snapshot and writes only additive research sidecar state/tables.
