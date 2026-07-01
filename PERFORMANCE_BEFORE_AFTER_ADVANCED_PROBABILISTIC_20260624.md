# Performance report

No unsupported percentage improvement is claimed. Implemented controls include bounded residual buffers, bounded BOCPD run length, append-only batched SQLite transactions, WAL/busy timeout, no training in rendering, and compact vectorized scoring.

Focused 37-test suite: 0.28 seconds in this container. Full-project test run exceeded the 120-second execution limit and exposed existing failures, so a valid global before/after comparison is not available.
