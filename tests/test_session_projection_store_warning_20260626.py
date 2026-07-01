from __future__ import annotations

import warnings
import numpy as np
import pandas as pd

from core.session_projection_store_20260625 import compute_session_statistics


def test_all_nan_projection_evidence_is_quiet_and_stays_unavailable():
    records = pd.DataFrame({
        "session": ["ASIA"],
        "horizon": [1],
        "settlement_status": ["SETTLED"],
        "base_error": [np.nan],
        "coverage": [np.nan],
        "direction_correct": [np.nan],
        "upper": [np.nan],
        "lower": [np.nan],
        "forecast_origin_time": [pd.Timestamp("2026-06-26T00:00:00Z")],
    })
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = compute_session_statistics(records)
    assert not caught
    assert pd.isna(result.loc[0, "interval_coverage"])
    assert pd.isna(result.loc[0, "average_interval_width"])
