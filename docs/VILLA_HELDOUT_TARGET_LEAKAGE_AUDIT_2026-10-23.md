# Villa 3M validation audit: observed-outlet leakage

Date: 2026-10-23

## Finding

A code review of `scripts/validate_gdr_3m.py` found that the nominally held-out prediction path used the observed outlet temperatures in three ways:

1. It averaged observed inlet and outlet temperatures to select water properties.
2. Those properties determined heat-transfer coefficients and mass-flow conversions in the model configuration.
3. It used the observed permeate outlet temperature to convert predicted mass flux to volumetric flux.

The outlet temperatures are measured response variables, not permitted prediction-time inputs for an unfitted held-out condition. This is target leakage. The previously recorded four-way Villa model-form comparison is therefore not eligible to support a clean held-out predictive-performance claim. Its numerical metrics must be treated as superseded pending a rerun; this does not establish that the corrected model will perform better or worse.

## Correction committed

Commit: `ef9255faf6723eae4cd6e2a7e0516841b9459dbe`

The prediction path now:
- computes properties and heat-transfer coefficients using measured inlet temperatures only;
- converts predicted mass flux to volumetric flux using the model-predicted mean permeate temperature, not the observed outlet temperature.

Observed outlet temperatures remain available for post-prediction residual reporting only. This correction removes the identified direct outlet-target path, but does not resolve all benchmark limitations.

## Required rerun and remaining limits

Rerun the existing GDR model-validation workflow and archive the new prediction/metric artifacts. Compare the corrected metrics against the previous run as a diagnostic only; do not pool them. Inspect solver failures, parameter-boundary fits, and per-condition residuals for all four predeclared model forms.

The benchmark remains within-workbook validation. The target flux is an OLS slope derived from cumulative distillate volume and is not an independent measurement from the workbook's theoretical flux column. Nominal flow and membrane/geometry assumptions remain uncertain. The source workbook's 3M identity and the CLARCOR label in the Theoretical sheet must remain explicitly documented. This finding does not close source reconstruction, independent validation, geographic integration, or publication gates.

## Status

- [x] Code path corrected for the identified observed-outlet leakage.
- [ ] Corrected workflow rerun and artifacts reviewed. The GDR ingestion workflow now runs the targeted regression tests and corrected four-form comparison, then uploads generated artifacts. This environment could not independently query the resulting GitHub Actions run status.
- [x] Regression tests added in `tests/test_villa_prediction_no_target_leakage.py` for inlet-only property selection and prediction-temperature flux conversion.
- [ ] Scientific validation gates reviewed using corrected artifacts.

Until the corrected rerun is complete, do not quote the earlier held-out metrics as validation evidence.


## Corrected rerun and permeance-identifiability result (2026-10-23)

The corrected model comparison was rerun after the leakage fix and after expanding the permeance grid from 0.01–1,000 to 0.01–10,000 kg m⁻² h⁻¹ bar⁻¹. Both artifact-producing workflows completed successfully on commit `867cb9f84fae85f677fb773901a29291dbea8f49`:

- [GDR DCMD model validation run #13](https://github.com/jouzia/ai-waste-heat-water/actions/runs/39981537582), artifact `gdr-model-validation`, SHA-256 `5027bd89ee9724b074f1dc23bb1ed4129c619bd7600e8e746df7dcc0071f31fa`.
- [GDR DCMD source-data ingestion](https://github.com/jouzia/ai-waste-heat-water/actions/runs/39981537413), artifact `gdr-villa-3m-countercurrent`, SHA-256 `e5b6b7338d4281d9df0c91c2e1634d154336b501745445d32be2cd6c1ab6d344`.

Both artifacts include `permeance_objective_profile.csv`. The ingestion artifact's 20-cell comparison and the dedicated 16-cell comparison give the same qualitative result: both Graetz–Lévêque forms remain at the upper bound, while both WaterTAP forms have an interior grid minimum at 562.34 kg m⁻² h⁻¹ bar⁻¹. This agreement across these two discretizations is a useful numerical robustness check, but it is not physical validation.

### Corrected 20-cell comparison

| Model form | Fitted permeance (kg m⁻² h⁻¹ bar⁻¹) | Boundary hit? | Held-out MAE (L m⁻² h⁻¹) | Held-out RMSE | Held-out MAPE |
|---|---:|:---:|---:|---:|---:|
| Graetz–Lévêque + smooth channel | 10,000 | Yes | 0.5844 | 0.7063 | 13.14% |
| Graetz–Lévêque + spacer porosity | 10,000 | Yes | 0.3869 | 0.5004 | 11.11% |
| WaterTAP + smooth channel | 562.34 | No | 0.3006 | 0.3976 | 10.63% |
| WaterTAP + spacer porosity | 562.34 | No | 0.5106 | 0.5830 | 14.30% |

### Objective-profile interpretation

For Graetz–Lévêque + smooth channel, the training objective falls from 0.08891 at 5,623 to 0.06419 at 10,000. For Graetz–Lévêque + spacer porosity, it falls from 0.02133 to 0.01762 over the same interval. Neither profile has an interior minimum in the searched range. The permeance parameter is therefore **not identified by this grid for either Graetz–Lévêque form**; the reported 10,000 value is a search-bound artifact and must not be described as a reliable physical estimate.

For WaterTAP + smooth channel, the grid objective reaches 0.03790 at 562.34, then increases to 0.06809 at 1,000 and continues increasing toward the upper bound. For WaterTAP + spacer porosity, it reaches 0.00962 at 562.34 and then increases to 0.14982 at 1,000 and 1.06956 at 10,000. These are interior minima on the coarse grid, not confidence intervals or proof that the physical membrane permeance is independently identifiable. The search spacing is 0.25 decades; any refinement must be predeclared and should not be used to tune against held-out conditions.

The dedicated 16-cell run gives held-out MAE/RMSE/MAPE of 0.5631/0.6856/12.83% for Graetz–Lévêque smooth, 0.3829/0.4941/11.18% for Graetz–Lévêque spacer porosity, 0.3185/0.4191/10.99% for WaterTAP smooth, and 0.5522/0.6245/15.02% for WaterTAP spacer porosity. The best-ranked variant changes slightly with discretization, reinforcing that this is a diagnostic comparison rather than a validated winner.

### Decision and follow-up

- Do not widen the permeance upper bound again as a purported fix.
- Keep both Graetz–Lévêque estimates explicitly flagged as boundary-limited and unresolved.
- Treat the WaterTAP permeance values as model-conditional fitted parameters, not independently measured membrane properties.
- Next prioritize source-level geometry/flow provenance, sensitivity to the assumed membrane conductivity and flow, and independent source-matched validation. Keep the six-condition same-workbook split labelled as internal held-out-condition evaluation.
- The successful reruns close the specific corrected-rerun/artifact-review task, but they do not close independent validation, source reconstruction, geographic integration, or publication-readiness gates.

## Status update

- [x] Corrected workflow rerun and artifacts reviewed.
- [x] Permeance objective profiles exported and interpreted.
- [x] Corrected 16-cell and 20-cell runs compared qualitatively.
- [ ] Scientific validation gates reviewed using independent evidence.
