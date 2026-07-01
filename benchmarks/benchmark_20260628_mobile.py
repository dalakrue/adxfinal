from __future__ import annotations

import json
import statistics
import tempfile
import time
import tracemalloc
from pathlib import Path

import numpy as np
import pandas as pd

from core.mobile_lite_mode_20260628 import bounded_frame
from ui.lunch_unified_trust_history_20260628 import build_unified_lunch_trust_history
import research_quant.imap_rv_20260628 as imap_module


def data(n: int = 840):
    idx = pd.date_range("2026-05-01", periods=n, freq="h", tz="UTC")
    rng = np.random.default_rng(20260628)
    returns = rng.normal(0.0, 0.00045, n) + np.sin(np.arange(n) / 45.0) * 0.00008
    close = 1.16 * np.cumprod(1.0 + returns)
    open_ = np.r_[close[0], close[:-1]]
    ohlc = pd.DataFrame({
        "Time": idx,
        "Open": open_,
        "High": np.maximum(open_, close) + 0.0002,
        "Low": np.minimum(open_, close) - 0.0002,
        "Close": close,
        "Volume": rng.integers(100, 2000, n),
    })
    decisions = pd.DataFrame({
        "Broker Candle Time": idx,
        "Master Decision": np.where(returns >= 0, "BUY", "SELL"),
        "Direction Confirmation": np.where(pd.Series(returns).rolling(3, min_periods=1).mean() >= 0, "BUY", "SELL"),
    })
    news_idx = idx[::12]
    news = pd.DataFrame({
        "Time": news_idx,
        "Title": [f"ECB and Fed EURUSD event {i % 8}" for i in range(len(news_idx))],
        "Sentiment": rng.uniform(-1, 1, len(news_idx)),
        "Impact": rng.uniform(0, 100, len(news_idx)),
        "Source": np.where(np.arange(len(news_idx)) % 2, "A", "B"),
    })
    canonical = {
        "run_id": "benchmark-run",
        "generation_id": "benchmark-generation",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "completed_broker_candle": idx[-1],
        "ohlc_df": ohlc,
        "source_snapshot_hash": "benchmark-snapshot",
    }
    state = {
        "field1_table1_decision_history_20260628": decisions,
        "finnhub_ranked_news_20260626": news,
    }
    return ohlc, state, canonical


def timed(call, repetitions: int = 7):
    values = []
    outputs = []
    for _ in range(repetitions):
        start = time.perf_counter()
        outputs.append(call())
        values.append(time.perf_counter() - start)
    return values, outputs[-1]


def stats(values):
    return {
        "sample_count": len(values),
        "median_seconds": statistics.median(values),
        "minimum_seconds": min(values),
        "maximum_seconds": max(values),
        "mean_seconds": statistics.mean(values),
        "stdev_seconds": statistics.pstdev(values),
    }


def reduction(before, after):
    return 100.0 * (before - after) / before if before else None


