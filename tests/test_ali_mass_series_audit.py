import importlib.util
import sys
from pathlib import Path

import pytest


def _load_module():
    path = Path(__file__).resolve().parents[1] / "scripts" / "audit_ali_mass_series.py"
    spec = importlib.util.spec_from_file_location("audit_ali_mass_series", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load mass-series audit from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_audit = _load_module()


def test_mass_series_audit_quantifies_negative_variation_without_repair() -> None:
    summary = _audit.summarize_series([0.0, 0.2, 0.19, 0.4])
    assert summary["n_readings"] == 4
    assert summary["negative_step_count"] == 1
    assert summary["total_negative_variation_kg"] == pytest.approx(0.01)
    assert summary["negative_variation_as_pct_of_positive_net_change"] == pytest.approx(5.0)
    assert summary["monotonic_non_decreasing"] is False
    assert "semantics not inferred" in summary["interpretation"]


def test_mass_series_audit_rejects_nonfinite_and_single_point_inputs() -> None:
    with pytest.raises(ValueError, match="At least two"):
        _audit.summarize_series([1.0])
    with pytest.raises(ValueError, match="finite"):
        _audit.summarize_series([0.0, float("nan")])


def test_mass_series_audit_monotonic_trace_has_zero_negative_variation() -> None:
    summary = _audit.summarize_series([0.0, 0.1, 0.2, 0.4])
    assert summary["monotonic_non_decreasing"] is True
    assert summary["negative_step_count"] == 0
    assert summary["total_negative_variation_kg"] == 0.0
