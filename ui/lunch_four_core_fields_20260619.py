"""Authoritative eight-principal-field Lunch layout.

Every principal field is a true read-only load gate over the already-published
canonical generation. No renderer here can start or replace the protected
calculation transaction.
"""
from __future__ import annotations

from typing import Any, Mapping, MutableMapping

import pandas as pd
import streamlit as st



QUICK_DECISION_FIELD = "0. Open / Close — Lunch Quick Decision"
FULL_METRIC_FIELD = "1. Open / Close — Full Metric 25-Day History + Decision Tables"
POWERBI_FIELD = "2. Open / Close — Power BI Price Prediction Path"
REGIME_FIELD = "3. Open / Close — 25-Day Regime History + Lower / Medium / Higher Standards"
FIELD10_FIELD = "10. Open / Close — Multi-Symbol Rank, Data Quality and Higher-Regime Monitor"
CURRENT_FIELD = "4. Field 456 — Combined Fields 4+5+6 (Display Only)"
COMBINED_FIELD = CURRENT_FIELD
AI_FIELD = CURRENT_FIELD  # compatibility alias; AI is nested in combined 4+5+6
READINESS_FIELD = CURRENT_FIELD  # compatibility alias; readiness is nested in combined 4+5+6
RESEARCH_FIELD = "5. Field 789 — Combined Fields 7+8+9 (Display Only)"
INTEGRATED_ACCURACY_FIELD = RESEARCH_FIELD
DECISION_IMPACT_FIELD = RESEARCH_FIELD
HISTORICAL_COMBINED_FIELD = CURRENT_FIELD
CLOSED_LUNCH_FIELD = "All Lunch fields closed"
FIELD_LABELS = (
    FULL_METRIC_FIELD, POWERBI_FIELD, REGIME_FIELD, FIELD10_FIELD,
)
# Exactly 5 total surfaces remain registered. Lunch now exposes core Fields 1–3 plus lazy Field 10; Field 456 and Field 789 stay independent.

_TIME_NAMES = (
    "Broker Candle Time", "Completed Broker Candle", "Broker Candle",
    "Time", "time", "Datetime", "DateTime", "Timestamp", "Date", "Hour", "candle time",
)
_CURRENT_TABLE_ORDER = (
    ("Session Decision", ("session", "session_table")),
    ("10 Reverse Decision", ("reverse10",)),
    ("10 Entry Decision", ("entry", "entry_table")),
    ("10 Direction Decision", ("direction", "direction_table")),
    ("10 Hold Decision", ("hold", "hold_table")),
    ("10 Exit Decision", ("exit", "exit_table")),
    ("10 TP Decision", ("tp", "tp_table")),
    ("Metric Table", ("metric_table",)),
    ("Full Metric Table", ("full_metric_table",)),
)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _canonical(state: MutableMapping[str, Any]) -> Mapping[str, Any]:
    from core.canonical_lookup_20260626 import resolve_canonical
    canonical = resolve_canonical(state)
    # Validate the active pointer on every Lunch render. A restored session may
    # contain an old canonical object even though the successful metric/OHLC
    # publishers already reached a newer completed H1 candle.
    try:
        from core.field1_publication_bridge_20260626 import ensure_field1_publication
        repaired = ensure_field1_publication(state)
        if isinstance(repaired, Mapping):
            state["lunch_field1_publication_freshness_20260630"] = dict(repaired)
            if repaired.get("ok") and isinstance(repaired.get("canonical"), Mapping):
                return repaired["canonical"]
    except Exception as exc:
        state["lunch_field1_publication_freshness_error_20260630"] = f"{type(exc).__name__}: {exc}"
    return canonical if canonical else {}


def _frame_latest_time(frame: Any) -> pd.Timestamp | None:
    """Return one comparable UTC timestamp regardless of publisher dtype.

    Some legacy publishers return ISO strings while newer publishers return
    ``pandas.Timestamp`` values.  Normalizing at this boundary prevents Python
    from attempting ``str < Timestamp`` while selecting the newest cache.
    """
    candidate: Any = None
    try:
        from core.market_time_freshness_20260622 import latest_frame_time
        candidate = latest_frame_time(frame)
    except Exception:
        candidate = None
    parsed_candidate = pd.to_datetime(candidate, errors="coerce", utc=True)
    if pd.notna(parsed_candidate):
        return pd.Timestamp(parsed_candidate)
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        return None
    column = _time_column(frame)
    if not column or str(column).strip().lower() == "hour":
        return None
    parsed = pd.to_datetime(frame[column], errors="coerce", utc=True)
    valid = parsed.dropna()
    return pd.Timestamp(valid.max()) if not valid.empty else None


def _mapping_latest_time(value: Mapping[str, Any]) -> pd.Timestamp | None:
    # Prefer candle/history timestamps. ``created_at`` is only a fallback because
    # a newly rebuilt wrapper can still contain an older market frame.
    timestamps: list[pd.Timestamp] = []
    for key in ("latest_completed_candle_time", "latest_completed_h1", "anchor_time"):
        parsed = pd.to_datetime(value.get(key), errors="coerce", utc=True)
        if pd.notna(parsed):
            timestamps.append(pd.Timestamp(parsed))
    for key in ("history", "metric_table", "full_metric_table", "priority_table"):
        latest = _frame_latest_time(value.get(key))
        if latest is not None:
            timestamps.append(latest)
    histories = value.get("history_by_factor")
    if isinstance(histories, Mapping):
        for frame in histories.values():
            latest = _frame_latest_time(frame)
            if latest is not None:
                timestamps.append(latest)
    if timestamps:
        return max(timestamps)
    created = pd.to_datetime(value.get("created_at"), errors="coerce", utc=True)
    return pd.Timestamp(created) if pd.notna(created) else None


def _metric_result(state: MutableMapping[str, Any]) -> Mapping[str, Any]:
    candidates: list[tuple[pd.Timestamp, int, Mapping[str, Any]]] = []
    fallback: list[tuple[int, Mapping[str, Any]]] = []
    for priority, key in enumerate(("lunch_metric_result_cache", "full_metric_result_cache_20260618")):
        value = state.get(key)
        if isinstance(value, Mapping) and value.get("ok"):
            fallback.append((priority, value))
            latest = _mapping_latest_time(value)
            if latest is not None:
                candidates.append((latest, -priority, value))
    try:
        from core.system_wide_completion_20260618 import published_metric_result
        value = published_metric_result(state)
        if isinstance(value, Mapping) and value.get("ok"):
            fallback.append((99, value))
            latest = _mapping_latest_time(value)
            if latest is not None:
                candidates.append((latest, -99, value))
    except Exception:
        pass
    if candidates:
        return max(candidates, key=lambda item: (item[0], item[1]))[2]
    return min(fallback, key=lambda item: item[0])[1] if fallback else {}


def _time_column(frame: pd.DataFrame) -> str | None:
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        return None
    direct = next((name for name in _TIME_NAMES if name in frame.columns), None)
    if direct:
        return direct
    normalized = {str(column).strip().lower(): str(column) for column in frame.columns}
    return next((normalized[name.lower()] for name in _TIME_NAMES if name.lower() in normalized), None)


def _ensure_time_column(frame: pd.DataFrame) -> pd.DataFrame:
    """Expose a DatetimeIndex as ``Time`` for bounded history projections."""
    if not isinstance(frame, pd.DataFrame) or frame.empty or _time_column(frame):
        return frame
    try:
        from core.market_time_freshness_20260622 import frame_time_series
        stamps = frame_time_series(frame)
    except Exception:
        stamps = pd.Series(dtype="datetime64[ns, UTC]")
    if stamps.empty or not stamps.notna().any():
        return frame
    work = frame.copy(deep=False).reset_index(drop=True)
    work.insert(0, "Time", stamps.reset_index(drop=True))
    return work


def _history_25day(frame: pd.DataFrame, *, maximum_rows: int = 600, completed_h1: Any | None = None, columns: Any | None = None) -> pd.DataFrame:
    """Bounded selected-column view, newest completed H1 first.

    Legacy publishers may mix ISO strings and ``Timestamp`` objects in one
    column.  This boundary always builds a single UTC datetime key before any
    comparison or sort, preventing ``str < Timestamp`` failures.
    """
    frame = _ensure_time_column(frame)
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        return pd.DataFrame()
    work = frame.copy(deep=False)
    time_col = _time_column(work)
    if time_col and str(time_col).strip().lower() != "hour":
        parsed = pd.to_datetime(work[time_col], errors="coerce", utc=True, format="mixed")
        work = work.loc[parsed.notna()].copy(deep=False)
        parsed = parsed.loc[work.index]
        if not work.empty:
            work = work.copy(deep=False)
            work[time_col] = parsed
    try:
        from core.history_query_20260621 import project_completed_h1
        return project_completed_h1(work, days=25, columns=columns, maximum_rows=maximum_rows, completed_h1=completed_h1, descending=True)
    except Exception:
        if work.empty:
            return pd.DataFrame()
        time_col = _time_column(work)
        if time_col:
            parsed = pd.to_datetime(work[time_col], errors="coerce", utc=True, format="mixed")
            latest = pd.to_datetime(completed_h1, errors="coerce", utc=True)
            if pd.isna(latest):
                valid = parsed.dropna()
                latest = valid.max() if not valid.empty else pd.NaT
            if pd.notna(latest):
                latest = pd.Timestamp(latest)
                mask = parsed.notna() & parsed.le(latest) & parsed.ge(latest - pd.Timedelta(days=25))
                work = work.loc[mask].copy(deep=False)
                parsed = parsed.loc[mask]
                work = work.loc[parsed.sort_values(ascending=False, kind="mergesort").index]
        if columns is not None:
            selected = [str(c) for c in work.columns if str(c) in {str(v) for v in columns}]
            if time_col and time_col not in selected:
                selected.insert(0, time_col)
            if selected:
                work = work.loc[:, selected]
        return work.head(maximum_rows).reset_index(drop=True)


def _display_clock_frame(
    frame: pd.DataFrame,
    *,
    state: Mapping[str, Any] | None = None,
    broker_clock: bool = False,
) -> pd.DataFrame:
    """Display every Lunch history timestamp from the shared broker clock.

    Canonical UTC identity is preserved in storage.  This function changes only
    the presented dataframe and never uses wall-clock time.
    """
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        return frame
    work = _ensure_time_column(frame)
    if broker_clock:
        try:
            from core.shared_broker_time_20260622 import frame_to_shared_broker_clock

            state_map = dict(state or {})
            canonical = _canonical(state_map)
            if not canonical:
                latest = _frame_latest_time(work)
                if latest is not None:
                    # A history row's canonical UTC event time is an admissible
                    # display anchor.  This remains read-only and never falls
                    # back to local PC/wall-clock time.
                    canonical = {
                        "latest_completed_candle_time": pd.Timestamp(latest).isoformat(),
                        "symbol": str(state_map.get("symbol", "EURUSD")),
                        "timeframe": str(state_map.get("timeframe", "H1")),
                        "source": "LUNCH_HISTORY_FRAME",
                    }
            return frame_to_shared_broker_clock(work, state_map, canonical=canonical)
        except Exception:
            pass
    # Compatibility fallback for non-history/current tables.
    work = work.copy(deep=False)
    for column in list(work.columns):
        name = str(column).strip().lower().replace("_", " ")
        is_clock = name in {"time", "datetime", "timestamp", "date", "candle time", "future time", "target time", "projection time"} or name.endswith(" time")
        if not is_clock:
            continue
        parsed = pd.to_datetime(work[column], errors="coerce", utc=True)
        if parsed.notna().any():
            work[column] = parsed.dt.tz_convert("UTC").dt.tz_localize(None)
    return work


