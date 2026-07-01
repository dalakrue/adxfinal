# Known Limitations

- Current probability construction is deliberately conservative and shadow-only; formal calibration awaits settled data.
- Conditional wrong-direction rates and hierarchy-level effective sample sizes remain insufficient until the ledger accumulates observations.
- Spread and volume are stored as unavailable when the existing feed does not publish them.
- The sandbox lacked the Streamlit runtime package, so direct `import app` could not execute here; compile, project preflight, and static import-contract tests passed.
- No live profitability or accuracy improvement is claimed.
