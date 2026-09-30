# Figure Digitization Protocol for Literature Validation

## Purpose

Recover experimental observations from published plots only when the source does not provide a machine-readable table. Digitized values are treated as measurements with extraction uncertainty, not exact source data.

## Required record

Each extracted point must record:

- source identifier;
- figure and panel;
- series/condition;
- x value and unit;
- y value and unit;
- pixel-to-axis calibration method;
- extraction tool/version;
- estimated digitization uncertainty;
- operator/date;
- whether the point is experimental, modeled, or a visual guide.

## Procedure

1. Preserve the original figure file or stable source reference.
2. Calibrate both axes using at least three known tick positions.
3. Extract experimental markers separately from fitted/model curves.
4. Do not digitize a smooth model line as experimental evidence.
5. Repeat a subset of points independently to estimate extraction variability.
6. Store raw pixel coordinates separately from converted physical values.
7. Keep the digitized dataset immutable once used in a benchmark.
8. Never silently round extracted values to create apparent agreement.

## Acceptance

Digitization is acceptable for exploratory reproduction when the source does not provide raw data. For a publication-grade validation claim, report that values were digitized and propagate the extraction uncertainty into the validation analysis.

## Keshavarzzadeh 2020 case

Figure 3 reports experimental markers and model curves for two inlet recirculation rates and four NaCl concentrations. The repository must extract only the experimental markers and preserve the panel/series mapping. No digitized point is currently represented as a validated observation in the repository.
