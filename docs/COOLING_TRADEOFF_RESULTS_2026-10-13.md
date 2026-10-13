# Cooling architecture water–energy–carbon trade-off execution

**Run:** [Cooling architecture water energy carbon trade-offs, run #2](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38428654552)  
**Commit:** `2ea59dc3695e2f6cd0912821305f3e8b322c7845`  
**Artifact:** `cooling-water-energy-carbon-tradeoffs`, ID `11829333067`, archive SHA-256 `8fef84310e3b3be32ad5e8bdc9999e2e8ee5b78a22f278b070843cacab7e6cd1`, expires 2027-01-11.  
**Coverage:** 1,440 scenarios across six cooling architectures, four membrane areas (2, 5, 10, 20 m²), five freshwater-displacement fractions (0 to 1), four grid-water factors, and three grid-carbon factors. The output CSV and Pareto front have separate SHA-256 checksums in the artifact manifest.

## Scenario-only Pareto result

The sweep retained **15 Pareto rows** (five distinct operating choices, repeated once for each of three grid-carbon factors). Five architecture families appear in the Pareto set; air-cooled is dominated under these particular hypothetical assumptions. Representative water/energy/output values are:

| Architecture | Net consumption change (L) | Incremental electricity (kWh) | Freshwater produced (L) |
|---|---:|---:|---:|
| Evaporative | −1.75 | 1.77 | 4.61 |
| Direct liquid | −4.00 | 3.27 | 4.61 |
| Hybrid | −3.06 | 2.72 | 4.61 |
| Rear-door heat exchanger | −7.44 | 6.31 | 8.23 |
| Immersion | −10.45 | 9.17 | 11.54 |

These values describe the selected illustrative scenarios only. They do **not** establish that immersion cooling is generally best, that any real facility would be water-positive, or that these architecture factors are representative. The assumptions were deliberately varied to expose trade-offs rather than assert a measured ranking.

## Accounting boundary

- Net water change is additional operational water consumption minus the declared avoided freshwater consumption.
- Gross distillate is not counted as avoided water unless the specified displacement fraction says it replaces freshwater consumption.
- Incremental electricity includes the architecture's assumed incremental facility electricity plus MD auxiliary electricity.
- Operational emissions are incremental electricity multiplied by a declared grid-carbon factor. Embodied emissions, equipment manufacturing, water treatment/post-treatment emissions, brine management emissions, and baseline IT electricity are excluded.
- Grid water and carbon factors are scenario inputs, not location-specific measurements.

## Scientific status

This completes a reproducible **scenario execution**, not physical validation. The result is conditional on a fixed one-hour workload, fixed water activity, illustrative cooling factors, and an MD model that has not passed source-matched or held-out validation. The Pareto front is not a publication-ready recommendation. Empirical cooling architecture data, local grid-water/carbon factors, measured workload/temperature traces, and validated MD parameters remain necessary before interpreting the front physically.
