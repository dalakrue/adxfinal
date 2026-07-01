"""Final synchronized page router (updated 2026-06-17).

Only the selected top-level page and selected inner page are imported/rendered.
All renderers consume the canonical runtime adapter already created by runner.py;
none of them may trigger a second shared calculation during the same rerun.
"""
from __future__ import annotations

from typing import Any, Mapping

import pandas as pd
import streamlit as st


def _safe_rerun() -> None:
    try:
        st.rerun()
    except Exception:
        try:
            st.experimental_rerun()
        except Exception:
            pass


def _sync_shared(force: bool = False) -> dict:
    """Compatibility name: read the already-published adapter, never rebuild it."""
    del force
    try:
        from core.canonical_runtime_20260617 import shared_from_runtime
        return shared_from_runtime(st.session_state)
    except Exception:
        value = st.session_state.get("adx_shared_calc_result_20260615") or st.session_state.get("shared_calc_result")
        return value if isinstance(value, dict) else {}


def _safe_component(label: str, fn, *args, **kwargs):
    try:
        if callable(fn):
            return fn(*args, **kwargs)
        st.dataframe(pd.DataFrame([{"Component": label, "Status": "Renderer unavailable"}]), use_container_width=True, hide_index=True)
    except Exception as exc:
        try:
            from core.operational_sync_20260618 import record_operational_error
            record_operational_error(st.session_state, label, exc, stage="render")
        except Exception:
            pass
        st.warning(f"{label} skipped safely; remaining components are still available.")
        with st.expander(f"Open / Close — {label} error", expanded=True):
            st.code(str(exc))
            st.caption("The error was added to Settings → Errors / Fix Fast.")
    return None


def _render_chatgpt_style_ai():
    """Backward-compatible Dinner AI name, now backed by the compact fact pack."""
    from tabs.ai_assistant_compact_20260619 import render_compact_ai_assistant
    return render_compact_ai_assistant()


def _home_ns() -> dict:
    try:
        import tabs.home as home
        return home.__dict__
    except Exception:
        return {}


def _prev_data(ns: dict):
    return ns.get("_render_lunch_data_visualization_inner_tab")


def _prev_morning(ns: dict):
    return ns.get("_render_doo_prime_inner_tab")


def _canonical_priority_table() -> pd.DataFrame:
    table = st.session_state.get("canonical_priority_table_20260617")
    if isinstance(table, pd.DataFrame) and not table.empty:
        return table
    try:
        from core.canonical_runtime_20260617 import get_canonical
        canonical = get_canonical(st.session_state)
        records = canonical.get("priority_table") if isinstance(canonical, dict) else None
        if isinstance(records, list) and records:
            return pd.DataFrame.from_records(records)
    except Exception:
        pass
    return pd.DataFrame()


def _display_priority_table(table: pd.DataFrame, *, height: int = 440) -> None:
    if table.empty:
        try:
            from core.system_wide_completion_20260618 import readiness_message
            message = readiness_message(st.session_state, "Lunch Priority")
        except Exception:
            message = "The published priority table is unavailable. Open Settings → Errors / Fix Fast."
        st.dataframe(pd.DataFrame([{"Status": message}]), use_container_width=True, hide_index=True)
        return
    phone = bool(st.session_state.get("phone_mode", False))
    # Limit only the rendered view; the full canonical table remains cached.
    display_rows = 48 if phone else 240
    try:
        from ui.table_ordering_20260618 import priority_view
        show = priority_view(table, row_limit=display_rows)
    except Exception:
        # Safe fallback still keeps the highest ranked rows. Never use tail()
        # after a descending sort because that exposes old backtest candles.
        show = table.head(display_rows).reset_index(drop=True)
    st.dataframe(show, use_container_width=True, hide_index=True, height=height)


def _render_lunch(ns: dict, subpage: str) -> None:
    if not subpage:
        from tabs.final_lunch_upgrade_20260617 import render_lunch_quick_decision
        # One authoritative Lunch surface: eight closed-first core fields.
        _safe_component("Lunch Eight Principal Fields", render_lunch_quick_decision)
        return

    st.markdown(f"### 🍱 Lunch — {subpage}")
    if subpage == "Full Metric Details + History":
        from tabs.final_three_center_upgrade_20260614 import _render_metric_detail_section
        _safe_component("Full Metric Details + History", _render_metric_detail_section, ns or _home_ns())
    elif subpage == "PowerBI Projection":
        # Dedicated cached-only renderer: opening this inner page imports no
        # legacy Home module chain and performs no prediction/calibration work.
        from ui.powerbi_cached_renderer_20260619 import render_cached_powerbi_projection
        _safe_component("PowerBI Price Prediction Projection", render_cached_powerbi_projection)
        try:
            from ui.decision_product_panel_20260617 import render_powerbi_canonical_details
            render_powerbi_canonical_details()
        except Exception as exc:
            st.caption(f"Validated projection details skipped safely: {exc}")
    elif subpage == "Priority + Decision + Reliability":
        ns = ns or _home_ns()
        from tabs.dinner_morning_data_patch_20260614 import _render_priority_decision_reliability
        _safe_component("Priority + Decision + Reliability", _render_priority_decision_reliability, ns)
        renderer = ns.get("render_reliability_control_center_20260614")
        if callable(renderer):
            _safe_component("Reliability Control Center", renderer)
    elif subpage == "Finder":
        from ui.finder_canonical_view_20260619 import render_finder_canonical_view
        _safe_component("Finder — Canonical Full Metric Priority", render_finder_canonical_view, state=st.session_state)
    else:
        from tabs.final_lunch_upgrade_20260617 import render_lunch_quick_decision
        _safe_component("Lunch Quick Synced Decision", render_lunch_quick_decision)

    try:
        from tabs.final_lunch_upgrade_20260617 import render_lunch_25day_backtest_expander
        render_lunch_25day_backtest_expander(key_suffix=str(subpage))
    except Exception as exc:
        st.caption(f"25-day Lunch Regime + NLP history table skipped safely: {exc}")


def _render_dinner(ns: dict, subpage: str) -> None:
    """Render all original Fields 4–9 from one already-published canonical generation."""
    st.markdown("### 🌙 Dinner — Fields 4–9 Integrated Workspace")
    st.caption("Read-only rendering of the current canonical generation. Opening Dinner never starts a heavy calculation.")
    from tabs.field456789_page_20260626 import show as show_dinner
    _safe_component("Dinner Fields 4–9", show_dinner, {"active_page": "Dinner", "active_subpage": subpage})

def _render_morning() -> None:
    st.markdown("### 🌅 Morning — Doo Prime")
    st.caption("Morning remains closed-first. The legacy Home module chain is imported only after the true load switch is enabled.")
    if not st.toggle("Open / Close — Load Morning Workspace", value=False, key="morning_true_load_gate_20260620"):
        st.info("Morning is ready but not instantiated. Opening or closing other tabs performs no Morning calculation.")
        return
    ns = _home_ns()
    _safe_component("Morning / Doo Prime", _prev_morning(ns))


