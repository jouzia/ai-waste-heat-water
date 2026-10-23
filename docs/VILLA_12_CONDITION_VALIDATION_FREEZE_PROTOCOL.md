# Villa et al. 12-condition benchmark: validation freeze protocol

## Purpose and current status

This protocol defines the next executable validation pass using the public Villa et al. (2018) GDR dataset, DOI 10.15121/1452747. The dataset provides configuration-specific workbooks and raw data sheets; the repository has exported 12 nominal temperature-condition sheets for one 3M counter-current DCMD workbook. The source landing page confirms that the workbook's “Data” sheet contains the data and the “Theoretical” sheet contains both steady-state experimental-run values and calculated values.

Source: https://gdr.openei.org/submissions/1016

**Status: protocol specified; execution and numerical results are not asserted by this document.**

## Why the benchmark is not yet a clean validation result

The repository's prior audit identifies the following risks that must be resolved before calculating or interpreting a validation score:

- The workbook's “Theoretical” sheet carries a CLARCOR label inconsistent with the selected 3M workbook.
- The reported Flux (LMH) column is constant at 42.0, and signed MD Water Flux values are near zero; neither should be treated as observed flux without source clarification.
- Some flow channels contain negative or infinite values.
- The derived 12-condition flux summary matches an OLS transform of cumulative distillate volume, so it is a processing cross-check, not an independent measurement.
- Cumulative volume/time, effective membrane area, timing interval, and temperature-channel mapping must be verified from the workbook and its specifications before fitting or scoring.

These are provenance and measurement-semantics issues, not mere software failures.

## Freeze rules

Before looking at the final held-out metrics:

1. Freeze the source workbook SHA-256, sheet names, cell ranges, units, and extraction script revision in a run manifest.
2. Use raw cumulative distillate volume and elapsed time only if their measurement semantics are confirmed from the source workbook. Do not use workbook-calculated flux as a substitute for the raw data.
3. Derive a flux only with a source-backed active membrane area and a documented time basis. Keep the original cumulative observations and all derived values side by side.
4. Record each of the 12 conditions by its actual nominal hot/cold temperature settings and preserve observed inlet/outlet temperatures separately from nominal set points.
5. Choose the held-out conditions or grouping rule before fitting. Never choose the split based on which model performs best.
6. Fit model parameters only on training conditions. Do not recalibrate against held-out observations.
7. Report per-condition signed bias, MAE, RMSE, sample count, and any invalid/omitted observations. Include pooled metrics only alongside condition-level results.
8. Compare every predeclared model form on the exact same observations and split. Report model ranking changes, not just the best score.
9. Propagate model-form spread through gross MD water production and the break-even calculation. Do not infer a positive net-water benefit from a flux fit alone.
10. If source channel semantics or boundary conditions cannot be resolved, mark the affected condition ineligible and report the exclusion rule. Do not silently repair, interpolate, or relabel source data.

## Required outputs for a validation run

A successful run should create a frozen manifest plus machine-readable predictions containing, at minimum:

- dataset_id, source_sha256, condition_id, split, observed_channel, observed_value, observed_unit
- predicted_value, predicted_unit, model_id, model_version, fit_parameter_source
- validity_flag, exclusion_reason, residual, absolute_error, and squared_error
- the source workbook sheet/cell or exported-row locator for every observation

The run must fail closed if a condition has no provenance locator, if observed and predicted units differ, or if a held-out observation contributes to parameter fitting.

## Reporting language

Until the freeze rules are executed and the results reviewed, describe the 12-condition benchmark as a **candidate source-matched validation dataset under audit**, not as successful validation. A held-out split within this one workbook is internal validation; it is not independent external validation.

Even after execution, passing this benchmark does not close the primary 1999 source-reconstruction gate, the independent-validation gate, the geographic integration gate, or the final publication gate.

## Acceptance checklist

- [ ] Source workbook hash and license recorded.
- [ ] Data sheet, theoretical sheet, and specifications cross-walked.
- [ ] Measurement channels and units verified.
- [ ] Active membrane area and flux calculation verified.
- [ ] 12 conditions have provenance locators and eligibility flags.
- [ ] Holdout split frozen before fitting.
- [ ] Unfitted predictions and condition-level residuals archived.
- [ ] Model-form comparison uses identical held-out rows.
- [ ] Downstream water and break-even sensitivity generated from frozen predictions.
- [ ] Run passes automated provenance, unit, and split-leakage checks.
