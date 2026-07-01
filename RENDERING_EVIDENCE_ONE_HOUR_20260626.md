# Rendering Evidence

Static and deterministic evidence:
- `lunch/field_01/renderer.py` invokes operational rendering before protected Full Metric History and no longer uses a Shadow expander.
- `lunch/field_02/renderer.py` invokes the operational path renderer before existing charts; UI renders both protected raw and operational safe path series.
- `lunch/field_03/renderer.py` renders next-H1 compatibility before protected regime history.
- Field 8 and Field 9 registry modules exist and invoke the operational renderer.
- Field 9's former unconditional early return was removed.

A live screenshot was not fabricated because this delivery environment has no connected broker/API runtime data or active Streamlit browser session.
