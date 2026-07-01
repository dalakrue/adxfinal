# Final Field 1 / NLP / Navigation Repair

## Repaired
- Canonical lookup now recovers the exact published Settings status and Quick publication manifest when the active pointer is temporarily absent.
- Final post-run consistency now executes after direction-confirmation and connected-news publication.
- Table 1 now reads existing Field 1/Table 3 history aliases directly and can display genuine history even while identity is diagnostically unbound.
- Table 4 now accepts genuine Finnhub and Research Lab NLP aliases, while retaining an explicitly labeled local-technical fallback.
- Separate top-level Field 456 and Field 789 menu routes are restored.
- AirLLM remains wired to the independent AI Assistant with deterministic canonical fallback.

## Validation
- Full automated suite: 57 passed.
- No protected production formula or threshold was intentionally changed.

## Deployment note
AirLLM inference itself was not executed because no model artifact/configuration was supplied in the uploaded ZIP. The backend is lazy and requires ADX_ENABLE_AIRLLM=1, ADX_AIRLLM_MODEL_ID, optional package installation, and adequate server resources.
