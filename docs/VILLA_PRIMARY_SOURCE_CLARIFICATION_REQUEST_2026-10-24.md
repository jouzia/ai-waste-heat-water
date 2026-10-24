# Primary-source clarification request: Villa et al. DCMD workbook

Date prepared: 2026-10-24

## Purpose

This request lists the minimum primary-source evidence needed to determine whether the Villa et al. (2018) workbook can support a defensible transport-model validation exercise. It is a request template, not evidence that the questions have been answered. Until documentary responses are archived, the corresponding provenance issues remain unresolved.

Dataset landing page: https://gdr.openei.org/submissions/1016  
Dataset DOI: 10.15121/1452747  
Workbook audited: `3M 0.2 Micron Plate and Frame Countercurrent DCMD.xls`  
Audited workbook SHA-256: `5b80da45f991a8572a8a77372535cf0ba3dc40eb46a3c32c58e09e9d608dd8bb`

## Questions requiring primary-source answers

### A. Device and membrane identity

1. Was the experimental module the 3M 0.2-micron polypropylene plate-and-frame membrane named in the workbook filename and Specifications sheet, or the CLARCOR QL822 module named in the Theoretical worksheet narrative?
2. If the Theoretical worksheet was copied from another module or study, which cells/columns are original measurements for this workbook and which are transferred or calculated values?
3. Please provide the module model, membrane material, nominal pore rating, and membrane lot or part number if available.

**Evidence requested:** original instrument/test report, workbook provenance note, manufacturer datasheet, or a source-author clarification that explicitly identifies the relevant workbook and worksheet.

### B. Active membrane area and geometry

4. Is 0.23088 m² the installed effective active membrane area for the reported tests, or only the nominal sheet area? Does it account for gaskets, seals, masked edges, or inactive area?
5. Are the listed channel dimensions, spacer dimensions, filament diameter, porosity, and hydraulic diameters the as-tested geometry? Which hydraulic-diameter convention was used in the original calculations?
6. Is the 0.231 m² value in the Theoretical worksheet merely a rounded form of 0.23088 m², or does it refer to a different module?

**Evidence requested:** dimensioned module drawing, active-area calculation, test configuration record, or explicit source documentation. Keep the 0.23088 m² value labelled as workbook-nominal until confirmed.

### C. Flow channels, signs, and units

7. For each column below, what physical stream and sensor does it represent, and what is the sign convention?
   - MD Feed Flowrate (High) [LPM]
   - MD Distillate Flowrate (High) [LPM]
   - MD Feed Flowrate (Low) [LPM]
   - MD Distillate Flowrate (Low) [LPM]
   - MD Heating Flowrate [LPM]
   - MD Cooling Flowrate [LPM]
8. Why are all finite MD Feed Flowrate (High) observations negative, all finite MD Cooling Flowrate observations negative, and both MD-side “Low” columns non-finite (`Inf`) in the retained trace rows?
9. Do these fields represent signed instrument readings, controller setpoints, differences from a reference, or exported/calculated values? Were any sign inversions or unit conversions applied during export?
10. What are the instrument make/model, range, calibration status, and sensor placement for each flow channel?

**Evidence requested:** instrument/channel map, original logger export, sensor manual or calibration record, and an explanation of the negative and `Inf` values. Do not take absolute values, impute missing values, or fit a flow-dependent model to these channels until resolved.

### D. Temperature channels and boundary conditions

11. Please map each MD and preheater (PH) inlet/outlet temperature column to the physical sensor location and stream.
12. Which values are controller setpoints, which are measured temperatures, and which are calculated values?
13. The first metadata row repeats “20C/40C 0.4LMH” across sheets whose names indicate different temperature conditions. Which source field is authoritative for each condition's nominal setpoints, and what does “0.4LMH” denote in that metadata row?

**Evidence requested:** logger channel map, test protocol, or contemporaneous test sheet. Preserve nominal condition labels and measured channels separately in the meantime.

### E. Distillate volume, elapsed time, and flux

14. What do the cumulative distillate volume and runtime fields represent, including units, sampling interval, time origin, resets, and any corrections?
15. Is the workbook's constant “Flux (LMH)” value of 42.0 a setpoint, a nominal value, or an observed measurement? What is the provenance of the signed MD Water Flux field?
16. Was the “Theoretical” sheet flux calculated from cumulative volume versus time, and if so, which area and time interval were used?
17. Are raw volume/time measurements available independently of the workbook-derived flux values?

**Evidence requested:** original logger data, calculation workbook or formulas, units, timing protocol, and a documented flux equation. The OLS slope derived from cumulative distillate volume versus runtime is a processing cross-check, not an independent measurement.

## Minimum closure package

For every answer, archive the response with its date, author/source, exact document filename or URL, relevant page/sheet/cell locator, and SHA-256 where applicable. Distinguish directly documented facts from recollection or inference. A verbal answer without a traceable source can guide follow-up but should not by itself be treated as independent verification.

Recommended machine-readable response fields:

`question_id`, `answer`, `evidence_type`, `evidence_locator`, `source_date`, `source_sha256`, `reviewer`, `status`, `remaining_uncertainty`.

## Decision rules after response

- If device identity, active area, or volume/time semantics remain unresolved, do not call derived flux an independently verified observed target.
- If flow sign conventions and channel mappings remain unresolved, keep MD-side flow unknown/nominal and do not silently repair signs or substitute absolute magnitudes.
- If outlet temperature measurements are used to tune properties, transfer coefficients, or prediction conversions, the evaluation is not an unfitted held-out prediction. The corrected no-target-leakage implementation and regression tests must remain in place.
- A split across conditions from this same workbook is internal validation only. It cannot close independent validation or source reconstruction.
- Do not make a positive net-water-benefit claim from this benchmark alone. Keep the publication and validation gates open until the necessary evidence and reproducible artifacts exist.

## Current disposition

This request does not resolve any of the above issues. It turns the existing provenance audit into a concrete evidence request. Current model-comparison metrics remain diagnostic, and scenario sensitivity results remain conditional model outputs rather than field predictions.
