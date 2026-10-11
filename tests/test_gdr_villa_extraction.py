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
