# Pre-registration: Ali et al. (2020) held-out transient trace

**Registration date:** 2026-10-13  
**Source:** Ali, Orfi & Najib (2020), PLOS ONE 15(3):e0230207, DOI [10.1371/journal.pone.0230207](https://doi.org/10.1371/journal.pone.0230207), CC BY 4.0.

## Purpose and scope

This is a pre-specified **within-study operating-condition holdout**, not an independent study-level validation. The purpose is to test whether the source-reconstructed 10-cell spatial DCMD model transfers to a different nominal flow/target-temperature condition without fitting to that trace.

## Locked trace assignment

- **Development / diagnostic trace:** `S2_Data.xlsx`, worksheet `50`, nominal circulation flow 50 L/h, nominal hot-inlet target 50 °C. This trace is already being used for source-reconstruction diagnostics and is not a held-out result.
- **Held-out trace:** `S3_Data.xlsx`, worksheet `60`, nominal circulation flow 100 L/h, nominal hot-inlet target 60 °C.

The held-out trace is selected by a deterministic rule: use the first complete transient sheet at the next nominal flow tier (100 L/h) and the 60 °C target. Selection is made before computing or inspecting model-versus-observation metrics for that trace. Do not replace it with a more favorable trace after seeing results.

## Locked model and analysis

1. Use the **10-cell spatial** model, with the source-published spatial heat-loss correction for the nominal flow as the primary case. Also run the same case with no heat-loss correction as a pre-specified model-form comparison.
2. Use the source-reported geometry and initial outlet temperatures from the first complete measured row. Use measured hot- and cold-inlet temperature histories from the observation ledger.
3. Use the current documented IAPWS95 property closure and cached 0.1 K grid. Record the model-code commit, input-ledger checksum, raw workbook SHA-256, number of rows, and actual time span.
4. Do not fit membrane parameters, pore size, tortuosity, heat-transfer coefficients, heat-loss correction, salinity, or any time shift to this held-out trace.
5. Do not shift the time origin to align mass. The raw `mw (kg)` column is nonmonotonic in 13 of 18 timed traces and its cumulative/reset semantics are not verified. Preserve raw readings and do not compute mass error metrics or infer a lag until the source measurement/collection protocol is resolved.
6. Do not split adjacent time points randomly. The entire trace remains held out as one operating condition.

## Primary metrics and admissibility checks

Report all values without dropping unfavorable intervals:

- Hot-outlet temperature MAE, RMSE, and bias.
- Cold-outlet temperature MAE, RMSE, and bias.
- Raw `mw` reading range, first/last values, monotonicity, negative-step count, and raw time series; no comparison to predicted cumulative mass until semantics are verified.
- Predicted outlet temperature range relative to the measured inlet/initial-outlet envelope.
- Whether predicted mass rate is nonnegative and accumulated mass monotonic.
- Residuals versus time and the time at which measured cumulative mass first becomes positive.
- Solver tolerance, input-knot integration method, time-grid sensitivity, and spatial cell count.

The model's cumulative-mass output may be reported as a model output only; it must not be compared with raw `mw` at this stage. The current exploratory mass-state quadrature is trapezoidal at measured input knots. Before treating mass predictions quantitatively, verify source measurement semantics and repeat the held-out calculation on a refined input/output grid.

## Interpretation policy

- This same-paper trace can establish operating-condition transfer only; it does not satisfy independent study-level validation.
- If the model fails a physical envelope, mass monotonicity, or source-data provenance check, record the failure and keep the gate false.
- If the model passes, report the errors and uncertainty; do not describe a pass as proof of universal transferability.
- No model parameter may be tuned on this trace and then reported as held-out performance.

