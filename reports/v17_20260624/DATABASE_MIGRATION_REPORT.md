# Database migration report

The migration is additive and idempotent. It creates `rg17_run`, `rg17_origin`, `rg17_field8`, `rg17_field9` and `rg17_ai`. It alters or deletes no existing table.

Executed tests:
- clean in-memory/file database migration twice: PASS;
- copied database containing `existing_user_history`: PASS, row preserved;
- transaction rollback on validation failure is implemented in `publish`.