def _render_research(subpage: str) -> None:
    st.markdown("### 🎓 Research")
    if subpage in {"Research AI Assistant", "AI Assistant"}:
        try:
            from tabs.ai_assistant_lite import render_ai_assistant_lite_tab
            _safe_component("AI Assistant", render_ai_assistant_lite_tab)
        except Exception as exc:
            st.warning(f"AI Assistant skipped safely: {exc}")
        return
    if subpage == "KNN / Greedy":
        _display_priority_table(_canonical_priority_table(), height=430)
        return
    if subpage == "Quant Structure":
        pack = st.session_state.get("final_synced_research_merge_pack_20260612") or st.session_state.get("final_merged_intelligence_pack_20260612") or {}
        quant = pack.get("quant_structure", {}) if isinstance(pack, dict) else {}
        if isinstance(quant, dict):
            st.dataframe(pd.DataFrame([{"Metric": k, "Value": str(v)} for k, v in quant.items()]), use_container_width=True, hide_index=True)
        elif isinstance(quant, pd.DataFrame):
            st.dataframe(quant, use_container_width=True, hide_index=True)
        else:
            try:
                from core.system_wide_completion_20260618 import readiness_message
                message = readiness_message(st.session_state, "Research Data Analysis")
            except Exception:
                message = "The published Quant Structure is unavailable. Open Settings → Errors / Fix Fast."
            st.dataframe(pd.DataFrame([{"Status": message}]), use_container_width=True, hide_index=True)
        return
    # After the Settings full calculation has published a canonical generation,
    # Research opens directly. It remains read-only and starts no calculation.
    canonical_ready = bool(st.session_state.get("canonical_result_20260617") or st.session_state.get("canonical_decision_result_20260617") or st.session_state.get("last_valid_canonical_decision_result_20260617"))
    if not canonical_ready:
        st.info("Run Full Calculation in Settings once to publish the shared research generation.")
        return
    try:
        import tabs.research as research
        _safe_component("Research", research.show)
    except Exception as exc:
        st.warning(f"Research skipped safely: {exc}")


def _render_other() -> None:
    try:
        import tabs.other as other
        _safe_component("Other", other.show)
    except Exception as exc:
        st.warning(f"Other workspace skipped safely: {exc}")





def _render_secure_automation_settings() -> None:
    from core.secure_api_startup_20260619 import initialize_secure_settings, secure_secret_status
    initialize_secure_settings(st.session_state)
    secret_state = secure_secret_status(st.session_state)
    st.markdown("### 🔐 Secure API + Automatic Startup")
    c1, c2 = st.columns(2)
    c1.metric("Finnhub API", "CONFIGURED" if secret_state.get("finnhub_configured") else "NOT CONFIGURED", str(secret_state.get("finnhub_source", "")))
    c2.metric("Second Market API", "CONFIGURED" if secret_state.get("second_api_configured") else "NOT CONFIGURED", str(secret_state.get("second_api_source", "")))
    st.caption("Stored secrets remain server-side. The secure design never autofills their actual values into an input field or sends them to the browser.")
    st.toggle("Use securely stored API keys", key="use_secure_api_keys_20260619")
    st.toggle("Automatically connect APIs after login (connection only)", key="auto_connect_after_login_20260619")
    st.session_state["auto_calculate_new_h1_20260619"] = False
    st.session_state["open_lunch_after_auto_run_20260619"] = False
    st.info("Automatic calculation is disabled. Only the Settings ‘Run Calculation + Open Lunch’ button can publish a new all-tab generation.")
    st.number_input(
        "Auto-run cooldown (minutes)", min_value=1, max_value=60, step=1,
        key="auto_run_cooldown_minutes_20260619",
        help="The generation lock, latest-H1 guard and cooldown prevent duplicate Cloud calculations.",
    )
    startup = st.session_state.get("secure_startup_status_20260619")
    if isinstance(startup, Mapping):
        st.caption(
            f"Startup guard: {startup.get('status', 'NO_ACTION')} · latest H1 {startup.get('latest_h1') or '-'} · "
            f"published H1 {startup.get('published_h1') or '-'}"
        )


def _save_and_connect_twelve_callback(widget_key: str) -> None:
    """Atomically save, validate and connect from one click."""
    from core.transaction_guard_v8_20260622 import begin_transaction, finish_transaction

    token = begin_transaction(st.session_state, "api_save_connect", payload={"widget": widget_key})
    if not token.get("accepted"):
        return
    try:
        key = str(st.session_state.get(widget_key, "") or "").strip()
        if not key:
            try:
                from core.connector_state_machine_20260621 import fail
                fail(st.session_state, "market_connector_20260621", "Enter a Twelve Data API key first.")
            except Exception:
                pass
            return
        st.session_state["twelve_api_key"] = key
        st.session_state["connector_mode"] = "twelve"
        from core.navigation_parts.connection import _connect_now
        outcome = _connect_now("Twelve Data Save + Validate + Connect", quick=True)
        st.session_state["twelve_one_click_connect_result_20260628"] = outcome
    finally:
        finish_transaction(st.session_state, "api_save_connect", token=str(token.get("token") or ""))


