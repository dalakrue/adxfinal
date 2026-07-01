"""Backward-compatible V9 wrapper for the split implementation.
# Settings transaction owns build_quant_research_v4_transaction; implementation remains in split parts.

Public names and runtime behavior are preserved; implementation source is stored
in bounded modules under ``core/settings_run_orchestrator_v9_parts``.
"""

from core.v9_compat_loader import export_split_namespace as _export_split_namespace

_export_split_namespace(globals(), __file__, __name__)
del _export_split_namespace

# V11 additive post-publication hook. The protected V10 transaction runs first;
# this computes only shadow research from its immutable published snapshot.
_v10_run_settings_calculation = run_settings_calculation

def run_settings_calculation(*args, **kwargs):
    # Exact-source reuse is checked before any protected or shadow engine runs.
    # A prior FULL generation may satisfy QUICK, but QUICK never substitutes for
    # a requested FULL thesis/research generation.
    try:
        import streamlit as st
        from core.runtime_state_cache_20260628 import reusable_completed_generation
        requested_scope = str(st.session_state.get("settings_calculation_scope_20260625") or "FULL").upper()
        reused = reusable_completed_generation(st.session_state, requested_scope)
        if reused:
            return reused
    except Exception:
        requested_scope = "FULL"
    status = _v10_run_settings_calculation(*args, **kwargs)
    try:
        import streamlit as st
        if str(st.session_state.get('settings_calculation_scope_20260625') or 'FULL').upper() in {'QUICK', 'LUNCH_CORE'}:
            if isinstance(status, dict):
                status['calculation_scope']='LUNCH_FIELDS_1_TO_3' if str(st.session_state.get('settings_calculation_scope_20260625') or '').upper() == 'LUNCH_CORE' else 'QUICK_FIELDS_1_TO_9_PLUS_AI'
                try:
                    from core.canonical_runtime_20260617 import get_canonical
                    from core.quick_source_signature_20260626 import publish_quick_manifest
                    canonical = get_canonical(st.session_state)
                    if isinstance(canonical, dict) and canonical:
                        publish_quick_manifest(st.session_state, status, canonical)
                        st.session_state['settings_run_status_20260617'] = status
                except Exception as manifest_exc:
                    status.setdefault('diagnostics', {})['quick_manifest_error'] = f"{type(manifest_exc).__name__}: {manifest_exc}"
            try:
                from core.post_run_consistency_20260626 import enforce_post_run_consistency
                enforce_post_run_consistency(st.session_state, status)
            except Exception as consistency_exc:
                status.setdefault('diagnostics', {})['post_run_consistency_error'] = f"{type(consistency_exc).__name__}: {consistency_exc}"
            try:
                from core.runtime_state_cache_20260628 import save_runtime_state
                status["runtime_warm_cache_20260628"] = save_runtime_state(
                    st.session_state, status=status, scope=str(st.session_state.get('settings_calculation_scope_20260625') or 'QUICK').upper()
                )
                st.session_state["settings_run_status_20260617"] = status
            except Exception as cache_exc:
                status.setdefault("diagnostics", {})["runtime_warm_cache_error"] = f"{type(cache_exc).__name__}: {cache_exc}"
            return status
        from core.services.research_service import build_and_store_shadow_research
        from core.runtime_state_cache_20260628 import phone_research_profile
        with phone_research_profile(st.session_state):
            research_status = build_and_store_shadow_research(st.session_state)
        if isinstance(status, dict):
            status["field_07_research_v11"] = research_status
            st.session_state["settings_run_status_20260617"] = status
        try:
            from core.services.field8_service import build_and_publish_field8
            from core.runtime_state_cache_20260628 import phone_research_profile
            with phone_research_profile(st.session_state):
                field8_status = build_and_publish_field8(st.session_state)
        except Exception as field8_exc:
            field8_status = {"ok": False, "published": False, "error": f"{type(field8_exc).__name__}: {field8_exc}"}
        if isinstance(status, dict):
            status["field_08_integrated_history_20260624"] = field8_status
            st.session_state["settings_run_status_20260617"] = status
        try:
            from core.services.field8_quant_research_v15_service import build_and_publish_v15
            from core.runtime_state_cache_20260628 import phone_research_profile
            with phone_research_profile(st.session_state):
                v15_status = build_and_publish_v15(st.session_state)
        except Exception as v15_exc:
            v15_status = {"ok": False, "shadow_only": True, "error": f"{type(v15_exc).__name__}: {v15_exc}"}
        if isinstance(status, dict):
            status["field8_quant_research_v15_20260624"] = v15_status
            st.session_state["settings_run_status_20260617"] = status
    except Exception as exc:
        research_status = {
            "ok": False,
            "shadow_only": True,
            "production_decision_unchanged": True,
            "error": f"{type(exc).__name__}: {exc}",
        }
        try:
            import streamlit as st
            st.session_state["field_07_research_error_v11"] = research_status["error"]
            if isinstance(status, dict):
                status["field_07_research_v11"] = research_status
                st.session_state["settings_run_status_20260617"] = status
        except Exception:
            pass
    try:
        import streamlit as st
        from core.post_run_consistency_20260626 import enforce_post_run_consistency
        enforce_post_run_consistency(st.session_state, status)
    except Exception as consistency_exc:
        if isinstance(status, dict):
            status.setdefault("diagnostics", {})["post_run_consistency_error"] = f"{type(consistency_exc).__name__}: {consistency_exc}"
    # Additive ARCEF-SV publication. It reads the frozen canonical generation and
    # never mutates protected production values or Field 1 Table 3.
    try:
        import streamlit as st
        from core.canonical_runtime_20260617 import get_canonical
        from core.thesis_engine.orchestrator import publish_arcef_result
        canonical = get_canonical(st.session_state)
        if canonical is not None:
            if hasattr(canonical, "to_dict"):
                canonical_payload = canonical.to_dict()
            elif isinstance(canonical, dict):
                canonical_payload = dict(canonical)
            elif hasattr(canonical, "__dict__"):
                canonical_payload = dict(vars(canonical))
            else:
                canonical_payload = {}
            from core.runtime_state_cache_20260628 import phone_research_profile
            with phone_research_profile(st.session_state):
                arcef = publish_arcef_result(st.session_state, canonical_payload)
            if isinstance(status, dict):
                status["arcef_sv"] = {"ok": arcef.get("ok", False), "run_id": arcef.get("run_id"), "algorithm_version": arcef.get("algorithm_version")}
                st.session_state["settings_run_status_20260617"] = status
    except Exception as arcef_exc:
        if isinstance(status, dict):
            status.setdefault("diagnostics", {})["arcef_sv_error"] = f"{type(arcef_exc).__name__}: {arcef_exc}"
    # CRCEF-SV is the final additive shadow publisher. It consumes the exact
    # frozen generation after all protected Field 1-9 publishers and never
    # mutates the canonical object.
    try:
        import streamlit as st
        from core.canonical_runtime_20260617 import get_canonical
        from core.canonical_lookup_20260626 import resolve_canonical
        from research_quant.orchestrator import publish_crcef_sv_research
        protected_canonical = get_canonical(st.session_state)
        canonical_for_research = resolve_canonical(st.session_state, preferred=protected_canonical)
        from core.runtime_state_cache_20260628 import phone_research_profile
        with phone_research_profile(st.session_state):
            crcef = publish_crcef_sv_research(st.session_state, canonical_for_research)
        if isinstance(status, dict):
            status["crcef_sv_research_20260627"] = {
                "ok": bool(crcef.get("ok")),
                "status": crcef.get("status"),
                "run_id": crcef.get("run_id"),
                "generation_id": crcef.get("generation_id"),
                "production_decision_unchanged": True,
            }
            st.session_state["settings_run_status_20260617"] = status
    except Exception as crcef_exc:
        if isinstance(status, dict):
            status.setdefault("diagnostics", {})["crcef_sv_error"] = f"{type(crcef_exc).__name__}: {crcef_exc}"
    try:
        import streamlit as st
        from core.runtime_state_cache_20260628 import save_runtime_state
        cache_report = save_runtime_state(st.session_state, status=status, scope="FULL")
        if isinstance(status, dict):
            status["runtime_warm_cache_20260628"] = cache_report
            st.session_state["settings_run_status_20260617"] = status
    except Exception as cache_exc:
        if isinstance(status, dict):
            status.setdefault("diagnostics", {})["runtime_warm_cache_error"] = f"{type(cache_exc).__name__}: {cache_exc}"
    return status
