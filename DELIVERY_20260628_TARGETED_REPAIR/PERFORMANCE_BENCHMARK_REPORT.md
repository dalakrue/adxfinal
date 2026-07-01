# Performance Benchmark Report

## Method

A reproducible synthetic benchmark used 600 completed H1 rows and five Dinner field histories. Original and repaired archives were run in separate Python processes. Results are in `evidence/benchmark_original.json` and `evidence/benchmark_repaired.json`.

## Results

| Path | Original | Repaired | Interpretation |
|---|---:|---:|---|
| ARERT label map with 60,000 values including `pandas.NA` | **Failed immediately** | 168.4 ms median | Functional repair; original had no valid timing because it crashed. |
| Mixed-timestamp 25-day history, 600 rows | 18.1 ms | 22.6 ms | Both synthetic cases completed; repaired path adds defensive normalization. |
| Dinner 600×5 cold build | 547.9 ms | 724.6 ms | Repaired output performs extra source-quality and four-label protective work; no cold-run improvement claim. |
| Dinner same-generation warm cache | 0.021 ms | 0.036 ms | Both are effectively negligible; repaired cache avoids rebuilding 88-column output. |
| Finder selected-hour filter | Not present | 7.8 ms | New bounded display-only function. |
| Finder complete copy payload | Not present | 11.4 ms | New bounded export/copy function. |
| Process RSS at benchmark end | 388.6 MB | 387.2 MB | Similar; not a controlled peak-RAM proof. |

## Important conclusion

The requested **30–50% total reduction is not claimed**. The benchmark proves that the crash is removed, same-generation Dinner reuse is extremely fast, and Finder filtering/copy generation is bounded. It does not prove a 30–50% cold-run, whole-app, or mobile-device reduction. A device-specific before/after profile using the user's live data and Streamlit Cloud instance is still required.
