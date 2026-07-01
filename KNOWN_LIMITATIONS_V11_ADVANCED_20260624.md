# Known Limitations

- Implemented capability is not proof of improved live or out-of-sample accuracy.
- Full 468-test regression was started twice; both runs reached roughly 19% with no failures before the execution time limit. Focused changed-area tests all passed.
- Streamlit is not installed in the packaging environment, so direct renderer import/app startup could not be completed here; static compile and non-Streamlit service imports passed.
- PBO is a bounded registry diagnostic, not a substitute for a large independently governed CSCV campaign.
- Existing Hamilton/Filardo engines require sufficient completed H1 data and safely return insufficient-evidence states otherwise.
