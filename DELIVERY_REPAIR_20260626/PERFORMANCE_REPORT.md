# Performance report

Measured on the same container workload: 20 executions over 5,000 all-NaN settled projection rows.

- Before: 0.212425 seconds; 1920 warnings.
- After: 0.242043 seconds; 0 warnings.
- No percentage performance-improvement claim is made. The repair targets warning-free unavailable-evidence handling, not protected calculation speed.
