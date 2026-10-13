# Ali et al. (2020) spatial-grid and solver-tolerance convergence audit

**Workflow:** [Ali spatial-grid and solver-tolerance convergence, run #1](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38438071835)  
**Code commit:** `e8d4a1a40e1ed8796ec9bcfb1d89c3612043a742`  
**Artifact:** `ali-spatial-grid-tolerance-convergence`, ID `11834251167`, SHA-256 `c537fb23c6865da830a0dca4fae882834f24975d95fb9bcb47e30f5bb59775e7`; retained until 2027-01-11.  
**Source:** Ali, Orfi & Najib (2020), PLOS ONE, DOI 10.1371/journal.pone.0230207, CC BY 4.0.  
**Trace:** S2 Data, worksheet `50`, 1,662 timestamped observations, nominal 50 L/h, measured warm-up inlet histories, observed initial outlet temperatures. No parameters were fitted.

## Design

The spatial finite-volume grid and ODE tolerances were varied on the same measured trace:

| Spatial cells | Relative tolerance | Absolute temperature tolerance (K) |
|---:|---:|---:|
| 5 | 1e-4 | 1e-4 |
| 10 | 1e-4 | 1e-4 |
| 20 | 1e-4 | 1e-4 |
| 10 | 1e-6 | 1e-6 |
| 20 | 1e-6 | 1e-6 |

The 20-cell, 1e-6 case is the numerical reference for this diagnostic. It is not an experimentally established truth.

## Numerical convergence findings

Comparing the 10-cell, 1e-4 result with the 20-cell, 1e-6 reference:

- Hot-outlet temperature difference: RMSE **0.00315 °C**, maximum absolute difference **0.00666 °C**.
- Cold-outlet temperature difference: RMSE **0.0722 °C**, maximum absolute difference **0.689 °C**.
- Predicted mass-rate difference: RMSE **0.0485 kg/h**, maximum absolute difference **0.292 kg/h**.
- Predicted accumulated-mass difference: RMSE **0.0314 kg**, maximum absolute difference **0.0474 kg**.

The solver-tolerance comparison at fixed 20 cells was much smaller: the 20-cell 1e-4 case differed from the 20-cell 1e-6 reference by RMSE **5.94e-5 °C** for cold-outlet temperature and **3.88e-4 kg/h** for predicted mass rate. This indicates that the tested ODE tolerance is not the dominant source of the remaining 10-vs-20-cell difference.

All five numerical runs had nonnegative predicted mass rates and monotone *model-predicted* accumulated mass. Those are internal physical-state checks only; they do not repair the source workbook's raw mass-field ambiguity.

## Model-to-observation residuals remain material

Against the measured S2/50 trace, the 10-cell, 1e-4 model had hot-outlet RMSE **0.324 °C** and cold-outlet RMSE **4.980 °C**. Refining to 20 cells did not materially reduce these empirical residuals: hot-outlet RMSE was **0.326 °C**, cold-outlet RMSE **5.005 °C**. A numerically converged model can still be structurally wrong or have a boundary-condition/property mismatch.

The source workbook's `mw` field is nonmonotonic in 14 of 19 complete timed worksheet traces, and its measurement/reset semantics are not sufficiently documented for a defensible cumulative-mass error metric. Predicted accumulated mass remains a model output only; no observed-mass comparison is made.

## Conclusion

**Numerical integration/grid stability is now partially characterized; source reconstruction and empirical validation are not passed.** The cold-side temperature mismatch and raw mass-field semantics remain blocking issues. The 20-cell reference is a diagnostic comparator, not a claim of physical truth. No net-freshwater-benefit or publication-readiness claim follows from this audit.
