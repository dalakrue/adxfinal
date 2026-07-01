# Security and API Setup Guide

## Never hard-code keys

Do not place real keys in Python, Markdown, Git commits, screenshots, or `.streamlit/secrets.example.toml`.

## Streamlit Cloud secrets

Open Streamlit Community Cloud → App settings → Secrets and add:

```toml
[api_keys]
finnhub = "your-finnhub-key"
second_api = "your-twelve-data-key"
openrouter = "your-openrouter-key"

[openrouter]
model = "openrouter/auto"
```

The project also supports environment variables:

```text
OPENROUTER_API_KEY
OPENROUTER_MODEL
```

## Temporary session input

Settings contains a password-masked OpenRouter temporary-session field plus Save + Connect and Clear controls. The complete key is never displayed after entry and is not persisted by the ARERT database.

## OpenRouter behavior

- validation uses a bounded timeout;
- chat requests use a bounded timeout;
- one retry is permitted for 429, 5xx, timeout, or network errors;
- non-retryable errors fail immediately;
- failure returns to the deterministic local grounded Assistant;
- only bounded canonical and research evidence is sent;
- keys are never copied into prompts, state summaries, or research records.

## Local files

Keep a real `.streamlit/secrets.toml` outside Git. The included `.gitignore` and example file should be reviewed before deployment.

## Scan evidence

`reports/SECRET_SCAN_20260628.json` recorded zero suspicious committed secrets in the delivered source/configuration/documentation scope.
