# Test report

| Test | Result | Evidence |
|---|---|---|
| Compile every Python file | PASS | `COMPILE.exit=0` |
| Targeted v17 + Field 8/9 + no-heavy-render tests | PASS | 33 passed |
| Clean DB migration | PASS | tables created idempotently |
| Copied existing DB migration | PASS | existing history row preserved |
| Protected Field 1 hash validation | PASS | identical to supplied v15 baseline |
| Single run ID / broker time / no future feature | PASS | v17 contract unit test |
| H1/H3/H6 settlement | PASS | independent settlement unit test |
| Historical-origin immutability | PASS | second publish did not rewrite origin interval |
| True Gaussian/sample CRPS | PASS | analytic unit tests |
| Dynamic weights / MCS evidence | PASS | weights sum to 1, survivors recorded |
| Field 9 overlap / WAIT cost | PASS | unit tests |
| Grounded AI routing / unsupported question | PASS | unit tests |
| Application import | NOT TESTABLE | `streamlit` package absent |
| Live startup smoke | NOT TESTABLE | `streamlit` executable absent |
| Full legacy pytest suite | SKIPPED (TIME LIMIT) | exceeded 120-second command window |
| Mobile visual smoke | NOT TESTABLE | no browser/runtime in container |

No unexecuted test is claimed as passed.
