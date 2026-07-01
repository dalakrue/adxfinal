# Performance report

All measurements used the same container and installed dependency set. No 30–50% improvement is claimed.

| Workload | Uploaded | Repaired | Measured delta |
|---|---:|---:|---:|
| Cold `import app` median, 3 runs | 4.43 s | 4.26 s | -0.17 s (-3.84%) |
| Cold import peak RSS median | 387,732 KiB | 387,332 KiB | -400 KiB (-0.10%) |
| 20 Short+Full serializer pairs, median | 0.2171 s | 0.2253 s | +0.0082 s (+3.78%) |
| Streamlit health startup, single run | 6.8070 s | 6.6820 s | -0.1250 s (-1.84%) |

These differences are small and noisy. The direct serializer microbenchmark did not improve; the repaired active UI instead builds it once and reuses it by immutable canonical identity. That call-avoidance is tested, but no unmeasured percentage is assigned.

Implemented non-calculation overhead controls: selected-page/selected-field rendering, duplicate-copy renderer removal, generation-keyed current payload reuse, unchanged-completed-candle reuse, bounded 25-day/24-news displays, and AirLLM exclusion from startup/base requirements.