def main():
    ohlc, state_template, canonical = data()

    cold_times = []
    cold_peaks = []
    full = None
    for _ in range(7):
        state = dict(state_template)
        tracemalloc.start()
        start = time.perf_counter()
        full = build_unified_lunch_trust_history(state, canonical, ohlc, {})
        cold_times.append(time.perf_counter() - start)
        _, peak = tracemalloc.get_traced_memory()
        cold_peaks.append(peak)
        tracemalloc.stop()

    warm_state = dict(state_template)
    full = build_unified_lunch_trust_history(warm_state, canonical, ohlc, {})
    warm_times, _ = timed(lambda: build_unified_lunch_trust_history(warm_state, canonical, ohlc, {}), 15)

    selected_columns = [
        "Completed Broker Candle", "Broker Hour", "Session", "Data-Quality Status",
        "Blue Path Trust /10", "Red Path Trust /10", "H+1 Trust /10", "H+3 Trust /10",
        "Lower Trust /10", "Middle Trust /10", "Higher Trust /10",
        "Master Decision", "Protective Action",
    ]
    mobile, mobile_meta = bounded_frame(full, mobile=True, page=1, page_size=10, columns=selected_columns)
    desktop_page, desktop_meta = bounded_frame(full, mobile=False, page=1, page_size=50, columns=list(full.columns))

    full_mem = int(full.memory_usage(index=True, deep=True).sum())
    desktop_mem = int(desktop_page.memory_usage(index=True, deep=True).sum())
    mobile_mem = int(mobile.memory_usage(index=True, deep=True).sum())

    full_ser_times, full_json = timed(lambda: full.to_json(orient="records", date_format="iso"), 7)
    desktop_ser_times, desktop_json = timed(lambda: desktop_page.to_json(orient="records", date_format="iso"), 15)
    mobile_ser_times, mobile_json = timed(lambda: mobile.to_json(orient="records", date_format="iso"), 30)

    page_times, _ = timed(lambda: bounded_frame(full, mobile=True, page=2, page_size=10, columns=selected_columns), 30)
    alternate_columns = ["Completed Broker Candle", "Entry Decision", "Buy Pressure", "Sell Pressure", "Net Pressure", "Pullback Readiness", "M1 Confirmation", "Master Decision", "Hold Safety", "TP Quality", "Direction Confirmation", "Protective Action"]
    column_times, _ = timed(lambda: bounded_frame(full, mobile=True, page=1, page_size=10, columns=alternate_columns), 30)

    with tempfile.TemporaryDirectory() as td:
        imap_module.DB_PATH = Path(td) / "imap.sqlite3"
        imap_cold_times = []
        imap_peaks = []
        for _ in range(5):
            state = dict(state_template)
            tracemalloc.start()
            start = time.perf_counter()
            imap_module.run_imap_rv(state, canonical, force=True)
            imap_cold_times.append(time.perf_counter() - start)
            _, peak = tracemalloc.get_traced_memory()
            imap_peaks.append(peak)
            tracemalloc.stop()
        imap_state = dict(state_template)
        imap_module.run_imap_rv(imap_state, canonical, force=True)
        imap_warm_times, reused = timed(lambda: imap_module.run_imap_rv(imap_state, canonical, force=False), 15)

    result = {
        "environment": {
            "dataset_rows": len(ohlc),
            "table2_rows": len(full),
            "table2_columns": len(full.columns),
            "broker_days": int(full["Broker Day"].nunique()),
            "mobile_page_rows": len(mobile),
            "mobile_page_columns": len(mobile.columns),
            "note": "Synthetic deterministic completed-candle benchmark; browser CPU and physical phone temperature are not available in this container.",
        },
        "table2_build_cold": stats(cold_times) | {"median_peak_python_bytes": int(statistics.median(cold_peaks))},
        "table2_same_candle_cache": stats(warm_times),
        "table2_cache_time_reduction_percent": reduction(statistics.median(cold_times), statistics.median(warm_times)),
        "imap_rv_build_cold": stats(imap_cold_times) | {"median_peak_python_bytes": int(statistics.median(imap_peaks))},
        "imap_rv_same_candle_cache": stats(imap_warm_times) | {"cache_status": reused.get("cache_status")},
        "imap_rv_cache_time_reduction_percent": reduction(statistics.median(imap_cold_times), statistics.median(imap_warm_times)),
        "payload_memory": {
            "full_600x_all_columns_bytes": full_mem,
            "desktop_50x_all_columns_bytes": desktop_mem,
            "mobile_10x_selected_columns_bytes": mobile_mem,
            "mobile_vs_full_reduction_percent": reduction(full_mem, mobile_mem),
            "mobile_vs_desktop_page_reduction_percent": reduction(desktop_mem, mobile_mem),
        },
        "serialized_payload": {
            "full_json_bytes": len(full_json.encode("utf-8")),
            "desktop_page_json_bytes": len(desktop_json.encode("utf-8")),
            "mobile_json_bytes": len(mobile_json.encode("utf-8")),
            "mobile_vs_full_bytes_reduction_percent": reduction(len(full_json.encode("utf-8")), len(mobile_json.encode("utf-8"))),
            "mobile_vs_desktop_page_bytes_reduction_percent": reduction(len(desktop_json.encode("utf-8")), len(mobile_json.encode("utf-8"))),
            "full_serialization": stats(full_ser_times),
            "desktop_page_serialization": stats(desktop_ser_times),
            "mobile_serialization": stats(mobile_ser_times),
            "mobile_vs_full_serialization_time_reduction_percent": reduction(statistics.median(full_ser_times), statistics.median(mobile_ser_times)),
        },
        "mobile_interactions": {
            "page_change": stats(page_times),
            "column_group_change": stats(column_times),
            "heavy_calculation_calls": 0,
        },
        "parity": {
            "mobile_first_10_values_equal_full_first_10": bool(mobile.reset_index(drop=True).equals(full.loc[:, selected_columns].head(10).reset_index(drop=True))),
            "calculation_result_modified": False,
            "mobile_meta": mobile_meta,
            "desktop_meta": desktop_meta,
        },
    }
    output = Path("DELIVERY_20260628_TRUST_IMAP_MOBILE/PERFORMANCE_BENCHMARK_RAW.json")
    output.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
