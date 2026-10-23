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
- [ ] Corrected workflow rerun and artifacts reviewed.
- [ ] Regression test added to prevent observed-outlet leakage from returning.
- [ ] Scientific validation gates reviewed using corrected artifacts.

Until the rerun is complete, do not quote the earlier held-out metrics as validation evidence.
