# Ali dynamic DCMD reconstruction: admissibility failure analysis

**Date:** 2026-10-13  
**Status:** blocking source-reconstruction issue; no experimental validation claim

## Reproducible diagnostic

The GitHub Actions workflow `Ali dynamic-model admissibility audit` executes a 17-case matrix for the lumped dynamic model against a one-minute, constant-input smoke trace (hot inlet 60 °C, cold inlet 25 °C, outlets initialized at the default 25 °C). The matrix tests the source default configuration at 50, 100, 200, and 300 L/h; the alternate 0.2 μm pore-radius interpretation; geometric area 9.8 m²; and the source-reported lumped heat-loss correction. A reduced-area case is retained only as a numerical control.

The completed diagnostic, [workflow run #6](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38431215693), reports **16/16 source-scale lumped cases rejected** by the physical outlet-temperature envelope guard and **1/1 reduced-area control accepted**. The envelope is [25, 60] °C. Across source-scale cases, predicted hot outlet minima range from 11.615 to 15.984 °C, while cold outlet maxima range from 38.920 to 42.906 °C. The default 50 L/h case predicts a hot outlet minimum of 11.714 °C and cold outlet maximum of 39.704 °C. Changing pore-radius interpretation, using 9.8 m² rather than 10 m², or applying the published empirical correction did not remove the failure. This matrix is a failure diagnostic, not model fitting.

The temperature overshoot is large, not a small tolerance issue. It indicates a serious inconsistency in the current lumped source reconstruction—likely in the coupling between bulk/interface heat transfer and the module's counter-current dynamics, not something that can be fixed by selecting one of the tested parameter variants. Do not fit parameters to force this smoke trace into the envelope.

## Additional implementation corrections

1. **Measured-input derivatives.** The mass-production-rate ODE now applies the chain rule to piecewise-linear inlet-temperature histories. In the spatial model, bulk-temperature derivatives include adjacent cell derivatives and the boundary derivative at the module edge. This is necessary when the model is driven by fluctuating measured inputs; the prior implementation included only outlet-temperature derivatives. A unit test checks the piecewise-linear derivative primitive.
2. **Spatial effective area.** Each spatial cell's membrane heat-transfer area is now the configured effective area divided by cell count. The hydraulic channel volume remains geometry-based. Previously the spatial heat-transfer area was always computed from length × width, so an explicit effective-area override was silently ignored.
3. **Failure reporting.** Lumped and spatial envelope rejections now include the actual predicted outlet ranges. This helps distinguish a small numerical tolerance issue from a large model-form or unit inconsistency.

These corrections improve the auditability of the implementation; they do not establish that the source equations or property closures are fully reconstructed.

## Scientific interpretation

The published Ali et al. (2020) paper reports a calibrated lumped model with an overall relative error of about 3.22% after applying an empirical heat-loss correction selected by trial and error. That source-reported metric is not a validation result for this repository. The current repository reconstruction still fails its own physical-admissibility check under the source-scale smoke conditions, so it cannot be used to fit transient traces or to claim predictive performance.

Before any dynamic fit is attempted, the next steps are:

- capture the actual predicted outlet ranges and inspect the source equations, state definitions, and unit/reference conventions line by line;
- independently verify whether the published membrane coefficient and enthalpy terms are implemented in consistent units and reference states;
- compare lumped and spatial energy balances against a hand-calculated limiting case and an independent steady-state solution;
- only then evaluate the extracted measured-input time series, preserving condition-level held-out traces and all source uncertainty.

The overall Research 2 completion gate remains **INCOMPLETE**. The dynamic source reconstruction, unfitted validation, held-out validation, uncertainty convergence, geographic integration, full reproducibility package, manuscript, and final publication audit must not be marked complete on the basis of this diagnostic.
