# Audit of the Ali–Orfi–Najib (2020) transient DCMD benchmark

Audit date: 2026-10-13

**Status update:** The five publisher XLSX files have now been downloaded, hashed, inspected, and extracted through the reproducible GitHub Actions workflow. See `docs/ALI_2020_SUPPORTING_DATA_AUDIT_2026-10-13.md` for the detailed counts, artifact locator, checksum, and quantitative tail-consistency diagnostics.

## Source and reuse

Ali, E., Orfi, J., & Najib, A. (2020). “Developing and validating a dynamic model of water production by direct-contact membrane distillation.” *PLOS ONE* 15(3), e0230207. DOI: https://doi.org/10.1371/journal.pone.0230207

The publisher labels the article open access under CC BY 4.0 and states that relevant data are in the article and Supporting Information. Five XLSX supplements are listed as S1 Data–S5 Data (DOIs ending in `s002` through `s006`). Retrieve the publisher files and record retrieval date, file hashes, sheet names, and units before extracting observations. Do not infer workbook contents from the labels alone.

## Source-confirmed experiment facts

- Pilot-scale spiral-wound counter-current DCMD module.
- Effective membrane area: 10 m²; membrane thickness: 230 μm; channel length: 14 m; channel height: 0.7 m; channel gap: 2 mm; pore diameter: 0.2 μm; porosity: 0.8; reported water-entry pressure: 4.1 bar.
- Equal hot- and cold-side flow rates were imposed by the test module.
- Flow rates considered: 50, 100, 200, and 300 L/h.
- Hot-feed temperature conditions span 50–80 °C; nominal cold-inlet temperature is 25 °C; reported feed salinity is 0.5%.
- The paper shows selected accumulated-mass experiments at 50 and 300 L/h; the 100 and 200 L/h responses are discussed but not shown in the same figures.
- Sampling interval: 10 s. Error bars represent uncertainty in accumulated mass estimated from standard deviation across repeated experiments under identical conditions.
- The cold inlet temperature fluctuated under manual control. The hot-side step response was not instantaneous because of external heater dynamics. Initial temperatures varied by approximately ±1–3 °C across tests.
- The paper reports that the uncorrected dynamic model had substantial model–plant mismatch. Its approximately 3% overall relative error is reported after adding a heat-loss correction whose tuning factors were selected by trial-and-error/heuristics. This result is not an independent benchmark for a new model and must not be copied as a prior or presented as unfitted validation.

## Observation hierarchy

1. **Primary measured series:** time, measured accumulated distillate mass, measured input histories, boundary temperatures, and repeat-run uncertainty, where present in the supplements.
2. **Source-transformed series:** production rates obtained by differentiating/smoothing mass or by dividing mass by time; record the exact operation and units.
3. **Source-fitted/extrapolated series:** straight-line mass accumulation fits and their extrapolated asymptotic rates; keep these separate from measurements.
4. **Published model outputs:** original paper's predicted curves and tuned cases; never label as observations.

## Required extraction sequence

1. Download all five publisher XLSX supplements; store immutable originals outside version control if file size/license practice requires it. Run `python scripts/inspect_ali_supplements.py --input-dir data/raw/ali_2020` to create a metadata-only manifest with file hashes and worksheet names. Record the retrieval URL and actual retrieval timestamp; the script's manifest creation timestamp is not a substitute for retrieval time.
2. Inspect every workbook and map each sheet to the paper's figures/tables and operating conditions. Do not assume S1 Data–S5 Data map one-to-one to the five operating flow rates.
3. Identify whether the workbook contains raw measured time series, processed rates, model predictions, or multiple categories. Preserve original values and add derived columns separately.
4. Reconstruct actual step-input histories and measured hot/cold boundary conditions. A nominal setpoint is not a substitute for a measured input trajectory.
5. Preserve repeated-run uncertainty and the stated 10 s sampling interval. Do not treat serial samples as independent replicates.
6. Freeze development/held-out operating conditions before calibration. A reasonable split must separate operating conditions, not randomly split adjacent points from the same transient trace.
7. Validate time-domain behavior separately from steady-state performance. Report at least accumulated-mass error, response-time/lag error, and rate error with the derivative/smoothing method stated. Include residual plots and uncertainty-aware intervals.
8. Treat the source's tuned heat-loss correction as a model-form hypothesis only. If estimated, fit it on development conditions and report held-out performance without re-tuning.

## Current status

**Source-linked extraction is complete; model validation remains pending.** The five publisher XLSX supplements are stored in a 90-day workflow artifact with checksums. The raw ledger contains 17,430 nonempty source rows; the structured extraction contains 17,385 transient records, of which 16,837 have complete timestamps, plus 16 steady-state observations and 34 tail-slope consistency diagnostics. 548 temperature-only rows without timestamps and two invalid steady-state rows are explicitly flagged/excluded from the relevant analyses. See `docs/ALI_2020_SUPPORTING_DATA_AUDIT_2026-10-13.md`.

The repository's current main MD model is not dynamically coupled to this transient dataset. No transient validation, source-parameter fitting, or independent validation claim is made. The repository's time-resolved workload module is currently only a tested integration primitive; it is not yet a dynamically coupled, experimentally validated MD system.


## New model-form diagnostic and transient admissibility finding (2026-10-13)

The source-linked S1 steady-state ledger drives a train/held-out-flow flux-law comparison. Training uses nominal 50, 100, and 200 L/h; the entire 300 L/h flow is held out. Fixed TPC=0.8 underpredicts the held-out flux strongly (MAE 0.828, RMSE 0.861 kg m⁻² h⁻¹). A three-parameter flow-dependent TPC alternative reduces held-out error (MAE 0.181, RMSE 0.214 under the stated 0.5% salinity interpretation), but it is a fitted within-source diagnostic and not independent validation. The TDS-proxy interpretation pushes fitted permeance to the configured upper bound, so salinity/property ambiguity remains material.

The separate transient reconstruction also exposed a physically inadmissible default 10 m², 50 L/h trajectory: the numerical solver returned a hot outlet below the global inlet-temperature envelope. The model now rejects this trajectory rather than silently accepting it. This is evidence of an unresolved model-form/parameter mismatch; it is not a validation success. The source-reconstruction and held-out-validation gates remain false.


## Raw mass-field semantic restriction (2026-10-13)

The latest source-linked audit covers 19 complete timed worksheet traces, of which 14 have nonmonotonic raw `mw` readings. Prior tail-slope comparisons that assumed cumulative mass are withdrawn and disabled. No transient mass/flux error is valid until the `mw` measurement/reset semantics are established. The raw values remain preserved without reinterpretation.
