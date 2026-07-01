"""Preferred Streamlit deployment entry point.

Run with: streamlit run app.py
"""
from __future__ import annotations
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# Must run before Streamlit/Tornado creates an event loop on Windows.
try:
    from core.windows_asyncio_compat_20260619 import install_windows_selector_policy
    install_windows_selector_policy()
except Exception:
    pass

# Legacy static contract only; execution no longer imports the old router:
# from adx_dashpoard import main
from core.app_shell import run_app

if __name__ == "__main__":
    run_app()
