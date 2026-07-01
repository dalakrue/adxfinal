"""Always-visible Settings controls for multi-symbol and run-mode selection.

This module is deliberately dependency-light.  Rendering the selector must not
import the multi-symbol calculation engine, runtime cache, cloudpickle, pandas,
or any optional connector.  The calculation engine reads the same public state
keys only after the user presses the single Run Calculation + Open Lunch button.
"""
from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

import streamlit as st

# Keep these values identical to core.multi_symbol_field10_20260701 without
# importing that heavier runtime module during Settings rendering.
SUPPORTED_SYMBOLS: tuple[str, ...] = (
    "EURUSD", "USDJPY", "AUDUSD", "GBPUSD", "USDCAD", "USDCHF",
    "EURJPY", "GBPJPY", "EURGBP", "NZDUSD", "XAUUSD", "BTCUSD",
    "NAS100", "US500",
)
SELECTED_KEY = "multi_symbol_selected_20260701"
ACTIVE_KEY = "multi_symbol_active_20260701"
_MULTI_WIDGET_KEY = "multi_symbol_searchable_selector_widget_20260701"
_MODE_KEY = "multi_symbol_calculation_mode_20260701"
_PENDING_KEY = "multi_symbol_selection_pending_20260701"
_EMPTY_SELECTION_KEY = "multi_symbol_empty_selection_20260702"


def normalize_symbol(value: Any, default: str = "EURUSD") -> str:
    raw = str(value or default).strip().upper().replace("/", "").replace(" ", "")
    aliases = {
        "XBTUSD": "BTCUSD", "BTCUSDT": "BTCUSD", "GOLD": "XAUUSD",
        "USTEC": "NAS100", "US100": "NAS100", "NDX": "NAS100",
        "NASDAQ100": "NAS100", "SPX500": "US500", "SP500": "US500",
        "SPX": "US500", "GSPC": "US500", "^GSPC": "US500",
    }
    return aliases.get(raw, raw) or default


def normalize_selected(values: Any) -> list[str]:
    if isinstance(values, str):
        values = [values]
    if not isinstance(values, (list, tuple, set)):
        values = []
    selected: list[str] = []
    for value in values:
        symbol = normalize_symbol(value)
        if symbol in SUPPORTED_SYMBOLS and symbol not in selected:
            selected.append(symbol)
    return selected


def _publish_selection(state: MutableMapping[str, Any], values: list[str]) -> list[str]:
    selected = normalize_selected(values)
    state[SELECTED_KEY] = selected
    state[_MULTI_WIDGET_KEY] = list(selected)
    state[_EMPTY_SELECTION_KEY] = not bool(selected)
    for symbol in SUPPORTED_SYMBOLS:
        state[f"multi_symbol_checkbox_{symbol}_20260701"] = symbol in selected
    if selected:
        active = normalize_symbol(state.get(ACTIVE_KEY) or state.get("symbol") or selected[0])
        if active not in selected:
            active = selected[0]
        state[ACTIVE_KEY] = active
        state["symbol"] = active
        state["selected_symbol"] = active
        state["ws_symbol"] = active
    return selected


def _multiselect_changed() -> None:
    _publish_selection(st.session_state, list(st.session_state.get(_MULTI_WIDGET_KEY) or []))


