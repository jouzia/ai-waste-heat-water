# Evidence integration update — 2026-10-02

## Purpose

This update freezes two externally verified evidence tracks that materially affect the research design:

1. DOE guidance establishes that data-center heat reuse is temperature-quality dependent and can reduce cooling-tower heat rejection and associated water use when recovered heat displaces a cooling burden.
2. The Villa et al. (2018) NREL/OEDI membrane-distillation dataset is publicly accessible and the associated catalog metadata identifies a CC BY licence, resolving the repository's earlier licence-status uncertainty.

## DOE data-center heat-reuse evidence

The U.S. Department of Energy's *Best Practices Guide for Energy-Efficient Data Center Design* states that higher server-exit air/water temperatures improve waste-heat reuse opportunities, and identifies temperature level and proximity to a heat host as important conditions. It also notes that heat reuse can reduce or eliminate some chiller/cooling-tower operation when the recovered heat is actually useful to a host.

Research consequence:

- Do not model waste heat as an undifferentiated energy quantity.
- Preserve source-temperature distributions and heat-reuse availability.
- Treat avoided cooling as a counterfactual, not an automatic credit.
- Keep a redundant heat-rejection path in the integrated scenario because the heat host may be unavailable.
- Report direct cooling-water effects separately from electricity-related water effects.

A DOE FEMP data-center cooling-water resource also defines WUE as site water use per IT electricity and describes cooling-tower evaporation and blowdown as important water-demand mechanisms.

## Villa et al. 2018 open dataset

Official NREL/OEDI/GDR record:

- DOI: 10.15121/1452747
- Dataset: *Membrane Specifications for Multi-Configuration Membrane Distillation Model*
- Seven XLS/XLSX workbooks
- Configurations include flat-sheet and spiral-wound DCMD plus AGMD, with multiple manufacturers and flow configurations.
- The official record identifies the dataset as publicly accessible.
- The U.S. data.gov catalogue mirror identifies the licence as CC BY.

The official dataset record states that the workbooks distinguish "theoretical", "Specifications", and "Data" worksheets. This is important for validation because calculated/theoretical columns must not be silently treated as measured observations.

Research consequence:

- The dataset is now eligible for controlled extraction into the validation pipeline.
- Raw workbooks should remain external unless redistribution terms for the exact files are independently verified.
- The repository should store metadata, checksums, extraction code, and derived observation tables with source attribution.
- Measured observations, source-calculated values, and model predictions must remain separate.
- Development/held-out configuration splits must be frozen before calibration.

## Ali et al. 2020 transient dataset

The PLOS ONE article is CC BY 4.0 and explicitly provides five XLSX supporting-data files. The experiment uses a 10 m² spiral-wound DCMD module with 10 s sampling and records accumulated distillate mass during stepped operating conditions.

The paper reports that its unmodified dynamic models showed substantial model–plant mismatch and that adding a heat-loss term reduced the reported overall relative error to approximately 3%. This is source-reported evidence of model-form sensitivity, not validation of this repository's model.

Research consequence:

- The transient dataset is retained as a separate validation track.
- Measured accumulated mass must be used as the primary observation.
- Extrapolated steady-state correlations and source-model predictions must not be mixed with measurements.
- A dynamic model is required before this track can become a quantitative validation result.

## Evidence status after this update

The research remains incomplete until the raw observations are extracted, independently checked, and passed through unfitted and held-out validation. No quantitative validation claim is promoted by this document.
