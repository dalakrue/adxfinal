from pathlib import Path

import pandas as pd

from core.serialization_compat_20260702 import dumps, loads, SERIALIZER_BACKEND


ROOT = Path(__file__).resolve().parents[1]


def test_serializer_round_trip_supports_runtime_cache_payload():
    payload = {
        "symbol": "EURUSD",
        "frame": pd.DataFrame({"time": pd.to_datetime(["2026-07-01T10:00:00Z"]), "close": [1.17]}),
    }
    restored = loads(dumps(payload, protocol=5))
    assert restored["symbol"] == "EURUSD"
    pd.testing.assert_frame_equal(restored["frame"], payload["frame"])
    assert SERIALIZER_BACKEND in {"cloudpickle", "pickle"}


def test_cloudpickle_is_explicit_deployment_dependency_and_has_fallback():
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    compat = (ROOT / "core/serialization_compat_20260702.py").read_text(encoding="utf-8")
    runtime_cache = (ROOT / "core/runtime_state_cache_20260628.py").read_text(encoding="utf-8")
    multi_symbol = (ROOT / "core/multi_symbol_field10_20260701.py").read_text(encoding="utf-8")
    assert "cloudpickle>=3.0,<4" in requirements
    assert "import pickle as _serializer" in compat
    assert "import cloudpickle" not in runtime_cache
    assert "import cloudpickle" not in multi_symbol



def test_serializer_imports_with_cloudpickle_blocked(monkeypatch):
    import builtins
    import importlib.util

    compat_path = ROOT / "core/serialization_compat_20260702.py"
    original_import = builtins.__import__

    def blocked_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "cloudpickle":
            raise ImportError("simulated missing cloudpickle")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    spec = importlib.util.spec_from_file_location("serialization_compat_fallback_test", compat_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    assert module.SERIALIZER_BACKEND == "pickle"
    assert module.loads(module.dumps({"ok": True})) == {"ok": True}

def test_three_calculation_modes_are_always_visible_and_independent():
    ui_source = (ROOT / "ui/multi_symbol_settings_20260701.py").read_text(encoding="utf-8")
    router_source = (ROOT / "tabs/antd_page_router_20260615.py").read_text(encoding="utf-8")
    for label in (
        "1. Quick — Fields 1–9 + AI",
        "2. Full — Fields 1–9 + thesis + AI",
        "3. Super Quick — Lunch Fields 1–3",
    ):
        assert label in ui_source
        assert label in router_source
    assert "horizontal=False" in ui_source
    assert "Render the advanced selector and the three calculation choices independently" in router_source
    assert "Multi-symbol selector skipped safely:" not in router_source
    assert "active symbol instead of aborting the main calculation button" in router_source
    assert "Waiting for connected data" in router_source
    assert "No timestamp" not in router_source


def test_critical_start_controls_are_dependency_free_and_ordered_before_run():
    ui_source = (ROOT / "ui/multi_symbol_settings_20260701.py").read_text(encoding="utf-8")
    router_source = (ROOT / "tabs/antd_page_router_20260615.py").read_text(encoding="utf-8")

    assert "from core.multi_symbol_field10_20260701" not in ui_source
    assert "import cloudpickle" not in ui_source
    assert "Multi-Symbol Selection — Always Visible" in ui_source
    assert "3 Run Calculation Choices — Always Visible" in ui_source
    assert "with st.container(border=True)" in ui_source

    settings_source = router_source[router_source.index("def _render_settings()"):]
    key_center = settings_source.index("_render_mobile_api_key_center()")
    market = settings_source.index("_render_market_connector_section()")
    finnhub = settings_source.index("_render_finnhub_connector_section()")
    symbols = settings_source.index("render_multi_symbol_selector")
    modes = settings_source.index("render_calculation_mode_selector")
    run_button = settings_source.index('"▶ Run Calculation + Open Lunch"')
    assert key_center < market < finnhub < symbols < modes < run_button
    assert settings_source.count("_render_market_connector_section()") == 1
    assert settings_source.count("_render_finnhub_connector_section()") == 1
    assert settings_source.count("_render_mobile_api_key_center()") == 1
    assert "Twelve Data + MT5 Market Connector — Always Visible" in router_source
    assert "Finnhub Connector — Always Visible" in router_source


def test_selector_source_can_import_without_cloudpickle_or_multi_symbol_engine(monkeypatch):
    import builtins
    import importlib.util
    import sys
    import types

    streamlit_stub = types.ModuleType("streamlit")
    streamlit_stub.session_state = {}
    monkeypatch.setitem(sys.modules, "streamlit", streamlit_stub)
    original_import = builtins.__import__

    def blocked_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "cloudpickle" or name.startswith("core.multi_symbol_field10_20260701"):
            raise ImportError(f"blocked optional dependency: {name}")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    path = ROOT / "ui/multi_symbol_settings_20260701.py"
    spec = importlib.util.spec_from_file_location("multi_symbol_settings_no_optional_deps", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    assert module.normalize_selected(["EUR/USD", "USTEC", "SPX500"]) == ["EURUSD", "NAS100", "US500"]


def test_always_visible_selector_and_three_modes_render_with_minimal_streamlit(monkeypatch):
    import importlib.util
    import sys
    import types

    class Context:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            return False

    class Column:
        def __init__(self, parent):
            self.parent = parent
        def button(self, *args, **kwargs):
            return False
        def metric(self, *args, **kwargs):
            return None
        def checkbox(self, label, key=None, **kwargs):
            return bool(self.parent.session_state.get(key, False))

    class FakeStreamlit(types.ModuleType):
        def __init__(self):
            super().__init__("streamlit")
            self.session_state = {"symbol": "EURUSD"}
            self.messages = []
        def container(self, **kwargs):
            return Context()
        def expander(self, *args, **kwargs):
            return Context()
        def markdown(self, value, **kwargs):
            self.messages.append(str(value))
        def caption(self, value, **kwargs):
            self.messages.append(str(value))
        def success(self, value, **kwargs):
            self.messages.append(str(value))
        def error(self, value, **kwargs):
            self.messages.append(str(value))
        def info(self, value, **kwargs):
            self.messages.append(str(value))
        def multiselect(self, label, options, key=None, **kwargs):
            value = list(self.session_state.get(key) or [])
            self.session_state[key] = value
            return value
        def columns(self, count, **kwargs):
            n = count if isinstance(count, int) else len(count)
            return [Column(self) for _ in range(n)]
        def selectbox(self, label, options, index=0, key=None, **kwargs):
            value = self.session_state.get(key)
            if value not in options:
                value = options[index]
            self.session_state[key] = value
            return value
        def radio(self, label, options, index=0, key=None, **kwargs):
            value = self.session_state.get(key)
            if value not in options:
                value = options[index]
            self.session_state[key] = value
            return value
        def button(self, *args, **kwargs):
            return False
        def rerun(self):
            return None

    fake = FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake)
    path = ROOT / "ui/multi_symbol_settings_20260701.py"
    spec = importlib.util.spec_from_file_location("multi_symbol_settings_render_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)

    selected = module.render_multi_symbol_selector(fake.session_state)
    scope = module.render_calculation_mode_selector(fake.session_state)
    assert selected == ["EURUSD"]
    assert scope == "QUICK"
    assert any("Multi-Symbol Selection — Always Visible" in message for message in fake.messages)
    assert any("3 Run Calculation Choices — Always Visible" in message for message in fake.messages)
