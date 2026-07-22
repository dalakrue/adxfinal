"""Responsive Field 3 record cards for narrow phone screens.

Desktop keeps the complete Streamlit dataframe. Phone mode presents the most
important values as stacked cards so an iPhone-width screen never requires the
user to swipe across dozens of columns. The complete table remains available in
one collapsed expander for audit/export use.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from html import escape
from typing import Any

import pandas as pd


def is_phone_mode(state: Mapping[str, Any]) -> bool:
    return bool(
        state.get("phone_mode")
        or state.get("extreme_mobile_lite_mode_20260628")
        or str(state.get("mobile_ui_mode_20260628") or "").strip().lower() == "phone"
    )


def _display(value: Any) -> str:
    if value is None or value is pd.NA:
        return "—"
    try:
        if pd.isna(value):
            return "—"
    except Exception:
        pass
    if isinstance(value, float):
        if abs(value) >= 1000:
            return f"{value:,.2f}"
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def inject_field3_mobile_card_css(st: Any) -> None:
    st.markdown(
        """
<style id="field3-mobile-cards-20260722">
.f3-phone-card {
  width:100%; box-sizing:border-box; margin:.42rem 0; padding:.68rem;
  border:1px solid rgba(14,116,144,.20); border-radius:14px;
  background:linear-gradient(145deg,rgba(255,255,255,.94),rgba(239,248,255,.86));
  box-shadow:0 4px 13px rgba(2,132,199,.07); overflow:hidden;
}
.f3-phone-head {display:flex; align-items:center; justify-content:space-between; gap:.5rem; margin-bottom:.5rem;}
.f3-phone-symbol {font-weight:900; font-size:1rem; color:#0f172a; overflow-wrap:anywhere;}
.f3-phone-rank {font-weight:900; font-size:.76rem; padding:.22rem .5rem; border-radius:999px;
  background:rgba(186,230,253,.82); color:#075985; white-space:nowrap;}
.f3-phone-grid {display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.42rem .55rem;}
.f3-phone-item {min-width:0; padding:.38rem .42rem; border-radius:10px; background:rgba(255,255,255,.72);}
.f3-phone-label {font-size:.64rem; line-height:1.15; font-weight:800; color:#64748b; margin-bottom:.16rem;
  overflow-wrap:anywhere;}
.f3-phone-value {font-size:.79rem; line-height:1.25; font-weight:800; color:#0f172a; overflow-wrap:anywhere; word-break:break-word;}
@media (max-width:390px) {
  .f3-phone-card {padding:.58rem;}
  .f3-phone-grid {gap:.36rem;}
  .f3-phone-label {font-size:.61rem;}
  .f3-phone-value {font-size:.75rem;}
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_responsive_records(
    st: Any,
    state: Mapping[str, Any],
    frame: pd.DataFrame,
    *,
    preferred_columns: Sequence[str],
    rank_column: str | None = "Rank",
    symbol_column: str = "Symbol",
    desktop_height: int | None = None,
    full_table_label: str = "Full table — swipe only when needed",
    max_phone_rows: int = 24,
) -> None:
    """Render a dataframe on desktop or no-horizontal-scroll cards on phone."""
    if not isinstance(frame, pd.DataFrame) or frame.empty:
        return
    if not is_phone_mode(state):
        kwargs = {"use_container_width": True, "hide_index": True}
        if desktop_height is not None:
            kwargs["height"] = int(desktop_height)
        st.dataframe(frame, **kwargs)
        return

    inject_field3_mobile_card_css(st)
    columns = [column for column in preferred_columns if column in frame.columns]
    if symbol_column in frame.columns and symbol_column not in columns:
        columns.insert(0, symbol_column)
    if rank_column and rank_column in frame.columns and rank_column not in columns:
        columns.insert(0, rank_column)
    compact = frame.loc[:, columns].head(max_phone_rows).copy() if columns else frame.head(max_phone_rows).copy()

    blocks: list[str] = []
    for position, (_, row) in enumerate(compact.iterrows(), start=1):
        symbol = _display(row.get(symbol_column, f"Row {position}"))
        rank_value = _display(row.get(rank_column)) if rank_column and rank_column in compact.columns else str(position)
        items: list[str] = []
        for column in compact.columns:
            if column in {symbol_column, rank_column}:
                continue
            items.append(
                '<div class="f3-phone-item">'
                f'<div class="f3-phone-label">{escape(str(column))}</div>'
                f'<div class="f3-phone-value">{escape(_display(row.get(column)))}</div>'
                '</div>'
            )
        blocks.append(
            '<div class="f3-phone-card">'
            '<div class="f3-phone-head">'
            f'<div class="f3-phone-symbol">{escape(symbol)}</div>'
            f'<div class="f3-phone-rank">Rank {escape(rank_value)}</div>'
            '</div>'
            f'<div class="f3-phone-grid">{"".join(items)}</div>'
            '</div>'
        )
    st.markdown("".join(blocks), unsafe_allow_html=True)
    if len(frame) > max_phone_rows:
        st.caption(f"Showing the first {max_phone_rows} rows in phone cards.")
    with st.expander(full_table_label, expanded=False):
        kwargs = {"use_container_width": True, "hide_index": True}
        if desktop_height is not None:
            kwargs["height"] = int(desktop_height)
        st.dataframe(frame, **kwargs)


__all__ = ["is_phone_mode", "inject_field3_mobile_card_css", "render_responsive_records"]
