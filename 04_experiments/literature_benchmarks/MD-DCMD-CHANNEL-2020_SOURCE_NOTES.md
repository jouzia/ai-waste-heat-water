# Source notes: Keshavarzzadeh et al. (2020) DCMD benchmark

Source: Keshavarzzadeh, A. H. (2020), *Design and bio-inspired optimization of direct contact membrane distillation for desalination based on constructal law*, Scientific Reports 10, 16790.

## Why this source is a useful benchmark

The paper presents a one-dimensional flat-sheet DCMD model and reports comparison against experimental data from Martínez-Díez and Vázquez-González. The validation module is explicitly described as counter-flow, with nine feed and nine permeate channels. The paper compares predicted and experimental water mass flux over feed temperatures, flow rates, and NaCl concentrations. citeturn1view0

Source locations:
- DCMD configuration and counter-current flow: Fig. 1 / modeling text.
- Membrane transport: Eqs. (1)-(8).
- Feed/permeate energy and mass balances: Eqs. (9)-(18).
- Membrane thermal conduction: Eqs. (19)-(22).
- Channel heat-transfer correlation: Eqs. (23)-(26).
- Experimental validation configuration: Validation section and Fig. 3.
- Thermal efficiency definition: Eq. (27).

The published validation figure is available as the article's Figure 3 image:
https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41598-020-73964-7/MediaObjects/41598_2020_73964_Fig3_HTML.png

Figure 3 contains two panels: Q = 7 cm³/s and Q = 11 cm³/s, each with experimental markers for 0, 0.55, 1.15, and 1.67 M NaCl and model curves. The paper defines T_b1 as the average of inlet and outlet feed bulk temperature. citeturn1view0

## Critical distinction: Table 1 is NOT the validation dataset

The article's Table 1 gives the input parameters for the paper's DCMD model case: length 5 m, width 0.5 m, channel depth 5 mm, membrane thickness 200 µm, porosity 0.7, pore size 0.45 µm, feed inlet 70 °C, permeate inlet 25 °C, feed and permeate flow rates 10 L/min, and feed salinity 35,000 ppm. These values are useful for reproducing the paper's *model case*, but they must not be substituted for the separate Martínez-Díez experimental conditions behind Figure 3. citeturn2search0

## Confirmed validation facts

- Validation configuration: counter-flow flat-sheet module.
- Nine feed channels and nine permeate channels.
- PTFE membrane reported with 80% void fraction and 60 µm thickness.
- Nominal pore size is printed as "0.2 mm" in the 2020 paper; this unit is preserved verbatim until the 1999 primary source is checked.
- Recirculation rates: 7 and 11 cm³/s.
- NaCl concentrations: 0, 0.55, 1.15, and 1.67 M.
- Figure 3 experimental observations are marker data; the continuous lines are model results and must not be digitized as observations. citeturn1view0

## Figure-digitization status

**Status: not yet publication-grade digitized.**

The source figure has been located and its experimental/model series have been mapped, but no point is entered into the repository as an observation until the required pixel-to-axis calibration, raw pixel-coordinate archive, repeated extraction, and digitization uncertainty estimate are completed.

This deliberately prevents approximate visual transcription from being mistaken for exact experimental data.

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