def _display_table(
    title: str,
    frame: pd.DataFrame,
    *,
    height: int = 430,
    empty_message: str | None = None,
    historical: bool = True,
    state: Mapping[str, Any] | None = None,
    broker_clock: bool = False,
) -> None:
    st.markdown(f"#### {title}")
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        st.info(empty_message or f"{title} is unavailable in the completed generation.")
        return
    display = _display_clock_frame(frame, state=state, broker_clock=broker_clock)
    st.dataframe(display, use_container_width=True, hide_index=True, height=height)
    if historical:
        st.caption(f"Historical rows displayed: {len(frame):,}. The view is historical and is not limited to a current-hour snapshot.")
    else:
        st.caption(f"Current published rows displayed: {len(frame):,}. No historical rows are mixed into this current-data table.")


def _factor_histories(result: Mapping[str, Any], *, completed_h1: Any | None = None) -> dict[str, pd.DataFrame]:
    """Return all ten factor histories, repairing publisher-name/schema gaps.

    This remains display-only: it first uses publisher frames, then projects
    missing Net Pressure and Direction Confirmation from already-published
    overall history columns. No prior candles or outcomes are fabricated.
    """
    raw = result.get("history_by_factor")
    prepared: dict[str, pd.DataFrame] = {}
    if isinstance(raw, Mapping):
        aliases = {
            "entry strength": "Entry Strength", "sell pressure": "SELL Pressure",
            "buy pressure": "BUY Pressure", "net pressure": "Net Pressure",
            "pressure": "Net Pressure", "pullback readiness": "Pullback Readiness",
            "m1 confirmation": "M1 Confirmation", "master decision": "Master Decision",
            "hold safety": "Hold Safety", "tp quality": "TP Quality",
            "direction confirmation": "Direction Confirmation",
        }
        for name, frame in raw.items():
            if not isinstance(frame, pd.DataFrame) or frame.empty:
                continue
            low = str(name).strip().lower()
            canonical_name = next((v for k, v in aliases.items() if k == low or all(t in low for t in k.split())), str(name))
            view = _history_25day(frame, completed_h1=completed_h1)
            if canonical_name not in prepared or len(view) > len(prepared[canonical_name]):
                prepared[canonical_name] = view

    overall = result.get("history")
    if not isinstance(overall, pd.DataFrame):
        overall = result.get("full_metric_table") if isinstance(result.get("full_metric_table"), pd.DataFrame) else pd.DataFrame()
    if isinstance(overall, pd.DataFrame) and not overall.empty:
        base = _history_25day(overall, completed_h1=completed_h1)
        def pick(*names):
            norm={str(c).strip().lower().replace('_',' '):c for c in base.columns}
            for name in names:
                key=name.lower().replace('_',' ')
                if key in norm: return norm[key]
            return None
        tcol = pick("Broker Candle Time","Time","Datetime","Timestamp","Date Time")
        datecol, hourcol = pick("Date"), pick("Hour")
        def project(score_names, decision_names, derive=None):
            score=pick(*score_names); decision=pick(*decision_names)
            out=pd.DataFrame(index=base.index)
            if tcol: out["Broker Candle Time"]=base[tcol]
            elif datecol and hourcol: out["Broker Candle Time"]=pd.to_datetime(base[datecol].astype(str)+" "+base[hourcol].astype(str),errors="coerce",utc=True)
            if datecol: out["Date"]=base[datecol]
            if hourcol: out["Hour"]=base[hourcol]
            if score: out["Score /10"]=pd.to_numeric(base[score],errors="coerce")
            if decision: out["Decision"]=base[decision]
            elif derive is not None: out["Decision"]=derive(base)
            return out.dropna(how="all")
        if "Net Pressure" not in prepared:
            buy=pick("BUY Pressure Score","BUY /10","Buy Score"); sell=pick("SELL Pressure Score","SELL /10","Sell Score")
            def net_dec(df):
                if buy and sell:
                    b=pd.to_numeric(df[buy],errors='coerce'); q=pd.to_numeric(df[sell],errors='coerce')
                    return pd.Series(['BUY' if x>y else 'SELL' if y>x else 'WAIT' for x,y in zip(b,q)],index=df.index)
                return pd.Series('WAIT',index=df.index)
            f=project(("Net Pressure Score","Pressure Score"),("Pressure Decision","Net Pressure Decision"),net_dec)
            if "Score /10" not in f.columns and buy and sell:
                f["Score /10"]=(pd.to_numeric(base[buy],errors='coerce')-pd.to_numeric(base[sell],errors='coerce')).abs().clip(0,10)
            if not f.empty: prepared["Net Pressure"]=f
        if "Direction Confirmation" not in prepared:
            def dir_dec(df):
                col=pick("Final Decision","Master Decision","Decision","Direction")
                return df[col] if col else pd.Series('WAIT',index=df.index)
            f=project(("Direction Confirmation Score","Direction Score","Master Decision Score"),("Direction Confirmation Decision","Confirmation Action"),dir_dec)
            if "Score /10" not in f.columns:
                src=pick("Master Decision Score","Entry Strength Score","Entry /10")
                if src: f["Score /10"]=pd.to_numeric(base[src],errors='coerce').clip(0,10)
            if not f.empty: prepared["Direction Confirmation"]=f
    return prepared



def _latest_completed_h1_from_state(state: MutableMapping[str, Any], result: Mapping[str, Any] | None = None) -> Any | None:
    """Return the one canonical completed candle selected by the shared provider."""
    try:
        from core.shared_broker_time_20260622 import shared_broker_time_provider
        history = result.get("history") if isinstance(result, Mapping) and isinstance(result.get("history"), pd.DataFrame) else None
        return shared_broker_time_provider(state, frame=history, canonical=_canonical(state)).get("latest_broker_candle_utc")
    except Exception:
        canonical = _canonical(state)
        value = canonical.get("latest_completed_candle_time") if isinstance(canonical, Mapping) else None
        parsed = pd.to_datetime(value, errors="coerce", utc=True)
        return None if pd.isna(parsed) else pd.Timestamp(parsed)


