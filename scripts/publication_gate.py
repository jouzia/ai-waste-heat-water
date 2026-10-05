"""Publication-readiness gate.

This script intentionally fails while any mandatory scientific gate remains
unmet. It is a claim-control mechanism, not a quality score.
"""


def _root():
    from pathlib import Path

    return Path(__file__).resolve().parents[1]


def _load(path: str):
    import yaml

    root = _root()
    return yaml.safe_load((root / path).read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    registry = _load("04_experiments/BENCHMARK_REGISTRY.yaml")
    matrix = _load("04_experiments/VALIDATION_MATRIX.yaml")
    for case in registry.get("cases", []):
        status = case.get("validation_status")
        if status == "validated_held_out":
            bench = case.get("benchmark_file")
            if not bench:
                failures.append(f"{case['source_id']}: held-out case has no benchmark file")
            else:
                ledger = _root() / bench.replace(".yaml", "_observations.yaml")
                if not ledger.exists():
                    failures.append(f"{case['source_id']}: observation ledger missing")

    for case in matrix.get("cases", []):
        if case.get("quantitative_claim") is True:
            failures.append(
                f"{case['source_id']}: quantitative_claim must remain false until validation gate passes"
            )

    required_docs = [
        "docs/PRIMARY_SOURCE_VALIDATION_GATE.md",
        "docs/UNCERTAINTY_PLAN.md",
        "docs/GLOBAL_SENSITIVITY_PROTOCOL.md",
        "docs/GEOGRAPHIC_LAYER.md",
        "10_manuscript/MANUSCRIPT_PLAN.md",
    ]
    root = _root()
    for path in required_docs:
        if not (root / path).exists():
            failures.append(f"missing required protocol: {path}")

    if failures:
        print("PUBLICATION GATE: NOT READY")
        for item in failures:
            print(f"- {item}")
        return 1

    print("PUBLICATION GATE: READY FOR FINAL AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
