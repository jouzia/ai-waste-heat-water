# Nayar density correlation and Reference Salinity closure audit

**Date:** 2026-11-06  
**Status:** source reconciliation; no CPC or DCMD solver changes  
**Related work:** Nayar (2016) vapour-pressure variant; Reference Salinity / film-concentration basis audit; feed-side concentration-polarization and diffusivity audits

## Executive finding

The open salinity-convention question is resolved from the primary Nayar et al. (2016) article: its nomenclature defines (S_R) as reference-composition salinity, and the authors explicitly state that the correlations in the paper are expressed as functions of Reference Salinity, with the shorthand (S) meaning Reference Salinity. Therefore, the project's Nayar vapour-pressure input named and supplied as Reference Salinity in g/kg is source-consistent.

The same article provides a seawater density correlation whose salinity basis is Reference Salinity. Its atmospheric/reference-pressure density expression (Eq. 19, Table 6) is a defensible candidate for converting Reference Salinity mass-fraction proxy to a volumetric equivalent in a future film-theory implementation. At the present 40–70 °C feed temperatures, the article defines the reference pressure (P_0) as 0.101 MPa (atmospheric pressure), so Eq. 19 is the applicable branch; the pressure correction in Eq. 18 is not needed for a near-atmospheric DCMD channel.

This resolves the density-correlation selection question at the property level. It does **not** resolve salt diffusivity, the spacer-channel Sherwood closure, the variable-density film balance, or the feed-interface composition. No concentration-polarization calculation is enabled by this audit.

## 1. Nayar salinity convention: primary-source resolution

Nayar et al. (2016), Section 1 and nomenclature, distinguish:
- (S_R): Reference Salinity / reference-composition salinity, g/kg;
- (S_P): Practical Salinity;
- (S_K): Knudsen Salinity.

The article explicitly states that its correlations are expressed as functions of Reference Salinity and that the shorthand (S) used in the paper means Reference Salinity. This statement applies to the seawater property correlations, including the natural-seawater vapour-pressure relation in Eq. 5 and the density relation in Table 6.

Consequences:
1. Keep the Nayar vapour-pressure function input in Reference Salinity g/kg.
2. Do not silently substitute Practical Salinity, Absolute Salinity, NaCl molality, or kg/m³.
3. Retain the distinction between Reference Salinity and Absolute Salinity. Nayar's chosen correlation basis is Reference Salinity; the fact that Absolute Salinity is the physical mass fraction does not authorize replacing the paper's stated input scale.

## 2. Density correlation suitable for the current temperature range

Nayar et al. Table 6 gives:

`rho_sw(t,S,P) = rho_sw(t,S,P_0) F_P`  (Eq. 18)

with the reference-pressure density:

`rho_sw(t,S,P_0) = a1 + a2*t + a3*t^2 + a4*t^3 + a5*t^4
                 + b1*x + b2*x*t + b3*x*t^2 + b4*x*t^3 + b5*x^2*t^2`  (Eq. 19)

where:
- `t` is ITS-90 temperature in °C;
- `S` is Reference Salinity in g/kg;
- `x = S/1000` is kg/kg;
- density is kg/m³.

Coefficients:

| Coefficient | Value |
|---|---:|
| a1 | 9.999e2 |
| a2 | 2.034e-2 |
| a3 | -6.162e-3 |
| a4 | 2.261e-5 |
| a5 | -4.657e-8 |
| b1 | 8.020e2 |
| b2 | -2.001 |
| b3 | 1.677e-2 |
| b4 | -3.060e-5 |
| b5 | -1.613e-5 |

For (t le 100 ^\circ C), Nayar et al. define (P_0=0.101) MPa. The present feed-side sweep (40, 50, 60, 70 °C; 15, 35, 38 g/kg) is therefore on the atmospheric-reference-pressure branch. Eq. 19 can be used directly for the bulk density at the stated channel pressure to engineering accuracy; a non-atmospheric pressure correction would require Eq. 18 / Eq. 20 and a declared pressure input.

The article's Table 6 reports the density correlation's primary-data range as 0–180 °C, 0–150 g/kg and (P=P_0) in the near-atmospheric interval 0.1–1 MPa, with maximum uncertainty ±0.14%. The current temperature/salinity sweep lies within that stated range. This is a correlation uncertainty statement, not a guarantee that the complete film-theory CPC prediction has ±0.14% uncertainty.

## 3. Consistent volumetric concentration conversion

For the Reference-Salinity mass-fraction proxy:

`w_R = S_R/1000`

and the corresponding volumetric proxy concentration is:

`C_R = rho_Nayar(t,S_R,P_0) * S_R/1000`

where `C_R` is kg/m³. This conversion makes the density basis and salinity scale explicit.

For bulk conditions, `rho_Nayar` is now a source-backed candidate density closure matched to the Nayar Reference Salinity input. A future interface conversion must still decide whether it:
- assumes constant bulk density across the concentration film, in which case the conventional exponential film multiplier can be applied directly to the mass-fraction proxy; or
- solves a variable-density salt mass balance, in which case the interface density and mass-average velocity must be included in a derived governing equation.

Do not add an ad hoc density-ratio correction to the constant-density exponential equation and label it a variable-density model.

## 4. Relationship to the Wyon baseline

The Wyon Appendix A density correlation remains part of the source-faithful Wyon pathway and must not be replaced as a side effect of this audit. The Nayar density expression is a separate property correlation selected for a future Nayar/Reference-Salinity CPC research path.

No numerical Wyon-vs-Nayar density comparison is asserted here. A valid comparison would first need to evaluate both correlations at identical ITS-90 temperatures, Reference Salinity inputs, and pressure, while preserving Wyon's documented salinity and temperature conversions.

## 5. Implementation decision

**Selected candidate for future CPC volumetric conversion:** Nayar et al. (2016), Table 6, Eq. 19, at (P_0=0.101) MPa for (t le 100\ ^\circ C).

**Not implemented in this change:**
- no new density function or property substitution;
- no feed-side concentration-polarization calculation;
- no salt diffusivity selection;
- no Sherwood correlation selection;
- no variable-density film solver;
- no changes to Wyon defaults, Nayar vapour-pressure calculations, or existing benchmark outputs.

The next gating work remains the salt transport coefficient and geometry-specific Sherwood closure. Until both are source-supported for the Wyon channel and relevant temperature/salinity range, CPC must remain unimplemented.

## References

1. Nayar, K.G., Sharqawy, M.H., Banchik, L.D., and Lienhard V, J.H. (2016). *Thermophysical properties of seawater: A review and new correlations that include pressure dependence*. Desalination 390, 1–24. DOI: [10.1016/j.desal.2016.02.024](https://doi.org/10.1016/j.desal.2016.02.024). Author manuscript: [MIT DSpace record](https://dspace.mit.edu/entities/publication/f41d977b-998b-425d-8c56-4fbc645084ec). Relevant locations: nomenclature and Section 1 (Reference Salinity convention); Eqs. 18–20 and Table 6 (density correlation and validity).
2. Sharqawy, M.H., Lienhard V, J.H., and Zubair, S.M. (2010). *Thermophysical properties of seawater: a review of existing correlations and data*. Desalination and Water Treatment 16, 354–380. DOI: [10.5004/dwt.2010.1079](https://doi.org/10.5004/dwt.2010.1079). Source cited by Nayar for the reference-pressure density expression.
3. IOC, SCOR and IAPSO (2010). *The International Thermodynamic Equation of Seawater – 2010: Calculation and Use of the Thermodynamic Properties of Seawater*. TEOS-10 Manual.
