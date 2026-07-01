# Rollback

1. Restore the pre-upgrade project ZIP.
2. Or remove the advanced causal imports/block from `core/services/research_service.py` and the collapsed renderer blocks from Lunch Fields 2–8.
3. New database tables are additive; they may remain unused safely. To remove them, back up the SQLite database first and drop only tables listed in `migrations/20260624_advanced_causal_forecast.sql`.
4. Field 1 requires no rollback because it was not changed.
