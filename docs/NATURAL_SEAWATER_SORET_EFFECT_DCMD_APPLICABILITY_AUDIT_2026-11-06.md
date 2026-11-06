# Natural-seawater Soret effect: relevance to feed-side DCMD concentration polarization

**Date:** 2026-11-06  
**Status:** literature/applicability audit; no transport solver changes  
**Related work:** feed-side concentration-polarization audit; salt-diffusivity evidence audit; Caldwell binary-NaCl domain audit; Reference Salinity and Nayar density closure audits

## Executive finding

A 2025 experimental study reports thermodiffusion (Soret) of natural seawater and seawater brine at approximately 41–42 °C. This is directly relevant to the physical question of salt transport in a DCMD feed-side temperature boundary layer: the salt flux need not be purely Fickian when a temperature gradient is present.

For a binary representation, the study writes the mass flux as

`J = -rho D grad(C) - rho C(1-C) D_T grad(T)`

with Soret coefficient `S_T = D_T/D`. At steady state:

`grad(C) = -S_T C(1-C) grad(T)`.

Thus a future DCMD concentration-polarization model that uses only `k_s = Sh D_s / D_h` and an isothermal Fickian film law omits a potentially relevant thermodiffusive contribution.

The published natural-seawater Soret values are not ready to insert into the Wyon solver. The experiment uses a different, non-membrane channel geometry and stable thermal stratification; the extracted coefficients rely on simplifying assumptions for multicomponent seawater; the measured cation concentration is not Nayar Reference Salinity; and the reported estimates vary by extraction route. No coefficient is extrapolated to 70 °C, and no Soret term is implemented here.

## 1. Primary experimental evidence

Xu and Torres (2025), *All-liquid thermal desalination and brine concentration via multichannel thermodiffusion*, Nature Water 3, 617–631, DOI: 10.1038/s44221-025-00428-5.

The paper reports natural seawater and natural seawater brine measurements in a single-channel thermodiffusion unit (TSU). Its channel is 500 mm long, 20 mm wide and 1 mm high. The upper and lower walls are independently temperature-controlled; the study uses a thermally stratified configuration rather than a membrane-distillation feed channel.

The article reports more than one natural-seawater Soret estimate:
- At 42 °C, `S_T,sw = 3.8_{-0.6}^{+0.4} × 10^-3 K^-1` and `S_T,br = 3.2_{-1.7}^{+1.8} × 10^-3 K^-1`.
- At 41 °C, another reported extraction gives `S_T,sw = 1.7_{-0.3}^{+0.4} × 10^-3 K^-1` and `S_T,br = 1.6_{-0.2}^{+0.1} × 10^-3 K^-1`.

These are not one interchangeable constant or a single pooled confidence interval. The paper describes alternative reductions of a multicomponent measurement, including an individual-cation/binary-solution simplification and a collective-cation/ion-water simplification. Preserve the method dependence when citing these results.

The natural-seawater feed in the paper is characterized by total major-cation concentration from ICP-MS (approximately 14,000 ppm); the brine is approximately 35,000 ppm total cations. These are not Nayar Reference Salinity values and must not be passed directly to the Nayar vapour-pressure equation.

## 2. Governing transport implication

For the paper's binary/quasi-binary representation:

`J_s = -rho D_s grad(C) - rho C(1-C) D_T grad(T)`

and

`S_T = D_T/D_s`.

At steady state with zero net salt flux:

`grad(C)/(C(1-C)) = -S_T grad(T)`.

Integration gives:

`logit(C_2) - logit(C_1) = -S_T (T_2-T_1)`.

For dilute-to-moderate salt mass fractions, the concentration-ratio response is approximately governed by `S_T ΔT`. As an order-of-magnitude illustration only, the published natural-seawater range of roughly 1.7–3.8 × 10^-3 K^-1 would give `S_T ΔT ≈ 0.0085–0.057` across a hypothetical 5–15 K liquid-layer temperature difference. This corresponds to a few-percent scale in the equilibrium concentration ratio, not a predicted DCMD CPC. The temperature difference is illustrative, not measured for the Wyon configuration.

The sign reported for natural seawater is thermophobic in the paper's convention: salt is driven toward the colder region. In a DCMD feed boundary layer where the membrane interface is cooler than the hot bulk feed, that direction could reinforce feed-side interfacial salt accumulation. Actual direction and magnitude must be evaluated with the local temperature field and a consistently defined multicomponent salt coordinate.

## 3. Why the coefficient is not directly transferable

1. **Different geometry and flow regime.** The TSU is a 500 × 20 × 1 mm stratified channel. Wyon's feed channel has a different cross-section, hydraulic characterization and forced-flow conditions; it also has a membrane interface. The measured coefficient does not provide a Wyon-channel Sherwood number.
2. **Multicomponent reduction.** The paper notes that a five-component system has many cross-diffusion coefficients. Its reported Soret estimates require simplifying assumptions, including neglecting cross-diffusion terms or treating the mixture as an effective binary system of ions and water. This is not a full natural-seawater Onsager transport matrix.
3. **Concentration basis.** ICP-MS measured major cations, not Reference Salinity or total dissolved salt mass fraction. The coefficient is not automatically a Soret coefficient for `S_R/1000`.
4. **Temperature coverage.** The reported natural-seawater measurements are near 41–42 °C. They do not establish `S_T(T,S)` over the complete 40–70 °C model sweep.
5. **Coupled thermal and concentration fields.** The experiment is designed to produce stable thermodiffusive stratification. A forced-convection DCMD boundary layer has a different velocity, thermal and concentration field; its Soret contribution must be solved with the local gradients and boundary conditions.

## 4. Consequence for the CPC model design

The earlier isothermal film-theory expression remains a useful limiting model, but it is not a complete transport equation when a temperature gradient and nonzero Soret coefficient are retained.

A future opt-in research model should distinguish at least:
- isothermal Fickian salt diffusion;
- thermal diffusion (Soret) driven by `grad(T)`;
- multicomponent cross-diffusion / electroneutrality assumptions;
- convective transport and the geometry-specific hydrodynamic closure.

A scalar effective `D_s` and a Sherwood correlation alone are insufficient to represent all of these effects. The Soret coefficient is a ratio `D_T/D_s`; it does not independently supply the absolute Fickian diffusivity or the salt-side mass-transfer coefficient.

**Decision:** record natural-seawater Soret transport as a potentially material missing mechanism. Do not numerically correct the existing Nayar-vs-Wyon sweep, and do not enable CPC until the concentration coordinate, Fickian diffusivity, Soret closure, and Wyon-channel transport closure are jointly justified.

## References

1. Xu, S. and Torres, J.F. (2025). *All-liquid thermal desalination and brine concentration via multichannel thermodiffusion*. Nature Water 3, 617–631. DOI: [10.1038/s44221-025-00428-5](https://doi.org/10.1038/s44221-025-00428-5).
2. Caldwell, D.R. (1973). *Thermal and Fickian diffusion of sodium chloride in a solution of oceanic concentration*. Deep-Sea Research and Oceanographic Abstracts 20, 1029–1039. DOI: [10.1016/0011-7471(73)90073-9](https://doi.org/10.1016/0011-7471(73)90073-9).
3. Poisson, A. and Papaud, A. (1983). *Diffusion coefficients of major ions in seawater*. Marine Chemistry 13, 265–280. DOI: [10.1016/0304-4203(83)90002-6](https://doi.org/10.1016/0304-4203(83)90002-6).
