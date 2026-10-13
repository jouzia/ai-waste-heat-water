# Pre-registered Ali et al. (2020) S3/60 transient trace result

**Workflow:** [Ali preregistered held-out transient trace, run #7](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38437531397)  
**Code commit:** `8914f2aacb00303576ef0292994e287444879722`  
**Artifact:** `ali-2020-preregistered-heldout-S3-60C`, ID `11832963911`, SHA-256 `93236965af372e15bd3c8deb2c7fb6c1ec89548d54976f4ea0ef614f2c458593`; retained until 2027-01-11.  
**Source:** Ali, Orfi & Najib (2020), PLOS ONE, DOI 10.1371/journal.pone.0230207, CC BY 4.0.

## Frozen trace and protocol

- Workbook/worksheet: S3 Data, sheet `60`.
- Nominal circulation flow: 100 L/h.
- Nominal hot-inlet target: 60 °C.
- 1,068 complete timestamped observations over 177.83 min, sampled at approximately 10-second intervals.
- Measured inlet histories and measured initial outlet temperatures were used.
- The 10-cell spatial model was evaluated without fitting to this trace. The authors' published heat-loss correction (`f_los=0.20` for 100 L/h) is shown as a separate reproduction case, not a newly estimated coefficient.
- Raw `mw` observations are preserved but not used for cumulative-mass error metrics because their measurement/reset semantics remain unverified.

## Results

| Metric | No heat-loss correction | Published correction, not refitted |
|---|---:|---:|
| Hot-outlet temperature MAE | 1.358 °C | 1.545 °C |
| Hot-outlet temperature RMSE | 2.079 °C | 2.173 °C |
| Hot-outlet bias | −1.297 °C | −1.525 °C |
| Cold-outlet temperature MAE | 3.208 °C | 2.547 °C |
| Cold-outlet temperature RMSE | 3.323 °C | 2.643 °C |
| Cold-outlet bias | +3.070 °C | −2.546 °C |

The correction reduces cold-outlet RMSE by about 20.5% but worsens hot-outlet RMSE by about 4.5% and changes the cold-side bias sign. This is a model-form trade-off, not an across-output improvement. No mass-rate or accumulated-mass error is reported.

## Interpretation

This is a **pre-registered within-study held-out operating condition**, not independent external validation: the development and held-out traces are from the same paper and experimental plant. It is useful for checking transfer across operating conditions without refitting, but the temperature errors remain material and the correction does not improve both outlets simultaneously.

The source-reconstruction and held-out-validation gates remain **false**. The result does not establish a validated MD model or a net freshwater benefit. The raw mass-field semantics and the broader source-specific property/heat-transfer crosswalk remain unresolved.
