"""Two-way symbol selector shared by Settings, Home, and connector surfaces."""
from __future__ import annotations

from typing import Any, MutableMapping


def render_global_symbol_selector(
    state: MutableMapping[str, Any],
    *,
    key_prefix: str,
    auto_refresh_library: bool = True,
    show_refresh_status: bool = True,
) -> str:
    import streamlit as st

    from core.symbol_universe_20260629 import (
        SYMBOL_GROUPS, apply_symbol_selection, category_for_symbol,
        normalize_instrument,
    )

    active = normalize_instrument(state.get("symbol") or "EURUSD")
    categories = list(SYMBOL_GROUPS) + ["Type another symbol"]
    default_category = category_for_symbol(active)
    if default_category not in categories:
        default_category = "Type another symbol"

    st.markdown("##### Global Instrument Selection")
    mode = st.radio(
        "Choose from the library or type a broker/provider symbol",
        ["Instrument library", "Type symbol"],
        horizontal=True,
        key=f"{key_prefix}_symbol_mode_20260629",
    )

    selected = active
    refresh_result: dict[str, Any] | None = None
    if mode == "Instrument library":
        current_category = default_category if default_category != "Type another symbol" else categories[0]
        category = st.selectbox(
            "Instrument group",
            list(SYMBOL_GROUPS),
            index=list(SYMBOL_GROUPS).index(current_category) if current_category in SYMBOL_GROUPS else 0,
            key=f"{key_prefix}_symbol_category_20260629",
        )
        options = list(SYMBOL_GROUPS[category])
        index = options.index(active) if active in options else 0
        selected = st.selectbox(
            "Symbol",
            options,
            index=index,
            key=f"{key_prefix}_symbol_library_20260629",
            help="20 FX pairs, 20 high-volume equities, the S&P 500 index, plus existing metals/crypto symbols.",
        )
        selected = normalize_instrument(selected)
        remembered = normalize_instrument(state.get(f"{key_prefix}_last_library_symbol_20260629") or active)
        state[f"{key_prefix}_last_library_symbol_20260629"] = selected
        if selected != active and selected != remembered:
            result = apply_symbol_selection(state, selected, reason=f"{key_prefix}:library")
            if auto_refresh_library and result.get("changed"):
                try:
                    from core.app.refresh import refresh_data
                    refresh_result = refresh_data(
                        state,
                        symbol_override=selected,
                        timeframe_override=str(state.get("timeframe") or "H1"),
                    )
                except Exception as exc:
                    refresh_result = {"ok": False, "status": "FAILURE", "message": f"{type(exc).__name__}: {exc}"}
    else:
        with st.form(f"{key_prefix}_manual_symbol_form_20260629", clear_on_submit=False):
            typed = st.text_input(
                "Type symbol",
                value=active,
                key=f"{key_prefix}_manual_symbol_20260629",
                placeholder="Examples: XAUUSD, EURUSD, AAPL, SPX, BRK.B",
            )
            apply_clicked = st.form_submit_button("Apply Typed Symbol + Refresh Data", use_container_width=True)
        if apply_clicked:
            selected = normalize_instrument(typed, active)
            result = apply_symbol_selection(state, selected, reason=f"{key_prefix}:manual")
            try:
                from core.app.refresh import refresh_data
                refresh_result = refresh_data(
                    state,
                    symbol_override=selected,
                    timeframe_override=str(state.get("timeframe") or "H1"),
                )
            except Exception as exc:
                refresh_result = {"ok": False, "status": "FAILURE", "message": f"{type(exc).__name__}: {exc}"}

    active = normalize_instrument(state.get("symbol") or selected)
    cols = st.columns(3)
    cols[0].metric("Active Symbol", active)
    cols[1].metric("Timeframe", str(state.get("timeframe") or "H1"))
    cols[2].metric("Calculation State", "REFRESHED — RUN NEEDED" if state.get("selected_symbol_pending_run_20260629") else "SYNCHRONIZED")

    if show_refresh_status:
        refresh_result = refresh_result or state.get("last_refresh_result_20260621")
        if isinstance(refresh_result, dict):
            status = str(refresh_result.get("status") or "NOT RUN")
            message = str(refresh_result.get("message") or "")
            quality = refresh_result.get("quality") if isinstance(refresh_result.get("quality"), dict) else {}
            st.caption(
                f"Latest symbol refresh: {status} · source={refresh_result.get('source', state.get('source', 'DISCONNECTED'))} · "
                f"rows={quality.get('rows', state.get('last_connection_rows', 0))} · {message[:180]}"
            )
    return active


__all__ = ["render_global_symbol_selector"]
