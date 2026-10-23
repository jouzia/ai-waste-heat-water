# Villa 3M workbook: geometry and flow-channel provenance audit

Date: 2026-10-23

## Scope

This is a source-level audit of the workbook exported from the public NREL Geothermal Data Repository submission (DOI [10.15121/1452747](https://gdr.openei.org/submissions/1016)). It does not infer missing sensor semantics or treat spreadsheet specifications as independently verified manufacturer data.

Workbook filename: `3M 0.2 Micron Plate and Frame Countercurrent DCMD.xls`  
SHA-256: `5b80da45f991a8572a8a77372535cf0ba3dc40eb46a3c32c58e09e9d608dd8bb`  
Raw trace sheets: 12 nominal conditions; extracted ledger: 631 rows.

## Findings

### 1. Geometry and active membrane area

The Specifications sheet states: membrane area 0.23088 m²; channel length 1.04 m; channel width 0.222 m; channel height 0.0018 m; spacer length/width/height 1.04/0.222/0.0018 m; mesh length/width 0.016/0.0108 m; filament diameter 0.0009 m; spacer porosity 0.9210; hydraulic diameter 0.003571 m when neglecting the spacer and 0.002520 m using the porosity method. The first condition sheet independently displays 0.23088 m², while the Theoretical sheet narrative says 0.231 m². The 0.00012 m² difference is consistent with rounding, but the source does not independently establish whether the stated area is the effective active area under the experimental gasket/seal configuration.

The Specifications sheet also labels membrane porosity (85%) and mean pore radius (0.59 µm) as “not used in calculation.” These are source-stated specifications, not independently measured geometry.

**Disposition:** use 0.23088 m² only as the documented workbook nominal area, with sensitivity analysis around active area. Do not silently replace it with a different value or describe it as independently verified active area.

### 2. Flow channels are not interpretable as volumetric flow without resolving sign/units

Across the 631 retained observations in the 12 raw condition sheets, the exported flow-channel audit found:

| Workbook column | Finite numeric observations | Observed range | Negative values | Non-finite/malformed cells |
|---|---:|---:|---:|---:|
| MD Feed Flowrate (High) [LPM] | 631 | −0.611687 to −0.596159 | 631 | 1,457 blank cells |
| MD Distillate Flowrate (High) [LPM] | 631 | 0.407957 to 0.430598 | 0 | 1,457 blank cells |
| MD Feed Flowrate (Low) [LPM] | 0 | — | — | 631 `Inf` plus 1,457 blanks |
| MD Distillate Flowrate (Low) [LPM] | 0 | — | — | 631 `Inf` plus 1,457 blanks |
| MD Heating Flowrate [LPM] | 631 | 1.239070 to 1.264059 | 0 | 1,457 blank cells |
| MD Cooling Flowrate [LPM] | 631 | −0.194927 to −0.170396 | 631 | 1,457 blank cells |

The repeated negative signs may represent sensor orientation, an offset, or a channel/label issue, but the workbook alone does not distinguish these explanations. The two low-flow channels contain `Inf` for every retained row and cannot supply usable measured flow values. The “High” feed flow is negative in all retained rows despite the LPM label; do not convert its sign to positive or interpret its magnitude as a measured feed rate without source documentation. The heating/cooling channels appear numerically finite, but their interpretation and units should still be checked against instrument definitions before use as thermal boundary conditions.

**Disposition:** treat MD-side flow as unknown/nominal for current model runs. Do not calibrate or validate a flow-dependent model against these channels until channel sign conventions, meter ranges, sensor placement, and calibration are documented.

### 3. Condition labels and temperature channels

The first metadata row of each raw condition sheet repeats the text “20C/40C 0.4LMH” even on sheets whose names are 20-45, 20-65, 30-40, etc. This is a copy-forward metadata inconsistency, not evidence that every worksheet has the same setpoint. The worksheet names and measured inlet/outlet means are retained separately in the exported summary; nominal labels should not be substituted for measured temperatures.

The workbook reports MD inlet/outlet temperature channels, plus preheater (“PH”) channels. The current summary uses the MD-side inlet/outlet columns identified by their header labels. A source instrument diagram or channel map was not found in the extracted workbook evidence, so physical sensor locations and the intended meaning of each channel are not independently confirmed.

**Disposition:** preserve both nominal worksheet labels and measured channel summaries; record the channel map as unresolved pending an instrument diagram or source author/manufacturer clarification.

### 4. Equipment identity and Theoretical worksheet

The workbook filename and Specifications sheet identify a 3M, 0.2-micron polypropylene membrane, while the Theoretical sheet narrative says “CLARCOR QL822 0.231 m².” That discrepancy is unresolved. The Theoretical sheet is excluded from the observation ledger because it mixes calculated and experimental-run values. The derived flux is an OLS slope of cumulative distillate volume over runtime, not an independent measurement source.

**Disposition:** do not use the Theoretical sheet as a direct observed target or assume the CLARCOR and 3M descriptions are interchangeable. Source identity and the theoretical-sheet provenance need clarification.

## Implications for model and net-water claims

1. The 12 condition flux values are derived from cumulative volume and runtime; their high OLS (R^2) values characterize within-run linearity, not external model validity.
2. Flow rates and effective area remain uncertain inputs. Sensitivity analyses should report how these uncertainties propagate through flux, gross freshwater production, energy penalties, and net-water break-even results.
3. The current four-form comparison is a within-workbook diagnostic only. It cannot establish a preferred physically correct transport model.
4. No positive net-water benefit should be claimed from this benchmark alone.

## Required closure evidence

- Obtain the original instrument/channel map or source author clarification for the six flow columns and the MD/PH temperature channels.
- Resolve the 3M versus CLARCOR QL822 label conflict from primary documentation.
- Establish the effective active membrane area and the timing/volume measurement semantics from primary documentation.
- If clarification cannot be obtained, explicitly retain these as unresolved assumptions, propagate plausible ranges in sensitivity analysis, and keep the independent-validation gate open.

## Reproducibility provenance

The reviewed ingestion artifact reports the source workbook SHA-256 above, 631 observation rows, source worksheet and Excel row locators, and excludes the Theoretical worksheet. Artifact: `gdr-villa-3m-countercurrent`, workflow run [39981537413](https://github.com/jouzia/ai-waste-heat-water/actions/runs/39981537413), artifact SHA-256 `e5b6b7338d4281d9df0c91c2e1634d154336b501745445d32be2cd6c1ab6d344`.

This audit documents the evidence currently available; it does not resolve the source ambiguities by assumption.
