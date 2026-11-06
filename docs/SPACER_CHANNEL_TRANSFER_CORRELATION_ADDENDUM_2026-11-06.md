# Spacer-channel hydrodynamics and Sherwood-correlation applicability addendum

**Date:** 2026-11-06  
**Status:** literature applicability addendum; no solver changes  
**Related audit:** `FEED_CONCENTRATION_POLARIZATION_CORRELATION_AUDIT_2026-11-06.md`

## Purpose

This addendum refines the interpretation of the nominal feed Reynolds-number calculation in the concentration-polarization audit. The previous audit correctly rejected the laminar Graetz–Leveque closure for the nominal Reynolds numbers, but its comparison with the conventional smooth-pipe transition threshold is not sufficient to classify the actual membrane-channel flow or validate a smooth-duct turbulent Sherwood correlation.

## Key correction

The current nominal feed Reynolds values (approximately 7,943–13,083 across the audited temperature/salinity endpoints) are calculated using the Wyon local-model inputs:

`Re = rho u D_h / mu`

with `u = 1.85 m/s` and `D_h = 0.003 m`.

These values establish that the nominal hydraulic-diameter Reynolds number is high. They do **not** establish that the real membrane channel behaves like a smooth circular pipe, nor that a generic turbulent-pipe Sherwood equation predicts its salt mass transfer. In spacer-filled channels, spacer geometry can trigger recirculation and unsteady flow at Reynolds numbers far below conventional smooth-pipe transition values. The correct classification depends on the actual channel and spacer geometry, not a single textbook threshold.

## Evidence from spacer-specific membrane-distillation studies

### 1. Spacer-filled-channel flow and heat-transfer regime

The 2023 experimental study *Review and Analysis of Heat Transfer in Spacer-Filled Channels of Membrane Distillation Systems* tested NaCl solutions over 1–95 g/kg and 30–80 °C. Its experiments covered Reynolds numbers of approximately 100–1,500 and derived:

`Nu = 0.158 Re^0.652 Pr^0.277`

The authors discuss literature reporting spacer-induced vortex formation and unsteady flow at Reynolds numbers around 180–350, with transition behaviour dependent on spacer mesh, roughness, and geometry. Their correlation is explicitly bounded to `100 < Re < 1500`; it must not be extrapolated to the project's nominal Re near 8,000–13,000. It is also a **Nusselt** correlation for the studied spacer/plate arrangement, not a validated Sherwood correlation for the Wyon channel.

The important result for this project is methodological: a spacer-filled channel may not follow smooth-pipe regime boundaries, and transfer correlations require geometry-specific validation.

### 2. Direct DCMD mass-transfer measurements with different spacers

Ve et al. (2021), *Experimental investigation of the effect of the spacer and operating conditions on mass transfer in direct contact membrane distillation*, investigated five spacers and operating conditions including feed velocity and concentration. The authors derived mass-transfer correlations for the investigated spacers and a general correlation for that tested set. They report that the Grober empty-channel correlation could describe mass-transfer characteristics in their spacer-filled channels after comparison with experimental Sherwood numbers.

This is not evidence that Grober, or any single correlation, transfers unchanged to Wyon's configuration. It demonstrates that the appropriate closure is an empirical, setup-dependent question that must be checked against the actual spacer/channel design.

### 3. Calibration rather than blind correlation transfer

The 2016 study *Calibration and analysis of a direct contact membrane distillation model using Monte Carlo filtering* reports that off-the-shelf Nusselt equations cannot be directly applied to spacer-filled channels without calibration to the particular spacer. It also treats the mass-transfer Sherwood closure as geometry- and flow-regime-dependent and uses heat/mass-transfer analogy only after channel heat-transfer calibration.

This supports a staged workflow: establish the actual channel geometry and calibrate/validate the channel transfer model before using its Sherwood analogue to estimate membrane-interface salinity.

## Consequences for the Wyon/Nayar model

1. Retain the previous conclusion that the laminar Graetz–Leveque correlation is not justified for the current nominal Reynolds numbers.
2. Do not replace it automatically with `Sh = 0.023 Re^0.8 Sc^(1/3)`. That expression is a smooth-duct turbulent candidate, not a Wyon-specific closure.
3. Do not apply the 2023 spacer-channel Nusselt fit: its Reynolds validity interval (100–1,500), geometry, and measured response differ from the present nominal case.
4. Do not treat the 2021 spacer-specific Sherwood results as directly transferable without matching the spacer, channel dimensions, and operating domain.
5. Recalculate Reynolds number if the actual free-flow area, spacer blockage, hydraulic diameter, or superficial/interstitial velocity differs from the current nominal input definition.
6. Keep the Wyon baseline and the existing Nayar three-model decomposition unchanged. The bulk Reference Salinity remains an explicit proxy; no numerical CPC or membrane-interface salinity is introduced by this addendum.

## Required geometry and validation metadata

Before choosing a predictive Sherwood closure, recover or establish:

- feed-channel width, height, and cross-sectional shape;
- whether the channel is empty or spacer-filled;
- spacer filament diameter, orientation, mesh size, pitch, porosity, and contact with the membrane;
- whether the quoted 1.85 m/s is superficial, cross-sectional mean, or interstitial velocity;
- the hydraulic-diameter convention and wetted perimeter used to obtain 0.003 m;
- flow development length and inlet conditions;
- an applicable salt mutual/effective diffusivity for the selected solution chemistry and temperature/salinity range;
- experimental or independently validated heat/mass-transfer data for the same channel/spacer configuration.

The Wyon source configuration and the local surface-solver input set should not be assumed to contain these details merely because a hydraulic diameter and velocity are available.

## Recommended next step

Treat channel geometry identification as the gating task. Search the Wyon thesis and its cited experimental apparatus references for a documented feed-channel cross-section or spacer specification. If these cannot be recovered, record the geometry as unknown and do not select a predictive Sherwood closure. A separately parameterized CPC sensitivity may be used for exploratory uncertainty analysis, but it must be labelled as an assumed mass-transfer coefficient rather than a validated interface-salinity prediction.

## Sources

1. Ve, Q. L. et al. (2021). *Experimental investigation of the effect of the spacer and operating conditions on mass transfer in direct contact membrane distillation*. Desalination 500, 114839. DOI: 10.1016/j.desal.2020.114839. https://www.sciencedirect.com/science/article/pii/S0011916420315174
2. *Review and Analysis of Heat Transfer in Spacer-Filled Channels of Membrane Distillation Systems* (2023). Membranes 13(10), 842. DOI: 10.3390/membranes13100842. https://pmc.ncbi.nlm.nih.gov/articles/PMC10608446/
3. *Calibration and analysis of a direct contact membrane distillation model using Monte Carlo filtering* (2016). Journal of Membrane Science. https://www.sciencedirect.com/science/article/pii/S0376738816304641
4. Wyon (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University. https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf
