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

## Next implementation gate

1. Build a dedicated source-compatible axial solver using the source Eqs. 9-18.
2. Derive source B at each control-volume membrane temperature rather than supplying
   a fitted constant permeance.
3. Implement source enthalpy and latent-heat terms explicitly.
4. Convert the two volumetric flow cases to mass flow with recorded assumptions.
5. Run all eight source-condition combinations before touching experimental markers.
6. Compare the unfitted source runner to digitized observations.
7. Only then evaluate the generic modern/IAPWS model against the same observations.
8. Preserve both results as separate model forms for uncertainty/model-form analysis.

## Status

**Source equations: reconciled.**

**Source-exact axial solver: pending.**

**Experimental validation: blocked pending primary-source marker extraction and
source-exact first run.**
