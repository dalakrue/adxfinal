# Performance report

A bounded synthetic benchmark executed ten cycles of MCS (five models, 300 observations, 100 bootstrap repetitions), energy score, variogram score, and HAR volatility.

See `PERFORMANCE_BENCHMARK.json` for measured elapsed time and peak Python allocation.

No valid before-upgrade benchmark was included in the supplied project, so a percentage improvement claim would be unverified. The implementation bounds bootstrap repetitions, block sizes, retained state, and database rows; rendering remains lazy and read-only.
