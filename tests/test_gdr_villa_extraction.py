import importlib.util
import math
import sys
from pathlib import Path

import pytest


def _load_script_module(module_name: str, filename: str):
    script_path = Path(__file__).resolve().parents[1] / "scripts" / filename
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load script module from {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_extractor = _load_script_module(
    "gdr_villa_extractor", "extract_gdr_villa_flux_summary.py"
)
_validator = _load_script_module("gdr_villa_validator", "validate_gdr_3m.py")
fit_volume_slope = _extractor.fit_volume_slope
_metrics = _validator._metrics


def test_volume_slope_recovers_exact_linear_trace() -> None:
    times = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    volumes = [1.25 + 0.75 * time for time in times]

    slope, standard_error, r_squared, rmse, lag = fit_volume_slope(times, volumes)

    assert slope == pytest.approx(0.75)
    assert standard_error == pytest.approx(0.0, abs=1e-12)
    assert r_squared == pytest.approx(1.0)
    assert rmse == pytest.approx(0.0, abs=1e-12)
    assert lag >= 1


def test_volume_slope_rejects_degenerate_runtime() -> None:
    with pytest.raises(ValueError, match="no variation"):
        fit_volume_slope([1.0, 1.0, 1.0, 1.0], [0.1, 0.2, 0.3, 0.4])


def test_flux_metrics_are_correct_for_known_errors() -> None:
    metrics = _metrics([1.0, 2.0, 3.0], [1.1, 1.8, 3.3])

    assert metrics["n"] == 3
    assert metrics["mae_l_m2_h"] == pytest.approx(0.2)
    assert metrics["rmse_l_m2_h"] == pytest.approx(math.sqrt(0.14 / 3))
    assert metrics["bias_l_m2_h"] == pytest.approx(0.0666666667)
    assert metrics["mape_percent"] == pytest.approx(10.0)


_ledger_extractor = _load_script_module(
    "gdr_villa_observation_ledger", "extract_gdr_villa_observation_ledger.py"
)


class _FakeSheet:
    def __init__(self, name: str, rows: list[list[object]]) -> None:
        self.name = name
        self._rows = rows
        self.nrows = len(rows)

    def cell_value(self, row: int, column: int) -> object:
        return self._rows[row][column]


def test_observation_ledger_preserves_source_rows_and_raw_sensor_values() -> None:
    rows = [[""] * 25 for _ in range(7)]
    rows[3][2], rows[3][4], rows[3][6] = 1.0, 0, 0.10
    rows[3][17], rows[3][21], rows[3][22], rows[3][23], rows[3][24] = (
        "Inf", 45.0, 25.0, 42.0, 28.0
    )
    rows[4][2], rows[4][4], rows[4][6] = 2.0, 0, 0.20
    rows[4][17] = "Inf"
    rows[5][2], rows[5][6] = "bad-runtime", 0.30
    rows[6][2], rows[6][6] = 3.0, 0.40  # Must not resume after a broken trace.
    sheet = _FakeSheet("20-40", rows)

    extracted = _ledger_extractor.extract_sheet_rows(
        sheet,
        workbook_filename="benchmark.xls",
        source_sha256="abc123",
    )

    assert len(extracted) == 2
    assert extracted[0]["observation_id"] == "VILLA3M-20-40-row4"
    assert extracted[0]["excel_row_1based"] == 4
    assert extracted[0]["distillate_volume_l"] == 0.10
    assert extracted[0]["feed_flowrate_low_lpm_raw"] == "Inf"
    assert extracted[0]["source_file_sha256"] == "abc123"


def test_observation_ledger_excludes_theoretical_sheet() -> None:
    sheet = _FakeSheet("Theoretical", [[""] * 25 for _ in range(5)])
    assert _ledger_extractor.extract_sheet_rows(
        sheet, workbook_filename="benchmark.xls", source_sha256="abc123"
    ) == []


def test_observation_ledger_source_checksum_is_pinned() -> None:
    assert _ledger_extractor.validate_source_checksum(
        _ledger_extractor.EXPECTED_SOURCE_SHA256
    ) is None
    with pytest.raises(ValueError, match="Source workbook SHA-256 changed"):
        _ledger_extractor.validate_source_checksum("different-source-checksum")
