# Known limitations

- Live MT5/Twelve Data/Finnhub refresh and broker settlement could not be exercised without credentials and a live terminal.
- Browser clipboard behavior was not physically tested on an iPhone. The active controls use isolated clickable components and reveal manual selected text only after clipboard failure.
- AirLLM is optional, disabled, and not installed in the base deployment. No model download or inference benchmark was performed; server suitability remains deployment-specific.
- Streamlit Community Cloud/local ephemeral filesystems may not provide durable database persistence across rebuilds. Existing database files and records were left unchanged.
- Table 4 stays empty when genuine published news evidence is absent. It does not create placeholder headlines or weights.
- The project still contains legacy compatibility modules. Active routing and lazy imports prevent unselected pages from rendering, but the legacy source files are retained to avoid breaking imports.
- Performance measurements are limited and noisy; they support no broad speed/RAM percentage claim.
