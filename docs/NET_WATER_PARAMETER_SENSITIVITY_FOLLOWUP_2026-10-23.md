# Net-water parameter sensitivity follow-up

Date: 2026-10-23

## Status
This is a predeclared analysis plan, not a claim that the additional numerical experiment has been executed.

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
