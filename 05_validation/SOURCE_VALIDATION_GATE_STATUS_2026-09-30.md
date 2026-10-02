# Source-validation gate status — updated 2026-10-01

## Keshavarzzadeh et al. (2020)

The published model is a one-dimensional counter-current flat-sheet DCMD model. Its displayed formulation includes membrane vapor-pressure transport, control-volume mass balances, feed/permeate enthalpy balances, membrane conduction, and convective heat-transfer correlations. The paper evaluates two recirculation rates (7 and 11 cm³/s) and four NaCl concentrations (0, 0.55, 1.15, 1.67 mol/L) against experimental markers. See the primary article and the repository crosswalk before interpreting its validation claim.

## Repository implementation status

- Source membrane transport equations: implemented and unit-tested.
- Source water-activity conversion: implemented with explicit molarity-to-mole-fraction conversion.
- Source membrane conductivity: implemented.
- Source Keshavarzzadeh axial counter-current runner: implemented.
- Counter-current permeate mass direction: corrected to follow source Eq. 12.
- Liquid enthalpy inversion: explicit and isolated from the source equations.
- Eight-case source-condition execution matrix: registered, with missing Figure 3 boundary conditions explicitly blocking quantitative execution.
- Eight-case **software smoke matrix**: added for two flow rates and four salinities using explicitly provisional 60/30 °C boundary temperatures; these are not source conditions and are not experimental validation.
- Counter-current feed/permeate mass conservation and interface-gradient smoke checks: tested.
- Incremental cooling-water accounting: corrected so baseline data-center cooling is not double-counted as intervention burden.
- CI: green on current commit 6a86881342d419f42ae4395587c7ae89173167b4 (run 276); pytest and Ruff completed successfully. Runs 274–275 exposed a missing explicit test factor after removal of unproven workload defaults; the test was corrected and run 276 passed.
- Experimental validation accuracy: **not claimed**.

## Remaining quantitative gate

The source paper identifies Figure 3 experimental markers but the exact observation values and all boundary conditions needed to reproduce each plotted point are not fully recoverable from the accessible text alone. The repository therefore does not populate observations from model curves or undocumented defaults.

Before publication-level validation:

1. obtain the primary experimental source and/or an accessible author/legal copy;
2. extract the experimental markers and exact boundary conditions;
3. archive figure pixel coordinates and axis calibration when digitization is required;
4. independently re-extract a predefined subset;
5. source-match or quantify uncertainty in the explicit engineering property closures;
6. freeze the unfitted source runner;
7. execute all eight source-condition groups only after exact boundary conditions are available;
8. compare predicted and observed flux with MAE, RMSE, bias, and appropriate relative error;
9. preserve failures and model-form differences.

## Important provenance issue

Keshavarzzadeh (2020) labels the Figure 3 experimental symbols with reference 25 in the caption, while reference 25 in that article is a Geothermics ground-source heat-exchanger paper. The Martínez-Díez & Vázquez-González (1999) DCMD paper is reference 37. The repository therefore treats Figure 3 as reproduced experimental evidence until the primary-source marker set is crosswalked.

## Interpretation rule

A green software CI run establishes implementation quality only. It does not establish agreement with the physical experiment. No publication claim of experimental validation should be made until the observation ledger is populated and the unfitted comparison is complete.
