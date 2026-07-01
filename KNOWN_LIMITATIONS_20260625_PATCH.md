# Known limitations — 2026-06-25 patch

- This patch fixes the AI Assistant routing regression at the normalization layer and updates the main programmatic AI navigation buttons, but other legacy modules that still write raw navigation keys may benefit from future cleanup to use the same helper.
- Quick Run now skips several known heavy shadow publications in `tabs/antd_page_router_20260615.py`, but the protected core Settings orchestration still needs a full runtime profile to prove measured savings.
- The green less-risky path fallback is additive and conservative. It does not alter the protected main path. Its visibility now depends only on having a valid canonical current price and main path, plus optional evidence modifiers.
- The new Quick Decision field is implemented in the active Lunch selector architecture. The old unconditional header display was removed.
- Field 7 and Field 8 history views are improved through standardized projection from currently available stored evidence. A full schema-specific database migration for new dedicated history tables was not added in this patch.
