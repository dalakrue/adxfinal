# ADX Quant Pro Repair — 2026-06-26

## Fixed
- Quick Run Decision History now displays the newly published current completed-candle row immediately as PENDING when no settled archive exists. It does not invent prior rows.
- Field 456 and Field 789 are accepted by the authoritative navigation stabilizer instead of being reset to Settings.
- Canonical identity lookup now falls back to last-valid canonical and canonical-sync snapshot state for Lunch Fields 1–3.
- Removed the duplicate menu Copy Short/Copy Full pair. Exactly two recreated copy controls remain at the top of Lunch.
- Power BI session evidence/status and the session-adjusted projection are grouped in one bordered frame while calculations remain independent.
- Added Field 1 Table 4: latest 24 NLP-news rows with next-hour sentiment, technical, session, regime, and combined evidence bias. This is display-only and does not modify protected logic.
- Added optional lazy AirLLM 2.11.0 dependency for Python 3.9–3.12. AirLLM remains server-side and opt-in through deployment environment variables.

## Safety
No protected production decision rule, threshold, prediction formula, regime formula, historical outcome, or Field 1 calculation was changed.

## AirLLM deployment
Set `ADX_ENABLE_AIRLLM=1` and `ADX_AIRLLM_MODEL=<compatible-model-id>` only on a server with adequate storage/RAM/GPU. The iPhone renders the chat UI only.
