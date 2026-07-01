# Security Report

A static scan checked for the user-provided Twelve Data key, Finnhub key and common `sk-`/OpenRouter key patterns. No hard-coded match was found in the delivered project.

API keys remain runtime secrets. Mobile page navigation does not intentionally reconnect or fetch external data; refresh/calculation remains explicit. The AI layer continues to use bounded evidence rather than sending the complete database.
