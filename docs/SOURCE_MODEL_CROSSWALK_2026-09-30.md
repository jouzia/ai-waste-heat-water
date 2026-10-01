# Source-model crosswalk: Keshavarzzadeh (2020) vs repository implementation

Date: 2026-09-30

## Purpose

This document freezes the source-model reconciliation step before any quantitative
comparison with the experimental markers reproduced in Keshavarzzadeh et al. (2020).
The source paper is open access and explicitly defines a one-dimensional, counter-flow,
flat-sheet DCMD model. It reports mass flux as a function of average feed bulk
temperature for two inlet flow rates (7 and 11 cm^3/s) and NaCl concentrations
0, 0.55, 1.15 and 1.67 M.

Source: Keshavarzzadeh, Scientific Reports 10, 16790 (2020),
DOI 10.1038/s41598-020-73964-7.

## Crosswalk

| Source element | Source formulation | Repository status | Validation consequence |
|---|---|---|---|
| Membrane flux | J = B(P_w,f,m - P_w,p,m) | Implemented in `source_membrane_flux_coefficient`; channel model currently accepts permeance directly | Source runner must derive B from membrane properties before comparison |
| Membrane B | Knudsen + molecular diffusion resistance, source Eq. 2 | Implemented | Must use source-compatible pore radius, thickness, porosity, tortuosity, pressure and membrane temperature |
| Tortuosity | tau = 1/epsilon | Implemented as explicit source assumption | No independent fitting allowed |
| Gas diffusivity product | PD = 1.895e-5 T^2.072 | Implemented inside source B function | Source units must remain SI |
| Feed water activity | gamma_w(1-X), gamma_w = 1 - 0.5X - 10X^2 | Implemented | X must be converted from the plotted NaCl molarity input; direct use of 1.67 as X is invalid |
| Saturation pressure | exp(23.1964 - 3816.44/(T-46.13)) | Implemented | Source temperature convention must be preserved |
| Axial feed/permeate balances | Source Eqs. 9-18 use enthalpy balances and membrane-surface vapor enthalpy | **Not yet source-exact in the generic channel solver** | Current `md_channel.py` uses cp-based bulk energy updates; do not call it a source reproduction |
| Membrane conduction | q_m = k_m(T_f,m-T_p,m)/delta | Implemented in source conductivity + channel thermal balance | Source-specific k_m must be used |
| Membrane conductivity | k_m = epsilon k_v + (1-epsilon) k_s; source Eqs. 20-21 | Implemented | Temperature-dependent source properties must be retained |
| Boundary heat transfer | source Eqs. 23-26 | Implemented in `channel_transport.py` | Geometry/aspect-ratio convention must be frozen |
| Flow direction | Counter-current | Supported in `md_channel.py` | Counter-current boundary condition must be used for source reproduction |
| Experimental x-axis | Average feed bulk temperature = mean inlet/outlet bulk feed temperature | Registry/ledger documented | Must derive exactly from source conditions |
| Experimental flow cases | 7 and 11 cm^3/s | Registry documented | Must convert volumetric flow to mass flow using an explicit density convention |
| Experimental salinity cases | 0, 0.55, 1.15, 1.67 M NaCl | Registry documented | Must preserve source molarity and separately record conversion used by source activity equation |

## Critical finding

The repository currently contains the individual source equations, but the existing
general-purpose 1-D channel solver is **not yet a source-exact implementation** because
its axial thermal update uses constant- cp energy increments rather than the source's
enthalpy/vapor-enthalpy formulation in Eqs. 9-18.

Therefore:

- the current generic channel output must not be presented as a reproduction of
  Keshavarzzadeh (2020);
- source-equation unit tests demonstrate implementation integrity, not experimental
  agreement;
- a dedicated source-compatible runner is required before Figure 3 validation;
- no model parameter may be fitted to Figure 3 before the first unfitted run.

## Source / primary provenance issue

Keshavarzzadeh states that its Figure 3 symbols are experimental data, but the figure
caption cites reference 25, while the article's bibliography identifies the
Martínez-Díez & Vázquez-González (1999) DCMD paper as reference 37. The repository
therefore treats the 2020 figure as a development benchmark until the experimental
markers are cross-walked to the primary 1999 source.

The 1999 primary paper is independently identified as Journal of Membrane Science
156(2), 265-273, DOI 10.1016/S0376-7388(98)00349-4. Its reported experimental
configuration includes a flat TF200 PTFE membrane, 80% void fraction, 60 micrometre
thickness, 0.2 micrometre nominal pore size, and nine feed/nine permeate channels.

## Source-runner implementation status (2026-10-01)

A dedicated `source_keshavarzzadeh_runner.py` now implements the source-structured
counter-current axial march, source membrane-flux coefficient, source water-activity
equation, membrane conduction, source heat-transfer correlation, and enthalpy-based
control-volume updates. The solver explicitly isolates its engineering property
closures because the accessible source text does not provide a complete property
table/closure sufficient to reconstruct every numerical detail without assumptions.

This is therefore a **source-structure implementation, not yet a source-exact numerical
reproduction**. In particular, liquid cp/enthalpy, density, viscosity, thermal
conductivity, and latent-heat closures remain explicit engineering approximations.
They must be replaced or source-matched, or their influence must be quantified as
model-form uncertainty, before calling the implementation source-exact.

## Next validation gate

1. Freeze the property closures and record their provenance/uncertainty.
2. Execute all eight source-condition combinations using documented, non-invented
   boundary conditions. Figure 3 inlet temperatures must not be inferred from the
   separate Table 1 design case.
3. Check axial temperature profiles, positive driving force, mass conservation,
   energy-balance residuals, and numerical convergence.
4. Obtain or reconstruct the experimental markers and exact boundary conditions.
5. Archive digitization calibration, pixel coordinates, uncertainty, and an independent
   repeat extraction for a predefined subset.
6. Run the source-structure implementation unfitted, then compare predictions with
   observations using MAE, RMSE, bias, and appropriate relative error.
7. Evaluate the modern/IAPWS model on the same observations and preserve both model
   forms for uncertainty analysis.

## Status

**Source equations: reconciled and unit-tested.**

**Dedicated source-structure runner: implemented; CI verification pending for the latest mass-balance/convergence regression.**

**Source-exact reproduction: not yet established.**

**Experimental validation: blocked pending source-matched boundary conditions and
primary-source marker crosswalk.**
