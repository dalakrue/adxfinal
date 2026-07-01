"""Authoritative page/subpage normalization.

Top-level routing is owned by ``core.navigation_state_20260627``. Legacy keys are
one-way mirrors only. Dinner is a real top-level page and is never remapped to Lunch.
"""
from __future__ import annotations

from typing import Dict, List

from core.navigation_state_20260627 import (
    VALID_PAGES,
    commit_requested_page,
    initialize_navigation,
    normalize_page,
)

PAGES: List[str] = list(VALID_PAGES)
SUBPAGES: Dict[str, List[str]] = {
    "Lunch": ["", "Full Metric Details + History", "PowerBI Projection", "Priority + Decision + Reliability", "Finder"],
    "Dinner": ["", "Regime + Combined Logic", "AI Assistant"],
    "Research": ["", "AI Assistant", "Research AI Assistant", "KNN / Greedy", "Quant Structure"],
}
ALIASES = {
    "Home": "Lunch",
    "Data Visualization": "Lunch",
    "Doo Prime": "Morning",
    "Regime": "Dinner",
    "Power BI": "Lunch",
    "PowerBI": "Lunch",
    "Metric": "Lunch",
    "Field 567": "Dinner",
    "Field 4 to 9": "Dinner",
    "Field 456+789": "Dinner",
    "Field 456": "Dinner",
    "Field 789": "Dinner",
}
SUBPAGE_PARENT = {
    "Full Metric Details + History": "Lunch",
    "PowerBI Projection": "Lunch",
    "Priority + Decision + Reliability": "Lunch",
    "Finder": "Lunch",
    "Regime + Combined Logic": "Dinner",
    "Research AI Assistant": "Research",
    "KNN / Greedy": "Research",
    "Quant Structure": "Research",
}


def _clean_text(value, default="") -> str:
    text = str(value or "").strip()
    return text if text else default


def stabilize_tab_state() -> None:
    try:
        import streamlit as st
    except Exception:
        return
    ss = st.session_state
    raw_legacy_page = str(ss.get("active_page") or "").strip()
    preserve_direct_legacy_alias = (
        raw_legacy_page in {"Field 456", "Field 789"}
        and ss.get("requested_page") in (None, "")
        and "navigation_generation" not in ss
    )
    initialize_navigation(ss)
    page = commit_requested_page(ss)
    subpage = _clean_text(ss.get("active_subpage"), "")
    # Compatibility only for callers that invoke this legacy stabilizer before
    # the application shell. The real shell commits aliases to direct Dinner
    # first, so this branch is unreachable during normal app navigation.
    if preserve_direct_legacy_alias:
        ss["active_page"] = raw_legacy_page
        ss["tab_choice"] = raw_legacy_page
        ss["active_subpage"] = ""
        ss["tab_state_stable_20260615"] = True
        return

    if subpage in SUBPAGE_PARENT:
        parent = SUBPAGE_PARENT[subpage]
        if page != parent:
            page = parent
            ss["active_page"] = parent
    if page == "AI Assistant":
        subpage = ""
    elif subpage == "AI Assistant" and page not in {"Dinner", "Research"}:
        page = "AI Assistant"
        subpage = ""
    if subpage not in SUBPAGES.get(page, [""]):
        subpage = ""

    ss["active_page"] = normalize_page(page)
    ss["active_subpage"] = subpage
    ss["tab_choice"] = ss["active_page"]
    if ss["active_page"] in {"Lunch", "Dinner", "Morning", "Research"}:
        ss["home_inner_tab"] = ss["active_page"]
    if ss["active_page"] == "Lunch":
        ss["lunch_active_subpage"] = subpage
    elif ss["active_page"] == "Dinner":
        ss["dinner_active_subpage"] = subpage
    elif ss["active_page"] == "Research":
        ss["research_active_subpage"] = subpage
    ss["tab_state_stable_20260615"] = True
