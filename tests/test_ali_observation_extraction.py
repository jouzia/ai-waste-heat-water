import importlib.util
import sys
from pathlib import Path

import pytest


def _load_script():
    path = Path(__file__).resolve().parents[1] / "scripts" / "extract_ali_2020_observations.py"
    spec = importlib.util.spec_from_file_location("ali_2020_observation_extractor", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load observation extractor from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_extractor = _load_script()


def test_ali_source_registry_pins_all_five_workbook_hashes() -> None:
    assert set(_extractor.EXPECTED_SHA256) == {
        "S1_Data.xlsx", "S2_Data.xlsx", "S3_Data.xlsx", "S4_Data.xlsx", "S5_Data.xlsx"
    }
    assert len(set(_extractor.EXPECTED_SHA256.values())) == 5
    assert _extractor.FLOW_BY_FILE == {
        "S2_Data.xlsx": 50,
        "S3_Data.xlsx": 100,
        "S4_Data.xlsx": 200,
        "S5_Data.xlsx": 300,
    }


@pytest.mark.parametrize(
    ("raw", "normalized"),
    [
        ("Time", "time"),
        ("Thim ", "thim"),
        ("Thut", "thut"),
        ("mw (kg)", "mwkg"),
        ("FR (L/h)", "frlh"),
        ("T_Cin", "tcin"),
        (None, ""),
    ],
)
def test_header_normalization_handles_source_variants(raw, normalized) -> None:
    assert _extractor.normalize_header(raw) == normalized


def test_finite_number_rejects_nonfinite_and_boolean_values() -> None:
    assert _extractor.finite_number(1.25) == pytest.approx(1.25)
    assert _extractor.finite_number(float("nan")) is None
    assert _extractor.finite_number(float("inf")) is None
    assert _extractor.finite_number(True) is None


def test_linear_slope_recovers_known_cumulative_mass_rate() -> None:
    assert _extractor._linear_slope([0.0, 1.0, 2.0], [1.0, 3.0, 5.0]) == pytest.approx(2.0)
