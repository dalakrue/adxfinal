"""Lunch Field 10: lazy multi-symbol rank and institutional shadow validation."""
from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from typing import Any

import pandas as pd
import streamlit as st

from core.multi_symbol_field10_20260701 import (
    ACTIVE_KEY,
    LAST_RESOURCE_KEY,
    MANIFEST_KEY,
    PROGRESS_KEY,
    SELECTED_KEY,
    activate_symbol_result,
    load_field10_tables,
    normalize_selected,
    normalize_symbol,
)

FIELD10_LABEL = "10. Open / Close — Multi-Symbol Rank, Data Quality and Higher-Regime Monitor"


def _switch_active_symbol() -> None:
    symbol = normalize_symbol(st.session_state.get("field10_active_symbol_widget_20260701") or "EURUSD")
    report = activate_symbol_result(st.session_state, symbol)
    st.session_state["field10_last_activation_20260701"] = report


def _show_progress(progress: Mapping[str, Any]) -> None:
    if not progress:
        return
    value = float(progress.get("overall_percent") or 0.0)
    st.progress(min(1.0, max(0.0, value / 100.0)), text=f"Overall progress: {value:.1f}% — {progress.get('current_stage') or 'Ready'}")
    cols = st.columns(4)
    cols[0].metric("Completed", int(progress.get("completed_symbols") or 0))
    cols[1].metric("Remaining", int(progress.get("remaining_symbols") or 0))
    cols[2].metric("Failed", int(progress.get("failed_symbols") or 0))
    eta = progress.get("estimated_remaining_seconds")
    elapsed_text = f"{float(progress.get('elapsed_seconds') or 0):.1f}s"
    if isinstance(eta, (int, float)):
        elapsed_text += f" / ETA {float(eta):.1f}s"
    cols[3].metric("Elapsed / ETA", elapsed_text)
    symbol_rows = []
    for symbol, item in (progress.get("symbols") or {}).items():
        item = item if isinstance(item, Mapping) else {}
        symbol_rows.append({
            "Symbol": symbol,
            "Progress": f"{float(item.get('percent') or 0):.0f}%",
            "Status": item.get("status", "WAITING"),
            "Stage": item.get("stage", "Queued"),
            "Elapsed Seconds": item.get("elapsed_seconds", ""),
            "Error": item.get("error", ""),
        })
    if symbol_rows:
        st.dataframe(pd.DataFrame(symbol_rows), use_container_width=True, hide_index=True, height=min(360, 42 + 35 * len(symbol_rows)))


def _search(frame: pd.DataFrame, query: str) -> pd.DataFrame:
    if frame.empty or not query.strip():
        return frame
    normalized = query.strip().casefold()
    mask = frame.astype(str).apply(
        lambda column: column.str.casefold().str.contains(normalized, regex=False, na=False)
    ).any(axis=1)
    return frame.loc[mask]


