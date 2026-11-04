# Wyon (2025) coupled DCMD membrane-surface solver: isolated reconstruction

**Date:** 2026-11-04  
**Scope:** Source-equation implementation of the local steady membrane-surface problem only. This is not a reproduction of Wyon's complete DCMD module, heat exchanger, pump sizing, 80-module plant, or annual techno-economic results.

## Implemented equations

The new module `src/ai_water/wyon_2025_surface_reference.py` transcribes Wyon (2025):

- Eq. (9): `Nu = 0.023 (1 + 6 d_h/L) Re^0.8 Pr^(1/3)`.
- Eq. (9) in the thesis numbering for film transfer: `alpha = Nu k / d_h` (the Nusselt and film-coefficient equations appear as Eq. 10 and Eq. 9, respectively, in the thesis text).
- Eq. (14): combined Knudsen/molecular mass-transfer coefficient, with the two transport resistances combined in series.
- Eq. (16): `tau = (2 - epsilon)^2 / epsilon`.
- Eq. (17): vapour enthalpy `H_v = 1.7535 T + 2024.3` kJ/kg, with absolute temperature in kelvin.
- Appendix A Eq. (9): pure-water saturation pressure, evaluated as printed by Wyon.
- Appendix A Eq. (10): `D P_m = 1.895e-5 T^2.072`.

The local interface energy balance follows Eqs. (7), (8), and (13):
`q_f = q_m = q_p`, `q_m = J H_v + (k_m/delta_m)(T_f,m - T_p,m)`, and `J = c (p_f,m - p_p,m)`.

## Numerical method

Instead of iterating two unconstrained surface temperatures, the implementation uses the common heat flux q as a scalar unknown. Film balances give:

`T_f,m = T_f - q/alpha_f`  
`T_p,m = T_p + q/alpha_p`

A bisection solve then enforces equality between q and the membrane latent-plus-conductive heat flux. The physical upper bound is the heat flux at which the two interface temperatures meet. This enforces the local energy balance without fitting parameters.

## Source-faithful choices and limitations

1. Wyon states that pure-water vapour pressure is used for both the seawater feed and pure-water permeate over the modelled 40–100°C range. The baseline therefore deliberately applies Wyon's pure-water Eq. A9 on both sides. The Nayar natural-seawater correlation is not silently substituted.
2. Wyon assumes total membrane-pore pressure of 1 bar and transitional diffusion (Knudsen number 0.5). These are explicit model assumptions, not measured local pore pressures.
3. Pore radius is an input. For the final PTFE configuration, the thesis lists pore size 0.45 μm; this implementation requires the radius (0.225 μm if the listed size is interpreted as diameter).
4. The film heat-transfer coefficients are explicit inputs. The Nusselt correlation is implemented, but density, viscosity, heat capacity, and fluid thermal conductivity must be computed from the exact Wyon Appendix A property correlations before the complete Wyon module is claimed reproduced.
5. The model returns local steady flux and interface temperatures. It does not yet solve outlet enthalpies, feed concentration change, channel pressure drop, heat-exchanger outlet conditions, module parallelization, or plant-scale annual output.
6. The thesis's source equations and parameters were read from the readable 53-page thesis copy documented in `docs/PRIOR_ART_WYON_2025_FULLTEXT_AUDIT_2026-11-01.md`; the institutional PDF endpoint was not successfully retrieved in this session. Verify transcription against the institutional file before publication.
7. The thesis reports an unresolved heat-flux discrepancy of up to approximately 11% and a validation/case-study temperature-range mismatch. The implementation is a source-equation reconstruction, not a validated solver.

## Verification tests

The test suite checks:
- Wyon Eq. A9 against independently recorded values at 40, 60, 80, and 100°C;
- tortuosity and positive mass-transfer coefficient;
- Nusselt/film coefficient calculation;
- coupled interface ordering and equality of feed, membrane and permeate heat fluxes;
- rejection of a reversed thermal driving force.

These are equation and numerical-invariant tests. They do not establish agreement with Wyon's reported flux, the original Termpiyakul experiment, or the full thesis case study.

## Next reproduction gates

1. Transcribe and test all Wyon Appendix A property correlations for seawater and pure water (cp, thermal conductivity, density, viscosity, enthalpy and vapour pressure), preserving temperature/salinity scales.
2. Compute `Re`, `Pr`, `Nu`, and `alpha` from the final Table 7 geometry and source-specific fluid properties; do not use guessed constant film coefficients.
3. Reconstruct the stream enthalpy balances and feed salinity update for one module.
4. Reproduce the thesis's initial PVDF validation configuration separately from the final PTFE case-study configuration.
5. Compare against the cited experimental heat-flux observations at matched conditions and report the unresolved discrepancy.
6. Only after the one-module calculation is reproduced, scale to 80 modules and audit the heat-exchanger and pump calculations.

## References

Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University, report LUTFD2/TFEM--25/5229--SE. [Institutional record](https://lup.lub.lu.se/student-papers/record/9198095).
