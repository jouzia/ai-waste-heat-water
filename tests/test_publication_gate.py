import importlib.util
import sys
from pathlib import Path


def _load_publication_gate():
    path = Path(__file__).resolve().parents[1] / "scripts" / "publication_gate.py"
    spec = importlib.util.spec_from_file_location("publication_gate_module", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load publication gate from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_gate = _load_publication_gate()


def _status(status: str = "COMPLETE", *, false_gate: str | None = None) -> dict:
    gates = {name: True for name in _gate.REQUIRED_GATE_NAMES}
    if false_gate is not None:
        gates[false_gate] = False
    return {
        "status": status,
        "gates": gates,
        "claim_policy": {"publication_ready_claim": False},
    }


def test_publication_gate_fails_when_project_is_incomplete() -> None:
    status = _status("INCOMPLETE", false_gate="held_out_validation")
    failures = _gate._status_failures(status)
    assert any("expected 'COMPLETE'" in failure for failure in failures)
    assert any("held_out_validation" in failure for failure in failures)


def test_publication_gate_fails_if_any_gate_is_false_even_when_status_says_complete() -> None:
    status = _status("COMPLETE", false_gate="held_out_validation")
    failures = _gate._status_failures(status)
    assert len(failures) == 1
    assert "held_out_validation" in failures[0]


def test_publication_gate_rejects_missing_required_gate() -> None:
    status = _status()
    del status["gates"]["held_out_validation"]
    failures = _gate._status_failures(status)
    assert any("missing required scientific gates" in failure for failure in failures)


def test_publication_gate_accepts_only_complete_true_gates() -> None:
    status = _status()
    assert _gate._status_failures(status) == []
