# Known Limitations
- Full statistical MCS and White Reality Check bootstrap require a larger matched settled sample and are fail-closed.
- Missing USD, spread or liquidity factors remain NaN with reason codes; they are not fabricated as zero.
- Research trust is shadow-only and has not been promoted or optimized on the full data set.
- Python 3.12 and a live Streamlit server were not available in the test container.
- One unrelated legacy Finnhub test remains environment-stub sensitive.
