"""
Pytest tests for sales_visualiser.py
Run with: pytest -q
Requires:  python -m pip install dash\[testing]
"""
import importlib.util
import pytest
import pathlib

# Resolve the path to sales_visualiser.py
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
APP_PATH = ROOT_DIR / "app.py"
MODULE_NAME = "sales_app_under_test"

@pytest.fixture
def app():
    """Load Dash app from file"""
    spec = importlib.util.spec_from_file_location(MODULE_NAME, APP_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app

# Tests
def test_header_present(dash_duo, app):
    dash_duo.start_server(app)
    header = dash_duo.find_element("#header")
    assert header is not None
    assert header.text == "Pink Morsel Visualiser"


def test_graph_present(dash_duo, app):
    dash_duo.start_server(app)
    graph = dash_duo.find_element("#graph svg")
    # The dcc.Graph is present and Plotly has rendered an <svg>
    assert graph is not None
    assert graph.tag_name == "svg"


def test_region_picker_present(dash_duo, app):
    dash_duo.start_server(app)
    radio = dash_duo.find_element("#region_picker")
    assert radio is not None
    # Verify we have the five expected options
    options = [lab.text for lab in radio.find_elements("css selector", "label")]
    assert options == ["all", "north", "east", "south", "west"]