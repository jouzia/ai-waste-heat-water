# Demo Mode

Demo mode is a presentation configuration, not a scientific result set.

## Rules

- Every numerical value in configs/demo.yaml is illustrative unless separately marked as source-backed.
- The demo must display the distinction between gross distillate and net freshwater-consumption change.
- No demo output may be described as experimental validation, industrial performance, or a measured water saving.
- The benchmark validation ledger remains authoritative for scientific evidence.
- Negative or zero net-benefit outcomes must remain displayable.
- Source-backed results and scenario-only demonstrations must be visually and textually distinguished.

## Scientific gate

The repository's current implementation has been confirmed on main to contain the counter-current DCMD solver, heat-quality/exergy layer, validation matrix, and regression tests. This confirms source-state integration, but it does not substitute for a green CI run or physical validation.

The demonstration configuration is therefore intentionally conservative in its claims.

## Reproducible demo entry point

From a clean checkout:

```bash
python scripts/run_demo.py
```

The runner loads `configs/demo.yaml`, executes the same coupled `simulate()` engine used by the research code, and emits a JSON ledger containing:

- IT energy and generated/recoverable heat
- heat exergy relative to the declared ambient reference
- MD thermal, cooling, conductive, and pumping burdens
- gross distillate, feed withdrawal, and concentrate
- direct and indirect water consumption
- explicitly declared avoided freshwater consumption
- net consumption change and its sign interpretation

The runner intentionally does **not** convert gross distillate into avoided freshwater consumption. That displacement must be supplied as an explicit counterfactual input.

This entry point is a reproducibility convenience and presentation layer; it does not upgrade the benchmark or validation status.
