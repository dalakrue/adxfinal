# QUICK Fields 1–3 Call Graph

```text
app.py
└── adx_dashpoard.main
    └── Settings renderer / active router
        └── run_settings_calculation(scope=QUICK)
            ├── load + normalize completed EURUSD H1
            ├── Field 1 protected calculation/cache
            ├── protected Power BI central calculation/cache
            ├── Field 3 protected regime calculation
            ├── canonical atomic publication
            ├── QUICK early return (before Field 7/8 wrapper services)
            └── publish_quick_manifest
                ├── normalized OHLC digest
                ├── source/protected identity
                └── run/generation/snapshot timing manifest
    └── route Lunch -> Field 1
        ├── Field 1 cached renderer + session lens
        ├── Field 2 cached renderer + session shadow
        └── Field 3 daily-locked renderer
```

Reuse path:

```text
Settings QUICK click
└── try_reuse_quick_fields_123
    ├── canonical exists
    ├── latest completed H1 matches
    ├── Field 1/2/3 caches ready
    ├── full source signature exactly matches
    └── reuse immutable generation; no protected calculation rerun
```