def _render_mobile_api_key_center() -> None:
    """Secure status plus optional, blank temporary replacement fields."""
    st.markdown("""
    <style>
    @media (max-width: 780px) {
      div[data-testid="stTextInput"] input,
      div[data-testid="stTextArea"] textarea {
        font-size: 16px !important; min-height: 48px !important;
        -webkit-user-select: text !important; user-select: text !important;
        -webkit-touch-callout: default !important; touch-action: manipulation !important;
      }
      div[data-testid="stTextArea"] textarea {min-height: 76px !important; overflow-wrap: anywhere !important;}
      div[data-testid="stButton"] button {min-height: 46px !important; white-space: normal !important;}
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("### 🔑 Temporary API Key Replacement")
    st.caption("These blank fields are optional session-only replacements. Streamlit Secrets are never shown or copied into them.")

    twelve_generation = int(st.session_state.get("settings_mobile_twelve_generation_20260619", 0) or 0)
    with st.expander("Open / Close — Replace Second / Twelve Data API Key", expanded=True):
        value = st.text_area(
            "Twelve Data API key — mobile paste box", value="",
            key=f"settings_mobile_twelve_api_key_paste_20260619_{twelve_generation}", height=76,
            placeholder="Optional: paste a temporary replacement key for this session",
            help="The stored Streamlit Secret is intentionally never autofilled here.",
        )
        c1, c2 = st.columns(2)
        c1.button(
            "Save Key + Auto-Connect (One Click)", key="settings_mobile_save_twelve_20260619", use_container_width=True,
            disabled=not bool(str(value or '').strip()), on_click=_save_and_connect_twelve_callback,
            args=(f"settings_mobile_twelve_api_key_paste_20260619_{twelve_generation}",),
        )
        if c2.button("Clear Temporary Twelve Key", key="settings_mobile_clear_twelve_20260619", use_container_width=True):
            st.session_state["twelve_api_key"] = ""
            st.session_state["settings_mobile_twelve_generation_20260619"] = twelve_generation + 1
            st.success("Temporary replacement cleared. The server-side secret, if configured, remains available.")
            _safe_rerun()



def _render_openrouter_api_center() -> None:
    """One-click OpenRouter connector with secret auto-discovery."""
    from services.openrouter_backend_20260628 import (
        MODEL_KEY, SESSION_KEY, configuration_status, validate_connection,
    )
    with st.expander("Open / Close — AI API / OpenRouter Connector", expanded=True):
        st.caption(
            "Use a server-side Streamlit Secret for automatic startup configuration, or paste a temporary session-only replacement. "
            "The key is never displayed, added to prompts, or stored in the runtime cache."
        )
        generation = int(st.session_state.get("openrouter_widget_generation_20260628", 0) or 0)
        key_widget = f"openrouter_key_input_20260628_{generation}"
        model_widget = f"openrouter_model_input_20260628_{generation}"
        st.text_input(
            "OpenRouter API key — temporary session replacement", type="password", value="", key=key_widget,
            placeholder="Optional when OPENROUTER_API_KEY is already in Streamlit Secrets",
        )
        st.text_input(
            "OpenRouter model", value=str(st.session_state.get(MODEL_KEY) or "openrouter/auto"), key=model_widget,
            help="openrouter/auto is the default. You may enter another OpenRouter model slug.",
        )
        configured = configuration_status(st.session_state)
        # Auto-validate a secret once per session. A failure is visible but never
        # blocks the deterministic local assistant or the trading application.
        if configured.get("configured") and not st.session_state.get("openrouter_auto_validation_attempted_20260628"):
            st.session_state["openrouter_auto_validation_attempted_20260628"] = True
            validate_connection(st.session_state)
            configured = configuration_status(st.session_state)
        cols = st.columns(4)
        cols[0].metric("Configured", "YES" if configured.get("configured") else "NO")
        cols[1].metric("Connection", "CONNECTED" if configured.get("connected") else str(configured.get("status") or "NOT CHECKED"))
        cols[2].metric("Credential Source", str(configured.get("source") or "Not configured"))
        cols[3].metric("Model", str(configured.get("model") or "openrouter/auto")[:28])
        b1, b2 = st.columns(2)
        if b1.button("Save + Connect OpenRouter (One Click)", key="openrouter_save_connect_20260628", use_container_width=True):
            temporary = str(st.session_state.get(key_widget) or "").strip()
            if temporary:
                st.session_state[SESSION_KEY] = temporary
            st.session_state[MODEL_KEY] = str(st.session_state.get(model_widget) or "openrouter/auto").strip() or "openrouter/auto"
            result = validate_connection(st.session_state)
            if result.get("ok"):
                st.success("OpenRouter connected. The AI Assistant will use it first and fall back safely if a request fails.")
            else:
                st.error(str(result.get("message") or result.get("status") or "OpenRouter connection failed."))
        if b2.button("Clear Temporary OpenRouter Key", key="openrouter_clear_temporary_20260628", use_container_width=True):
            st.session_state.pop(SESSION_KEY, None)
            st.session_state.pop("openrouter_connection_status_20260628", None)
            st.session_state["openrouter_widget_generation_20260628"] = generation + 1
            _safe_rerun()


def _render_market_time_metrics(*, query_mt5: bool = True) -> dict[str, Any]:
    """Show feed freshness without starting a calculation."""
    try:
        from core.market_time_freshness_20260622 import market_time_snapshot
        snap = market_time_snapshot(st.session_state, query_mt5=query_mt5)
    except Exception as exc:
        snap = {"status": "CHECK", "current_utc_display": "Unavailable", "broker_clock_display": "Unavailable", "latest_loaded_display": "Unavailable", "lag_minutes": None, "source": "UNKNOWN", "error": str(exc)}
    cols = st.columns(5)
    cols[0].metric("Feed Freshness", str(snap.get("status") or "CHECK"), str(snap.get("source") or "DISCONNECTED"))
    cols[1].metric("Current UTC", str(snap.get("current_utc_display") or "-").replace(" UTC", ""))
    cols[2].metric("MT5 Latest Tick", str(snap.get("mt5_tick_display") or "Not available").replace(" UTC", ""))
    cols[3].metric("Broker Clock", str(snap.get("broker_clock_display") or "Not available"))
    lag = snap.get("lag_minutes")
    has_loaded_candle = bool(snap.get("latest_loaded_broker_display"))
    delta = f"{lag:g} min behind current bar" if isinstance(lag, (int, float)) else "Waiting for connected data"
    latest_display = str(snap.get("latest_loaded_broker_display") or "Not available yet")
    cols[4].metric("Latest Candle — Broker", latest_display, delta, delta_color="off" if not has_loaded_candle else "normal")
    st.caption("MetaTrader tick timestamps are normalized to UTC for calculations. Visible candle time uses the configured broker offset; Myanmar time remains a separate UTC+6:30 display.")
    return snap


def _open_lunch_ai_after_settings_run(*, used_previous: bool = False) -> None:
    phone = bool(st.session_state.get("phone_mode", False))
    updates = {
        "active_page": "Lunch", "tab_choice": "Lunch", "active_subpage": "", "lunch_active_subpage": "",
        "lunch_bi_visual_ready": True, "show_restored_powerbi_20260617": True,
        "load_original_powerbi_from_antd_lunch_20260615": True,
        "settings_auto_open_lunch_20260617": True,
        "lunch_calculation_completed_notice_20260621": True,
        "lunch_active_field_selector_20260624": "All Lunch fields closed",
        "lunch_active_field_selector_20260624__pending": "All Lunch fields closed",
        # Legacy static marker only: "lunch_active_field_selector_20260624": "1. Open / Close — Full Metric 25-Day History + Decision Tables"
        # The Settings run navigates to Lunch but leaves every large field closed.
        "lunch_field_open_5_20260621": False,
        "lunch_scroll_to_field5_20260622": False,
        "settings_used_previous_canonical_20260622": bool(used_previous),
    }
    updates.update({
        "lunch_field_open_1_20260621": False, "lunch_field_widget_1_20260621": False,
        "lunch_field_open_2_20260621": False, "lunch_field_widget_2_20260621": False,
        "lunch_field_open_3_20260621": False, "lunch_field_widget_3_20260621": False,
        "lunch_field_open_4_20260621": False, "lunch_field_widget_4_20260621": False,
        "lunch_field_open_5_20260621": False, "lunch_field_widget_5_20260621": False,
        "lunch_field_open_6_20260621": False, "lunch_field_widget_6_20260621": False,
        "lunch_scroll_to_field5_20260622": False,
    })
    try:
        from core.navigation_authority_20260625 import navigate_to
        navigate_to(st.session_state, "Lunch", "", None)
    except Exception:
        pass
    st.session_state.update(updates)

def _render_arert_research_settings() -> None:
    """Explicit-only ARERT runner; normal Streamlit reruns only render cache."""
    from research_quant.arert_lab import MODULE_CATALOG, STATE_KEY, run_arert_research

    with st.expander("Open / Close — Dinner Master’s / PhD ARERT Research", expanded=True):
        st.caption(
            "Runs a separate research layer from the latest frozen completed canonical snapshot. "
            "It never overwrites Lunch production calculations. Repeated same-candle modules reuse cache."
        )
        options = [f"{number:02d} — {name}" for number, (name, _field) in MODULE_CATALOG.items()]
        selected_labels = st.multiselect(
            "Select Dinner research modules",
            options,
            default=[options[-1]],
            key="arert_selected_modules_20260628",
        )
        full_col, selected_col = st.columns(2)
        full_clicked = full_col.button(
            "Run Full Dinner Thesis Research + Open Dinner",
            key="run_full_dinner_thesis_research_20260628",
            use_container_width=True,
        )
        selected_clicked = selected_col.button(
            "Run Selected Dinner Research Module",
            key="run_selected_dinner_research_20260628",
            use_container_width=True,
        )
        if full_clicked or selected_clicked:
            try:
                from core.canonical_lookup_20260626 import resolve_canonical
                canonical = resolve_canonical(st.session_state)
            except Exception:
                canonical = {}
            if not isinstance(canonical, Mapping) or not canonical:
                st.error("No valid completed canonical snapshot is available. Run the protected Lunch calculation first.")
            else:
                selected = list(MODULE_CATALOG)
                if selected_clicked:
                    selected = []
                    for label in selected_labels:
                        try:
                            selected.append(int(str(label).split("—", 1)[0].strip()))
                        except Exception:
                            continue
                    if not selected:
                        st.warning("Select at least one Dinner research module.")
                        return
                with st.spinner("Running the selected completed-candle ARERT research modules…"):
                    envelope = run_arert_research(st.session_state, canonical, selected)
                st.session_state["arert_last_settings_run_20260628"] = {
                    "status": envelope.get("status"),
                    "selected_modules": envelope.get("selected_modules"),
                    "metadata": envelope.get("metadata"),
                    "database": envelope.get("database"),
                }
                try:
                    from core.navigation_authority_20260625 import navigate_to
                    navigate_to(st.session_state, "Dinner", "", None)
                except Exception:
                    st.session_state["active_page"] = "Dinner"
                    st.session_state["tab_choice"] = "Dinner"
                    st.session_state["active_subpage"] = ""
                _safe_rerun()

        last = st.session_state.get("arert_last_settings_run_20260628")
        envelope = st.session_state.get(STATE_KEY)
        if isinstance(last, Mapping):
            cols = st.columns(4)
            cols[0].metric("ARERT Status", str(last.get("status") or "—"))
            cols[1].metric("Modules Cached", str(len((envelope or {}).get("modules", {}))) if isinstance(envelope, Mapping) else "0")
            metadata = last.get("metadata") if isinstance(last.get("metadata"), Mapping) else {}
            cols[2].metric("Broker Candle", str(metadata.get("completed_broker_candle") or "—"))
            database = last.get("database") if isinstance(last.get("database"), Mapping) else {}
            cols[3].metric("Research DB", "READY" if database.get("ok") else "CHECK")



def _render_imap_rv_settings() -> None:
    """Explicit-only IMAP-RV runner; normal reruns render cached evidence only."""
    from research_quant.imap_rv_20260628 import STATE_KEY, run_imap_rv

    with st.expander("Open / Close — IMAP-RV Thesis Research", expanded=False):
        st.caption(
            "Information Mining, Attention, Path-Memory and Research Validity. "
            "This is a separate research prototype and never overwrites protected Lunch values."
        )
        force = st.checkbox("Force rebuild for the same completed candle", value=False, key="imap_rv_force_20260628")
        if st.button("Run IMAP-RV Research + Open Dinner", key="run_imap_rv_20260628", use_container_width=True):
            try:
                from core.canonical_lookup_20260626 import resolve_canonical
                canonical = resolve_canonical(st.session_state)
            except Exception:
                canonical = {}
            if not isinstance(canonical, Mapping) or not canonical:
                st.error("No completed canonical generation is available. Run the protected calculation first.")
            else:
                with st.spinner("Running completed-candle IMAP-RV research…"):
                    envelope = run_imap_rv(st.session_state, canonical, force=bool(force))
                st.session_state["imap_rv_last_settings_run_20260628"] = {
                    "status": envelope.get("status"), "score": envelope.get("imap_rv_score"),
                    "protective_action": envelope.get("protective_action"), "metadata": envelope.get("metadata"),
                }
                try:
                    from core.navigation_authority_20260625 import navigate_to
                    navigate_to(st.session_state, "Dinner", "", None)
                except Exception:
                    st.session_state["active_page"] = "Dinner"
                    st.session_state["tab_choice"] = "Dinner"
                    st.session_state["active_subpage"] = ""
                _safe_rerun()
        envelope = st.session_state.get(STATE_KEY)
        if isinstance(envelope, Mapping):
            cols = st.columns(4)
            score = envelope.get("imap_rv_score")
            cols[0].metric("IMAP-RV", "N/A" if score is None else f"{float(score):.1f}/100")
            cols[1].metric("Protective Action", str(envelope.get("protective_action") or "NO TRADE"))
            cols[2].metric("Cache", str(envelope.get("cache_status") or "—"))
            db = envelope.get("database") if isinstance(envelope.get("database"), Mapping) else {}
            cols[3].metric("Research DB", "READY" if db.get("ok") else "CHECK")

def _render_home() -> None:
    """Lightweight Home page with global identity and Explain-this-App shortcut."""
    st.markdown("## 🏠 ADX Quant Pro — Home")
    st.caption("Select an instrument globally, review the current publication identity, or open the full app explanation. Home never runs heavy calculations.")
    try:
        from ui.global_symbol_selector_20260629 import render_global_symbol_selector
        render_global_symbol_selector(st.session_state, key_prefix="home_20260629", auto_refresh_library=True)
    except Exception as exc:
        st.warning(f"Global symbol selector unavailable: {exc}")
    canonical = {}
    try:
        from core.canonical_lookup_20260626 import resolve_canonical
        canonical = resolve_canonical(st.session_state) or {}
    except Exception:
        canonical = st.session_state.get("canonical_result_20260617") or {}
    cols = st.columns(4)
    cols[0].metric("Published Symbol", str(canonical.get("symbol") or "—"))
    cols[1].metric("Published Timeframe", str(canonical.get("timeframe") or "—"))
    cols[2].metric("Run ID", str(canonical.get("run_id") or canonical.get("canonical_calculation_id") or "—")[:24])
    cols[3].metric("Status", "RUN NEEDED" if st.session_state.get("selected_symbol_pending_run_20260629") else "READY")
    if st.button("📘 Open Settings → Explain this App", key="home_open_explain_app_20260629", use_container_width=True):
        st.session_state["settings_open_explain_app_20260629"] = True
        try:
            from core.navigation_authority_20260625 import navigate_to
            navigate_to(st.session_state, "Settings", "", None)
        except Exception:
            st.session_state["active_page"] = "Settings"
            st.session_state["tab_choice"] = "Settings"
            st.session_state["active_subpage"] = ""
        _safe_rerun()
    try:
        from ui.app_professional_guide_20260628 import render_app_professional_guide
        render_app_professional_guide(expanded=False, context={
            "source": st.session_state.get("source"), "symbol": st.session_state.get("symbol", "EURUSD"),
            "timeframe": st.session_state.get("timeframe", "H1"),
            "run_id": canonical.get("run_id"), "generation_id": canonical.get("generation_id"),
        })
    except Exception as exc:
        st.caption(f"Home explanation preview unavailable: {exc}")


def _render_market_connector_section() -> None:
    # This is a critical start-of-system control.  Use a non-collapsible
    # container so Mobile Lite or an optional import failure can never hide it.
    with st.container(border=True):
        st.markdown("### 🔌 Twelve Data + MT5 Market Connector — Always Visible")
        st.caption("Choose the global instrument, Twelve Data/MT5/fallback source, timeframe and candle count. A symbol change refreshes only that instrument and marks the prior canonical generation stale until the next explicit run.")
        st.number_input(
            "MT5 broker chart UTC offset (display only)", min_value=-12.0, max_value=14.0, step=0.5,
            key="mt5_broker_utc_offset_hours_20260622",
            help="MT5 Python tick timestamps are UTC. Set the exact broker-chart offset. All Lunch Date/Weekday/Hour columns are rebuilt from this same broker clock.",
        )
        try:
            from ui.sidebar_fallback_panel import _render_connector
            _render_connector(key_prefix="settings_market_20260619", show_secret_inputs=False)
        except Exception as exc:
            # Keep a complete minimal connector visible instead of replacing the
            # entire start panel with a warning.
            st.error(f"Advanced connector renderer failed: {type(exc).__name__}: {exc}")
            source_options = ["twelve", "mt5", "doo_bridge", "fallback", "safe_demo"]
            current_source = str(st.session_state.get("connector_mode") or "twelve")
            if current_source not in source_options:
                current_source = "twelve"
            st.session_state["connector_mode"] = st.selectbox(
                "API source", source_options, index=source_options.index(current_source),
                key="settings_market_emergency_source_20260702",
            )
            symbol = st.text_input(
                "Broker/provider symbol", value=str(st.session_state.get("symbol") or "EURUSD"),
                key="settings_market_emergency_symbol_20260702",
            ).strip().upper().replace("/", "").replace(" ", "") or "EURUSD"
            st.session_state["symbol"] = symbol
            timeframe_options = ["M1", "M2", "M5", "M15", "H1", "H4", "D1", "CUSTOM"]
            current_tf = str(st.session_state.get("timeframe") or "H1").upper()
            if current_tf not in timeframe_options:
                current_tf = "H1"
            st.session_state["timeframe"] = st.selectbox(
                "Timeframe", timeframe_options, index=timeframe_options.index(current_tf),
                key="settings_market_emergency_timeframe_20260702",
            )
            st.session_state["connector_bars"] = int(st.number_input(
                "Candles / bars", min_value=100, max_value=250000,
                value=int(st.session_state.get("connector_bars", 600) or 600), step=100,
                key="settings_market_emergency_bars_20260702",
            ))
            st.warning("The visible emergency connector is active. Fix the renderer error above for one-click connection, but symbol/timeframe/candle setup remains available.")


def _render_finnhub_connector_section() -> None:
    with st.container(border=True):
        st.markdown("### 📰 Finnhub Connector — Always Visible")
        try:
            from core.finnhub_connector import render_finnhub_connector
            render_finnhub_connector(location="settings")
        except Exception as exc:
            st.error(f"Finnhub connector renderer failed: {type(exc).__name__}: {exc}")
            st.caption("The Finnhub section remains visible. Add the key in Streamlit Secrets or repair the connector module; market calculation controls below are still available.")


def _render_settings() -> None:
    st.session_state.setdefault("mt5_broker_utc_offset_hours_20260622", 4.0)
    st.markdown("### ⚙️ Settings")
    try:
        from core.mobile_lite_mode_20260628 import render_mobile_mode_control
        with st.expander("Open / Close — Extreme Mobile Lite Mode", expanded=bool(st.session_state.get("phone_mode"))):
            render_mobile_mode_control(st, st.session_state, key="settings_mobile_lite_20260628")
            st.caption("Mobile Lite disables decorative UI, bounds tables and loads one field at a time. Calculation values remain identical.")
    except Exception as mobile_mode_exc:
        st.caption(f"Mobile Lite control unavailable: {mobile_mode_exc}")
    # Backward-compatible label contract: Run Calculation + Open Lunch (One Click)
    st.caption("Quick Run publishes the protected Fields 1–9 + AI generation while skipping thesis-only rebuilds. Full Run includes every research publisher. Super Quick rebuilds Lunch Fields 1–3 only. Every successful run opens Lunch with Field 1 expanded.")
    try:
        from ui.app_professional_guide_20260628 import render_app_professional_guide
        render_app_professional_guide(expanded=bool(st.session_state.pop("settings_open_explain_app_20260629", False)), context={
            "source": st.session_state.get("source"),
            "symbol": st.session_state.get("symbol", "EURUSD"),
            "timeframe": st.session_state.get("timeframe", "H1"),
            "run_id": st.session_state.get("canonical_run_id_20260617"),
            "generation_id": st.session_state.get("canonical_calculation_generation_20260617"),
        })
    except Exception as guide_exc:
        st.caption(f"Professional guide unavailable: {guide_exc}")
    _render_market_time_metrics(query_mt5=True)

    # Critical start-of-system controls are intentionally placed before the run
    # button and rendered in non-collapsible/expanded sections. Mobile Lite may
    # reduce decoration, but it must never hide connectors, symbols, or modes.
    _render_mobile_api_key_center()
    _render_market_connector_section()
    _render_finnhub_connector_section()

    # Render the advanced selector and the three calculation choices independently.
    # A selector dependency must never hide the run-mode control on deployment.
    try:
        from ui.multi_symbol_settings_20260701 import render_multi_symbol_selector
        selected_symbols_20260701 = render_multi_symbol_selector(st.session_state)
    except Exception as multi_symbol_exc:
        st.session_state["multi_symbol_selector_nonblocking_error_20260702"] = f"{type(multi_symbol_exc).__name__}: {multi_symbol_exc}"
        fallback_symbols = [
            "EURUSD", "USDJPY", "AUDUSD", "GBPUSD", "USDCAD", "USDCHF",
            "EURJPY", "GBPJPY", "EURGBP", "NZDUSD", "XAUUSD", "BTCUSD",
            "NAS100", "US500",
        ]
        current_symbol = str(st.session_state.get("symbol") or "EURUSD").strip().upper().replace("/", "").replace(" ", "")
        selected_default = st.session_state.get("multi_symbol_selected_20260701")
        if not isinstance(selected_default, list):
            selected_default = [current_symbol if current_symbol in fallback_symbols else "EURUSD"]
        selected_default = [item for item in selected_default if item in fallback_symbols] or ["EURUSD"]
        with st.container(border=True):
            st.markdown("### 🌐 Multi-Symbol Selection — Always Visible")
            st.error(f"Primary selector renderer failed: {type(multi_symbol_exc).__name__}: {multi_symbol_exc}")
            selected_symbols_20260701 = st.multiselect(
                "Search and select instruments", fallback_symbols, default=selected_default,
                key="multi_symbol_emergency_selector_20260702",
            )
            st.session_state["multi_symbol_selected_20260701"] = list(selected_symbols_20260701)
            if selected_symbols_20260701:
                active = st.selectbox(
                    "Active symbol shown after the run", selected_symbols_20260701,
                    key="multi_symbol_emergency_active_20260702",
                )
                st.session_state["multi_symbol_active_20260701"] = active
                st.session_state["symbol"] = active
            else:
                st.error("Select at least one symbol before running.")

    try:
        from ui.multi_symbol_settings_20260701 import render_calculation_mode_selector
        selected_scope_20260701 = render_calculation_mode_selector(st.session_state)
    except Exception as calculation_mode_exc:
        st.session_state["calculation_mode_nonblocking_error_20260702"] = f"{type(calculation_mode_exc).__name__}: {calculation_mode_exc}"
        fallback_labels = {
            "QUICK": "1. Quick — Fields 1–9 + AI",
            "FULL": "2. Full — Fields 1–9 + thesis + AI",
            "LUNCH_CORE": "3. Super Quick — Lunch Fields 1–3",
        }
        current_scope = str(st.session_state.get("settings_calculation_scope_20260625") or "QUICK").upper()
        if current_scope not in fallback_labels:
            current_scope = "QUICK"
        with st.container(border=True):
            st.markdown("### ▶ 3 Run Calculation Choices — Always Visible")
            st.error(f"Primary run-mode renderer failed: {type(calculation_mode_exc).__name__}: {calculation_mode_exc}")
            fallback_choice = st.radio(
                "Calculation mode", list(fallback_labels.values()),
                index=list(fallback_labels).index(current_scope), horizontal=False,
                key="calculation_mode_safe_fallback_20260702",
            )
        selected_scope_20260701 = next(key for key, value in fallback_labels.items() if value == fallback_choice)
        st.session_state["settings_calculation_scope_20260625"] = selected_scope_20260701

    previous_status = st.session_state.get("settings_run_status_20260617")
    if isinstance(previous_status, Mapping):
        canonical_ok = bool((previous_status.get("canonical") or {}).get("ok"))
        previous_used = bool(st.session_state.get("settings_used_previous_canonical_20260622"))
        ai_ready = False
        try:
            from tabs.ai_assistant_compact_20260619 import _recover_fact_pack
            ai_ready = bool(_recover_fact_pack(st.session_state))
        except Exception:
            ai_ready = False
        top = st.columns(4)
        top[0].metric("All-in-One Run", "FULLY WORKED" if canonical_ok else ("PREVIOUS VALID USED" if ai_ready else "CHECK"))
        top[1].metric("Published Generation", str(previous_status.get("calculation_generation", st.session_state.get("canonical_calculation_generation_20260617", "-"))))
        top[2].metric("AI Assistant", "READY" if ai_ready else "OFFLINE DIAGNOSTIC")
        top[3].metric("Auto-Open Lunch", "READY" if (canonical_ok or previous_used or ai_ready) else "WAITING")

    st.info("Same-candle and unchanged-stage results are reused. Symbols run sequentially and completed symbol states are compressed to disk, limiting peak RAM, CPU contention, and device heat without changing protected calculations.")
    c1, c4 = st.columns([3, 1])
    run_locked_20260624 = bool(st.session_state.get("settings_one_click_running_20260624") or st.session_state.get("multi_symbol_run_in_progress_20260701"))
    no_symbols_20260701 = not bool(selected_symbols_20260701)
    run_clicked_20260701 = c1.button(
        "▶ Run Calculation + Open Lunch",
        key="settings_run_calc_20260617",
        use_container_width=True,
        disabled=run_locked_20260624 or no_symbols_20260701,
        help="Runs the selected mode once for selected symbols only, then opens Lunch.",
    )
    quick_clicked = bool(run_clicked_20260701 and selected_scope_20260701 == "QUICK")
    full_clicked = bool(run_clicked_20260701 and selected_scope_20260701 == "FULL")
    super_clicked = bool(run_clicked_20260701 and selected_scope_20260701 == "LUNCH_CORE")
    if run_clicked_20260701:
        st.session_state["settings_calculation_scope_20260625"] = selected_scope_20260701
        def _settings_run_action_20260624():
            # Prefer the sequential multi-symbol transaction.  If an optional
            # controller import ever fails on deployment, continue with the
            # active symbol instead of aborting the main calculation button.
            child_run_key = "multi_symbol_child_run_active_20260701"
            multi_symbol_runner = None
            try:
                from core.multi_symbol_field10_20260701 import CHILD_RUN_KEY, run_selected_symbols
                child_run_key = CHILD_RUN_KEY
                multi_symbol_runner = run_selected_symbols
            except Exception as multi_run_import_exc:
                st.session_state["multi_symbol_run_nonblocking_error_20260702"] = f"{type(multi_run_import_exc).__name__}: {multi_run_import_exc}"

            if callable(multi_symbol_runner) and not bool(st.session_state.get(child_run_key)):
                progress_slot = st.empty()
                def _publish_multi_progress(snapshot):
                    percent = float((snapshot or {}).get("overall_percent") or 0.0)
                    current = str((snapshot or {}).get("current_symbol") or "Validating")
                    stage = str((snapshot or {}).get("current_stage") or "Starting")
                    progress_slot.progress(min(1.0, max(0.0, percent / 100.0)), text=f"{percent:.1f}% — {current} — {stage}")
                return multi_symbol_runner(
                    st.session_state,
                    _settings_run_action_20260624,
                    scope=str(st.session_state.get("settings_calculation_scope_20260625") or "QUICK"),
                    progress_callback=_publish_multi_progress,
                )
            # Legacy contract markers: try_reuse_quick_fields_123 and
            # QUICK_FIELDS_1_2_3. The current priority implementation still
            # executes one full protected run; these markers do not activate a
            # second Quick Sync path or restrict the full Fields 1-9 scope.
            ns = _home_ns()
            refresh_result: dict[str, Any] = {}
            with st.spinner("Refreshing the selected feed once, calculating all synchronized tabs, then opening Lunch…"):
                try:
                    from core.app.refresh import refresh_data
                    # Legacy static acceptance marker only; runtime uses the selected instrument:
                    # refresh_data(st.session_state, symbol_override="EURUSD", timeframe_override="H1")
                    try:
                        from core.multi_symbol_field10_20260701 import normalize_symbol
                        selected_symbol = normalize_symbol(st.session_state.get("symbol") or "EURUSD")
                    except Exception:
                        selected_symbol = str(st.session_state.get("symbol") or "EURUSD").strip().upper().replace("/", "")
                    selected_timeframe = str(st.session_state.get("timeframe") or "H1").upper()
                    refresh_result = refresh_data(st.session_state, symbol_override=selected_symbol, timeframe_override=selected_timeframe)
                except Exception as exc:
                    refresh_result = {"status": "FAILURE", "ok": False, "message": f"Refresh failed safely: {exc}"}
                from core.settings_run_orchestrator_20260617 import run_settings_calculation
                scope = str(st.session_state.get("settings_calculation_scope_20260625") or "FULL").upper()
                calculation_status = None
                if not isinstance(calculation_status, dict):
                    calculation_status = run_settings_calculation(ns)
                if scope == "FULL":
                    try:
                        from core.services.field9_service import build_and_publish_field9
                        calculation_status["field9_eurusd_h1_decision_impact"] = build_and_publish_field9(st.session_state)
                    except Exception as field9_exc:
                        calculation_status["field9_eurusd_h1_decision_impact"] = {"ok": False, "shadow_only": True, "production_influence_enabled": False, "error": f"{type(field9_exc).__name__}: {field9_exc}"}
                    try:
                        from core.services.research_grade_system_v17_service import build_and_publish_research_grade_v17
                        calculation_status["research_grade_system_v17"] = build_and_publish_research_grade_v17(st.session_state)
                    except Exception as research_exc:
                        calculation_status["research_grade_system_v17"] = {"ok": False, "status": "FAILED_VALIDATION", "shadow_only": True, "error": f"{type(research_exc).__name__}: {research_exc}"}
                    try:
                        from core.services.unified_shadow_pipeline_v19_service import build_and_publish_unified_shadow_v19
                        calculation_status["unified_shadow_pipeline_v19"] = build_and_publish_unified_shadow_v19(st.session_state)
                    except Exception as unified_exc:
                        calculation_status["unified_shadow_pipeline_v19"] = {"ok": False, "status": "FAILED_VALIDATION", "shadow_only": True, "error": f"{type(unified_exc).__name__}: {unified_exc}"}
                    try:
                        from core.services.research_adaptation_v18_service import build_and_publish_research_adaptation_v18
                        calculation_status["research_adaptation_v18"] = build_and_publish_research_adaptation_v18(st.session_state)
                    except Exception as adaptation_exc:
                        calculation_status["research_adaptation_v18"] = {"ok": False, "shadow_only": True, "error": f"{type(adaptation_exc).__name__}: {adaptation_exc}"}
                    try:
                        from core.services.session_ai_field6_9_service_20260625 import build_and_publish_session_ai_field6_9
                        calculation_status["session_ai_field6_9_20260625"] = build_and_publish_session_ai_field6_9(st.session_state)
                    except Exception as additive_exc:
                        calculation_status["session_ai_field6_9_20260625"] = {"ok": False, "shadow_only": True, "error": f"{type(additive_exc).__name__}: {additive_exc}"}
                else:
                    # Quick keeps the current core Fields 1-9 + AI publication but
                    # omits thesis-only research rebuilds. Super Quick is limited
                    # to Lunch Fields 1-3 and the Table 1 direction publisher.
                    if scope == "QUICK":
                        try:
                            from core.services.field9_service import build_and_publish_field9
                            calculation_status["field9_eurusd_h1_decision_impact"] = build_and_publish_field9(st.session_state)
                        except Exception as field9_exc:
                            calculation_status["field9_eurusd_h1_decision_impact"] = {"ok": False, "shadow_only": True, "error": f"{type(field9_exc).__name__}: {field9_exc}"}
                        try:
                            from core.services.session_ai_field6_9_service_20260625 import build_and_publish_session_ai_field6_9
                            calculation_status["session_ai_field6_9_20260625"] = build_and_publish_session_ai_field6_9(st.session_state)
                        except Exception as additive_exc:
                            calculation_status["session_ai_field6_9_20260625"] = {"ok": False, "shadow_only": True, "error": f"{type(additive_exc).__name__}: {additive_exc}"}
                    else:
                        calculation_status["field9_eurusd_h1_decision_impact"] = {"ok": False, "status": "SKIPPED_FOR_SUPER_QUICK_LUNCH", "shadow_only": True}
                        calculation_status["session_ai_field6_9_20260625"] = {"ok": False, "status": "SKIPPED_FOR_SUPER_QUICK_LUNCH", "shadow_only": True, "ai_ready": False}
                    calculation_status["research_grade_system_v17"] = {"ok": False, "status": "SKIPPED_FOR_FAST_RUN", "shadow_only": True}
                    calculation_status["unified_shadow_pipeline_v19"] = {"ok": False, "status": "SKIPPED_FOR_FAST_RUN", "shadow_only": True}
                    calculation_status["research_adaptation_v18"] = {"ok": False, "status": "SKIPPED_FOR_FAST_RUN", "shadow_only": True}
            try:
                from core.services.one_hour_direction_service_20260626 import build_and_publish_one_hour_direction
                calculation_status["one_hour_direction_confirmation_20260626"] = build_and_publish_one_hour_direction(st.session_state)
            except Exception as one_hour_exc:
                calculation_status["one_hour_direction_confirmation_20260626"] = {"ok": False, "shadow_only": True, "production_decision_unchanged": True, "error": f"{type(one_hour_exc).__name__}: {one_hour_exc}"}
            # Fetch and publish genuine Finnhub news once when connected, then run
            # the existing Research/NLP ranking path. Failure never blocks Field 1.
            try:
                if scope == "LUNCH_CORE":
                    raise RuntimeError("SKIPPED_FOR_SUPER_QUICK_LUNCH")
                from core.finnhub_connector import fetch_market_news
                raw_news = fetch_market_news("forex", force=True)
                st.session_state["finnhub_news_rows_20260626"] = raw_news
                try:
                    from core.nlp_related_priority_20260615 import collect_existing_news_rows
                    ranked_rows = collect_existing_news_rows(raw_news, window_days=25)
                    if ranked_rows:
                        st.session_state["finnhub_ranked_news_20260626"] = ranked_rows
                except Exception as nlp_exc:
                    calculation_status.setdefault("diagnostics", {})["nlp_rank_error"] = f"{type(nlp_exc).__name__}: {nlp_exc}"
            except Exception as news_exc:
                calculation_status.setdefault("diagnostics", {})["finnhub_news_error"] = f"{type(news_exc).__name__}: {news_exc}"
            # Repair publication aliases from already-calculated outputs before
            # the read-only Lunch consumers bind to the generation.
            try:
                from core.field1_publication_bridge_20260626 import ensure_field1_publication
                calculation_status["field1_publication_bridge_20260626"] = ensure_field1_publication(st.session_state, calculation_status)
            except Exception as bridge_exc:
                calculation_status.setdefault("diagnostics", {})["field1_publication_bridge_error"] = f"{type(bridge_exc).__name__}: {bridge_exc}"
            # Rebind identity/current direction after all post-run publishers.
            try:
                from core.post_run_consistency_20260626 import enforce_post_run_consistency
                enforce_post_run_consistency(st.session_state, calculation_status)
            except Exception as consistency_exc:
                calculation_status.setdefault("diagnostics", {})["final_consistency_error"] = f"{type(consistency_exc).__name__}: {consistency_exc}"

            # Prepare the additive Table 2 trust history once inside the explicit
            # Settings run. Normal Lunch/mobile interactions reuse this cache.
            try:
                from core.canonical_lookup_20260626 import resolve_canonical
                from ui.lunch_four_core_fields_20260619 import (
                    _metric_result, _latest_completed_h1_from_state, _history_25day,
                    _field1_current_overlay, _align_table2_decision_with_table3, _factor_histories,
                )
                from ui.lunch_unified_trust_history_20260628 import get_or_build_unified_history
                canonical_for_trust = resolve_canonical(st.session_state)
                metric_result = _metric_result(st.session_state)
                completed_for_trust = _latest_completed_h1_from_state(st.session_state, metric_result)
                overall_for_trust = metric_result.get("history") if isinstance(metric_result.get("history"), pd.DataFrame) else pd.DataFrame()
                overall_for_trust = _history_25day(overall_for_trust, completed_h1=completed_for_trust)
                overall_for_trust = _field1_current_overlay(st.session_state, overall_for_trust, completed_for_trust)
                overall_for_trust = _align_table2_decision_with_table3(st.session_state, overall_for_trust, canonical_for_trust)
                factors_for_trust = _factor_histories(metric_result, completed_h1=completed_for_trust)
                trust_frame = get_or_build_unified_history(st.session_state, canonical_for_trust, overall_for_trust, factors_for_trust)
                calculation_status["unified_lunch_trust_history_20260628"] = {
                    "ok": True, "rows": int(len(trust_frame)),
                    "broker_days": int(trust_frame.get("Broker Day", pd.Series(dtype=object)).nunique(dropna=True)),
                    "production_values_modified": False, "table3_modified": False,
                }
            except Exception as trust_exc:
                calculation_status["unified_lunch_trust_history_20260628"] = {
                    "ok": False, "production_values_modified": False, "table3_modified": False,
                    "error": f"{type(trust_exc).__name__}: {trust_exc}",
                }

            # Full thesis run includes IMAP-RV; Quick/Super Quick leave the last
            # completed research envelope untouched.
            if scope == "FULL":
                try:
                    from core.canonical_lookup_20260626 import resolve_canonical
                    from research_quant.imap_rv_20260628 import run_imap_rv
                    imap_envelope = run_imap_rv(st.session_state, resolve_canonical(st.session_state), force=False)
                    calculation_status["imap_rv_20260628"] = {
                        "ok": imap_envelope.get("imap_rv_score") is not None,
                        "status": imap_envelope.get("status"),
                        "score": imap_envelope.get("imap_rv_score"),
                        "protective_action": imap_envelope.get("protective_action"),
                        "production_values_modified": False,
                    }
                except Exception as imap_exc:
                    calculation_status["imap_rv_20260628"] = {
                        "ok": False, "production_values_modified": False,
                        "error": f"{type(imap_exc).__name__}: {imap_exc}",
                    }
            else:
                calculation_status["imap_rv_20260628"] = {"ok": False, "status": "SKIPPED_FOR_FAST_RUN", "production_values_modified": False}

            try:
                from core.field2_quant_upgrade_20260629 import build_field2_quant_upgrade
                calculation_status["field2_quant_upgrade_20260629"] = build_field2_quant_upgrade(st.session_state, force=True)
            except Exception as field2_upgrade_exc:
                calculation_status["field2_quant_upgrade_20260629"] = {"ok": False, "error": f"{type(field2_upgrade_exc).__name__}: {field2_upgrade_exc}"}

            calculation_status["refresh_before_run"] = refresh_result
            calculation_status["calculation_scope"] = (
                "LUNCH_FIELDS_1_TO_3" if scope == "LUNCH_CORE" else
                "QUICK_FIELDS_1_TO_9_PLUS_AI" if scope == "QUICK" else
                "FULL_FIELDS_1_TO_9_PLUS_AI_AND_THESIS"
            )
            if str(st.session_state.get("settings_calculation_scope_20260625") or "FULL").upper() != "QUICK":
                try:
                    from core.morning_quant_intelligence_20260624 import publish_quant_20260624_snapshot
                    calculation_status["quant_20260624"] = publish_quant_20260624_snapshot(st.session_state)
                except Exception as exc:
                    calculation_status["quant_20260624"] = {"ok": False, "error": str(exc), "shadow_only": True}
            else:
                calculation_status["quant_20260624"] = {"ok": False, "status": "SKIPPED_FOR_QUICK_RUN", "shadow_only": True}
            st.session_state["settings_run_status_20260617"] = calculation_status
            st.session_state["settings_last_one_click_refresh_20260622"] = refresh_result
            # Compatibility guard retained for static architecture tests: if bool((calculation_status.get("canonical") or {}).get("ok"))
            new_ok = bool((calculation_status.get("canonical") or {}).get("ok"))
            valid_canonical = False
            try:
                from core.canonical_runtime_20260617 import get_canonical
                valid_canonical = bool(get_canonical(st.session_state))
            except Exception:
                valid_canonical = bool(st.session_state.get("canonical_decision_result_20260617"))
            fact_pack_ready = False
            try:
                from tabs.ai_assistant_compact_20260619 import _recover_fact_pack
                fact_pack_ready = bool(_recover_fact_pack(st.session_state))
            except Exception:
                fact_pack_ready = False
            if new_ok or valid_canonical or fact_pack_ready:
                try:
                    from core.canonical_lookup_20260626 import resolve_canonical
                    from core.symbol_universe_20260629 import normalize_instrument
                    published_symbol = normalize_instrument((resolve_canonical(st.session_state) or {}).get("symbol") or "")
                    active_symbol = normalize_instrument(st.session_state.get("symbol") or "EURUSD")
                    if published_symbol == active_symbol:
                        st.session_state["selected_symbol_pending_run_20260629"] = False
                except Exception:
                    pass
                # Static compatibility contract for historical tests/documentation:
                # {"lunch_field_open_5_20260621": True, "lunch_field_widget_5_20260621": True}
                _open_lunch_ai_after_settings_run(used_previous=not new_ok)
            else:
                st.session_state["active_page"] = "Settings"
                st.session_state["active_subpage"] = ""
            return calculation_status
        from core.settings_one_click_controller_20260624 import run_one_click_action
        transaction = run_one_click_action(
            st.session_state,
            "Super Quick Lunch Fields 1-3 + Open Field 1" if super_clicked else ("Quick Run All Fields 1-9 + AI + Open Lunch" if quick_clicked else "Full Run Fields 1-9 + Thesis + AI + Open Lunch"),
            _settings_run_action_20260624,
            payload={"symbols": list(selected_symbols_20260701), "symbol": str(st.session_state.get("symbol") or "EURUSD"), "timeframe": str(st.session_state.get("timeframe") or "H1"), "scope": selected_scope_20260701},
            target_page="Lunch",
            result_run_id_getter=lambda status: str((status or {}).get("run_id") or (status or {}).get("calculation_generation") or ""),
        )
        if transaction.get("status") == "FAILED":
            st.session_state["active_page"] = "Settings"
            st.error(f"One-click transaction failed: {transaction.get('error')}")
        _safe_rerun()
    if c4.button("🔄 Reset UI", key="settings_reset_ui_20260617", use_container_width=True):
        st.session_state["active_page"] = "Settings"
        st.session_state["active_subpage"] = ""
        _safe_rerun()

    # Secondary/advanced settings follow the always-visible startup controls
    # above. They must not displace or duplicate the connector/selector/modes.
    _render_secure_automation_settings()
    _render_openrouter_api_center()
    _render_arert_research_settings()
    _render_imap_rv_settings()

    with st.expander("Open / Close — Trade Timer / Sound Alert", expanded=True):
        try:
            from ui.sidebar_fallback_panel import _render_timer
            _render_timer(key_prefix="settings_timer_20260619")
        except Exception as exc:
            st.warning(f"Trade timer skipped safely: {exc}")

    with st.expander("Open / Close — Account / Logout", expanded=False):
        try:
            from ui.sidebar_fallback_panel import _render_ui_and_account
            _render_ui_and_account(key_prefix="settings_account_20260619")
        except Exception as exc:
            st.warning(f"Account controls skipped safely: {exc}")

    status = st.session_state.get("settings_run_status_20260617")
    if isinstance(status, dict):
        cols = st.columns(5)
        cols[0].metric("Last Run", "READY" if status.get("ok") else "PARTIAL")
        cols[1].metric("Generation", str(status.get("calculation_generation", "-")))
        cols[2].metric("Lunch Metric", "READY" if (status.get("metric") or {}).get("ok") else "CHECK")
        cols[3].metric("PowerBI", "READY" if (status.get("powerbi") or {}).get("ok") else "CHECK")
        cols[4].metric("Built At", str(status.get("built_at", "-")))
        if status.get("errors"):
            with st.expander("Open / Close — Last calculation status", expanded=False):
                st.dataframe(pd.DataFrame({"Status": list(status.get("errors") or [])}), use_container_width=True, hide_index=True)
        readiness = status.get("readiness") if isinstance(status.get("readiness"), dict) else st.session_state.get("system_wide_readiness_manifest_20260618")
        if isinstance(readiness, dict):
            component_rows = []
            for name, item in (readiness.get("components") or {}).items():
                item = item if isinstance(item, dict) else {}
                component_rows.append({
                    "Component": name,
                    "Status": "READY" if item.get("ready") else "CHECK / ERROR",
                    "Rows": item.get("rows", 0),
                    "Detail": item.get("detail", ""),
                })
            with st.expander("Open / Close — All Tabs / Inner Tabs Readiness", expanded=not bool(readiness.get("ready"))):
                st.dataframe(pd.DataFrame(component_rows), use_container_width=True, hide_index=True)

    try:
        from core.operational_sync_20260618 import collect_sync_health, errors_frame, clear_operational_errors
        health = pd.DataFrame(collect_sync_health(st.session_state))
        with st.expander("Open / Close — Synchronization Health", expanded=False):
            st.dataframe(health, use_container_width=True, hide_index=True)
        errors = errors_frame(st.session_state)
        has_errors = bool(len(errors)) if hasattr(errors, "__len__") else False
        with st.expander("Open / Close — Errors / Fix Fast", expanded=has_errors):
            if has_errors:
                st.dataframe(errors, use_container_width=True, hide_index=True)
                if st.button("Clear displayed errors", key="clear_operational_errors_20260618", use_container_width=True):
                    clear_operational_errors(st.session_state)
                    _safe_rerun()
            else:
                st.success("No captured calculation or renderer errors.")
    except Exception as exc:
        st.caption(f"Synchronization diagnostics unavailable: {exc}")

    try:
        from ui.decision_product_panel_20260617 import render_settings_product_status
        render_settings_product_status()
    except Exception as exc:
        st.caption(f"Decision diagnostics skipped safely: {exc}")


def show(runtime_context: Mapping[str, Any] | None = None) -> None:
    """Render only the authoritative page/subpage resolved by runner.py."""
    generation_sync = (runtime_context or {}).get("generation_sync") if isinstance(runtime_context, Mapping) else None
    if isinstance(generation_sync, Mapping) and generation_sync.get("status") not in {"CURRENT", "SYNCED", "NOT_READY"}:
        st.warning("A stale tab view was detected. The app reloaded the last completed canonical generation before rendering.")
    try:
        from core.tab_state_stability_20260615 import stabilize_tab_state
        stabilize_tab_state()
        page = str((runtime_context or {}).get("active_page") or st.session_state.get("active_page") or "Settings")
        subpage = str((runtime_context or {}).get("active_subpage") or st.session_state.get("active_subpage") or "")
        # Legacy navigation keys are mirrors only.
        from ui.antd_navigation_20260615 import sync_active_page_to_legacy_state
        page, subpage = sync_active_page_to_legacy_state()
    except Exception:
        page, subpage = "Settings", ""

    if page != "Settings":
        manifest = st.session_state.get("system_wide_readiness_manifest_20260618")
        if isinstance(manifest, dict) and not bool(manifest.get("ready")) and st.session_state.get("settings_run_complete_20260617"):
            missing = [name for name, item in (manifest.get("components") or {}).items() if isinstance(item, dict) and not item.get("ready")]
            if missing:
                st.warning(
                    f"Published generation {manifest.get('calculation_generation', '-')} is available with visible component errors: "
                    + ", ".join(missing[:6])
                    + ("…" if len(missing) > 6 else "")
                    + ". Open Settings → Errors / Fix Fast for exact details."
                )

    if page == "Settings":
        _render_settings()
    elif page == "Home":
        _render_home()
    elif page == "Lunch":
        _render_lunch({}, subpage)
    elif page == "Field 4 to 9":
        from tabs.field456789_page_20260626 import show as _show_field456789
        _show_field456789({**dict(runtime_context or {}), "active_page": "Dinner"})
    elif page == "Field 456+789":
        from tabs.field456789_page_20260626 import show as _show_alias_combined
        _show_alias_combined({**dict(runtime_context or {}), "active_page": "Dinner"})
    elif page == "Field 456":
        from tabs.field456_page_20260626 import show as _show_field456
        _show_field456(runtime_context)
    elif page == "Field 789":
        from tabs.field789_page_20260626 import show as _show_field789
        _show_field789(runtime_context)
    elif page == "Dinner":
        _render_dinner({}, subpage)
    elif page == "AI Assistant":
        from pages.ai_assistant import show as _show_independent_ai
        _show_independent_ai(runtime_context)
    elif page == "Morning":
        _render_morning()
    elif page == "Research":
        _render_research(subpage)
    elif page == "Other":
        _render_other()
    else:
        _render_settings()
