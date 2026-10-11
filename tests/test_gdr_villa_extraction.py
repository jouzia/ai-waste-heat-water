import math

import pytest

from scripts.extract_gdr_villa_flux_summary import fit_volume_slope
from scripts.validate_gdr_3m import _metrics


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
