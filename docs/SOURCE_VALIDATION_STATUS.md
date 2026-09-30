# Source validation status

Last updated: 2026-09-30

## Current gate

The Keshavarzzadeh et al. (2020) source formulation has been transcribed into a dedicated source-model pathway. The published paper defines a one-dimensional counter-current flat-sheet DCMD control-volume model with membrane mass transfer, feed/permeate mass balances, enthalpy balances, membrane conduction, and an entry-effect Nusselt correlation. The paper compares model results with experimental markers for two flow rates (7 and 11 cm^3/s) and four NaCl concentrations (0, 0.55, 1.15, 1.67 M).

This repository now keeps that source formulation separate from the preferred modern thermodynamic pathway.

## Important provenance limitation

The 2020 Figure 3 caption says the symbols are experimental data but cites reference 25. Reference 25 in the 2020 paper is a Geothermics ground-source heat-exchanger paper, while the Martinez-Diez & Vazquez-Gonzalez 1999 membrane-distillation paper is reference 37. Therefore the Figure 3 markers are not currently treated as independently verified primary-source observations.

The primary 1999 publication is identified by DOI 10.1016/S0376-7388(98)00349-4, but the quantitative observation ledger remains intentionally unpopulated until the primary experimental conditions and flux observations can be extracted and independently checked.

## Eight-case matrix

The frozen matrix contains:

- 7 cm^3/s × 0, 0.55, 1.15, 1.67 M NaCl
- 11 cm^3/s × 0, 0.55, 1.15, 1.67 M NaCl

The case matrix is stored at:
`04_experiments/literature_benchmarks/MD-DCMD-CHANNEL-2020-source_cases.yaml`

No repository default is allowed to fill the missing primary boundary temperatures.

## Validation order

1. Extract primary observations and boundary conditions.
2. Archive source locators and digitization metadata.
3. Freeze the source-model configuration.
4. Run the source model unfitted for all eight cases.
5. Independently re-extract a predefined subset.
6. Compare observed and modeled flux using MAE/RMSE/bias and uncertainty intervals where justified.
7. Only after the development/held-out split is frozen may any calibration be performed.
8. Compare the source model with the modern thermodynamic model as a model-form uncertainty analysis.

## Do not claim

The repository must not currently claim that the source model has reproduced or validated the published experimental Figure 3. Software tests establish implementation integrity only; they do not establish physical agreement.
