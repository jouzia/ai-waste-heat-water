# Keshavarzzadeh 2020 source-model formulation

This document freezes the source-specific formulation used for the first quantitative MD reproduction track.

## Evidence boundary

Keshavarzzadeh et al. (2020) describes a one-dimensional counter-current flat-sheet DCMD model and compares water mass flux against experimental data reported by Martínez-Díez and Vázquez-González (1999). The validation figure contains two recirculation rates (7 and 11 cm³/s) and four NaCl concentrations (0, 0.55, 1.15, and 1.67 M). The plotted feed temperature is the average of inlet and outlet bulk feed temperature.

The paper is open access under CC BY 4.0.

## Frozen source equations

The source formulation includes:
- membrane flux coefficient B from Eq. (2), with tortuosity τ = 1/ε;
- source NaCl activity expression from Eqs. (6)-(7);
- source Antoine saturation-pressure equation from Eq. (8);
- axial feed/permeate mass and energy balances from Eqs. (9)-(18);
- membrane conductivity from Eqs. (19)-(21);
- membrane conductive heat transfer from Eq. (22);
- developing-flow Nusselt correlation from Eqs. (23)-(26).

These equations are implemented in source_keshavarzzadeh.py and the source-specific heat-transfer functions in channel_transport.py.

## Important separation

The source model is not the same thing as the project's preferred modern thermodynamic model.

For validation, the source formulation must first be run with source-compatible geometry, operating conditions, properties, and temperature conventions. Source-text discrepancies are preserved rather than silently corrected.

No parameter is fitted to Figure 3 observations at this stage.

## Primary experimental provenance and discrepancy resolution

The 2020 paper identifies Martínez-Díez & Vázquez-González (1999) as the experimental source. The primary experiment reports:
- Gelman Instrument TF200 PTFE;
- 80% void fraction;
- 60 µm membrane thickness;
- 0.2 µm nominal pore size;
- nine feed and nine permeate channels;
- each channel 55.0 mm long, 7.0 mm wide, and 0.45 mm high;
- effective transport membrane area 33.7×10^-4 m².

The 2020 validation text prints the nominal pore size as 0.2 mm, whereas the primary 1999 experimental source reports 0.2 µm. This is treated as a documented source-text discrepancy. The primary experimental value is used for provenance and validation inputs; the 2020 printed value is not silently rewritten in the evidence ledger.

## Current validation state

Status: **primary geometry reconciled; source formulation locked; numerical reproduction pending**.

Still required before numerical validation:
1. calibrated extraction of experimental markers from Figure 3;
2. raw pixel-coordinate archive;
3. digitization repeatability estimate;
4. exact inlet temperature conditions for plotted points;
5. unfitted model run;
6. observed-vs-predicted error metrics;
7. sensitivity to source-compatible transport/property choices.

A source author's claim of agreement is not used as validation of this repository implementation.

## Unit-consistency audit (2026-09-30)

The source equation for water activity uses a dimensionless salt mole-fraction variable X in the wider MD literature. The implementation must therefore convert NaCl molarity to mole fraction before applying `gamma_w = 1 - 0.5X - 10X^2`; passing values such as 1.67 M directly as X would be dimensionally invalid. This conversion is tracked as an explicit source-reproduction assumption and must be sensitivity-tested.
