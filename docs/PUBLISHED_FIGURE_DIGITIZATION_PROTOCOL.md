# Published-figure digitization protocol (fallback only)

Status: protocol defined; no figure points have been digitized or promoted to observations.

## Why this route exists

Ali, Orfi & Najib (2020) report that the relevant experimental data are in the manuscript and Supporting Information. The publisher/PMC record lists five XLSX supporting datasets. Original workbooks remain the preferred source. Figure digitization is a documented fallback only when the underlying numeric series cannot be recovered, and it must never be presented as equivalent to original instrument/workbook data.

Source: Ali E, Orfi J, Najib A (2020), *PLOS ONE* 15(3):e0230207. DOI: https://doi.org/10.1371/journal.pone.0230207. Article: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207. The article is CC BY 4.0; retain attribution and the source figure identifier.

## Eligibility decision

Before digitizing, record an acquisition attempt for each relevant supporting workbook, including URL, retrieval date, HTTP/tool outcome, and reason the numeric data could not be obtained. Do not infer a failed download from an untried URL. If original data become available later, replace the digitized benchmark with original data and preserve the old record for provenance.

Only digitize a figure when all of these are true:
- The plotted variable and its units are legible.
- Axis scale, bounds, and tick labels can be calibrated unambiguously.
- The relevant experimental condition and series can be mapped to the paper's condition description.
- Points are visually separable enough to support a stated extraction uncertainty.
- A second person or a second independent pass can check a subset or all extracted points.

If any condition fails, classify the figure as qualitative-only and exclude it from numerical validation.

## Extraction procedure

1. Download the publisher-hosted figure at the highest available resolution. Preserve the unmodified file and calculate its SHA-256.
2. Record the article DOI, figure/panel identifier, image URL, image hash, licence/attribution, and the digitization software/version.
3. Calibrate each axis independently using at least two labelled ticks per axis; use three or more where practical. Explicitly record linear versus logarithmic scale.
4. Extract points by series. Preserve the source's plotted sampling and do not interpolate extra points to create apparent temporal resolution.
5. Store the raw digitizer output unchanged. Any unit conversion, time-zero alignment, smoothing, resampling, or derived flux calculation must be a separate transformation with code and a new output.
6. Estimate coordinate-reading uncertainty from marker/line thickness, pixel resolution, calibration residuals, and repeat extraction. Report the method; do not claim instrument measurement uncertainty from pixel uncertainty.
7. Perform a second independent extraction for at least 20% of points, including transient regions, peaks/steps, and steady state. If the series is small, double-extract every point. Report maximum and median disagreement in data units.
8. Keep digitized points in a separate dataset namespace and label every record `evidence_type=figure_digitization`. Never merge them invisibly with raw workbook observations.
9. Hash the raw figure, digitized CSV, and transformation script. Record the source commit and random seed for any later uncertainty propagation.

## Minimum observation ledger fields

Use `02_data/derived/digitized_points_template.csv` as a blank header template. Required metadata include:
- source DOI and figure/panel;
- source image URL and SHA-256;
- series/condition identifier;
- digitized x and y with units;
- axis scale and calibration bounds;
- estimated x/y digitization uncertainty;
- extractor, software/version, and extraction date;
- independent-check method and disagreement;
- inclusion status and exclusion reason;
- evidence type and provenance notes.

A blank template is not data and must not be counted as an extracted observation.

## Validation and reporting restrictions

- Figure-digitized data are secondary measurements derived from a published visualization. They are not original experimental rows.
- Do not tune parameters on a digitized series and then report fit to that same series as independent validation.
- If a digitized curve is used for exploratory model checking, report it separately from workbook-derived validation and perform sensitivity analysis to digitization uncertainty.
- Do not compute strong precision metrics from points sampled from a plotted line unless the extraction uncertainty and serial dependence are acknowledged. Dense digitized points are not independent replicates.
- If a plotted line represents a fitted/correlated response rather than raw measurements, label it as such and do not call its digitized points experimental observations.
- A figure-level extraction must not be used to reconstruct omitted values, missing operating conditions, or unreported uncertainty.
- Preserve negative or poor model performance; do not select only visually favourable segments.

## Acceptance checklist

A digitized series is eligible for exploratory comparison only when:
- [ ] source image and hash are archived;
- [ ] figure/panel, axes, units, scale, and series identity are documented;
- [ ] calibration is reproducible;
- [ ] point-level uncertainty is recorded;
- [ ] independent re-extraction/check is complete;
- [ ] data and transformations are separately versioned;
- [ ] it is explicitly excluded from claims of raw-data or independent experimental validation.

Even after acceptance, this fallback does not by itself satisfy the primary-observation-extraction or unfitted-validation gates. Those gates require a source-appropriate validation design and documented evidence review.