def render_multi_symbol_selector(state: MutableMapping[str, Any] | None = None) -> list[str]:
    """Render the critical multi-symbol selector without any optional imports."""
    state = state if state is not None else st.session_state

    pending = state.pop(_PENDING_KEY, None)
    if pending is not None:
        _publish_selection(state, list(pending))

    initial = [item for item in normalize_selected(state.get(SELECTED_KEY)) if item in SUPPORTED_SYMBOLS]
    if not initial and not bool(state.get(_EMPTY_SELECTION_KEY, False)):
        default_symbol = normalize_symbol(state.get("symbol") or "EURUSD")
        initial = [default_symbol] if default_symbol in SUPPORTED_SYMBOLS else ["EURUSD"]
    state[SELECTED_KEY] = list(initial)

    widget_value = normalize_selected(state.get(_MULTI_WIDGET_KEY))
    if widget_value != initial:
        state[_MULTI_WIDGET_KEY] = list(initial)

    # A normal container is used instead of an expander so this start-of-system
    # control cannot be collapsed or hidden by Mobile Lite mode.
    with st.container(border=True):
        st.markdown("### 🌐 Multi-Symbol Selection — Always Visible")
        st.caption(
            "Select one or more instruments before running. Selected symbols are processed sequentially; "
            "saved completed symbols can be reopened without recalculating them."
        )
        st.multiselect(
            "Search and select instruments",
            options=list(SUPPORTED_SYMBOLS),
            key=_MULTI_WIDGET_KEY,
            on_change=_multiselect_changed,
            help="Search and select one, several, or all supported instruments.",
        )

        b1, b2, b3 = st.columns(3)
        if b1.button("Select all", key="multi_symbol_select_all_20260701", use_container_width=True):
            state[_PENDING_KEY] = list(SUPPORTED_SYMBOLS)
            st.rerun()
        if b2.button("Clear all", key="multi_symbol_clear_all_20260701", use_container_width=True):
            state[_PENDING_KEY] = []
            st.rerun()

        selected_now = normalize_selected(state.get(SELECTED_KEY))
        b3.metric("Selected", len(selected_now))

        if selected_now:
            active = normalize_symbol(state.get(ACTIVE_KEY) or state.get("symbol") or selected_now[0])
            if active not in selected_now:
                active = selected_now[0]
            active = st.selectbox(
                "Active symbol shown after the run",
                options=selected_now,
                index=selected_now.index(active),
                key="multi_symbol_settings_active_widget_20260701",
            )
            state[ACTIVE_KEY] = active
            state["symbol"] = active
            state["selected_symbol"] = active
            state["ws_symbol"] = active
            st.success("Selected symbols: " + ", ".join(selected_now))
        else:
            st.error("Select at least one symbol. The calculation button stays disabled until a symbol is selected.")

        # The full checkbox alternative remains available but does not replace
        # or hide the always-visible searchable selector above.
        with st.expander("Optional checkbox selection", expanded=False):
            columns = st.columns(2)
            for index, symbol in enumerate(SUPPORTED_SYMBOLS):
                key = f"multi_symbol_checkbox_{symbol}_20260701"
                state.setdefault(key, symbol in selected_now)
                columns[index % 2].checkbox(symbol, key=key)
            if st.button("Apply checkbox selection", key="multi_symbol_apply_checkboxes_20260701", use_container_width=True):
                checked = [
                    symbol for symbol in SUPPORTED_SYMBOLS
                    if bool(state.get(f"multi_symbol_checkbox_{symbol}_20260701"))
                ]
                state[_PENDING_KEY] = checked
                st.rerun()

    return normalize_selected(state.get(SELECTED_KEY))


def render_calculation_mode_selector(state: MutableMapping[str, Any] | None = None) -> str:
    """Always render exactly three historical calculation scopes."""
    state = state if state is not None else st.session_state
    labels = {
        "QUICK": "1. Quick — Fields 1–9 + AI",
        "FULL": "2. Full — Fields 1–9 + thesis + AI",
        "LUNCH_CORE": "3. Super Quick — Lunch Fields 1–3",
    }
    reverse = {value: key for key, value in labels.items()}
    current = str(state.get("settings_calculation_scope_20260625") or "QUICK").upper()
    if current not in labels:
        current = "QUICK"

    # This is intentionally not an expander: all three run choices must remain
    # visible on phone, desktop, Streamlit Cloud, and minimal deployments.
    with st.container(border=True):
        st.markdown("### ▶ 3 Run Calculation Choices — Always Visible")
        selected_label = st.radio(
            "Calculation mode",
            options=list(labels.values()),
            index=list(labels).index(current),
            horizontal=False,
            key=_MODE_KEY,
            help="Choose exactly one mode, then press the single Run Calculation + Open Lunch button.",
        )
        scope = reverse[selected_label]
        descriptions = {
            "QUICK": "Runs the complete operational Fields 1–9 and AI path while reusing unchanged research-only stages.",
            "FULL": "Runs Fields 1–9, AI, and all thesis/research publishers.",
            "LUNCH_CORE": "Runs only Lunch Fields 1–3 for the fastest focused refresh.",
        }
        state["settings_calculation_scope_20260625"] = scope
        st.info(descriptions[scope])
        st.caption(f"Selected run mode: {selected_label}")
    return scope


__all__ = [
    "SUPPORTED_SYMBOLS", "SELECTED_KEY", "ACTIVE_KEY", "normalize_symbol",
    "normalize_selected", "render_multi_symbol_selector", "render_calculation_mode_selector",
]
