# Known Limitations — 20260624 Morning Quant Upgrade

- The local container did not have Streamlit installed, so a live browser/server startup smoke test could not be executed here. Python compilation and core import smoke tests passed.
- The new advanced research methods are shadow-only and advisory. They do not alter production BUY/SELL/WAIT decisions or Field 1.
- Connector-specific one-click behavior is preserved in existing renderers; the new shared controller is integrated into the main Run Calculation + Open Lunch button and is available for further connector migration.
- BOCPD and duration layers are compact robust shadow approximations suitable for evidence display and testing; they are not promoted production regime engines.
