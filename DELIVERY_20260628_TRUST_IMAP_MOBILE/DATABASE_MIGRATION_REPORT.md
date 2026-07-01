# Database Migration Report

- No production table was deleted, renamed or overwritten.
- IMAP-RV writes to a separate versioned research SQLite database: `data/imap_rv_research.sqlite3`.
- The persistence layer stores canonical identity, status, score, action, reason, metadata and serialized research tables.
- Existing production databases remain untouched.
- A full indexed SQL migration for every Table 2 history row was not added in this delivery; the complete frame is cached/published and exportable.
