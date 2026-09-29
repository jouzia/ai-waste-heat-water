# Source notes: Keshavarzzadeh et al. (2020) DCMD benchmark

Source: Keshavarzzadeh, A. H. (2020), Design and bio-inspired optimization of direct contact membrane distillation for desalination based on constructal law, Scientific Reports 10, 16790.

## Why this source is a useful benchmark

The paper presents a one-dimensional flat-sheet DCMD model and reports comparison against experimental data from Martínez-Díez and Vázquez-González. The validation module is explicitly described as counter-flow, with nine feed and nine permeate channels. The paper compares predicted and experimental water mass flux over feed temperatures, flow rates, and NaCl concentrations.

Source locations:
- DCMD configuration and counter-current flow: Fig. 1 / modeling text.
- Membrane transport: Eqs. (1)-(8).
- Feed/permeate energy and mass balances: Eqs. (9)-(18).
- Membrane thermal conduction: Eqs. (19)-(22).
- Channel heat-transfer correlation: Eqs. (23)-(26).
- Experimental validation configuration: Validation section and Fig. 3.
- Thermal efficiency definition: Eq. (27).

## Important model-form requirements

The repository reduced-order md_channel model must not be presented as a reproduction of this paper until all of the following are matched or explicitly treated as model-form differences:
1. Counter-current flow arrangement.
2. Source membrane transport formulation, rather than an arbitrary fitted permeance.
3. Source membrane properties and temperature dependence.
4. Source channel heat-transfer correlation.
5. Source water-vapor-pressure/activity formulation.
6. Source experimental operating conditions.
7. Source observed flux values digitized from the validation figure or obtained from a lawful machine-readable dataset.
8. Source definition of the plotted average feed bulk temperature.

The current benchmark therefore remains parameterized / not numerically validated.

## Reproducibility rule

Do not tune a permeance or heat-transfer coefficient until after an unfitted source-condition run has been recorded. If fitting is later required, the fitted parameters must be marked as development parameters and the independent validation cases must remain untouched.

## Licensing / reuse

The article is open access under CC BY 4.0. Repository use should preserve attribution and identify modifications. Do not redistribute third-party experimental data unless the applicable source terms permit redistribution.

## Evidence boundary

The paper itself states that its numerical model agrees well with experimental data. That statement is source evidence, not validation of this repository implementation. This project must independently compute its own observed-versus-predicted error before claiming reproduction.