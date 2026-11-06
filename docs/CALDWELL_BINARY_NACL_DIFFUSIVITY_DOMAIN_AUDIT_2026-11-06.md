# Caldwell binary-NaCl diffusivity: equation, units, and domain audit

**Date:** 2026-11-06  
**Status:** source-reconciliation note; no solver changes  
**Related work:** feed-side concentration-polarization applicability; seawater salt-diffusivity evidence audit

## Executive finding

Caldwell's 1973 and 1974 papers provide a useful *binary NaCl* Fickian-diffusivity candidate, but they do not establish a natural-seawater mutual diffusivity. The 1974 abstract explicitly gives a 2–52 °C measurement range for 0.5 N NaCl solution. This supports a narrowly labelled binary-electrolyte sensitivity over the overlap with the present feed-temperature sweep (40–52 °C), not a predictive seawater concentration-polarization model over 40–70 °C.

The 1973 abstract reports a second temperature expression but does not state its full validity interval in the accessible abstract. Do not use that expression to claim validated coverage above 52 °C. The 1981 Caldwell & Eide measurements cover 0.5–40 °C for separate electrolyte solutions and therefore do not fill the 52–70 °C gap.

## 1. Primary-source equations and unit conversion

### Caldwell (1973)

Caldwell reports ordinary (Fickian) NaCl diffusivity in 0.5-normal aqueous NaCl as

`D_{1973}=10^{-5}(0.44+0.0423T)\;\mathrm{cm^2\,s^{-1}}`

where the abstract identifies T in °C through the surrounding temperature-dependent expressions. Since 1 cm²/s = 10⁻⁴ m²/s,

`D_{1973}=10^{-9}(0.44+0.0423T)\;\mathrm{m^2\,s^{-1}}`.

The abstract describes the solution as 0.5 normal (its parenthetical concentration notation is reproduced in the source). The accessible abstract does not state the full temperature validity interval for this equation. Treat it as a reported correlation whose domain still requires full-text verification, not as permission to extrapolate to 70 °C.

### Caldwell (1974)

The follow-up pressure study explicitly reports measurements at 0.5 N over 2–52 °C and gives the salt diffusivity as

`D_{1974}=10^{-7}(62+3.63T)\;\mathrm{cm^2\,s^{-1}}`

at atmospheric pressure (P = 0 in the paper's pressure-dependent expression), with T in °C. Converted to SI units,

`D_{1974}=10^{-11}(62+3.63T)\;\mathrm{m^2\,s^{-1}}`.

This is the more defensible source-bounded binary-NaCl candidate for the 40–52 °C overlap. It remains a binary NaCl solution measurement, not a natural-seawater coefficient.

## 2. Numerical cross-check in the documented overlap

| T (°C) | Caldwell 1973 expression (m²/s) | Caldwell 1974, P = 0 (m²/s) |
|---:|---:|---:|
| 40 | 2.132 × 10⁻⁹ | 2.072 × 10⁻⁹ |
| 50 | 2.555 × 10⁻⁹ | 2.435 × 10⁻⁹ |
| 52 | 2.640 × 10⁻⁹ | 2.508 × 10⁻⁹ |

The two reported expressions differ by approximately 2.9–5.3% across 40–52 °C. This is a cross-publication equation comparison, not a statistical confidence interval or a validated uncertainty bound. The 1973 equation's validity interval is not established by the accessible abstract, so the table is a numerical comparison only; the 1974 equation carries the explicit 2–52 °C domain.

## 3. Why this does not resolve natural-seawater diffusivity

1. **Different solution chemistry.** Caldwell's measurements are for binary NaCl. Natural seawater contains multiple principal ions and cannot be represented as binary NaCl without an explicit composition approximation.
2. **Different transport observable.** Poisson & Papaud (1983) report ionic self-diffusion in natural seawater. Those tracer coefficients are not automatically the mutual salt diffusivity needed for a bulk salinity-gradient film model.
3. **Cross-diffusion matters.** Miller et al. (1986) measured a ternary NaCl–MgCl₂–H₂O seawater analogue and found significant cross terms; four coefficients are required for a ternary system. A single scalar coefficient requires a defined reduced composition coordinate and derivation.
4. **Temperature coverage is incomplete.** Caldwell (1974) explicitly covers 2–52 °C. The present sweep extends to 70 °C. The 1981 Caldwell & Eide study covers 0.5–40 °C. None of these sources, as currently verified, establishes a natural-seawater mutual coefficient across 40–70 °C.
5. **Thermodiffusion is separate.** The Soret coefficients reported in these papers describe transport driven by temperature gradients and must not be substituted for the isothermal Fickian diffusivity in the conventional CPC film expression.

## 4. Recommended use in this project

A future opt-in sensitivity may use the Caldwell (1974) relation only if it is explicitly named, for example, `binary_nacl_caldwell_1974`, and is restricted to 2–52 °C. It must not be exposed as the default seawater diffusivity or used to claim validated natural-seawater CPC.

For the existing 40, 50, 60, and 70 °C sweep:
- 40 and 50 °C are inside the Caldwell (1974) temperature domain;
- 60 and 70 °C are outside it and must be rejected by a strict domain guard, not extrapolated silently;
- even at 40 and 50 °C, the solution-chemistry mismatch remains, so the result is a binary-NaCl approximation sensitivity only.

Before even that sensitivity is coupled to a Sherwood closure, the model must still define the concentration basis and the geometry-appropriate mass-transfer correlation. The Wyon Table 6 hydraulic-diameter discrepancy and the unverified spacer state remain unresolved. No CPC calculation is introduced by this note.

## References

1. Caldwell, D. R. (1973). *Thermal and Fickian diffusion of sodium chloride in a solution of oceanic concentration*. Deep-Sea Research and Oceanographic Abstracts 20(11), 1029–1039. DOI: 10.1016/0011-7471(73)90073-9. https://www.sciencedirect.com/science/article/pii/0011747173900739
2. Caldwell, D. R. (1974). *The effect of pressure on thermal and Fickian diffusion of sodium chloride*. Deep-Sea Research and Oceanographic Abstracts 21(5), 369–375. DOI: 10.1016/0011-7471(74)90041-2. https://www.sciencedirect.com/science/article/pii/0011747174900412
3. Caldwell, D. R. & Eide, S. A. (1981). *Soret coefficient and isothermal diffusivity of aqueous solutions of five principal salt constituents of seawater*. Deep-Sea Research Part A 28(12), 1605–1618. DOI: 10.1016/0198-0149(81)90100-X.
4. Poisson, A. & Papaud, A. (1983). *Diffusion coefficients of major ions in seawater*. Marine Chemistry 13(4), 265–280. DOI: 10.1016/0304-4203(83)90002-6.
5. Miller, D. G., Ting, A. W., Rard, J. A. & Eppstein, L. B. (1986). *Ternary diffusion coefficients of the brine systems NaCl (0.5 M)-Na₂SO₄ (0.5 M)-H₂O and NaCl (0.489 M)-MgCl₂ (0.051 M)-H₂O (seawater composition) at 25°C*. Geochimica et Cosmochimica Acta 50(11), 2397–2403. DOI: 10.1016/0016-7037(86)90021-9.
