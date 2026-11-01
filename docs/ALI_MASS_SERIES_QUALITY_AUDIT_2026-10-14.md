# Ali et al. (2020) raw `mw` series quality audit

**Audit date:** 2026-10-14  
**Source:** Ali, Orfi & Najib (2020), *PLOS ONE* 15(3), e0230207, DOI [10.1371/journal.pone.0230207](https://doi.org/10.1371/journal.pone.0230207), CC BY 4.0.  
**Reproducible implementation:** `scripts/audit_ali_mass_series.py`; automated ingestion workflow `.github/workflows/ali-2020-ingest.yml`. The workflow passed as [run #25](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38594771813) on commit `023185044b9e6b1e72fe9304020de5038d604ba8`. Its 90-day source artifact is [artifact 11909251785](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38594771813), SHA-256 `26777e3037635d741f516aaa29d7ad1e40b61ba3449142ff9094546cb30899b2`, retained until 2027-01-12. The workflow verified 19 timed `mw` worksheets and 14 nonmonotonic traces without changing raw values.

## Question and scope

The supporting workbooks contain columns labelled `mw` or `mw (kg)`. The existing observation audit found that this raw field is nonmonotonic in 14 of 19 complete timed worksheets. This audit quantifies the raw signed increments; it does **not** infer whether every value is a cumulative collected-mass reading, a noisy balance output, or another source-defined quantity. No smoothing, monotonic correction, reset repair, unit conversion, or model fitting is performed.

The article discusses accumulated distillate mass and repeated-run uncertainty, but a column label alone does not establish exact workbook measurement semantics or the instrument processing chain. Raw values therefore remain preserved verbatim and source-linked.

## Metrics

For each timed worksheet, the script reports:

- Number of finite readings and first/last/minimum/maximum raw value.
- Net change from first to last reading.
- Count and fraction of negative adjacent increments.
- Total negative variation, defined as the sum of the magnitudes of all negative adjacent increments.
- Total negative variation divided by the positive net change, when that net change is positive.
- Largest single negative increment and its magnitude relative to the positive net change.
- Original workbook SHA-256, worksheet name, raw header labels, Excel row range, and raw time range.
- Whether the time column is strictly increasing.

The ratio of negative variation to net change is a **diagnostic**, not a measurement uncertainty estimate. It may be inflated when the series is close to zero or has many small fluctuations. It must not be interpreted as a mass-error percentage without a justified measurement model.

## Local raw-workbook inspection

The initial audit of the publisher's five downloaded XLSX files found 19 timed worksheets with usable numeric time/`mw` pairs; 14 have at least one negative adjacent step and five are non-decreasing throughout the retained trace. Examples of nonmonotonic series include:

| Workbook / worksheet | Readings | Negative steps | Net change (kg) | Total negative variation / net change | Largest single drop / net change |
|---|---:|---:|---:|---:|---:|
| S2 / 40 | 1,722 | 113 | 1.7125 | 81.13% | 2.04% |
| S2 / 50 | 1,662 | 79 | 3.5013 | 24.16% | 0.87% |
| S2 / 55 | 454 | 22 | 1.1918 | 19.69% | 2.75% |
| S2 / 60 | 944 | 19 | 2.8694 | 6.39% | 0.68% |
| S2 / 70 | 932 | 9 | 2.3400 | 4.62% | 1.21% |
| S3 / 50 | 1,653 | 39 | 8.0832 | 4.10% | 0.32% |
| S3 / 60 | 1,068 | 9 | 8.0930 | 1.58% | 0.34% |
| S4 / 50 | 577 | 4 | 4.4651 | 0.49% | 0.42% |
| S5 / 50 | 879 | 1 | 14.7879 | 0.07% | 0.07% |

These values are an initial local reproduction from the source workbooks. The committed script and ingestion workflow are the durable reproducibility path; the workflow artifact supplies the machine-generated per-sheet report and manifest.

## Interpretation and restriction

The traces do not show a single uniform failure pattern. Some have many small negative steps relative to net accumulation; others have only one or a few. In the S2/50 trace, for example, the largest single drop is about 0.031 kg while the full-trace net change is about 3.50 kg, but the sum of all negative increments is larger because many negative steps accumulate. This pattern is compatible with measurement noise, but it is not enough to prove that interpretation.

Until the source's exact `mw` definition and measurement/processing procedure are confirmed:

1. Preserve the raw series and row locators.
2. Do not relabel the column as validated cumulative distillate mass in the analytical schema.
3. Do not compare predicted cumulative mass with `mw` as if both had identical semantics.
4. Do not use a smoothed or isotonic-adjusted series as a primary observation without a predeclared measurement model and sensitivity analysis.
5. Keep model-predicted mass accumulation separate from observed raw readings.
6. Treat this audit as data-quality evidence, not dynamic-model validation.

**Decision:** the source mass-field interpretation remains unresolved. The script improves reproducibility and quantifies the issue; it does not close the source-reconstruction or held-out-validation gate.
