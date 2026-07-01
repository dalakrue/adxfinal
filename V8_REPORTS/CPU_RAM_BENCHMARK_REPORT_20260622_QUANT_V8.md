# CPU/RAM Benchmark Report

## Measured cold Morning import benchmark

Three independent subprocess runs compared the actual V7 legacy Morning implementation import with the V8 dedicated Morning renderer.

| Metric | V7 average | V8 average | Reduction |
|---|---:|---:|---:|
| Wall time | 15570.7 ms | 2443.3 ms | 84.31% |
| Peak traced Python memory | 89.44 MB | 28.82 MB | 67.78% |
| Maximum process RSS | 678.33 MB | 405.03 MB | 40.29% |

V7 target: `tabs.home_split.legacy.implementation`. V8 target: `tabs.doo_prime.morning_control_v8_20260622`.

This is a cold-import architecture benchmark, not a live broker/network or full-session throughput benchmark. Absolute RSS includes interpreter and dependency startup. Opening the protected Doo Prime legacy workspace deliberately from Morning → Analysis will still incur its legacy import cost.

V8 also records wall time, peak traced memory, H1 row count, settled row count and serialized result bytes inside each V8 Settings publication.
