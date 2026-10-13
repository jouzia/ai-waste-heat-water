# Ali dynamic DCMD reconstruction: admissibility failure analysis

**Date:** 2026-10-13  
**Status:** blocking source-reconstruction issue; no experimental validation claim

## Reproducible diagnostic

The GitHub Actions workflow `Ali dynamic-model admissibility audit` executes a 17-case matrix for the lumped dynamic model against a one-minute, constant-input smoke trace (hot inlet 60 °C, cold inlet 25 °C, outlets initialized at the default 25 °C). The matrix tests the source default configuration at 50, 100, 200, and 300 L/h; the alternate 0.2 μm pore-radius interpretation; geometric area 9.8 m²; and the source-reported lumped heat-loss correction. A reduced-area case is retained only as a numerical control.

The completed diagnostic, [workflow run #6](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38431215693), reports **16/16 source-scale lumped cases rejected** by the physical outlet-temperature envelope guard and **1/1 reduced-area control accepted**. The envelope is [25, 60] °C. Across source-scale cases, predicted hot outlet minima range from 11.615 to 15.984 °C, while cold outlet maxima range from 38.920 to 42.906 °C. The default 50 L/h case predicts a hot outlet minimum of 11.714 °C and cold outlet maximum of 39.704 °C. Changing pore-radius interpretation, using 9.8 m² rather than 10 m², or applying the published empirical correction did not remove the failure. This matrix is a failure diagnostic, not model fitting.

The temperature overshoot is large, not a small tolerance issue. It indicates a serious inconsistency in the current lumped source reconstruction—likely in the coupling between bulk/interface heat transfer and the module's counter-current dynamics, not something that can be fixed by selecting one of the tested parameter variants. Do not fit parameters to force this smoke trace into the envelope.

## Measured source-trace check

The reproducible source-trace workflow [run #14](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38432821521) evaluated the first 30 minutes of the S2 Data workbook, worksheet `50` (50 L/h nominal flow, 50 °C target), using the measured inlet histories and measured initial outlet temperatures. The extracted trace contains 181 observations at a median 10-second interval. Measured hot inlet rises from 18.77 °C to 48.72 °C; measured cold inlet ranges from 18.92 to 19.25 °C. Both measured cumulative-distillate observations remain zero through this 30-minute segment.

Both unrefitted lumped-model cases were rejected by the physical envelope guard:
- No heat-loss correction: predicted hot-outlet minimum 4.987 °C and cold-outlet maximum 44.650 °C.
- Published 50 L/h correction (0.077): predicted hot-outlet minimum 4.557 °C and cold-outlet maximum 43.662 °C.

The admissible envelope for this trace was [18.750, 61.290] °C. The predicted hot outlet falls more than 13 °C below the minimum measured inlet/initial-outlet temperature. This is a clear physical-admissibility failure on measured source inputs, not merely the earlier synthetic cold-start stress test. Artifact ID `11831163647`, ZIP SHA-256 `6d6bf926b0aadee377d7175ab67dd64bf4d31c6a8e38bb5894675df7c2064459`, retained through 2027-01-11.

The 3-cell coarse spatial model was then evaluated on the same 181-row warm-up subset in [workflow run #26](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38434956718). It improved the magnitude of the violation but did not pass the physical guard:
- No correction: hot-outlet range [17.802, 19.819] °C; cold-outlet range [18.873, 48.361] °C.
- Published spatial correction (0.15): hot-outlet range [17.362, 19.610] °C; cold-outlet range [18.878, 46.104] °C.

Both predictions still fall below the 18.750 °C lower envelope. The coarse spatial model is closer than the lumped model, consistent with counter-current axial gradients mattering, but the 3-cell result is not a converged discretization. Artifact ID `11832214020`, ZIP SHA-256 `5b2491e459b950967193d6717b9207a3bce2c14e0b3e0452e67f9b1d2e2f3100`; the artifact includes the exact extracted transient ledger and source workbook hash manifest. This run used an exploratory relative tolerance of 1e-4 and trapezoidal mass-state integration at the 10-second input knots; numerical time-grid convergence remains required.

The trace is a 30-minute warm-up subset, not the full experimental run and not a held-out validation result. The 10-cell spatial model was then run on the same trace in [workflow run #27](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38435255900), artifact ID `11832304007`, ZIP SHA-256 `7453cb643a33d79a04369df44c8508a1e0e6add1384b55ed15bd83a023407578`. Unlike the lumped and 3-cell coarse models, both 10-cell spatial cases stayed within the physical outlet envelope and maintained nonnegative, monotonic mass production. However, they are not validated:
- **10-cell, no correction:** hot-outlet MAE/RMSE 0.152/0.170 °C; cold-outlet MAE/RMSE 6.322/7.872 °C (positive bias 6.201 °C); predicted cumulative mass 0.616 kg at 30 min while the measured ledger remains 0 kg.
- **10-cell, published spatial correction 0.15:** hot-outlet MAE/RMSE 0.166/0.184 °C; cold-outlet MAE/RMSE 4.563/6.351 °C (positive bias 4.446 °C); predicted cumulative mass 0.556 kg at 30 min while the measured ledger remains 0 kg.

The published correction improves the cold-outlet and mass error modestly, but the early cumulative-mass discrepancy remains. The measured S2/50 trace is still at zero mass at 30 min and reaches about 0.55 kg by 60 min; the model predicts about that amount by 30 min. This pattern is consistent with a possible product-collection/time-origin lag, but that explanation is **unverified** and must not be implemented as a fitted time shift. Check the source methods and other traces before drawing a conclusion.

The 10-cell result shows why spatial counter-current resolution matters: it removes the gross outlet-envelope failure, but cold-side temperature and early accumulated-mass errors remain substantial. The 3-cell spatial result is not a converged discretization. The current comparison uses a relaxed exploratory tolerance profile and trapezoidal mass-state integration at 10-second input knots. Next steps: (1) audit the source's collection/measurement timing; (2) run time-grid and 5/10/20-cell convergence; (3) extend the comparison through the full S2/50 trace; and (4) evaluate an untouched flow/temperature trace as held-out evidence. Do not fit parameters to this trace and then report it as independent validation.

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
