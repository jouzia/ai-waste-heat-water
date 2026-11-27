"""Tests for the electricity-water evidence registry schema."""

import json
from pathlib import Path


def test_freshwater_input_is_distinct_from_consumption() -> None:
    """CEA SWC must be recordable without mislabelling it as consumptive use."""
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "geography"
        / "electricity_water_factor.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    metric = schema["properties"]["water_metric"]

    assert metric["type"] == "string"
    assert set(metric["enum"]) == {
        "consumption",
        "withdrawal",
        "freshwater_input",
    }
    assert "do not relabel" in metric["description"]
