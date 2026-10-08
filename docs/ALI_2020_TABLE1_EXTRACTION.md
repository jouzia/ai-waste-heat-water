# Ali, Orfi & Najib (2020): Table 1 transcription record

## Purpose and status

This file records values transcribed from **Table 1** of the source article, *Developing and validating a dynamic model of water production by direct-contact membrane distillation*, PLOS ONE 15(3), e0230207 (2020), DOI: [10.1371/journal.pone.0230207](https://doi.org/10.1371/journal.pone.0230207).

This is a **secondary transcription of author-reported model–plant relative errors**, not raw experimental observations and not an independent replication. The values can be used to document the source's reported model-form/calibration behavior. They must not be treated as validation results for this repository's model.

## Source and license

- Article: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207
- Table: Table 1, printed article page 10 (PDF page 10 in the uploaded article copy).
- Article license: Creative Commons Attribution 4.0 International (CC BY 4.0); cite the original authors and article when reusing.
- Transcription basis: the table's printed values, manually transcribed and checked against the accessible article page image.

## Columns

- `relative_error_percent_lumped_without_tuning`: source-reported error for the lumped model without tuning.
- `relative_error_percent_spatial_without_tuning`: source-reported error for the spatial model without tuning.
- `relative_error_percent_lumped_with_tuning`: source-reported error for the lumped model with tuning.
- `relative_error_percent_spatial_with_tuning`: source-reported error for the spatial model with tuning.
- `relative_error_percent_lumped_without_tuning_terminal_temperature`: source-reported error for the lumped model without tuning when terminal temperatures are used as approximations of bulk temperature.

The paper reports these values as percentage relative errors of model–plant mismatch. The `NA` flow rate on the overall row means the source reports an overall mean across flow rates, not a physical operating condition.

## Source-reported values

| Flow rate (L/h) | Lumped, no tuning (%) | Spatial, no tuning (%) | Lumped, tuned (%) | Spatial, tuned (%) | Lumped, no tuning with terminal-temperature approximation (%) |
|---:|---:|---:|---:|---:|---:|
| 50 | 7.78 | 14.00 | 3.08 | 3.04 | 49.08 |
| 100 | 10.01 | 15.97 | 3.78 | 2.90 | 46.46 |
| 200 | 9.31 | 18.92 | 3.29 | 3.54 | 53.19 |
| 300 | 16.99 | 25.19 | 2.71 | 3.51 | 56.51 |
| Overall mean | 11.02 | 18.52 | 3.22 | 3.25 | 51.31 |

## Interpretation limits

1. The tuned values reflect the original paper's own tuning/calibration procedure. They are not out-of-sample performance.
2. These aggregate errors do not supply time-indexed measured outlet temperatures or distillate-production observations, complete boundary conditions, or experimental uncertainty distributions.
3. The repository must not use these summary errors to fit its own model or claim experimental validation.
4. The five supporting XLSX files (S1 Data–S5 Data) remain the preferred source for the underlying data. Raw-workbook acquisition, hashing, sheet/range mapping, independent transcription, and held-out split are still required.
5. This transcription should be independently rechecked before inclusion in a publication-grade evidence package.

## Reproducibility

Machine-readable transcription: `01_literature/derived/ali_2020_table1_model_errors.csv`.

Extraction date: 2026-10-08. The original PDF is available in the current ChatGPT conversation upload; it has not been copied into the repository as raw source data.