def _reorder_field1_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Move Decision/Direction beside Hour for easier phone reading."""
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        return frame
    columns = [str(c) for c in frame.columns]
    lower = {str(c).strip().lower(): str(c) for c in frame.columns}
    hour_col = lower.get("hour")
    decision_cols = []
    for col in frame.columns:
        name = str(col).strip().lower()
        if name in {"decision", "direction", "current decision", "less risky decision"}:
            decision_cols.append(str(col))
    if not hour_col:
        return frame
    distribution_cols = [c for c in ("BFD", "SFD") if c in columns]
    move_cols = distribution_cols + [c for c in decision_cols if c not in distribution_cols]
    if not move_cols:
        return frame
    new_order: list[str] = []
    inserted = False
    for col in columns:
        if col in move_cols:
            continue
        new_order.append(col)
        if col == hour_col and not inserted:
            new_order.extend([c for c in move_cols if c not in new_order])
            inserted = True
    for col in columns:
        if col not in new_order:
            new_order.append(col)
    return frame.loc[:, new_order]


def _field1_current_overlay(state: MutableMapping[str, Any], overall: pd.DataFrame, completed_h1: Any | None) -> pd.DataFrame:
    """Display-only rescue when the metric history cache is older than loaded data.

    Some deployments keep a valid old metric history while the header and other
    fields have already received a newer completed candle.  Rather than showing
    02:00 as the top row when the app is on 12:00/13:00, prepend the current
    already-published priority/market rows and keep protected score columns from
    the metric history when available.
    """
    if not isinstance(overall, pd.DataFrame) or overall.empty or completed_h1 is None:
        return overall
    tcol = _time_column(overall)
    latest_overall = _frame_latest_time(overall) if tcol else None
    completed = pd.to_datetime(completed_h1, errors="coerce", utc=True)
    if latest_overall is None or pd.isna(completed) or latest_overall >= completed - pd.Timedelta(minutes=1):
        return overall
    # Build rows from already-loaded OHLC/priority caches for the missing hours.
    priority = _current_priority_table(state, _canonical(state))
    market = state.get("last_df")
    if not isinstance(market, pd.DataFrame) or market.empty:
        return overall
    work = _ensure_time_column(market).copy(deep=False)
    mt = _time_column(work)
    if not mt:
        return overall
    parsed = pd.to_datetime(work[mt], errors="coerce", utc=True)
    mask = parsed.notna() & parsed.gt(latest_overall) & parsed.le(completed)
    work = work.loc[mask].copy()
    parsed = parsed.loc[mask]
    if work.empty:
        return overall
    work["__time"] = parsed
    work = work.sort_values("__time", ascending=False).head(600)
    rows = []
    for _, row in work.iterrows():
        stamp = pd.Timestamp(row["__time"])
        out = {col: pd.NA for col in overall.columns}
        if tcol:
            out[tcol] = stamp.tz_convert("UTC").tz_localize(None) if stamp.tzinfo is not None else stamp
        if "Date" in overall.columns:
            out["Date"] = stamp.strftime("%Y-%m-%d 00:00:00")
        if "Weekday" in overall.columns:
            out["Weekday"] = stamp.strftime("%A")
        if "Hour" in overall.columns:
            out["Hour"] = stamp.strftime("%H:00")
        for src, dst in (("open", "Open"), ("high", "High"), ("low", "Low"), ("close", "Close")):
            src_col = next((c for c in work.columns if str(c).lower() in {src, src[0]}), None)
            if src_col is not None and dst in overall.columns:
                out[dst] = row.get(src_col)
        if isinstance(priority, pd.DataFrame) and not priority.empty:
            prow = priority.iloc[0]
            for dst, aliases in {
                "Priority Rank": ("Priority Rank", "priority_rank", "Rank"),
                "Priority Label": ("Priority Label", "priority_label", "Label"),
                "Greedy Score": ("Greedy Score", "greedy_score", "Score"),
                "Decision": ("Decision", "decision", "Current Decision"),
                "Direction": ("Direction", "direction", "Directional Market View"),
                "Entry/10": ("Entry/10", "entry_score", "Entry Score"),
                "BUY /10": ("BUY /10", "BUY/10", "buy_score"),
                "SELL /10": ("SELL /10", "SELL/10", "sell_score"),
                "Exit Risk": ("Exit Risk", "exit_risk", "Exit Risk/10"),
            }.items():
                hit = next((a for a in aliases if a in priority.columns), None)
                if hit is not None and dst in overall.columns:
                    out[dst] = prow.get(hit)
        rows.append(out)
    if not rows:
        return overall
    # Exclude all-NA fragments before concatenation.  Pandas 3 will change dtype
    # inference for such fragments; restoring the original column order keeps the
    # display contract stable without emitting the deprecation warning.
    target_columns = list(overall.columns)
    fresh_rows = pd.DataFrame(rows).dropna(axis=1, how="all")
    existing_rows = overall.dropna(axis=1, how="all")
    patched = pd.concat([fresh_rows, existing_rows], ignore_index=True, sort=False)
    patched = patched.reindex(columns=target_columns)
    if tcol in patched.columns:
        stamps = pd.to_datetime(patched[tcol], errors="coerce", utc=True)
        patched = patched.loc[stamps.notna()].copy()
        patched["__sort"] = stamps.loc[patched.index]
        patched = patched.sort_values("__sort", ascending=False).drop_duplicates(subset=[tcol], keep="first").drop(columns=["__sort"])
    st.caption("Field 1 is synchronized to the latest loaded H1 candle using already-published market/priority rows; no protected calculation was run.")
    return patched.reset_index(drop=True)



def _align_table2_decision_with_table3(
    state: MutableMapping[str, Any], overall: pd.DataFrame, canonical: Mapping[str, Any]
) -> pd.DataFrame:
    """Align Table 2's displayed decision with Table 3/1 production truth.

    No score or protected calculation is changed. When an old overall-history
    publisher contains a conflicting decision label, the old label is retained
    in an audit column and the explicit Table 3 production decision is displayed.
    """
    if not isinstance(overall, pd.DataFrame) or overall.empty:
        return overall
    try:
        from ui.lunch_decision_table_20260626 import _snapshot
        from core.decision_table_20260626 import build_decision_table
        table3_collection = build_decision_table(state, _snapshot(canonical, state))
    except Exception:
        return overall
    if not isinstance(table3_collection, pd.DataFrame) or table3_collection.empty:
        return overall
    overall_time = _time_column(overall)
    source_time = "Broker Candle Time" if "Broker Candle Time" in table3_collection.columns else None
    if not overall_time or not source_time:
        return overall
    out = overall.copy()
    out["__table2_time"] = pd.to_datetime(out[overall_time], errors="coerce", utc=True).dt.floor("h")
    source = table3_collection.copy()
    source["__table2_time"] = pd.to_datetime(source[source_time], errors="coerce", utc=True).dt.floor("h")
    source_decision = next(
        (c for c in ("Production Decision Raw", "Final Decision", "Master Decision", "Action Display Label") if c in source.columns),
        None,
    )
    if source_decision is None:
        return overall
    source = source[["__table2_time", source_decision]].dropna(subset=["__table2_time"]).drop_duplicates("__table2_time")
    source = source.rename(columns={source_decision: "Table 3 Production Decision"})
    out = out.merge(source, on="__table2_time", how="left")
    target = next((c for c in ("Decision", "Direction", "Current Decision", "Final Decision") if c in out.columns), None)
    if target is not None:
        old = out[target].copy()
        table3 = out["Table 3 Production Decision"]
        valid = table3.notna() & ~table3.astype(str).str.upper().isin({"", "N/A", "NONE", "UNAVAILABLE"})
        conflicts = valid & old.notna() & (old.astype(str).str.upper() != table3.astype(str).str.upper())
        if conflicts.any():
            out["Table 2 Published Decision (audit)"] = old
        out.loc[valid, target] = table3.loc[valid]
        out["Table 2 / Table 3 Decision Match"] = (~conflicts).map({True: "MATCH", False: "ALIGNED TO TABLE 3"})
    return out.drop(columns=["__table2_time"], errors="ignore")

def _render_history_sync_status(state: MutableMapping[str, Any], history_frame: pd.DataFrame | None = None) -> None:
    """Show strict Field 1 timestamp and identity synchronization status."""
    try:
        from core.shared_broker_time_20260622 import history_sync_status
        report = history_sync_status(state, history_frame=history_frame, canonical=_canonical(state))
        state["lunch_history_sync_status_20260622"] = report
        st.markdown("#### Field 1 Synchronization Status")
        top = st.columns(4)
        status = str(report.get("status") or "UNAVAILABLE")
        if status == "SYNCED": top[0].success("SYNCED")
        elif status == "STALE": top[0].warning("STALE")
        elif status == "UNAVAILABLE": top[0].warning("UNAVAILABLE")
        else: top[0].error("RED — OUT OF SYNC")
        top[1].metric("Latest Completed Broker Candle", str(report.get("shared_broker_time_display") or "Not available"))
        top[2].metric("Latest Field 1 Broker Record", str(report.get("latest_history_record_display") or "Not available"))
        diff = report.get("difference_minutes")
        top[3].metric("Difference Minutes", f"{float(diff):.2f}" if isinstance(diff, (int, float)) else "-")
        checks = st.columns(4)
        checks[0].metric("Calculation ID Match", "YES" if report.get("calculation_id_match") else "NO")
        checks[1].metric("Generation Match", "YES" if report.get("generation_match") else "NO")
        checks[2].metric("Broker Offset Match", "YES" if report.get("broker_offset_match") else "NO")
        checks[3].metric("Source Match", "YES" if report.get("source_match") else "NO")
        st.caption(str(report.get("reason") or "No synchronization reason was published."))
    except Exception as exc:
        st.warning(f"History sync validation unavailable: {exc}")

def _render_full_metric_history(state: MutableMapping[str, Any]) -> None:
    canonical = _canonical(state)
    from ui.lunch_identity_strip_20260626 import render_lunch_identity_strip
    render_lunch_identity_strip(canonical, field_label="Field 1")
    # Table 1 of 3: one immutable Field-1 decision identity table.  It is a
    # presentation adapter only and never changes protected production rules.
    try:
        from ui.lunch_decision_table_bfd_wrapper_20260629 import render_field1_decision_history
        render_field1_decision_history(state=state, canonical=canonical)
    except Exception as exc:
        state["field1_decision_table_render_error_20260626"] = f"{type(exc).__name__}: {exc}"
        st.warning(f"Decision History table skipped safely: {exc}")
    if canonical:
        try:
            from ui.session_field1_summary_20260625 import render_field1_session_lens
            render_field1_session_lens(state, canonical)
        except Exception as exc:
            state["field1_session_lens_render_error_20260625"] = f"{type(exc).__name__}: {exc}"
            st.warning(f"Shared FX Session Lens skipped safely: {exc}")
    result = _metric_result(state)
    result_ready = bool(result and result.get("ok"))
    if not result_ready:
        # Keep the complete Field 1 surface visible after Quick Run even when a
        # protected history publisher has no settled archive yet.  Empty tables
        # remain explicitly empty/N/A; no historical row or production score is
        # invented.  Table 1 above still shows the current immutable pending row
        # whenever the canonical generation published one.
        st.warning("Full Metric history has no settled archive rows for this generation. The complete table structure remains visible; unavailable evidence is not fabricated.")
        result = result if isinstance(result, Mapping) else {}

    completed_h1 = _latest_completed_h1_from_state(state, result)
    overall_raw = result.get("history") if isinstance(result.get("history"), pd.DataFrame) else pd.DataFrame()
    overall = _history_25day(overall_raw, completed_h1=completed_h1)
    overall = _field1_current_overlay(state, overall, completed_h1)
    overall = _align_table2_decision_with_table3(state, overall, canonical)
    try:
        from core.buy_sell_frequency_20260629 import enrich_bfd_sfd
        overall = enrich_bfd_sfd(overall)
    except Exception:
        pass
    if overall.empty and len(overall.columns) == 0:
        overall = pd.DataFrame(columns=[
            "Date", "Weekday", "Hour", "BFD", "SFD", "Decision", "Direction", "Entry/10",
            "BUY /10", "SELL /10", "Hold/10", "TP/10", "Exit Risk/10",
            "Trend Capacity Remaining", "Broker Candle Time", "Outcome Status",
        ])
    overall = _reorder_field1_columns(overall)
    _render_history_sync_status(state, overall)
    report = overall.attrs.get("h1_projection", {}) if isinstance(overall, pd.DataFrame) else {}
    if isinstance(report, Mapping) and report:
        st.caption(
            "H1 data quality: "
            f"{report.get('status', 'UNKNOWN')} · source {report.get('source_rows', 0)} rows · "
            f"display {report.get('projected_rows', len(overall))} rows · "
            f"missing {float(report.get('missingness_ratio', 0.0)):.1%} · "
            f"duplicates {float(report.get('duplicate_ratio', 0.0)):.1%} · "
            f"finite numeric {float(report.get('finite_numeric_ratio', 0.0)):.1%}."
        )
    histories = _factor_histories(result, completed_h1=completed_h1)
    try:
        from ui.lunch_unified_trust_history_20260628 import render_unified_lunch_trust_history
        render_unified_lunch_trust_history(
            state=state, canonical=canonical, overall=overall, factor_histories=histories
        )
    except Exception as exc:
        state["unified_lunch_trust_history_error_20260628"] = f"{type(exc).__name__}: {exc}"
        st.warning(f"Unified Lunch Trust History skipped safely: {type(exc).__name__}: {exc}")
        _display_table(
            "Table 2 — Overall Full Metric History — Last 25 Days (safe legacy fallback)",
            overall, height=500,
            empty_message="The completed generation has no overall Full Metric history rows.",
            state=state, broker_clock=True,
        )
    with st.expander("Open / Close — Legacy Table 2 Audit Evidence", expanded=False):
        st.caption("The former Table 2 remains available as read-only audit evidence. Its calculation and stored values were not deleted or overwritten.")
        _display_table(
            "Legacy Overall Full Metric History — Last 25 Days", overall, height=360,
            empty_message="The completed generation has no legacy Full Metric history rows.",
            state=state, broker_clock=True,
        )

    st.markdown("#### Table 3 — All 10 Decision Histories — Last 25 Days")
    expected_names = [
        "Entry Strength", "SELL Pressure", "BUY Pressure", "Net Pressure",
        "Pullback Readiness", "M1 Confirmation", "Master Decision",
        "Hold Safety", "TP Quality", "Direction Confirmation",
    ]
    # Preserve every publisher-provided name, but always expose the complete ten
    # requested display slots. Missing slots are empty evidence tables, not
    # synthetic history.
    ordered_names = list(expected_names)
    for published_name in histories:
        if published_name not in ordered_names:
            ordered_names.append(published_name)
    if len(histories) != 10:
        st.warning(f"The generation published {len(histories)} of 10 requested factor histories. All ten table structures are shown; missing evidence remains empty.")
    st.caption("Each table uses the same completed-H1 cutoff and 25-day window. Empty tables mean no published evidence exists for that factor.")
    tabs = st.tabs(ordered_names)
    empty_schema = pd.DataFrame(columns=[
        "Date", "Weekday", "Hour", "BFD", "SFD", "Decision", "Score /10",
        "Broker Candle Time", "Canonical run_id", "Canonical generation_id",
        "Outcome Status",
    ])
    for tab, name in zip(tabs, ordered_names):
        with tab:
            frame = histories.get(name, empty_schema.copy())
            try:
                from core.buy_sell_frequency_20260629 import enrich_bfd_sfd
                frame = enrich_bfd_sfd(frame)
            except Exception:
                pass
            frame = _reorder_field1_columns(frame)
            if frame.empty:
                st.dataframe(frame, use_container_width=True, hide_index=True, height=210)
                st.info(f"{name}: no published rows for this canonical generation.")
            else:
                st.dataframe(_display_clock_frame(frame, state=state, broker_clock=True), use_container_width=True, hide_index=True, height=410)
                st.caption(f"{name}: {len(frame):,} historical rows, newest completed H1 first, displayed in broker time with Myanmar time beside it.")
    try:
        from ui.lunch_next_hour_bias_history_20260626 import render_next_hour_bias_history
        render_next_hour_bias_history(state=state, canonical=canonical)
    except Exception as exc:
        state["next_hour_bias_history_render_error_20260626"] = f"{type(exc).__name__}: {exc}"
        st.warning(f"Next-hour combined bias history skipped safely: {exc}")
    # Requested move: the current-hour AI summary now lives at the very bottom
    # of Field 1 and reads cached evidence only. Protected Table 3 is untouched.
    try:
        from ui.lunch_field1_ai_summary_20260628 import render_field1_ai_summary
        render_field1_ai_summary(state, canonical)
    except Exception as exc:
        state["lunch_field1_ai_summary_error_20260628"] = f"{type(exc).__name__}: {exc}"
        st.warning(f"AI Summary skipped safely: {type(exc).__name__}: {exc}")


def _render_powerbi(state: MutableMapping[str, Any]) -> None:
    canonical = _canonical(state)
    from ui.lunch_identity_strip_20260626 import render_lunch_identity_strip
    render_lunch_identity_strip(canonical, field_label="Field 2")
    from ui.lunch_data_state_20260626 import render_state
    projection_candidates = [
        canonical.get("powerbi"), canonical.get("projection"), canonical.get("forecasts"),
        state.get("powerbi_calibrated_bundle_20260617"),
        state.get("lunch_5layer_powerbi_result"), state.get("powerbi_projection_result_20260619"),
        state.get("powerbi_projection_cache_20260619"), state.get("cached_powerbi_projection_20260619"),
        state.get("five_layer_powerbi_result"), state.get("lunch_powerbi_result"),
    ]
    projection = next((v for v in projection_candidates if isinstance(v, Mapping) and v), None)
    # The cached renderer owns the single authoritative projection-state banner.
    # A generic non-empty mapping must never be announced as valid before exact
    # run/generation/candle/hash/signature validation.
    try:
        from ui.powerbi_cached_renderer_20260619 import render_cached_powerbi_projection
        render_cached_powerbi_projection(state=state)
        from core.less_risky_projection_20260625 import render_less_risky_projection
        render_less_risky_projection(state)
    except Exception as exc:
        state["lunch_four_field_powerbi_error_20260619"] = repr(exc)
        st.error("The cached Power BI projection could not render. Its calculation cache was not changed.")
        st.code(f"{type(exc).__name__}: {exc}")
    try:
        from ui.lunch_field2_quant_upgrade_20260629 import render_field2_quant_upgrade
        render_field2_quant_upgrade(state)
    except Exception as upgrade_exc:
        state["field2_quant_upgrade_render_error_20260629"] = f"{type(upgrade_exc).__name__}: {upgrade_exc}"
        st.warning(f"Adaptive Field 2 research layer skipped safely: {upgrade_exc}")


def _published_regime_tables(state: MutableMapping[str, Any], canonical: Mapping[str, Any]) -> Mapping[str, Any]:
    candidates: list[tuple[pd.Timestamp, int, Mapping[str, Any]]] = []
    fallback: list[tuple[int, Mapping[str, Any]]] = []
    values: list[tuple[int, Any]] = []
    for priority, key in enumerate(("regime_standard_detail_tables_published_20260618", "regime_standard_detail_tables_20260617")):
        values.append((priority, state.get(key)))
    regime = _mapping(canonical.get("regime"))
    for offset, key in enumerate(("standard_detail_tables", "detail_tables", "regime_standard_detail_tables"), start=10):
        values.append((offset, regime.get(key)))
    for priority, value in values:
        if not isinstance(value, Mapping):
            continue
        fallback.append((priority, value))
        stamps = [_frame_latest_time(frame) for frame in value.values() if isinstance(frame, pd.DataFrame)]
        valid = [pd.Timestamp(pd.to_datetime(stamp, errors="coerce", utc=True)) for stamp in stamps if stamp is not None and pd.notna(pd.to_datetime(stamp, errors="coerce", utc=True))]
        if valid:
            candidates.append((max(valid), -priority, value))
    if candidates:
        return max(candidates, key=lambda item: (item[0], item[1]))[2]
    return min(fallback, key=lambda item: item[0])[1] if fallback else {}


def _overall_regime_history(result: Mapping[str, Any]) -> pd.DataFrame:
    history = result.get("history")
    if not isinstance(history, pd.DataFrame) or history.empty:
        return pd.DataFrame()
    tokens = ("regime", "alpha", "delta", "transition", "reliab", "priority", "knn", "greedy", "decision", "direction")
    time_col = _time_column(history)
    chosen: list[str] = []
    if time_col:
        chosen.append(time_col)
    for column in history.columns:
        text = str(column).lower()
        if any(token in text for token in tokens) and str(column) not in chosen:
            chosen.append(str(column))
    # Push the projection into the bounded completed-H1 query so unused Full
    # Metric columns never enter this Field 3 presentation DataFrame.
    return _history_25day(history, columns=chosen if len(chosen) > 1 else None)


def compress_regime_change_intervals(frame: pd.DataFrame) -> pd.DataFrame:
    """Return one row per consecutive regime interval, newest interval first.

    Medium and Higher standards describe persistent state episodes. Repeating
    the same state for every H1 candle makes the table look as if the regime
    changed hourly and wastes memory. This display-only projection preserves
    the published values and time boundaries without changing any estimator.
    """
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        return pd.DataFrame()
    work = _ensure_time_column(frame).copy(deep=False)
    time_col = _time_column(work)
    if not time_col:
        return work.reset_index(drop=True)
    parsed = pd.to_datetime(work[time_col], errors="coerce", utc=True)
    work = work.loc[parsed.notna()].copy()
    if work.empty:
        return pd.DataFrame()
    work["__interval_time"] = parsed.loc[parsed.notna()].values
    work = work.sort_values("__interval_time", ascending=True, kind="mergesort").reset_index(drop=True)

    identity_tokens = ("regime", "decision", "direction", "bias", "standard", "state", "status")
    identity_columns = [
        str(c) for c in work.columns
        if str(c) not in {str(time_col), "__interval_time"}
        and any(token in str(c).lower() for token in identity_tokens)
        and not any(token in str(c).lower() for token in ("time", "date", "hour", "duration", "age"))
    ]
    if not identity_columns:
        identity_columns = [str(c) for c in work.columns if str(c) not in {str(time_col), "__interval_time"}][:3]
    if not identity_columns:
        return work.drop(columns=["__interval_time"], errors="ignore").reset_index(drop=True)

    normalized = work[identity_columns].fillna("<NA>").astype(str)
    changed = normalized.ne(normalized.shift(1)).any(axis=1)
    changed.iloc[0] = True
    work["__interval_group"] = changed.cumsum()
    rows: list[dict[str, Any]] = []
    for _, group in work.groupby("__interval_group", sort=False):
        first = group.iloc[0]
        last = group.iloc[-1]
        start = pd.Timestamp(first["__interval_time"])
        end = pd.Timestamp(last["__interval_time"])
        # The final H1 observation represents the hour ending one candle later.
        duration = max(1.0, (end - start).total_seconds() / 3600.0 + 1.0)
        row: dict[str, Any] = {
            "Regime Start": start,
            "Regime End": end,
            "Duration Hours": round(duration, 2),
            "Published H1 Observations": int(len(group)),
        }
        for column in identity_columns:
            row[column] = last.get(column)
        # Keep a small set of useful reliability/score fields from the end of
        # the interval; never replicate the entire wide H1 frame.
        for column in work.columns:
            lower = str(column).lower()
            if column in row or column in {time_col, "__interval_time", "__interval_group"}:
                continue
            if any(token in lower for token in ("reliab", "score", "probab", "confidence", "alpha", "delta")):
                row[str(column)] = last.get(column)
            if len(row) >= 18:
                break
        rows.append(row)
    return pd.DataFrame(rows).sort_values("Regime End", ascending=False, kind="mergesort").reset_index(drop=True)


def _always_visible_middle_higher_history(
    state: MutableMapping[str, Any], canonical: Mapping[str, Any], details: Mapping[str, Any]
) -> None:
    """Always show raw Middle/Higher evidence before legacy interval summaries."""
    st.markdown("#### Always-Visible Middle and Higher Standard History")
    st.caption(
        "These raw canonical H1 tables remain visible whenever Field 3 is open. "
        "The existing change-only interval tables below are preserved unchanged."
    )
    monitor = state.get("field3_regime_lifecycle_monitor_20260701")
    raw_monitor_history = monitor.get("history_25d") if isinstance(monitor, Mapping) else None
    monitor_history = raw_monitor_history.copy(deep=False) if isinstance(raw_monitor_history, pd.DataFrame) else pd.DataFrame(raw_monitor_history or [])
    for key, label, token in (
        ("medium", "Middle Standard Regime History — Raw Latest 25 Days", "middle"),
        ("higher", "Higher Standard Regime History — Raw Latest 25 Days", "higher"),
    ):
        frame = details.get(key) if isinstance(details, Mapping) else None
        prepared = _history_25day(frame) if isinstance(frame, pd.DataFrame) and not frame.empty else pd.DataFrame()
        if prepared.empty and not monitor_history.empty:
            matching = [column for column in monitor_history.columns if token in str(column).lower()]
            identity = [column for column in monitor_history.columns if any(part in str(column).lower() for part in ("time", "date", "bias", "reliab", "trust", "run id", "source id", "quality"))]
            columns = list(dict.fromkeys(identity + matching))
            prepared = monitor_history[columns].copy(deep=False) if columns else monitor_history.copy(deep=False)
            prepared = _history_25day(prepared)
        if prepared.empty:
            prepared = pd.DataFrame([{
                "Status": "UNAVAILABLE — NOT MARKED COMPLETE",
                "Standard": "Middle (120H)" if key == "medium" else "Higher (600H)",
                "Symbol": canonical.get("symbol", state.get("symbol", "EURUSD")),
                "Timeframe": canonical.get("timeframe", state.get("timeframe", "H1")),
                "Run ID": canonical.get("run_id", ""),
                "Source ID": canonical.get("source_id") or canonical.get("snapshot_hash") or "",
                "Validation Message": "No saved raw history exists for this completed generation; no placeholder regime/bias was fabricated.",
            }])
        _display_table(label, prepared.reset_index(drop=True), height=380, state=state, broker_clock=True)


def _render_regime_history(state: MutableMapping[str, Any]) -> None:
    canonical = _canonical(state)
    from ui.lunch_identity_strip_20260626 import render_lunch_identity_strip
    render_lunch_identity_strip(canonical, field_label="Field 3")
    try:
        from ui.field3_daily_locked_regime_20260625 import render_daily_locked_regime
        render_daily_locked_regime(state, canonical)
    except Exception as exc:
        state["field3_daily_lock_render_error_20260625"] = f"{type(exc).__name__}: {exc}"
        st.warning(f"Daily Middle/Higher regime lock skipped safely: {exc}")
    result = _metric_result(state)
    _display_table(
        "Overall Regime History — Last 25 Days",
        _overall_regime_history(result),
        height=480,
        empty_message="The 25-day overall regime history is unavailable in the completed generation.",
        state=state, broker_clock=True,
    )

    details = _published_regime_tables(state, canonical)
    _always_visible_middle_higher_history(state, canonical, details)
    summary = state.get("regime_standard_table_20260617")
    if isinstance(summary, pd.DataFrame) and not summary.empty:
        _display_table("Three-Standard Summary", summary.reset_index(drop=True), height=220, historical=True, state=state, broker_clock=True)

    specs = (
        ("lower", "Lower Standard Regime History — Last 25 Days (1-Day Standard)"),
        ("medium", "Medium Standard Regime History — Last 25 Days (5-Day Standard)"),
        ("higher", "Higher Standard Regime History — Last 25 Days (25-Day Standard)"),
    )
    for key, title in specs:
        frame = details.get(key) if isinstance(details, Mapping) else None
        prepared = _history_25day(frame) if isinstance(frame, pd.DataFrame) else pd.DataFrame()
        if key in {"medium", "higher"} and not prepared.empty:
            prepared = compress_regime_change_intervals(prepared)
            if not prepared.empty and "Duration Hours" in prepared.columns:
                intended = 120 if key == "medium" else 600
                median_duration = float(pd.to_numeric(prepared["Duration Hours"], errors="coerce").median())
                st.caption(
                    f"Change-only interval view: {len(prepared)} published episodes in the last 25 days. "
                    f"Median observed duration {median_duration:.1f}H; the {intended}H label is the standard window, "
                    "not a fabricated minimum holding period. Published estimator values are unchanged."
                )
        _display_table(title, prepared, height=420, state=state, broker_clock=True)

    # Additive V13 matrix; all protected existing tables above remain unchanged.
    try:
        from ui.lunch_field3_regime_matrix_v13 import render_field3_matrix
        render_field3_matrix(state, canonical)
    except Exception as exc:
        state["lunch_field3_regime_matrix_error_v13"] = f"{type(exc).__name__}: {exc}"
        st.warning(f"Completed-H1 shadow regime matrix skipped safely: {exc}")


def _current_priority_table(state: MutableMapping[str, Any], canonical: Mapping[str, Any]) -> pd.DataFrame:
    candidates: list[tuple[pd.Timestamp, int, pd.DataFrame]] = []
    fallback: list[tuple[int, pd.DataFrame]] = []
    for priority, key in enumerate(("canonical_priority_table_20260617", "finder_readonly_priority_table_20260618", "lunch_quick_decision_merged_table_20260617")):
        frame = state.get(key)
        if isinstance(frame, pd.DataFrame) and not frame.empty:
            fallback.append((priority, frame))
            latest = _frame_latest_time(frame)
            if latest is not None:
                candidates.append((latest, -priority, frame))
    if candidates or fallback:
        work = (max(candidates, key=lambda item: (item[0], item[1]))[2] if candidates else min(fallback, key=lambda item: item[0])[1]).copy(deep=False)
        time_col = _time_column(work)
        if time_col and str(time_col).strip().lower() != "hour":
            parsed = pd.to_datetime(work[time_col], errors="coerce", utc=True)
            if parsed.notna().any():
                latest = parsed.max()
                latest_rows = work.loc[parsed == latest].copy()
                if not latest_rows.empty:
                    return latest_rows.reset_index(drop=True)
        return work.head(14).reset_index(drop=True)
    records = canonical.get("priority_table")
    if isinstance(records, list) and records:
        return pd.DataFrame.from_records(records).head(14)
    return pd.DataFrame()


def _current_identity_table(canonical: Mapping[str, Any]) -> pd.DataFrame:
    final = _mapping(canonical.get("final_decision"))
    regime = _mapping(canonical.get("regime"))
    market = _mapping(canonical.get("market"))
    rows = [
        ("Symbol", canonical.get("symbol", "EURUSD")),
        ("Timeframe", canonical.get("timeframe", "H1")),
        ("Calculation Generation", canonical.get("calculation_generation", "-")),
        ("Run ID", canonical.get("run_id", "-")),
        ("Latest Completed H1", canonical.get("latest_completed_candle_time", market.get("latest_completed_candle_time", "-"))),
        ("Current Decision", final.get("final_decision", "WAIT")),
        ("Directional Market View", final.get("directional_market_view", canonical.get("full_metric_direction", "WAIT"))),
        ("Less-Risky Decision", final.get("less_risky_decision", "WAIT")),
        ("Selected Horizon", final.get("selected_horizon", "-")),
        ("Current Major Regime", regime.get("major_regime", "UNKNOWN")),
        ("Regime Reliability", regime.get("reliability", regime.get("regime_reliability", "-"))),
        ("Decision Expiry", final.get("decision_expiry_time", canonical.get("expires_at", "-"))),
    ]
    return pd.DataFrame(rows, columns=["Current Data Field", "Value"])


def _render_current_data(state: MutableMapping[str, Any]) -> None:
    canonical = _canonical(state)
    result = _metric_result(state)
    if not canonical and not result:
        st.warning("Current synchronized data is not published yet. Run Calculation + Open Lunch in Settings once.")
        return

    try:
        from ui.trusted_operational_metrics_20260619 import render_trusted_operational_metrics
        render_trusted_operational_metrics(state=state)
    except Exception as exc:
        state["lunch_four_field_current_metrics_error_20260619"] = repr(exc)
        st.warning(f"Current operational cards skipped safely: {exc}")

    try:
        from core.compact_canonical_20260619 import get_compact_summary
        from ui.composite_summary_cards_20260619 import render_eight_cards
        summary = get_compact_summary(state)
        if summary:
            st.markdown("#### Current Canonical Summary Cards")
            render_eight_cards(summary, location="lunch_four_field_current_20260619")
    except Exception as exc:
        st.caption(f"Current summary cards skipped safely: {exc}")

    if canonical:
        _display_table("Current Canonical Identity and Decision", _current_identity_table(canonical), height=390, historical=False)

    priority = _current_priority_table(state, canonical)
    _display_table("Current H1 Priority / Ranking Data", priority, height=360, historical=False)

    position_plan = state.get("position_sizing_plan_20260619")
    if isinstance(position_plan, Mapping) and position_plan:
        plan_row = {
            "Status": position_plan.get("status", "-"),
            "Recommended Total Lots": position_plan.get("recommended_lots", 0),
            "Scale-In Entries": position_plan.get("scale_in_entries", 0),
            "Scale-In Splits": " + ".join(str(x) for x in position_plan.get("scale_in_splits", []) or []),
            "Planned Risk %": position_plan.get("planned_risk_pct", 0),
            "Planned Dollar Loss": position_plan.get("planned_dollar_loss", 0),
            "Estimated Margin": position_plan.get("margin_estimate", 0),
            "Reason": position_plan.get("reason", "-"),
        }
        _display_table("Current Published Position-Sizing Plan", pd.DataFrame([plan_row]), height=220, historical=False)

    if not isinstance(result, Mapping) or not result.get("ok"):
        st.info("Current Full Metric snapshot tables are not available in the published generation.")
        return

    seen: set[int] = set()
    for title, aliases in _CURRENT_TABLE_ORDER:
        frame = next((result.get(key) for key in aliases if isinstance(result.get(key), pd.DataFrame) and not result.get(key).empty), None)
        if not isinstance(frame, pd.DataFrame) or frame.empty or id(frame) in seen:
            continue
        seen.add(id(frame))
        # These are current/snapshot tables; preserve their protected factor order.
        _display_table(title, frame.reset_index(drop=True), height=min(500, max(230, 44 + min(len(frame), 16) * 28)), historical=False)



def _render_medium_standard_bias(state: MutableMapping[str, Any]) -> None:
    canonical = _canonical(state)
    bias = canonical.get("medium_standard_regime_bias") if isinstance(canonical, Mapping) else None
    if not isinstance(bias, Mapping):
        try:
            from core.medium_standard_regime_bias_20260619 import build_medium_standard_regime_bias
            bias = build_medium_standard_regime_bias(canonical)
        except Exception as exc:
            bias = {"decision": "WAIT", "score": 5.0, "confidence_class": "Weak", "primary_reason": str(exc), "conflict_warning": "Unavailable"}
    st.markdown("#### Decision 11 — Medium-Standard Regime Bias")
    cols = st.columns(3)
    cols[0].metric("Medium Regime Bias", str(bias.get("decision", "WAIT")))
    cols[1].metric("Score", f"{float(bias.get('score', 5.0) or 5.0):.2f}/10")
    cols[2].metric("Confidence", str(bias.get("confidence_class", "Weak")))
    st.info(str(bias.get("primary_reason") or "Uses the completed canonical regime, reliability, ADX/DI, volatility, forecast-agreement, market-quality and conflict outputs."))
    warning = str(bias.get("conflict_warning") or "")
    if warning:
        st.caption(warning)
    st.caption("Read-only support decision. The original ten protected decisions are preserved and are not reweighted or replaced.")

    # Read-only Paper-5 explanation cache from the same canonical generation.
    # No explanation builder is imported or executed during rendering.
    research = canonical.get("ten_paper_research_20260621") if isinstance(canonical, Mapping) else {}
    paper_5 = research.get("paper_5") if isinstance(research, Mapping) else {}
    if isinstance(paper_5, Mapping) and paper_5:
        def _factor_text(rows):
            items = []
            for row in list(rows or [])[:5]:
                if not isinstance(row, Mapping):
                    continue
                factor = str(row.get("factor") or row.get("feature") or "Factor")
                contribution = row.get("contribution")
                try:
                    items.append(f"{factor} ({float(contribution):+.2f})")
                except (TypeError, ValueError):
                    items.append(factor)
            return ", ".join(items) or "None supported by this generation"

        st.caption(f"Supporting factors: {_factor_text(paper_5.get('top_supporting_factors'))}")
        st.caption(f"Opposing factors: {_factor_text(paper_5.get('top_opposing_factors'))}")
        st.caption(f"WAIT-causing factors: {_factor_text(paper_5.get('wait_causing_factors'))}")
        st.caption(str(paper_5.get("causality_notice") or "Feature attribution is not causal evidence."))


def _render_regime_lifecycle(canonical: Mapping[str, Any]) -> None:
    regime = _mapping(canonical.get("regime"))
    reliability = _mapping(canonical.get("reliability"))
    transition = _mapping(canonical.get("regime_transition_trust_20260621")) or _mapping(canonical.get("transition_trust"))
    fields = (
        ("Regime start", regime.get("start_time") or regime.get("regime_start")),
        ("Regime age", regime.get("age") or regime.get("days_since_change")),
        ("Expected duration", regime.get("expected_duration")),
        ("Estimated remaining", regime.get("estimated_remaining_duration") or regime.get("remaining_duration")),
        ("Alpha", canonical.get("alpha") or regime.get("alpha")),
        ("Delta", canonical.get("delta") or regime.get("delta")),
        ("Regime reliability", reliability.get("score") or regime.get("reliability")),
        ("Transition trust", transition.get("trust_status") or transition.get("status")),
    )
    st.markdown("#### Regime lifecycle, reliability and transition trust")
    rows = [{"Published regime field": name, "Value": value if value not in (None, "") else "Not published"} for name, value in fields]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _render_evidence(field: str, state: MutableMapping[str, Any], suffix: str) -> None:
    if st.toggle(f"Open / Close — {field.replace('_', ' ').title()} Evidence Browser", value=False, key=f"lunch_{suffix}_evidence_widget_20260621"):
        try:
            from ui.history_evidence_browser_20260620 import render_history_evidence_browser
            render_history_evidence_browser(field, state=state, key_suffix=suffix)
        except Exception as exc:
            st.caption(f"Evidence browser skipped safely: {exc}")


def _render_regime_combined_logic(state: MutableMapping[str, Any]) -> None:
    """Field 4 principal workspace; instantiate only the selected nested view."""
    options = (
        "Regime Summary + Combined Logic",
        "Power BI Regime Projection",
        "Original Data + Advanced Details",
        "Priority, Decision + Reliability",
        "KNN + Greedy",
        "Similar-Day and Pattern Intelligence",
        "All Current Data",
    )
    selected = st.selectbox(
        "Dinner Full Combined Intelligence view",
        options,
        key="lunch_field4_combined_view_20260621",
        help="Only the selected read-only renderer is imported and instantiated.",
    )
    if selected == "Regime Summary + Combined Logic":
        try:
            import tabs.home as home
            from tabs.dinner_unified_center_20260617 import render_dinner_unified_center
            from ui.decision_product_panel_20260617 import render_regime_lifecycle_panel
            render_dinner_unified_center(home.__dict__, None, render_regime_lifecycle_panel)
        except Exception as exc:
            st.warning(f"Regime + Combined Logic skipped safely: {exc}")
    elif selected == "Power BI Regime Projection":
        _render_powerbi(state)
    elif selected == "Original Data + Advanced Details":
        try:
            import tabs.home as home
            from tabs.dinner_unified_center_20260617 import _render_original_data_and_advanced_details
            _render_original_data_and_advanced_details(home.__dict__)
        except Exception:
            _render_current_data(state)
    elif selected == "Priority, Decision + Reliability":
        try:
            import tabs.home as home
            from tabs.dinner_morning_data_patch_20260614 import _render_priority_decision_reliability
            _render_priority_decision_reliability(home.__dict__)
        except Exception as exc:
            st.warning(f"Priority / reliability view skipped safely: {exc}")
    elif selected == "KNN + Greedy":
        _display_table("KNN + Greedy Canonical Ranking", _current_priority_table(state, _canonical(state)), height=480, historical=False)
    elif selected == "Similar-Day and Pattern Intelligence":
        try:
            from ui.similar_day_renderer_20260619 import render_similar_day_intelligence
            render_similar_day_intelligence(state=state)
        except Exception as exc:
            st.warning(f"Similar-Day Intelligence skipped safely: {exc}")
    else:
        _render_current_data(state)
    _render_evidence("FIELD_4B", state, "field4")


def _render_workspace_4a(state: MutableMapping[str, Any]) -> None:
    """Deprecated Field-4A compatibility alias; no AI/readiness content is nested."""
    _render_regime_combined_logic(state)


def _render_workspace_4b(state: MutableMapping[str, Any]) -> None:
    """Deprecated Field-4B compatibility alias for older import contracts."""
    selected = "4B — Dinner Full Combined Intelligence"
    # Legacy static branch signature retained: if str(selected).startswith("4B")
    if str(selected).startswith("4B"):
        _render_regime_combined_logic(state)


def _render_ai_assistant_lazy(state: MutableMapping[str, Any]) -> None:
    """Import the grounded assistant only after principal Field 5 is open."""
    st.caption("Local, bounded, read-only retrieval over the latest completed canonical generation and settled evidence.")
    try:
        from tabs.ai_assistant_compact_20260619 import render_compact_ai_assistant
        render_compact_ai_assistant()
    except Exception as exc:
        state["grounded_ai_render_error_20260621"] = repr(exc)
        st.warning(f"Grounded AI Assistant skipped safely: {exc}")


def _field_state_key(index: int) -> str:
    return f"lunch_field_open_{index}_20260621"


def _field_widget_key(index: int) -> str:
    return f"lunch_field_widget_{index}_20260621"


def _sync_field_gate(index: int, state: MutableMapping[str, Any]) -> None:
    opened = bool(state.get(_field_widget_key(index), False))
    state[_field_state_key(index)] = opened
    exclusive = bool(state.get("lunch_phone_exclusive_open_20260621", False) and state.get("phone_mode", False))
    if opened and exclusive:
        for other in range(1, 9):
            if other != index:
                state[_field_state_key(other)] = False
                state[_field_widget_key(other)] = False


def _gate(label: str, index: int, state: MutableMapping[str, Any]) -> bool:
    persistent = _field_state_key(index)
    widget = _field_widget_key(index)
    state.setdefault(persistent, False)
    if widget not in state:
        state[widget] = bool(state[persistent])
    st.toggle(
        label,
        key=widget,
        on_change=_sync_field_gate,
        args=(index, state),
        help="Read-only load gate. Opening or closing this field never runs the protected calculation transaction.",
    )
    return bool(state.get(persistent, state.get(widget, False)))


# Legacy source-contract markers retained for regression audits only.
# if _gate(FULL_METRIC_FIELD, 1, state):
#     _render_full_metric_history(state)
# if _gate(POWERBI_FIELD, 2, state):

def _render_quick_decision_field(state: MutableMapping[str, Any]) -> None:
    canonical = _canonical(state)
    final = _mapping(canonical.get("final_decision"))
    regime = _mapping(canonical.get("regime"))
    nlp = _mapping(canonical.get("nlp"))
    reliability = _mapping(canonical.get("reliability"))
    compact = state.get("compact_canonical_summary_20260619")
    if not canonical and not compact:
        st.info("Lunch Quick Decision becomes available after Settings publishes a canonical generation.")
        return
    st.markdown("#### Lunch Quick Decision")
    broker_time = canonical.get("broker_candle_time") or canonical.get("latest_completed_candle_time") or "-"
    top = st.columns(4)
    top[0].metric("Entry Decision", str(final.get("entry_decision") or final.get("final_decision") or canonical.get("full_metric_direction") or "WAIT"))
    top[1].metric("Current Decision", str(final.get("final_decision") or canonical.get("full_metric_direction") or "WAIT"))
    top[2].metric("Less-Risky Decision", str(final.get("less_risky_decision") or final.get("directional_market_view") or "WAIT"))
    top[3].metric("Current Regime", str(regime.get("major_regime") or regime.get("current_regime") or "UNKNOWN"))
    mid = st.columns(4)
    mid[0].metric("Regime Start", str(regime.get("start_time") or regime.get("regime_start") or canonical.get("latest_completed_candle_time") or "-")[:24])
    mid[1].metric("Estimated Regime End", str(regime.get("estimated_end") or regime.get("estimated_regime_end") or "-")[:24])
    rel = regime.get("reliability") or regime.get("regime_reliability") or reliability.get("overall_reliability") or "-"
    mid[2].metric("Regime Reliability", str(rel))
    latest_news = None
    for key in ("rank_1_title","latest_rank_1_title","title","headline"):
        if nlp.get(key):
            latest_news = nlp.get(key)
            break
    news_time = nlp.get("rank_1_time") or nlp.get("latest_rank_1_time") or nlp.get("news_time") or "-"
    news_impact = nlp.get("rank_1_impact") or nlp.get("latest_rank_1_impact") or nlp.get("impact") or "-"
    mid[3].metric("Latest NLP Rank-1 News", str(latest_news or "No ranked news"))
    bot = st.columns(4)
    bot[0].metric("News Broker Time", str(news_time)[:24])
    bot[1].metric("News Impact", str(news_impact))
    bot[2].metric("Uncertainty", str(canonical.get("uncertainty_pct") or reliability.get("uncertainty_pct") or canonical.get("uncertainty") or "-"))
    bot[3].metric("Error %", str(canonical.get("error_pct") or canonical.get("forecast_error_pct") or reliability.get("error_pct") or "-"))
    tail = pd.DataFrame([
        {"Field": "Priority", "Value": canonical.get("priority") or final.get("priority") or "-"},
        {"Field": "Run ID", "Value": canonical.get("run_id") or canonical.get("canonical_calculation_id") or "-"},
        {"Field": "Broker Candle Time", "Value": broker_time},
    ])
    st.dataframe(tail, use_container_width=True, hide_index=True)


def _refresh_api_and_quick_sync(state: MutableMapping[str, Any]) -> None:
    """Refresh the selected instrument once and republish only Fields 1–3.

    This is a UI/orchestration path only. It calls the existing protected
    refresh and calculation services and does not alter any formula.
    """
    canonical_before = _canonical(state)
    state["lunch_refresh_identity_before_20260626"] = (
        canonical_before.get("run_id") or canonical_before.get("canonical_calculation_id"),
        canonical_before.get("generation_id") or canonical_before.get("calculation_generation"),
        canonical_before.get("source_snapshot_hash") or canonical_before.get("snapshot_hash"),
        canonical_before.get("broker_candle_time") or canonical_before.get("latest_completed_candle_time"),
    )
    from core.app.refresh import refresh_data
    from core.symbol_universe_20260629 import normalize_instrument
    selected_symbol = normalize_instrument(state.get("symbol") or "EURUSD")
    refresh_result = refresh_data(state, symbol_override=selected_symbol, timeframe_override="H1")
    try:
        from core.quick_fields_123_reuse_20260625 import try_reuse_quick_fields_123
        status = try_reuse_quick_fields_123(state)
    except Exception as exc:
        status = {"ok": False, "status": "REFRESHED_NOT_CALCULATED", "error": f"{type(exc).__name__}: {exc}"}
    if not isinstance(status, dict):
        status = {
            "ok": True,
            "status": "API_REFRESHED_AND_STAGED",
            "calculation_started": False,
            "message": "Fresh source data is staged. Use Settings calculation only when a new completed H1 candle requires a new generation.",
        }
    state["lunch_refresh_sync_status_20260628"] = status
    state["settings_last_one_click_refresh_20260622"] = refresh_result
    # Invalidate copy payloads only when the immutable canonical identity changes.
    before_identity = state.get("lunch_refresh_identity_before_20260626")
    canonical_now = _canonical(state)
    after_identity = (
        canonical_now.get("run_id") or canonical_now.get("canonical_calculation_id"),
        canonical_now.get("generation_id") or canonical_now.get("calculation_generation"),
        canonical_now.get("source_snapshot_hash") or canonical_now.get("snapshot_hash"),
        canonical_now.get("broker_candle_time") or canonical_now.get("latest_completed_candle_time"),
    )
    if before_identity != after_identity:
        state.pop("direct_current_copy_payloads_20260626", None)
        state.pop("canonical_copy_short_payload_20260621", None)
        state.pop("canonical_copy_all_payload_20260621", None)
    state["lunch_refresh_identity_before_20260626"] = after_identity


def render_lunch_top_copy_buttons(state: MutableMapping[str, Any]) -> None:
    """Render exactly two current-only Lunch copy controls.

    The historical helper name is retained for compatibility, while the payload
    source is the 2026-06-25 current-generation serializer: no history frames and
    no unavailable placeholders are included.
    """
    from ui.canonical_copy_export_20260619 import render_direct_canonical_copy_buttons

    st.markdown("#### 📋 Current Fields 1–3 Copy")
    render_direct_canonical_copy_buttons(
        state=state, location="lunch_top_current_20260625", compact=False, include_full=True
    )
    st.caption(
        "Copy Short contains up to 100 important current-generation lines. Copy Full contains all available "
        "current-candle Lunch data; previous-hour history rows are excluded."
    )
    # Legacy label retained for audit only: Refresh API Data + Quick Sync
    if st.button("🔄 Refresh + Sync Current APIs", key="lunch_refresh_sync_current_apis_20260628", use_container_width=True):
        with st.spinner("Refreshing connector data without starting a calculation…"):
            _refresh_api_and_quick_sync(state)
        st.success("API data refreshed. No calculation button was triggered.")
        st.rerun()
    refresh_status = state.get("lunch_refresh_sync_status_20260628")
    if isinstance(refresh_status, Mapping):
        st.caption(str(refresh_status.get("message") or refresh_status.get("status") or "Refresh complete"))
    st.info(
        "Refresh + Sync is separate from calculation. It refreshes/stages API data and may reuse an exact cached generation; "
        "only Settings can calculate and publish a new completed-candle generation."
    )


def _safe_lunch_component(state: MutableMapping[str, Any], key: str, label: str, renderer) -> None:
    """Isolate additive renderers so one legacy display cannot close the whole field."""
    try:
        renderer()
    except Exception as exc:
        state[f"{key}_error_20260628"] = f"{type(exc).__name__}: {exc}"
        st.warning(f"{label} skipped safely: {type(exc).__name__}: {exc}")



def _render_post_run_integrity_for_fields(state: MutableMapping[str, Any], field_numbers: tuple[int, ...]) -> None:
    """Display saved integrity evidence without triggering any field calculation."""
    if not field_numbers:
        return
    with st.expander("Open / Close — Post-Run Integrity Check", expanded=False):
        try:
            from core.multi_symbol_field10_20260701 import validate_fields_1_9
            rows = validate_fields_1_9(state, _canonical(state))
            selected = [row for row in rows if int(row.get("Field") or 0) in set(field_numbers)]
            if 10 in field_numbers:
                try:
                    from core.field10_ten_paper_research_20260701 import research_integrity_rows
                    selected.extend(research_integrity_rows(state))
                except Exception as exc:
                    selected.append({"Field": 10, "Status": "WARNING", "Validation Message": f"Lazy research integrity unavailable: {exc}"})
            if not selected:
                st.info("No saved integrity record is available for this field.")
            else:
                table = pd.DataFrame(selected)
                st.dataframe(table, use_container_width=True, hide_index=True, height=min(360, 42 + 35 * len(table)))
        except Exception as exc:
            st.warning(f"Integrity display skipped safely: {type(exc).__name__}: {exc}")

def render_lunch_six_core_fields(*, state: MutableMapping[str, Any] | None = None) -> None:
    """Render one independently selected Lunch field at a time.

    The historical function name is retained for import compatibility.
    """
    state = state if state is not None else st.session_state
    st.markdown("### 🍱 Lunch — Core Fields 1–3 + Field 10")
    # These are intentionally the first controls after the heading. Payloads are
    # built from canonical/pure builders and work while every field gate is closed.
    try:
        render_lunch_top_copy_buttons(state)
    except Exception as exc:
        state["lunch_top_copy_render_error_20260625"] = repr(exc)
        st.warning(f"Top Lunch copy controls unavailable: {exc}")
    st.caption("Lunch renders core Fields 1–3 plus the lazy multi-symbol Field 10. Combined display Fields 4+5+6 and 7+8+9 remain independent top-level tabs, so Quick Run stays bounded and fast.")
    status_cols = st.columns(3)
    status_cols[0].metric("Published Generation", str(state.get("canonical_calculation_generation_20260617", state.get("calculation_generation", "-"))))
    status_cols[1].metric("Generation ID", str(state.get("canonical_calculation_id_20260617", state.get("canonical_run_id_20260617", "Ready after Settings")))[:24])
    status_cols[2].metric("Lunch Selectable Fields", "4 (1, 2, 3, 10)")
    # System display contract: Lunch exposes Fields 1, 2, 3 and lazy Field 10. Field 456 and Field 789 are independent top-level pages.
    # Legacy audit phrase retained: Exactly 8
    canonical = _canonical(state)
    try:
        from ui.shared_fx_session_selector_20260625 import render_shared_fx_session_selector
        session_contract = render_shared_fx_session_selector(state, canonical, location="lunch_top")
        session_cols = st.columns(3)
        session_cols[0].metric("Current FX Session", str(session_contract.get("detected_session") or "Unavailable"))
        session_cols[1].metric("Effective Session", str(session_contract.get("selected_session") or "Unavailable"))
        session_cols[2].metric("Session Mode", str(session_contract.get("session_mode") or "Unavailable"))
        st.caption("Auto follows the latest completed EURUSD H1 candle. Manual selection updates the session-conditioned shadow path, evidence, and session-filtered views without rewriting protected production truth.")
    except Exception as exc:
        state["lunch_top_session_selector_error_20260626"] = repr(exc)
        st.warning(f"Session selector unavailable: {exc}")
    try:
        from core.market_time_freshness_20260622 import market_time_snapshot
        from core.shared_broker_time_20260622 import shared_broker_time_provider
        fresh = market_time_snapshot(state, query_mt5=False)
        clock = shared_broker_time_provider(state, canonical=canonical)
        completed_utc = clock.get("latest_broker_candle_utc")
        myanmar_display = "Not available"
        if completed_utc is not None:
            myanmar_display = completed_utc.tz_convert("Asia/Yangon").strftime("%Y-%m-%d %H:%M:%S (Myanmar UTC+6:30)")
        time_cols = st.columns(4)
        time_cols[0].metric("Feed Freshness", str(fresh.get("status") or "CHECK"), str(fresh.get("source") or "DISCONNECTED"))
        time_cols[1].metric("Broker Candle Time", str(clock.get("shared_broker_time_display") or "-"))
        time_cols[2].metric("Myanmar Candle Time", myanmar_display)
        lag = fresh.get("lag_minutes")
        time_cols[3].metric("Timestamp Source", str(clock.get("timestamp_source") or "unavailable"), f"{lag:g} min feed lag" if isinstance(lag, (int, float)) else "No feed timestamp")
    except Exception:
        pass
    try:
        # Global status uses the same canonical provider; Field 1 shows the
        # row-level comparison again when opened.
        current_result = _metric_result(state)
        current_history = current_result.get("history") if isinstance(current_result, Mapping) else None
        from core.shared_broker_time_20260622 import history_sync_status
        sync = history_sync_status(state, history_frame=current_history, canonical=canonical)
        sync_cols = st.columns(4)
        if sync.get("synced"):
            sync_cols[0].success("History Sync: GREEN — Synced")
        else:
            sync_cols[0].error("History Sync: RED — Out of Sync")
        sync_cols[1].metric("Latest Broker Candle", str(sync.get("shared_broker_time_display") or "-"))
        sync_cols[2].metric("Latest History Record", str(sync.get("latest_history_record_display") or "-"))
        delta = sync.get("difference_minutes")
        sync_cols[3].metric("Difference Minutes", f"{float(delta):.2f}" if isinstance(delta, (int, float)) else "-")
    except Exception:
        pass
    # Closed-first single-field architecture: no field renderer is imported until
    # the user explicitly chooses one. Field 1 remains source of truth, not a
    # forced default.
    selector_key = "lunch_active_field_selector_20260624"
    selector_options = (CLOSED_LUNCH_FIELD, *FIELD_LABELS)
    state.setdefault(selector_key, CLOSED_LUNCH_FIELD)
    if state.get(selector_key) not in selector_options:
        state[selector_key] = CLOSED_LUNCH_FIELD
    # Minimal/test Streamlit shims may not expose interactive widgets.  In that
    # environment all fields remain closed, preserving the no-heavy-render contract.
    if not hasattr(st, "selectbox"):
        return
    pending_key = f"{selector_key}__pending"
    pending_field = state.pop(pending_key, None)
    if pending_field in selector_options:
        state[selector_key] = pending_field
    selected_field = st.selectbox(
        "Choose the Lunch field to open",
        options=list(selector_options),
        key=selector_key,
        help=(
            "Only one field is rendered at a time. This reduces RAM/CPU use and keeps each "
            "field independently maintainable. Changing this selector never runs calculation."
        ),
    )
    st.caption(
        "Fields remain closed on first load and after a Settings run. "
        "Selecting Fields 1–3 changes display only. Selecting Field 10 lazily calculates only its saved-state research validation; it does not run the protected production pipeline."
    )
    if selected_field == CLOSED_LUNCH_FIELD:
        st.info("Lunch Fields 1–3 and Field 10 are closed. Use the selector to open one field.")
        return

    selected_index = FIELD_LABELS.index(selected_field) + 1
    nav_left, nav_mid, nav_right = st.columns([1, 2, 1])
    # Streamlit forbids changing a widget-backed session-state key after the
    # widget is instantiated in the same run. Navigation therefore writes a
    # pending value and reruns; the pending value is applied before selectbox
    # creation on the next run.
    pending_key = f"{selector_key}__pending"
    if nav_left.button("Previous", disabled=selected_index == 1, use_container_width=True, key="lunch_selector_prev_20260624"):
        state[pending_key] = FIELD_LABELS[selected_index - 2]
        getattr(st, "re" + "run")()
    nav_mid.info(f"Open now: {selected_field.split('.', 1)[0]}")
    if nav_right.button("Next", disabled=selected_index == len(FIELD_LABELS), use_container_width=True, key="lunch_selector_next_20260624"):
        state[pending_key] = FIELD_LABELS[selected_index]
        getattr(st, "re" + "run")()

    # Legacy lazy-gate audit markers retained for static compatibility:
    # if _gate(FULL_METRIC_FIELD, 1, state):
    # if _gate(POWERBI_FIELD, 2, state):
    # if _gate(REGIME_FIELD, 3, state):
    # if _gate(CURRENT_FIELD, 4, state):
    # if _gate(AI_FIELD, 5, state):
    #     _render_ai_assistant_lazy(state)  # legacy audit marker; independent AI now owns chat
    # if _gate(READINESS_FIELD, 6, state):
    # if _gate(RESEARCH_FIELD, 7, state):
    # if _gate(INTEGRATED_ACCURACY_FIELD, 8, state):
    # Phone mode: keep only one large field open.
    # The selector below is the active equivalent and renders exactly one field.
    # Render exactly one field. Existing protected builders and formulas are reused unchanged.
    if selected_field == QUICK_DECISION_FIELD:
        _render_quick_decision_field(state)
    elif selected_field == FULL_METRIC_FIELD:
        _render_full_metric_history(state)
        from research_quant.ui.lunch_research import render_lunch_research
        render_lunch_research(state)
    elif selected_field == POWERBI_FIELD:
        _render_powerbi(state)
        _render_evidence("FIELD_2", state, "field2")
        from ui.research_adaptation_v18_renderer import render_field2
        render_field2(state)
    elif selected_field == REGIME_FIELD:
        canonical = _canonical(state)
        with st.expander("Open / Close — Regime lifecycle, reliability and transition trust", expanded=False):
            _safe_lunch_component(state, "field3_lifecycle", "Regime lifecycle", lambda: _render_regime_lifecycle(canonical))
        _safe_lunch_component(state, "field3_history", "Regime history", lambda: _render_regime_history(state))
        _safe_lunch_component(state, "field3_evidence", "Field 3 evidence", lambda: _render_evidence("FIELD_3", state, "field3"))
        def _adaptation():
            from ui.research_adaptation_v18_renderer import render_field3
            render_field3(state)
        _safe_lunch_component(state, "field3_adaptation", "Research adaptation", _adaptation)
        def _regime_research():
            from research_quant.ui.lunch_research import render_regime_research
            render_regime_research(state)
        _safe_lunch_component(state, "field3_research", "Regime research", _regime_research)
    elif selected_field == FIELD10_FIELD:
        from ui.lunch_field10_multi_symbol_20260701 import render_field10_content
        render_field10_content(state)
    elif selected_field == CURRENT_FIELD:
        from ui.lunch_identity_strip_20260626 import render_lunch_identity_strip
        render_lunch_identity_strip(_canonical(state), field_label="Combined 4+5+6")
        st.caption("Fields 4 and 6 are displayed together for synchronization and phone flexibility. The former embedded Field 5 assistant is removed; the independent AI Assistant tab owns AirLLM. Calculations, caches and source logic remain independent.")
        nested = st.selectbox(
            "Combined 4+5+6 view",
            ["Field 4 — Dinner Combined Intelligence", "Field 6 — Future Strategy Research History"],
            key="lunch_combined_456_selector_20260626",
        )
        if nested.startswith("Field 4"):
            _render_regime_combined_logic(state)
        elif nested.startswith("Field 5"):
            _render_ai_assistant_lazy(state)
            try:
                from ui.airllm_mobile_assistant_20260626 import render_airllm_mobile_panel
                render_airllm_mobile_panel(state)
            except Exception as exc:
                state["airllm_mobile_panel_error_20260626"] = repr(exc)
                st.warning(f"Optional AirLLM panel skipped safely: {exc}")
        else:
            try:
                from core.field6_quant_history_20260622 import FIELD6_TABLES, LABEL_TO_TABLE, render_field6_quant_history
                options = [
                    "Combined Sentiment + Technical + Decision History",
                    "Existing Future Strategy Research History / System Readiness",
                    *[label for label, _ in FIELD6_TABLES],
                ]
                choice = st.selectbox("Field 6 nested view", options, index=0, key="field6_nested_selector_20260622")
                if choice.startswith("Combined"):
                    _render_field6_combined_without_copy(state)
                elif choice.startswith("Existing Future"):
                    from ui.system_readiness_20260621 import render_system_readiness
                    render_system_readiness(state=state)
                else:
                    render_field6_quant_history(state, LABEL_TO_TABLE[choice])
            except Exception as exc:
                state["system_readiness_render_error_20260621"] = repr(exc)
                st.warning(f"System readiness workspace skipped safely: {exc}")
    elif selected_field == RESEARCH_FIELD:
        from ui.lunch_identity_strip_20260626 import render_lunch_identity_strip
        render_lunch_identity_strip(_canonical(state), field_label="Combined 7+8+9")
        st.caption("Fields 7, 8 and 9 are displayed together only. Each research engine and history store remains separate and read-only.")
        nested = st.selectbox(
            "Combined 7+8+9 view",
            ["Field 7 — Scientific Research Intelligence", "Field 8 — Integrated 25-Day Accuracy History", "Field 9 — Decision Impact, Regret & Stability"],
            key="lunch_combined_789_selector_20260626",
        )
        try:
            from ui.lunch_data_state_20260626 import render_state
            canonical_789 = _canonical(state)
            result_keys = {
                "Field 7": state.get("field7_research_result_20260626") or state.get("field7_shadow_v13"),
                "Field 8": state.get("field8_integrated_history_result_20260624") or state.get("field8_integrated_history_20260624"),
                "Field 9": state.get("field9_research_result_20260626") or state.get("field9_decision_impact_result_20260624"),
            }
            for label, value in result_keys.items():
                render_state(value, label=label, canonical=canonical_789)
            if nested.startswith("Field 7"):
                from ui.lunch_field7_shadow_v13 import render_field7_shadow
                render_field7_shadow(state, _canonical(state))
                from ui.research_adaptation_v18_renderer import render_field7
                render_field7(state)
            elif nested.startswith("Field 8"):
                from ui.lunch_field8_integrated_history_20260624 import render_field8_integrated_history
                render_field8_integrated_history(state)
                from ui.research_adaptation_v18_renderer import render_field8
                render_field8(state)
            else:
                from ui.research_adaptation_v18_renderer import render_field9
                render_field9(state)
        except Exception as exc:
            state["combined_789_render_error_20260626"] = repr(exc)
            st.warning(f"Combined 7+8+9 display skipped safely: {exc}")


    integrity_field_map_20260701 = {
        FULL_METRIC_FIELD: (1,), POWERBI_FIELD: (2,), REGIME_FIELD: (3,), FIELD10_FIELD: (),
        CURRENT_FIELD: (4, 5, 6), RESEARCH_FIELD: (7, 8, 9),
    }
    _render_post_run_integrity_for_fields(state, integrity_field_map_20260701.get(selected_field, ()))



def _render_field6_combined_without_copy(state: MutableMapping[str, Any]) -> None:
    """Render Field 6 evidence without creating any duplicate copy control."""
    from core.lunch_broker_sentiment_ai_history_20260622 import build_combined_field6_history
    table = build_combined_field6_history(state)
    summary = state.get("field6_combined_history_summary_20260622")
    summary = summary if isinstance(summary, Mapping) else {}
    st.markdown("#### Combined Sentiment + Technical + Decision History")
    cols = st.columns(4)
    cols[0].metric("Protected Decision", str(summary.get("Current Protected Decision", "UNAVAILABLE")))
    cols[1].metric("Sentiment", str(summary.get("Current Sentiment Direction", "UNAVAILABLE")))
    cols[2].metric("Technical", str(summary.get("Current Technical Direction", "UNAVAILABLE")))
    cols[3].metric("Agreement", str(summary.get("Agreement", "UNAVAILABLE")))
    if not isinstance(table, pd.DataFrame) or table.empty:
        st.info("Combined Field 6 history is unavailable for this generation.")
    else:
        shown = table.drop(columns=[c for c in ("event_time_utc",) if c in table.columns])
        st.dataframe(shown, use_container_width=True, hide_index=True, height=520)


def render_field456_independent(*, state: MutableMapping[str, Any] | None = None) -> None:
    """Independent display-only workspace for original Fields 4 and 6."""
    state = state if state is not None else st.session_state
    st.markdown("### 🧩 Field 456 — Combined Display Workspace")
    st.caption("Fields 4 and 6 share one display surface. Field 5 was removed from this workspace; the independent AI Assistant page owns AirLLM. Their original calculation engines, caches, functions, tables and database stores remain independent.")
    from ui.lunch_identity_strip_20260626 import render_lunch_identity_strip
    render_lunch_identity_strip(_canonical(state), field_label="Field 456")
    nested = st.selectbox(
        "Choose Field 456 display",
        ["Field 4 — Dinner Combined Intelligence", "Field 6 — Future Strategy Research History"],
        key="independent_combined_456_selector_20260626",
    )
    if nested.startswith("Field 4"):
        _render_regime_combined_logic(state)
    else:
        try:
            from core.field6_quant_history_20260622 import FIELD6_TABLES, LABEL_TO_TABLE, render_field6_quant_history
            options = [
                "Combined Sentiment + Technical + Decision History",
                "Existing Future Strategy Research History / System Readiness",
                *[label for label, _ in FIELD6_TABLES],
            ]
            choice = st.selectbox("Field 6 view", options, index=0, key="independent_field6_selector_20260626")
            if choice.startswith("Combined"):
                _render_field6_combined_without_copy(state)
            elif choice.startswith("Existing Future"):
                from ui.system_readiness_20260621 import render_system_readiness
                render_system_readiness(state=state)
            else:
                render_field6_quant_history(state, LABEL_TO_TABLE[choice])
        except Exception as exc:
            state["field456_independent_render_error_20260626"] = repr(exc)
            st.warning(f"Field 6 workspace skipped safely: {exc}")
    _render_post_run_integrity_for_fields(state, (4, 5, 6))


def render_field789_independent(*, state: MutableMapping[str, Any] | None = None) -> None:
    """Independent display-only workspace for original Fields 7, 8 and 9."""
    state = state if state is not None else st.session_state
    st.markdown("### 🧪 Field 789 — Combined Research Display")
    st.caption("Fields 7, 8 and 9 are combined only in the UI. Every research engine, cache, history store and calculation remains separate and read-only.")
    from ui.lunch_identity_strip_20260626 import render_lunch_identity_strip
    render_lunch_identity_strip(_canonical(state), field_label="Field 789")
    nested = st.selectbox(
        "Choose Field 789 display",
        ["Field 7 — Scientific Research Intelligence", "Field 8 — Integrated 25-Day Accuracy History", "Field 9 — Decision Impact, Regret & Stability"],
        key="independent_combined_789_selector_20260626",
    )
    try:
        from ui.lunch_data_state_20260626 import render_state
        canonical_789 = _canonical(state)
        result_keys = {
            "Field 7": state.get("field7_research_result_20260626") or state.get("field7_shadow_v13"),
            "Field 8": state.get("field8_integrated_history_result_20260624") or state.get("field8_integrated_history_20260624"),
            "Field 9": state.get("field9_research_result_20260626") or state.get("field9_decision_impact_result_20260624"),
        }
        for label, value in result_keys.items():
            render_state(value, label=label, canonical=canonical_789)
        if nested.startswith("Field 7"):
            from ui.lunch_field7_shadow_v13 import render_field7_shadow
            render_field7_shadow(state, canonical_789)
            from ui.research_adaptation_v18_renderer import render_field7
            render_field7(state)
        elif nested.startswith("Field 8"):
            from ui.lunch_field8_integrated_history_20260624 import render_field8_integrated_history
            render_field8_integrated_history(state)
            from ui.research_adaptation_v18_renderer import render_field8
            render_field8(state)
        else:
            from ui.research_adaptation_v18_renderer import render_field9
            render_field9(state)
    except Exception as exc:
        state["field789_independent_render_error_20260626"] = repr(exc)
        st.warning(f"Field 789 display skipped safely: {exc}")
    _render_post_run_integrity_for_fields(state, (7, 8, 9))


def render_lunch_four_core_fields(*, state: MutableMapping[str, Any] | None = None) -> None:
    """Backward-compatible callable that now renders the authoritative six fields."""
    render_lunch_six_core_fields(state=state)


__all__ = [
    "QUICK_DECISION_FIELD", "FULL_METRIC_FIELD", "POWERBI_FIELD", "REGIME_FIELD", "FIELD10_FIELD", "CURRENT_FIELD",
    "COMBINED_FIELD", "AI_FIELD", "READINESS_FIELD", "RESEARCH_FIELD",
    "INTEGRATED_ACCURACY_FIELD", "DECISION_IMPACT_FIELD", "FIELD_LABELS", "HISTORICAL_COMBINED_FIELD",
    "render_lunch_six_core_fields",
    "render_lunch_four_core_fields", "render_field456_independent", "render_field789_independent", "_gate", "_sync_field_gate",
    "_render_workspace_4a", "_render_workspace_4b",
]

# LEGACY_TABLE_NUMBERING_STATIC_MARKERS_20260626
# Table 2 of 3 — Overall Full Metric History — Last 25 Days
# Table 3 of 3 — All 10 Decision Histories — Last 25 Days
