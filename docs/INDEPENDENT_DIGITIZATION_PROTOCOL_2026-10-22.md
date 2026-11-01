# Independent digitization protocol — secondary MD benchmark Figure 3

**Prepared:** 2026-10-22  
**Purpose:** Define a reproducible independent extraction before any new points are collected.  
**Dataset status:** Protocol only; no independent extraction has yet been performed.

## Source and admissibility

Use Figure 3 from Keshavarzzadeh (2020), *Scientific Reports* 10, 16790, DOI 10.1038/s41598-020-73964-7, as a **secondary-source figure**. Do not relabel extracted points as direct observations from Martínez-Díez & Vázquez-González (1999). The primary paper's publisher page is available at https://www.sciencedirect.com/science/article/pii/S0376738898003494, but the full primary PDF/table has not yet been verified.

## Independent workflow

1. Start from the original open-access PDF and render a fresh crop of Figure 3 at high resolution. Do not use either existing point CSV, pixel-coordinate table, QA overlay, or marker list while placing points.
2. Record the PDF URL, retrieval date, page number, crop rectangle, raster dimensions, and SHA-256 of the exact crop used.
3. Use a fresh PlotDigitizer or WebPlotDigitizer project. The tool supports XY axis calibration, manual point selection, and CSV/project export: https://plotdigitizer.com/docs and https://www.automeris.io/docs/digitize/.
4. Calibrate each panel separately using the furthest clearly readable tick marks. Record the pixel coordinates and numerical values of all four calibration anchors (two x and two y anchors), axis scale type, calibration residuals, and screenshot/project file.
5. Extract **experimental symbols only**, never model curves. Keep panels separate. Use the caption's four concentrations (0, 0.55, 1.15, 1.67 mol/L) as candidate labels but mark each assignment as uncertain when symbol identity cannot be distinguished from the image.
6. Preserve raw pixel coordinates and raw tool-exported coordinates. Do not convert flux to SI until the axis multiplier is verified from the printed label and, ideally, the primary article.
7. Export one CSV per panel and save the native project file (including the image where supported). Record software name/version, operator, date, and all manual corrections.
8. Only after the independent extraction is frozen, compare it with the existing first-pass and color-assisted review CSVs. Do not move independent points to make them match previous files.

## Comparison report requirements

For each matched point, report:
- panel, assigned concentration, point order, original pixel x/y;
- calibrated temperature and flux in **plotted-axis units**;
- absolute difference from the prior review-pass temperature and plotted flux;
- whether the marker identity is ambiguous, overlapping, clipped, or hidden by a curve;
- a disposition: retain, re-inspect, or exclude with a stated visual reason.

Summarize mean absolute error, maximum absolute difference, and root-mean-square difference for temperature and plotted flux, stratified by panel and concentration. These are **digitization-agreement diagnostics**, not measurement error or model validation. Where point matching is ambiguous, report the ambiguity rather than forcing a match.

## Predeclared decision rules

- Do not pool or fit the digitized points if the series mapping or flux-axis multiplier is unresolved.
- Do not call the second extraction independent if the operator can see prior point locations during extraction.
- If an independent point differs from the review pass by more than 1.0 K or 0.15 plotted flux units, flag it for visual adjudication; do not automatically replace either point.
- A consensus value may be created only after documenting both original values and the reason for adjudication. Keep the two raw extracts immutable.
- The figure is secondary-source-derived, so even a successful repeat does not satisfy primary-source reconstruction or independent physical validation.

## Required outputs

- Independent digitization CSV (raw and calibrated values; plotted flux only)
- Native project file
- Digitization metadata YAML
- Digitization agreement report
- SHA-256 manifest for crop, project, and CSV
- Updated gate assessment that remains INCOMPLETE unless all other scientific gates have independently passed

## Known open issues

1. Figure 3 caption cites a different reference from the validation paragraph for the experimental symbols.
2. The secondary paper's “0.2 mm” pore-size text conflicts with indexed primary-source text indicating 0.2 μm; this remains provisional pending direct primary-PDF verification.
3. The vertical-axis multiplier appears to imply plotted flux units of 10^-3 kg m^-2 s^-1, but conversion remains unverified.
4. Symbols near 0.55 and 1.15 mol/L overlap; uncertainty must be retained in the data model.

## Status

**Not executed.** This document defines a clean independent procedure; it is not evidence that a new extraction has occurred.
