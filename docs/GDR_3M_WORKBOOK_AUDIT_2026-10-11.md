# GDR 3M DCMD workbook audit and extraction record

Audit date: 2026-10-11

## Source and provenance

- Dataset: Villa et al. (2018), *Membrane Specifications for Multi-Configuration Membrane Distillation Model*.
- DOI: https://doi.org/10.15121/1452747
- GDR source page: https://gdr.openei.org/submissions/1016
- Workbook: `3M 0.2 Micron Plate and Frame Countercurrent DCMD.xls`
- Source download URL: https://gdr.openei.org/files/1016/Countercurrent%20DCMD%203M%200.231m%5E2%201%20LPM%204g%20NaCl_08.11.2017.xls
- Licence: CC BY 4.0; attribute the dataset, link the licence, and state modifications.
- File size: 13,192,704 bytes.
- SHA-256: `5b80da45f991a8572a8a77372535cf0ba3dc40eb46a3c32c58e09e9d608dd8bb`
- Retrieval/inspection artifact: GitHub Actions artifact `gdr-villa-3m-countercurrent`, latest run ID `38425489743`, artifact ID `11828433138`, SHA-256 `0ad2b425c0238bfa7aed0bb6f25e837fa29381ea96c0cee747e49710bd3b30d2`, retained until 2026-10-27; contains the raw workbook, worksheet CSV exports, row-level observation ledger (631 rows), and manifests. The raw workbook and generated ledger are not committed to git; the extraction code and workflow are committed.
- Derived flux summary: `04_experiments/literature_benchmarks/MD-OEDI-VILLA-2018_3M_flux_summary.csv`.

## Workbook structure

The workbook contains 12 time-series sheets (`20-40`, `20-45`, `20-50`, `20-55`, `20-60`, `20-65`, `30-40`, `30-45`, `30-50`, `30-55`, `30-60`, `30-65`), plus `Specifications` and `Theoretical`. It does not contain a worksheet literally named `Data`, despite the GDR landing-page description of a general `Data` worksheet. The first number in each condition label is the nominal cold-side setpoint (20 or 30 °C); the second is the nominal hot-feed setpoint (40–65 °C). Use measured temperatures, not nominal labels, in model comparisons.

The `Specifications` worksheet identifies the membrane as 3M, model 0.2 micron, polypropylene, thickness 110 μm, membrane area 0.23088 m², channel length 1.04 m, width 0.222 m, and channel height 0.0018 m. It lists 85% porosity and a mean pore radius of 0.59 μm but marks those properties as not used in its calculation. The GDR page describes a nominal 1 L/min feed flow and 4 g/L NaCl.

## Row-level observation ledger

The workflow now exports `artifacts/gdr_villa_exports/observation_ledger.csv` with **631 rows across 12 condition sheets**. Each row records the source DOI, workbook name, workbook SHA-256, worksheet, one-based Excel row, runtime, cumulative distillate volume, measured inlet/outlet temperatures, and selected raw flow/sensor values. Raw non-finite flow values such as `Inf` are preserved as text and not repaired. The `Theoretical` worksheet is excluded. The artifact is reproducible from the public CC BY 4.0 source with `scripts/download_gdr_villa.py` and `scripts/extract_gdr_villa_observation_ledger.py`; the current artifact is temporary (14-day retention), so the source download and extraction scripts remain the durable provenance path.

## Extraction method

1. Downloaded the original workbook and recorded the SHA-256 checksum above.
2. Exported worksheets to CSV using `xlrd` for inspection; the original XLS remains the source of record.
3. For each temperature sheet, selected rows with numeric `Runtime (hr)` and `MD Distillate Volume [L]` in the first measurement block. The actual observations are cumulative volume and time; the workbook's precomputed flux fields were not treated as observations.
4. Fit ordinary least squares to cumulative distillate volume versus runtime over each worksheet's available time-series rows. Divided the fitted volume rate by 0.23088 m² to obtain a derived volumetric flux in L m⁻² h⁻¹.
5. Calculated a Newey–West/HAC slope standard error with a Bartlett kernel and lag (L=lfloor4(n/100)^{2/9}floor), bounded to the available sample. The approximate 95% interval in the summary CSV is a time-series regression interval only; it is **not** measurement uncertainty or replicate-to-replicate uncertainty.
6. Preserved worksheet row ranges, time span, cumulative-volume endpoints, actual average inlet/outlet temperatures, fit diagnostics, source checksum, and a separate cross-check against the `Theoretical` sheet.

## Recomputed ledger-to-summary consistency check

After the row-level artifact was generated, a separate calculation recomputed an ordinary-least-squares slope of cumulative distillate volume versus runtime for each of the 12 worksheets, divided by the documented 0.23088 m² membrane area, and compared the result with the committed condition-level summary. All 12 values matched to within **4.82 × 10⁻⁹ L m⁻² h⁻¹** absolute difference. This confirms arithmetic consistency between the row-level CSV and the summary extraction; it is not an independent measurement, replicate check, or model validation because both are derived from the same workbook.

## Findings and anomalies requiring explicit treatment

- The 12 worksheets contain 20–129 time points each, with zero nonzero alarm flags in the selected time-series rows.
- The cumulative-volume trends are close to linear ((R^2) approximately 0.985–0.999). Derived average fluxes range from about 2.14 to 10.53 L m⁻² h⁻¹ across the 12 nominal conditions.
- The OLS-derived flux matches the `Theoretical` worksheet's summary flux to the displayed precision for all 12 conditions. This shows that the summary value is derived from the same cumulative-volume trace; it is **not an independent observation** and must not be counted as a second validation point.
- The `Theoretical` worksheet's note identifies “CLARCOR QL822” while the workbook filename and `Specifications` worksheet identify a 3M polypropylene membrane. Treat the Theoretical-sheet manufacturer note as a provenance conflict; use the source landing page and Specifications sheet for the provisional membrane identity, and do not use the conflicting note as a model input.
- The time-series sheets include a note such as `20C/40C 0.4LMH`, a `Flux (LMH)` column that is constant at 42.0, and an `MD Water Flux [LMH]` column with near-zero signed values. These do not agree with the cumulative-volume-derived flux and are excluded from the observation target. Do not “correct” them by inserting a decimal point or assuming a unit conversion.
- Several recorded flow channels show negative values or `Inf`, unlike the nominal 1 L/min specification. Do not use those channels as validated flow rates until their sensor/sign convention and provenance are resolved. Use nominal flow only as a documented provisional boundary condition and include it in sensitivity analysis.
- The `Theoretical` worksheet contains calculated values and stale/conflicting labels. It is retained only as a processing cross-check, not as raw data.

## Validation status

**Primary time-series observations have been extracted for 12 candidate operating conditions.** This advances data availability but does not yet constitute model validation. Before using these cases quantitatively, the model must be configured with the correct membrane properties, flow arrangement, measured boundary temperatures, and defensible channel heat-transfer coefficients. Freeze a development/held-out split by operating condition before fitting. The two cold-side setpoint groups (20 °C and 30 °C) are a candidate split, not yet a formally frozen validation design.

The raw workbook and the derived summary are CC BY 4.0 material; the summary is a transformed extraction. Cite Villa et al. (2018), preserve the source checksum, and identify the regression/uncertainty transformations.
