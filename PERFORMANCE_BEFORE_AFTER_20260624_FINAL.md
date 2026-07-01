# Performance Before/After

The added renderer performs no fitting, market-data fetch or production recalculation. It reads the already-published in-memory evidence, limits historical display to the latest 120 rows, and lazy-renders inside closed expanders. Therefore normal reruns add only compact dataframe/chart preparation. No unsupported percentage improvement is claimed.
