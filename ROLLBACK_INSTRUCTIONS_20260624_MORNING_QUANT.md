# Rollback Instructions — 20260624 Morning Quant Upgrade

To roll back only this upgrade:

1. Restore these two modified files from the uploaded source ZIP:
   - `tabs/antd_page_router_20260615.py`
   - `tabs/doo_prime/morning_control_v8_20260622.py`

2. Remove these added files:
   - `core/forecast_origin_ledger_20260624.py`
   - `core/morning_quant_intelligence_20260624.py`
   - `core/probabilistic_evaluation_20260624.py`
   - `core/regime_shadow_engine_20260624.py`
   - `core/settings_one_click_controller_20260624.py`
   - `tests/test_20260624_morning_quant_upgrade.py`

3. Optional database cleanup:
   - drop table `forecast_origin_ledger_20260624` only if you want to remove shadow ledger evidence.
   - no protected Field 1 table needs rollback because Field 1 was not changed.
