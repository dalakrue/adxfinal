# AI Assistant grounding report

The mandatory answer object is implemented with all required keys: answer text, short summary, intent, run identity, broker time, evidence fields/rows, confidence, sufficiency, freshness, warnings and suggested questions.

Supported deterministic intents include decision, forecasts, regime, expected value after costs, adverse impact, regret, flip conditions, synchronization, freshness and model reliability. Unsupported questions are rejected. Numeric values are composed only from the supplied saved payload.

External-provider composition remains optional in the existing assistant; the v17 deterministic contract is the safe fallback.