def _field10_history_filters(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply display-only filters without mutating the canonical/history store."""
    if frame.empty:
        return frame
    filtered = frame.copy()
    with st.expander("Open / Close — Field 10 history filters", expanded=False):
        date_series = None
        if "Broker Date" in filtered.columns:
            date_series = pd.to_datetime(filtered["Broker Date"], errors="coerce").dt.date
        elif "Broker Timestamp" in filtered.columns:
            date_series = pd.to_datetime(filtered["Broker Timestamp"], errors="coerce", utc=True).dt.date
        if date_series is not None and date_series.notna().any():
            minimum, maximum = date_series.dropna().min(), date_series.dropna().max()
            selected_range = st.date_input(
                "Broker-date range", value=(minimum, maximum), min_value=minimum, max_value=maximum,
                key="field10_history_date_range_20260701",
            )
            if isinstance(selected_range, (tuple, list)) and len(selected_range) == 2:
                start, end = selected_range
                filtered = filtered.loc[(date_series >= start) & (date_series <= end)]
                date_series = date_series.loc[filtered.index]

        filter_specs = (
            ("Current Session", "Session", "field10_filter_session_20260701"),
            ("Higher Standard Regime", "Regime", "field10_filter_regime_20260701"),
            ("Data Quality", "Data quality", "field10_filter_quality_20260701"),
            ("Less-Risky Bias", "Less-risky bias", "field10_filter_bias_20260701"),
            ("Final Action", "Final action", "field10_filter_action_20260701"),
        )
        available_specs = [spec for spec in filter_specs if spec[0] in filtered.columns]
        if available_specs:
            columns = st.columns(min(3, len(available_specs)))
            for index, (column, label, key) in enumerate(available_specs):
                options = sorted({str(v) for v in filtered[column].dropna().tolist() if str(v).strip()})
                selected = columns[index % len(columns)].multiselect(label, options=options, default=[], key=key)
                if selected:
                    filtered = filtered.loc[filtered[column].astype(str).isin(selected)]

        if "Rank" in filtered.columns:
            ranks = pd.to_numeric(filtered["Rank"], errors="coerce")
            if ranks.notna().any():
                low, high = int(ranks.min()), int(ranks.max())
                chosen = st.slider(
                    "Rank range", min_value=low, max_value=high, value=(low, high),
                    key="field10_filter_rank_20260701",
                )
                filtered = filtered.loc[ranks.between(chosen[0], chosen[1], inclusive="both")]
    return filtered


def _field10_styler(frame: pd.DataFrame):
    """Use restrained status colors while preserving text labels for accessibility."""
    if frame.empty:
        return frame

    def status_css(value: Any) -> str:
        text = str(value or "").strip().upper()
        if text in {"A", "PASS", "COMPLETED", "TRADE ALLOWED", "BUY", "SELL", "LOW", "GOOD"}:
            return "background-color:#d8f3dc;color:#153b22;font-weight:600"
        if text in {"B", "WARNING", "WAIT", "WAIT FOR PULLBACK", "HOLD AND PROTECT", "MODERATE", "AVERAGE", "PARTIAL"}:
            return "background-color:#ffe8b6;color:#5c3b00;font-weight:600"
        if text in {"C", "D", "FAIL", "FAILED", "NO TRADE", "BLOCKED", "HIGH", "POOR", "STALE"}:
            return "background-color:#ffd6d6;color:#641515;font-weight:600"
        if text in {"UNAVAILABLE", "INSUFFICIENT_DATA", "INSUFFICIENT SAMPLE", "WAITING", "N/A", "NONE", ""}:
            return "background-color:#eeeeee;color:#444444"
        if "LOCK" in text or text in {"INFORMATIONAL", "CANONICAL"}:
            return "background-color:#dcecff;color:#173a63"
        return ""

    styled = frame.style
    important = [
        c for c in (
            "Status", "Data Quality", "Spread Quality", "Less-Risky Bias", "Final Action",
            "Trade Permission", "Validation Status", "Lock Status", "Calculation Status",
            "Research Data Quality", "Research Permission", "Research Action", "Conflict",
            "Drift Status", "Structural Break Status", "Tail Risk Grade",
        ) if c in frame.columns
    ]
    if important:
        if hasattr(styled, "map"):
            styled = styled.map(status_css, subset=important)
        else:  # pandas < 2.1 compatibility
            styled = styled.applymap(status_css, subset=important)
    return styled


def _display_field10_table(frame: pd.DataFrame, *, height: int) -> None:
    st.dataframe(_field10_styler(frame), use_container_width=True, hide_index=True, height=height)


def _core_charts(daily: pd.DataFrame, hourly: pd.DataFrame) -> None:
    if not daily.empty and {"Symbol", "Data Quality Score"}.issubset(daily.columns):
        st.markdown("##### Today — Data Quality by Symbol")
        chart = daily[["Symbol", "Data Quality Score"]].dropna().set_index("Symbol")
        if not chart.empty:
            st.bar_chart(chart, use_container_width=True)
    if not hourly.empty and {"Data Quality Score", "Reliability"}.issubset(hourly.columns):
        scatter = hourly[["Data Quality Score", "Reliability"]].apply(pd.to_numeric, errors="coerce").dropna()
        if not scatter.empty and hasattr(st, "scatter_chart"):
            st.markdown("##### Hourly Data Quality vs Higher-Regime Reliability")
            st.scatter_chart(scatter, x="Data Quality Score", y="Reliability", use_container_width=True)
    if not hourly.empty and "Data Quality Score" in hourly.columns:
        values = pd.to_numeric(hourly["Data Quality Score"], errors="coerce").dropna()
        if not values.empty:
            bins = pd.cut(values, bins=[-0.01, 60, 75, 90, 100], labels=["D", "C", "B", "A"], include_lowest=True)
            hist = bins.value_counts(sort=False).rename("Hours").to_frame()
            st.markdown("##### Hourly Data-Quality Grade Distribution")
            st.bar_chart(hist, use_container_width=True)


_RESEARCH_GROUPS: Mapping[str, tuple[str, ...]] = {
    "Core Rank & Actions": (
        "Research Rank", "Rank Pool", "Symbol", "Broker Timestamp", "Production Action", "Research Action",
        "Research Permission", "Conflict", "Research Reliability", "Research Data Quality",
        "Research Data Quality Score", "Calculation Status", "Research Explanation",
    ),
    "Regime & Lifecycle": (
        "Research Rank", "Rank Pool", "Symbol", "Broker Timestamp", "Regime Probability", "Regime Entropy",
        "Expected Regime Duration", "Estimated Remaining Duration", "Transition Risk 1H",
        "Transition Risk 3H", "Transition Risk 6H", "Structural Break Status", "Break Count",
        "Break Strength", "Research Action",
    ),
    "Calibration & Intervals": (
        "Research Rank", "Rank Pool", "Symbol", "Broker Timestamp", "Brier Score", "Log Loss",
        "Calibration Error", "Conformal Status", "Conformal Coverage", "Interval Width",
        "DM p-value", "DM Candidate Superior", "SPA p-value", "SPA Superior",
    ),
    "Drift & State": (
        "Research Rank", "Rank Pool", "Symbol", "Broker Timestamp", "Drift Status", "Adaptive Window Size",
        "State Stability", "Innovation Z", "Structural Break Status", "Break Count", "Break Strength",
        "Calculation Status", "Research Explanation",
    ),
    "Portfolio & Tail Risk": (
        "Research Rank", "Rank Pool", "Symbol", "Broker Timestamp", "Correlation Cluster",
        "Duplicate Exposure Penalty", "CVaR 95", "Tail Risk Grade", "Research Reliability",
        "Research Permission", "Research Action",
    ),
}


def _research_view(frame: pd.DataFrame, group: str) -> pd.DataFrame:
    if frame.empty or group == "Full Research Audit":
        return frame
    columns = [column for column in _RESEARCH_GROUPS.get(group, ()) if column in frame.columns]
    return frame.loc[:, columns] if columns else frame


def _research_charts(current: pd.DataFrame, history: pd.DataFrame) -> None:
    if current.empty:
        return
    options = [
        "Research Reliability by Symbol",
        "Transition Risk by Symbol",
        "Tail Risk and Concentration",
        "Active-Symbol Research History",
    ]
    selected = st.selectbox("Research visualization", options, key="field10_research_chart_selector_20260701")
    if selected == "Research Reliability by Symbol":
        cols = [c for c in ("Symbol", "Research Reliability", "Research Data Quality Score") if c in current.columns]
        chart = current[cols].copy()
        if "Symbol" in chart and len(cols) > 1:
            chart = chart.set_index("Symbol").apply(pd.to_numeric, errors="coerce")
            st.bar_chart(chart, use_container_width=True)
    elif selected == "Transition Risk by Symbol":
        cols = [c for c in ("Symbol", "Transition Risk 1H", "Transition Risk 3H", "Transition Risk 6H") if c in current.columns]
        chart = current[cols].copy()
        if "Symbol" in chart and len(cols) > 1:
            chart = chart.set_index("Symbol").apply(pd.to_numeric, errors="coerce")
            st.line_chart(chart, use_container_width=True)
    elif selected == "Tail Risk and Concentration":
        cols = [c for c in ("Symbol", "CVaR 95", "Duplicate Exposure Penalty") if c in current.columns]
        chart = current[cols].copy()
        if "Symbol" in chart and len(cols) > 1:
            chart = chart.set_index("Symbol").apply(pd.to_numeric, errors="coerce")
            st.bar_chart(chart, use_container_width=True)
    else:
        if history.empty:
            st.info("Research history becomes available after Field 10 is opened for more than one completed generation.")
            return
        work = history.copy()
        time = pd.to_datetime(work.get("Broker Timestamp"), errors="coerce", utc=True)
        value_columns = [c for c in ("Research Reliability", "Research Data Quality Score", "Transition Risk 3H") if c in work.columns]
        if not value_columns or time.notna().sum() == 0:
            st.info("The stored research history has no chartable completed-candle values yet.")
            return
        work = work.loc[time.notna(), value_columns].apply(pd.to_numeric, errors="coerce")
        work.index = pd.DatetimeIndex(time.loc[time.notna()])
        st.line_chart(work.sort_index(), use_container_width=True)


def _render_research_layer(state: MutableMapping[str, Any], active: str, parent_run_id: str) -> None:
    from core.field10_ten_paper_research_20260701 import (
        ensure_field10_research_validation,
        load_field10_research_tables,
        load_research_registries,
        research_integrity_rows,
    )

    with st.spinner("Loading saved symbol generations and calculating the ten-paper shadow validation layer…"):
        report = ensure_field10_research_validation(state)
    if not report.get("ok"):
        st.warning(str(report.get("errors") or report.get("status") or "Research validation is unavailable."))
    else:
        st.caption(
            f"Ten-paper shadow layer: {report.get('status')} · calculated {report.get('calculated_symbols', 0)} · "
            f"cached {report.get('cached_symbols', 0)} · {float(report.get('elapsed_seconds') or 0):.3f}s. "
            "It does not overwrite the protected production decision."
        )
    tables = load_field10_research_tables(state, parent_run_id=parent_run_id, symbol=active)
    current, history = tables["current"], tables["history"]

    st.markdown("#### Institutional Quant Research Validation — Shadow Mode")
    if current.empty:
        st.info("No research rows were published. Missing or mismatched canonical identities were not replaced with placeholder statistics.")
    else:
        group = st.selectbox(
            "Research column group",
            [*_RESEARCH_GROUPS.keys(), "Full Research Audit"],
            key="field10_research_column_group_20260701",
        )
        query = st.text_input(
            "Search research results", key="field10_research_search_20260701",
            placeholder="symbol, drift, break, action, grade, explanation…",
        )
        view = _search(_research_view(current, group), query)
        _display_field10_table(view, height=min(560, 42 + 35 * max(1, len(view))))

    with st.expander("Open / Close — Ten-Paper Research History (latest 25 days / 600 rows)", expanded=False):
        if history.empty:
            st.info("No prior completed-generation research history is stored for this symbol.")
        else:
            research_query = st.text_input(
                "Search research history", key="field10_research_history_search_20260701",
                placeholder="action, status, model version, run ID…",
            )
            _display_field10_table(_search(history, research_query), height=520)

    _research_charts(current, history)

    with st.expander("Open / Close — Model and SPA Experiment Registries", expanded=False):
        registries = load_research_registries(parent_run_id=parent_run_id)
        st.markdown("##### Model Version Registry")
        if registries["models"].empty:
            st.info("No model-version registry row is available.")
        else:
            st.dataframe(registries["models"], use_container_width=True, hide_index=True)
        st.markdown("##### SPA / Candidate Experiment Registry")
        if registries["experiments"].empty:
            st.info("No experiment row is available for this parent run.")
        else:
            st.dataframe(registries["experiments"], use_container_width=True, hide_index=True, height=360)

    with st.expander("Open / Close — Field 10 Research Post-Run Integrity", expanded=False):
        integrity = pd.DataFrame(research_integrity_rows(state))
        st.dataframe(integrity, use_container_width=True, hide_index=True, height=min(360, 42 + 35 * max(1, len(integrity))))


def render_field10_content(state: MutableMapping[str, Any] | None = None) -> None:
    """Render Field 10 after the main Lunch selector has explicitly selected it."""
    state = state if state is not None else st.session_state
    st.caption(
        "Field 10 is selected. Basic cross-symbol evidence is read from the existing Field 10 store; "
        "the ten-paper research layer is now calculated lazily from saved canonical symbol generations. "
        "No connector refresh or protected Field 1–9 calculation is started."
    )
    manifest = state.get(MANIFEST_KEY) if isinstance(state.get(MANIFEST_KEY), Mapping) else {}
    progress = state.get(PROGRESS_KEY) if isinstance(state.get(PROGRESS_KEY), Mapping) else {}
    _show_progress(progress)
    selected = normalize_selected(manifest.get("selected_symbols") or state.get(SELECTED_KEY))
    if not selected:
        st.info("No multi-symbol generation is saved. Select instruments in Settings and run the one calculation button.")
        return
    active = normalize_symbol(state.get(ACTIVE_KEY) or manifest.get("active_symbol") or selected[0])
    if active not in selected:
        active = selected[0]
    state.setdefault("field10_active_symbol_widget_20260701", active)
    if state.get("field10_active_symbol_widget_20260701") not in selected:
        state["field10_active_symbol_widget_20260701"] = active
    st.selectbox(
        "Display completed result for symbol",
        options=selected,
        key="field10_active_symbol_widget_20260701",
        on_change=_switch_active_symbol,
        help="Restores the saved symbol generation only; no API request or production calculation is made.",
    )
    active = normalize_symbol(state.get("field10_active_symbol_widget_20260701") or active)
    parent_run_id = str(manifest.get("parent_run_id") or "")
    tables = load_field10_tables(state, parent_run_id=parent_run_id, symbol=active)
    summary, daily, hourly = tables["summary"], tables["daily"], tables["hourly"]

    top = st.columns(4)
    top[0].metric("Parent Run", parent_run_id[:24] or "-")
    top[1].metric("Selected Symbols", len(selected))
    top[2].metric("Completed", int(manifest.get("completed_symbols") or 0))
    top[3].metric("Active Symbol", active)

    active_summary = (manifest.get("symbol_summaries") or {}).get(active) if isinstance(manifest.get("symbol_summaries"), Mapping) else None
    field_validation = pd.DataFrame((active_summary or {}).get("field_validation") or []) if isinstance(active_summary, Mapping) else pd.DataFrame()
    with st.expander("Open / Close — Fields 1–9 Post-Run Integrity Check", expanded=False):
        if field_validation.empty:
            st.warning("No saved per-field validation report is available for this symbol generation.")
        else:
            st.dataframe(field_validation, use_container_width=True, hide_index=True, height=390)

    st.markdown("#### Multi-Symbol Run and Rank Summary")
    if summary.empty:
        st.warning("The saved summary is unavailable for this parent run.")
    else:
        _display_field10_table(summary, height=min(460, 42 + 35 * len(summary)))

    st.markdown("#### Today — Locked Higher-Standard Regime, Rank, Data Quality and Less-Risky Bias")
    if daily.empty:
        st.warning("Today's locked Higher-standard table is unavailable. No placeholder trading value has been created.")
    else:
        _display_field10_table(daily, height=min(500, 42 + 35 * len(daily)))

    st.markdown(f"#### {active} — Hourly Higher-Standard History (latest 25 days / up to 600 H1 rows)")
    if hourly.empty:
        st.warning("Hourly evidence is unavailable for this symbol. Run/source validation did not publish an empty table as success.")
    else:
        query = st.text_input("Search Field 10 history", key="field10_search_20260701", placeholder="regime, bias, grade, source ID, run ID…")
        filtered_hourly = _field10_history_filters(_search(hourly, query))
        st.caption(f"Showing {len(filtered_hourly):,} of {len(hourly):,} stored completed-candle rows.")
        _display_field10_table(filtered_hourly, height=520)

    _core_charts(daily, hourly)
    _render_research_layer(state, active, parent_run_id)

    resource = state.get(LAST_RESOURCE_KEY) if isinstance(state.get(LAST_RESOURCE_KEY), Mapping) else manifest.get("resource_report")
    if isinstance(resource, Mapping):
        with st.expander("Open / Close — RAM, CPU, heat proxy and calculation-time report", expanded=False):
            cols = st.columns(4)
            cols[0].metric("Total Time", f"{float(resource.get('total_elapsed_seconds') or 0):.2f}s")
            cols[1].metric("RSS Delta", f"{float(resource.get('rss_delta_mb') or 0):.2f} MB")
            cols[2].metric("CPU Time", f"{float(resource.get('cpu_seconds') or 0):.2f}s")
            cols[3].metric("Heat Proxy", str(resource.get("heat_proxy") or "UNKNOWN"))
            rows = pd.DataFrame(resource.get("rows") or [])
            if not rows.empty:
                st.dataframe(rows, use_container_width=True, hide_index=True)
            st.caption(str(resource.get("heat_proxy_note") or "Device temperature is not available to Streamlit."))


def render_field10_gate(state: MutableMapping[str, Any] | None = None) -> None:
    """Backward-compatible optional gate for legacy callers.

    The authoritative Lunch layout now places Field 10 inside the main field
    selector.  This wrapper remains for old imports and does not run unless its
    legacy toggle is explicitly opened.
    """
    state = state if state is not None else st.session_state
    st.markdown("---")
    if not st.toggle(FIELD10_LABEL, value=False, key="lunch_field10_gate_20260701"):
        return
    render_field10_content(state)


__all__ = ["FIELD10_LABEL", "render_field10_content", "render_field10_gate"]
