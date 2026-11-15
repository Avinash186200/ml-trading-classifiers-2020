"""Light checks: every notebook is valid JSON and is stored without outputs."""
import json
from pathlib import Path

import pytest

NOTEBOOKS = sorted((Path(__file__).resolve().parents[1] / "notebooks").glob("*.ipynb"))


def test_there_are_notebooks():
    assert NOTEBOOKS


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_is_clean(path):
    nb = json.loads(path.read_text(encoding="utf-8"))
    assert nb.get("nbformat") == 4
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            assert cell.get("outputs") == []
            assert cell.get("execution_count") is None
