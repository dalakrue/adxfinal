# Known limitations

- The governance sidecar does not claim live profitability or accuracy improvement.
- PBO is a bounded block-stability proxy, not a full combinatorially symmetric cross-validation implementation for every possible configuration.
- Hamilton/Filardo evidence is lightweight and deterministic; it does not replace the canonical regime.
- Application import smoke testing could not import the real Streamlit entry point in this build environment because `streamlit` is not installed; repository Streamlit preflight tests passed.
- The complete legacy pytest suite exceeded the execution window; targeted new and architecture acceptance suites passed.
