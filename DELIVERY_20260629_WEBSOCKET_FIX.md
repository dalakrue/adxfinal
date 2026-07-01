# WebSocket Connection Hardening — 2026-06-29

## Fault addressed
Mobile browser popup: `Failed to process a WebSocket message. RangeError: index out of range`.

## Changes
- Added a global Streamlit payload guard before any page renderer runs.
- Dataframes are Arrow-normalized and display-limited by rows/columns on mobile.
- JSON is recursively normalized and bounded before serialization.
- Plotly traces are downsampled for display while source calculations remain unchanged.
- Disabled WebSocket compression to avoid browser-side decompression/frame corruption.
- Set a conservative Streamlit message ceiling so accidental giant UI deltas fail safely instead of destabilizing the client.

## Non-deletion guarantee
No calculation, canonical snapshot, stored dataframe, export, history source, model, or decision logic was deleted or rewritten. Only browser display payloads are compacted.

## Operational note
No software can guarantee that a network interruption will never occur. This repair removes the application-controlled causes of oversized/fragmented messages and makes recurrence substantially less likely.

## Validation performed
- Python compileall: PASS for both entry files, runner, and new guard module.
- Payload guard unit smoke: PASS (2,000×120 table reduced to 300×45 for phone display; oversized JSON reduced below the transport target).
- Full Streamlit server smoke was not available in this repair container because the `streamlit` executable is not installed here.
