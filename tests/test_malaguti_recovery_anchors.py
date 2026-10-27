"""Integrity checks for source-transcribed Malaguti recovery anchors.

These checks protect the provenance table; they do not reproduce the paper's
thermodynamic model or validate its reported values empirically.
"""
from __future__ import annotations

import csv
from pathlib import Path

ANCHOR_PATH = (
    Path(__file__).resolve().parents[1]
    / "05_validation"
    / "data"
    / "malaguti_2026_agmd_recovery_anchors.csv"
)


def test_malaguti_anchor_table_has_expected_schema_and_four_unique_cases() -> None:
    with ANCHOR_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 4
    assert {
        "configuration",
        "configuration_name",
        "vaporization_efficiency",
        "delta_t_c",
        "recovery_percent",
        "source_status",
        "evidence_location",
        "independent_reproduction_status",
    }.issubset(rows[0].keys())

    cases = {
        (
            int(row["configuration"]),
            float(row["vaporization_efficiency"]),
            float(row["delta_t_c"]),
        )
        for row in rows
    }
    assert cases == {
        (3, 0.5, 30.0),
        (3, 0.5, 50.0),
        (3, 0.7, 30.0),
        (3, 0.7, 50.0),
    }


def test_malaguti_anchor_values_remain_source_targets_not_model_predictions() -> None:
    with ANCHOR_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    values = {
        (
            float(row["vaporization_efficiency"]),
            float(row["delta_t_c"]),
        ): float(row["recovery_percent"])
        for row in rows
    }
    assert values == {
        (0.5, 30.0): 2.2,
        (0.5, 50.0): 3.9,
        (0.7, 30.0): 3.0,
        (0.7, 50.0): 5.6,
    }
    assert all(row["source_status"] == "reported_in_main_article" for row in rows)
    assert all(
        row["independent_reproduction_status"]
        == "supplement_available_property_model_unverified"
        for row in rows
    )
