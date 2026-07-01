# Changelog V11

Date: 2026-06-24

- Preserved existing production calculations, prediction engines, strategy rules, tables, connectors, tabs, UI sections, and compatibility wrappers.
- Verified the modular seven-field Lunch registry, isolated field contracts, lightweight router, canonical context, and selected-field lazy rendering.
- Verified shadow-only EURUSD H1 Field 7 and separate Research Lab integration.
- Verified canonical snapshot, broker-time, repository, additive migration, logging, and error-boundary layers.
- Repaired pandas deprecation warnings in Filardo-transition and Realized-GARCH research modules.
- Replaced future-looking warm-up backfills with causal expanding/rolling or forward-only fallbacks.
- Made the V14 Field 1 protected-hash test self-contained by reading the baseline file included in the project instead of an external `/mnt/data` path.
- Executed 442 regression tests successfully in deterministic groups, warning-as-error tests, compile-all, and Streamlit Cloud preflight.
