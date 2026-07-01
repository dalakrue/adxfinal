# ADX Quant Pro final repair — 2026-06-26

## Implemented

- Removed the Settings section `Open / Close — NLP / AI Assistant API Key`, including its mobile key box, model field, endpoint field, save action and clear action.
- Removed the embedded Field 5 Grounded AI Assistant from the Field 456 selector and display path.
- Made the independent top-level AI Assistant the only AirLLM owner. AirLLM is lazy-loaded after a question is sent; deterministic canonical grounding remains the no-fabrication fallback when AirLLM is unavailable.
- Added `requirements-airllm.txt` and an AirLLM deployment guide. Base Streamlit deployment remains lightweight; AirLLM is installed only on a capable Python 3.12 server.
- Combined Field 456 and Field 789 display rendering on one page. Both existing navigation buttons open the same combined workspace, while all original engines, caches, persistence stores, functions and calculations remain independent.
- Added a post-run canonical consistency transaction that:
  - normalizes active and last-valid canonical aliases to one run/generation/candle identity;
  - publishes the source signature and snapshot identity when available;
  - binds already-built Power BI output to the exact active generation without creating a synthetic path;
  - publishes the current completed-candle direction-confirmation row from existing canonical values when no historical archive row exists;
  - never fabricates news, historical outcomes, scores, prediction paths or reliability evidence.
- Quick and Full Settings runs both execute the consistency transaction after the protected calculation completes.
- Preserved `app.py` as the deployment entry point and Python 3.12 runtime declarations.

## Verification

- Python compile check: passed for `core`, `tabs`, `ui`, `pages`, and `services`.
- Test suite: **53 passed**.
- Streamlit startup smoke test: application started successfully on a local headless server and stopped cleanly after the test timeout.

## AirLLM deployment boundary

Use `pip install -r requirements-airllm.txt`, set `ADX_ENABLE_AIRLLM=1`, and set `ADX_AIRLLM_MODEL_ID`. By default, model downloads remain disabled. A local model path is recommended for deterministic deployment capacity. If the package/model/server capacity is unavailable, the assistant reports the AirLLM status and uses canonical deterministic grounding rather than inventing an answer.

## Final Field 1 visibility hardening

- Field 1 no longer returns early when the protected full-metric archive is absent.
- Quick Run always exposes Table 1, Table 2, and all ten requested Table 3 factor-table structures.
- The current canonical completed-candle row is shown as PENDING when published.
- Missing historical evidence remains an explicitly empty schema/N/A state; no rows, scores, outcomes, or accuracy values are fabricated.
- Reverified after this change: 53 tests passed and the Streamlit startup smoke test passed.
