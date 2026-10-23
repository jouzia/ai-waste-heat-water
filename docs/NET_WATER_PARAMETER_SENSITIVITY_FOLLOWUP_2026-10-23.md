# Net-water parameter sensitivity follow-up

Date: 2026-10-23

## Status
The membrane-conductivity stress test has now been implemented and executed successfully in GitHub Actions. The flow-multiplier study remains blocked pending source-backed nominal flow data.

## Evidence boundary
The existing break-even envelope varies membrane area, permeance, temperature-polarization coefficient, recoverable-heat fraction, grid-water factor, cooling-water intensity, incremental electricity, and freshwater displacement. It holds membrane thermal conductivity at 0.03 W m-1 K-1 and thickness at 0.2 mm. The top-level screening model does not explicitly sweep feed/permeate flow.

The Villa workbook audit found the MD feed high-flow channel negative in all 631 retained rows, both MD low-flow channels recorded as Inf in all 631 rows, and an unresolved 3M versus CLARCOR identity discrepancy. These values cannot support empirical flow distributions. Do not take absolute values, impute, or infer physical flow without source documentation.

## Predeclared deterministic stress tests

| Factor | Test values | Interpretation |
|---|---|---|
| Villa nominal membrane area | 0.8x, 0.9x, 1.0x, 1.1x, 1.2x of 0.23088 m2 | Sensitivity-only perturbations; not a sourced uncertainty distribution |
| Membrane thermal conductivity | 0.015, 0.03, 0.06 W m-1 K-1 | Illustrative factor-of-two stress test; not a sourced material range |
| Feed/permeate mass flow | 0.5x, 1x, 2x of a documented nominal baseline | Do not execute until a defensible baseline is sourced; Villa flow channels are not usable for this purpose |
| Freshwater displacement | 0, 0.25, 0.5, 0.75, 1 | Counterfactual scenarios, not probabilities |
| Grid electricity-water factor | 0.1, 0.5, 1, 2 L/kWh | Scenario range only until region/year and consumption-vs-withdrawal basis are sourced |

For each executable scenario preserve Git SHA, model version, inputs, solver status, gross freshwater production, additional water consumption, net water-consumption change, break-even displacement threshold, and failure classification. Report all scenarios; do not interpret grid-point shares as real-world probabilities. Keep physical water consumption, withdrawal, and stress-weighted impact separate.

## Decision rules

1. If net-water sign changes under area/conductivity perturbations, no directional benefit claim is supported.
2. A break-even displacement threshold above 1 means even full displacement cannot offset modeled additional water consumption in that scenario.
3. Flow sensitivity remains unparameterized until source-backed nominal feed/permeate flow is available.
4. The next implementation should expose conductivity as a parameter in the break-even runner and produce a manifest and full scenario table before interpreting results.
5. Independent MD validation and geographic electricity-water factors remain open publication gates.


## Executed conductivity stress test — 2026-10-23

Implementation commit: `b31ae0b6c88d7f0d1c6a10e3467d46a68b12bf21`

Workflow: [Break-even and failure envelope, run 6](https://github.com/jouzia/ai-waste-heat-water/actions/runs/39988586088) — **success**.

Artifact: `break-even-failure-envelope`, SHA-256 `2b7fcbd38d5de036ece2b18569454fb8c61d0dd5429c2dfb32e645a4468325ac`. It contains the manifest, `break_even_failure_envelope.csv`, and `net_water_by_displacement.csv`. The workflow verified file checksums and coverage of 15,552 envelope rows and 77,760 displacement-sweep rows.

| Membrane thermal conductivity (W m⁻¹ K⁻¹) | Break-even possible at displacement ≤ 1 | Break-even impossible even at full displacement | No freshwater production |
|---:|---:|---:|---:|
| 0.015 | 1,177 / 5,184 (22.7%) | 2,279 / 5,184 (44.0%) | 1,728 / 5,184 (33.3%) |
| 0.030 | 646 / 5,184 (12.5%) | 1,730 / 5,184 (33.4%) | 2,808 / 5,184 (54.2%) |
| 0.060 | 270 / 5,184 (5.2%) | 1,242 / 5,184 (24.0%) | 3,672 / 5,184 (70.8%) |

These percentages are **fractions of the deliberately constructed scenario grid only**, not probabilities, likelihoods, or estimates of real-world occurrence. As conductivity increases across this illustrative stress test, the number of grid cells classified as break-even possible falls from 1,177 to 270, while no-production cells rise from 1,728 to 3,672. This demonstrates that conclusions depend materially on this model parameterization; it does not establish that higher conductivity physically causes these changes in a real membrane system.

The model's full-displacement net-consumption change spans −27.33 to +66.75 L at conductivity 0.015, −17.31 to +73.50 L at 0.030, and −11.76 to +87.00 L at 0.060 across the remaining scenario factors. Negative values occur in 1,177, 646, and 270 grid cells, respectively. Because the model is reduced-order and the parameter ranges are illustrative, these values are conditional model outputs, not field predictions or evidence of a net-water benefit.

### Interpretation and remaining limits

- The conductivity sweep is complete; the predeclared area sensitivity (0.8×–1.2× of 0.23088 m²) has **not** been added as a separate Villa-specific sweep in this run.
- Flow sensitivity remains unexecuted: do not infer flow baselines from the Villa workbook's negative/Inf channels.
- These are model screening scenarios, not empirical uncertainty distributions; grid-cell counts must not be presented as probability.
- Source reconstruction, independent/unfitted validation, model-form comparison, geographic integration, and publication-package gates remain open. No positive net-water-benefit conclusion is supported.
