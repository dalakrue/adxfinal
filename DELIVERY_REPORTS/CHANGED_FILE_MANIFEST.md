# Changed-file manifest

Changed: **22** · Added: **4** · Removed: **0**

## Changed
- `core/ai_canonical_intents_v10.py` — Use the read-only canonical fallback resolver; no AI scoring formula changed.
- `core/config/defaults.py` — Make the eight requested independent top-level routes authoritative.
- `core/decision_table_20260626.py` — Pin the Quick Run fallback row to its completed broker candle so it appears immediately as PENDING.
- `core/navigation_parts/main.py` — Align fallback navigation with the requested eight routes.
- `core/quick_source_signature_20260626.py` — Publish source snapshot hash and completed broker-candle aliases with the Quick manifest.
- `pages/ai_assistant.py` — Add explicit optional AirLLM selection while retaining the lightweight grounded fallback.
- `requirements-optional-heavy.txt` — Move AirLLM to explicit optional server dependencies.
- `requirements.txt` — Remove AirLLM from normal deployment startup dependencies.
- `services/current_canonical_copy_20260625.py` — Resolve current canonical identity through the shared read-only fallback chain.
- `ui/airllm_mobile_assistant_20260626.py` — Render status only; no import, download, model load, or inference during page render.
- `ui/canonical_copy_export_20260619.py` — Use shared canonical resolution and keep the only active direct Copy Short/Copy Full pair generation-cached.
- `ui/home_master_control_bar_20260615.py` — Align navigation controls with the requested independent pages.
- `ui/liquid_menu_popup_20260615.py` — Remove the duplicate popup copy renderer.
- `ui/lunch_decision_table_20260626.py` — Use the requested Table 1 title while preserving compatibility markers.
- `ui/lunch_four_core_fields_20260619.py` — Use shared canonical identity, requested table titles/Table 4 call, no-copy Field 6 display, and selected-field-only rendering.
- `ui/lunch_identity_strip_20260626.py` — Recover valid canonical identities from compatible aliases and display source signature.
- `ui/lunch_next_hour_bias_history_20260626.py` — Implement bounded display-only Table 4 from genuine published news/technical/session/regime evidence.
- `ui/lunch_restored.py` — Remove legacy duplicate copy controls.
- `ui/main_menu_drawer.py` — Replace legacy Dinner route with independent AI Assistant while retaining Field 456/789.
- `ui/powerbi_cached_renderer_20260619.py` — Use shared canonical identity only; protected central and session-shadow projection math remains unchanged.
- `ui/risk_position_panel_20260619.py` — Remove legacy duplicate copy/export invocation.
- `ui/system_readiness_20260621.py` — Remove Field 6 duplicate copy/export toggle.

## Added
- `PROTECTED_UPLOAD_HASHES_20260626.json` — Record SHA-256 values from the actual uploaded ZIP for protected-file verification.
- `core/canonical_lookup_20260626.py` — New read-only active/last-valid/sync/alias canonical resolver; no publication or calculation side effects.
- `services/airllm_backend_20260626.py` — New optional lazy server backend with environment gates, lock, bounded context/output, and deterministic fallback.
- `tests/test_delivery_acceptance_20260626.py` — New delivery acceptance tests for the requested repair contract.

## Removed
- None.
