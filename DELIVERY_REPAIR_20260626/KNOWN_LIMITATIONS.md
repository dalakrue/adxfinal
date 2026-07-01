# Known limitations

- Live broker/API execution was not performed because no production credentials or live terminal were used.
- AirLLM inference was not installed or benchmarked; it remains optional, disabled by default, and excluded from base requirements.
- Existing historical rows are not fabricated. With no settled archive, Field 1 Table 1 can only show the current completed-candle PENDING row.
- Streamlit smoke testing verified startup and health, not every interactive browser gesture on a physical iPhone.
