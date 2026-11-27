"""Guard the transcription and provenance of the 1998 Table 1 coefficients."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "validation" / "MD_1998_TABLE1_INFERRED_COEFFICIENTS.csv"


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_1998_table1_has_all_twelve_condition_rows() -> None:
    rows = load_rows()

    assert len(rows) == 12
    conditions = {
        (float(row["feed_concentration_mol_L"]), float(row["recirculation_rate_m3_s"]))
        for row in rows
    }
    assert len(conditions) == 12
    assert {float(row["feed_concentration_mol_L"]) for row in rows} == {
        0.0,
        0.55,
        1.15,
        1.67,
    }
    assert {float(row["recirculation_rate_m3_s"]) for row in rows} == {
        0.000007,
        0.000011,
        0.000015,
    }


def test_1998_table1_water_condition_coefficients_match_source() -> None:
    rows = {
        float(row["recirculation_rate_m3_s"]): row
        for row in load_rows()
        if float(row["feed_concentration_mol_L"]) == 0.0
    }

    assert float(rows[0.000007]["h_overall_W_m2_K"]) == 1800.0
    assert float(rows[0.000007]["h_reported_plus_minus_W_m2_K"]) == 90.0
    assert float(rows[0.000007]["C_times_1e7_kg_m2_s_Pa"]) == 14.9
    assert float(rows[0.000011]["h_overall_W_m2_K"]) == 2050.0
    assert float(rows[0.000015]["h_overall_W_m2_K"]) == 2690.0


def test_1998_table1_coefficients_are_not_misrepresented_as_raw_validation_data() -> None:
    for row in load_rows():
        assert row["source_id"] == "MD-DCMD-POLARIZATION-1998"
        assert row["source_locator"] == "Table 1, printed p. 4133"
        assert "Inferred from Eqs. 21 and 19" in row["coefficient_provenance"]
        assert "not specified" in row["uncertainty_semantics"]
        assert "not independent validation" in row["use_restriction"]
