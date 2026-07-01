# Evidence — Tab Switching Does Not Calculate

- `tabs/doo_prime/morning_control_v8_20260622.py` contains no import or call to `run_settings_calculation`, refresh, retrain, recalibrate or canonical publication.
- The router's `_render_morning()` imports only the dedicated V8 renderer and no longer calls `_home_ns()`.
- Lunch Field 1 display normalization is display-only and contains no Settings orchestrator call.
- V8 history queries occur only after the selected history's Load toggle is enabled and are cached by canonical calculation ID, generation, table, search, row limit and logic version.
- `core/settings_run_orchestrator_20260617.py` is the sole V8 calculation publication path.
- Static no-calculation tests, navigation tests and generation-preservation tests passed. The V8 suite explicitly verifies no calculation on Morning open, Lunch expander open and tab switch.
