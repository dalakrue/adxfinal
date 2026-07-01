"""Backward-compatible Streamlit entry point using the same application shell.

Run with: streamlit run adx_dashpoard.py
"""
from __future__ import annotations
import sys
import warnings
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

try:
    from pandas.errors import SettingWithCopyWarning
    warnings.filterwarnings("ignore", category=SettingWithCopyWarning)
except Exception:
    pass

from core.app_shell import run_app

def main() -> None:
    run_app()

if __name__ == "__main__":
    main()
