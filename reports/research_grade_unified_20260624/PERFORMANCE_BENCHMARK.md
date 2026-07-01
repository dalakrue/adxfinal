# Performance benchmark

- Scope: container synthetic benchmark; 540 matured horizon rows; not a production workload claim
- Median direct evaluation: 1.905647 s
- Peak traced allocation: 0.844 MiB
- First transactional publish: 0.334337 s
- Same-run idempotent cached publish: 0.002990 s
- Measured repeated-publication work reduction: 99.11%
- Cache behavior: first=False, second=True

This measurement applies only to the synthetic test workload and repeated publication of the same immutable run. It is not presented as a universal 30–50% end-to-end production improvement.
