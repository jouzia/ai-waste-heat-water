# Time-varying workload coupling

## Status

The repository now contains a piecewise-constant coupling layer from an explicit workload trace into the reduced-order heat-recovery and membrane-distillation engine.

Implemented:
- interval-specific IT power and duration;
- interval-specific source temperature;
- explicit recoverable-heat fraction;
- explicit recovery efficiency, heat-exchanger effectiveness, and usable-heat fraction;
- minimum source-temperature eligibility;
- interval-by-interval MD simulation;
- additive energy/water accounting;
- profile-level avoided-freshwater counterfactual applied exactly once;
- heat-availability fraction and heat-weighted source temperature diagnostics.

## Scientific boundary

This is not a transient CFD, plant-control, or measured data-center thermal model. IT electricity-to-heat remains a declared first-order approximation, and each interval is treated as piecewise constant.

A quantitative workload study still requires a provenance-backed workload trace and a declared mapping from workload/utilization to measured or modeled server power and source temperature. Until that evidence exists, this module is infrastructure rather than a published workload result.

## Reproducibility requirement

Every study trace must preserve:
1. source identifier and retrieval date;
2. original sampling interval;
3. power units and conversion;
4. temperature measurement/estimation method;
5. missing-data treatment;
6. aggregation/resampling rule;
7. boundary conditions;
8. parameter distributions, if stochastic;
9. exact trace hash;
10. development versus held-out designation.
