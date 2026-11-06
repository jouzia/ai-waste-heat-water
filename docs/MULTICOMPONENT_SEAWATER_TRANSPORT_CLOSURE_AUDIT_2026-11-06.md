# Multicomponent Seawater Transport-Closure Decision Audit

**Date:** 2026-11-06  
**Scope:** Candidate feed-side concentration-polarization (CP) transport closures for the DCMD operating envelope currently studied in this repository: 40–70 °C and Reference Salinity 15–38 g/kg.  
**Status:** Literature and model-applicability audit only. No numerical CP closure is approved or implemented by this document.

## Executive decision

Retain the existing no-CP baseline as the primary model. Do not introduce a scalar natural-seawater diffusivity, a tracer-diffusion surrogate, or a temperature-extrapolated binary-NaCl coefficient as though it were a validated natural-seawater mutual-diffusion closure.

The strongest physically structured candidate found is a multicomponent ionic transport model using coupled Onsager phenomenological coefficients and electrolyte thermodynamics (Pitzer activity derivatives). Felmy and Weare developed such a model for the six-component Na-K-Ca-Mg-Cl-SO4-H2O seawater system at 25 °C. Their follow-up explicitly states that the required data for their high-concentration formulation are unavailable at temperatures other than 25 °C. It is therefore a useful model architecture and a possible future reference-temperature benchmark, but it does not presently support a validated 40–70 °C closure.

A reduced-order collective-salt model may eventually be defensible if derived from, and validated against, a component-resolved model or suitable natural-seawater mutual-diffusion measurements over the required temperature and salinity domain. No such full-domain calibration was established in this audit.

## Decision context and required closure

The current Nayar/Wyon comparison uses bulk Reference Salinity as a simplifying proxy for feed-interface and mean-pore salinity. It does not resolve a feed-side concentration boundary layer. A CP extension would need to connect a bulk-to-interface salt transport relation to the salinity coordinate used by Nayar's natural-seawater vapour-pressure correlation.

A film-theory expression such as

\[
C_{f,m}=C_{f,b}\exp\left(\frac{J_v}{k_s\rho}\right)
\]

is not a complete closure by itself. It requires, at minimum:

1. A defensible definition of the transported concentration and reference frame.
2. A mutual/effective salt diffusivity or a coupled multicomponent transport model on the same composition basis.
3. A Sherwood-number correlation applicable to the actual feed-channel geometry, Reynolds-number range, and spacer condition.
4. A thermodynamically consistent conversion from the transported concentration to Nayar Reference Salinity, including density and mass-fraction basis.
5. A clear treatment of thermal diffusion (Soret transport), kept separate from isothermal Fickian diffusion.
6. Validation or uncertainty bounds for the combined transport closure.

The existing Wyon Table 6 channel has a rectangular 5 mm × 50 mm cross-section, 100 mm length, and hydraulic diameter 3 mm. Its nominal feed Reynolds numbers calculated from Wyon property correlations are approximately 7,943–13,083 over the investigated temperature/salinity corners. A laminar Graetz–Leveque Sherwood relation is not suitable for this nominal configuration. This does not establish that a smooth-channel turbulent correlation is suitable: spacer geometry and channel-specific flow development remain material.

## Candidate closure decision matrix

| Candidate | Evidence and domain | Advantages | Critical limitation for this project | Decision |
|---|---|---|---|---|
| No-CP baseline | Existing Wyon and paired Nayar local surface calculations | Reproducible, transparent, preserves the current property-model comparison | Omits feed-side concentration boundary layer | **Retain as primary baseline** |
| Binary NaCl Fickian proxy | Caldwell 1974 measured 0.5 N NaCl from 2–52 °C; Caldwell 1973 reports a related equation but its accessible abstract does not establish a full validity interval | Explicit Fickian coefficient and a bounded temperature interval for part of the project sweep | Binary NaCl is not natural seawater; only 40 and 50 °C points fall within Caldwell 1974's stated range; 60 and 70 °C are outside | **Sensitivity-only candidate; not a seawater closure** |
| Natural-seawater tracer self-diffusion | Poisson & Papaud measured major-ion self-diffusion at seawater salinity 34.86 and 25 °C; Na+ and Cl− temperature/salinity effects were also studied | Directly uses natural seawater matrix for tracer transport | Self-diffusion is not mutual salt diffusion; no scalar conversion to a salt CP coefficient is justified | **Reject as direct Fickian closure** |
| Ternary NaCl–MgCl2 mutual-diffusion matrix | Miller, Lee & Rard report four mutual coefficients at 25 °C for a simplified seawater composition; a cross coefficient exceeds one main-term coefficient | Demonstrates quantitatively that cross-diffusion can be important even in a reduced seawater analogue | Only a ternary analogue at 25 °C, not full natural seawater or 40–70 °C | **Useful structural evidence; not direct closure** |
| Six-component Onsager/Pitzer model | Felmy & Weare model Na-K-Ca-Mg-Cl-SO4-H2O at 25 °C from low to high ionic strength, using Onsager coefficients and Pitzer thermodynamics | Most composition-relevant coupled transport framework identified; reproduces relevant binary mutual coefficients and calculates seawater-composition transport | High-concentration parameterization requires data unavailable beyond 25 °C; significant coupling and speciation/association issues | **Best future model architecture; not yet valid over target temperature range** |
| Extended Nernst–Hartley dilute model | Felmy & Weare Part II report good agreement with existing mutual-diffusion data below about 0.2 M when chemical-potential derivatives are included | Potential fallback when only infinite-dilution mobilities are available | Current NaCl-equivalent salinity is roughly 0.26–0.68 mol/kg; this is not the stated dilute domain, and molality is not identical to molarity | **Not applicable as primary closure** |
| Empirical effective natural-seawater diffusivity | Would require measured bulk/interface concentration gradients and fluxes under comparable DCMD hydrodynamics | Could reduce a full matrix model to a practical one-dimensional CP closure | No source-backed coefficient and uncertainty envelope spanning 40–70 °C and 15–38 g/kg was established | **Do not parameterize yet** |
| Soret-coupled multicomponent transport | Xu & Torres (2025) report natural-seawater thermodiffusion results near 42 °C and a multicomponent flux formulation | Demonstrates that thermal diffusion may contribute to salt redistribution | Their simplifications neglect cross terms; cation-only measurements and specific TSU/LBC geometries; no validated Soret tensor over the DCMD domain | **Separate research sensitivity only; never substitute for Fickian diffusivity** |

## Primary evidence

### 1. Felmy & Weare (1991), six-component seawater model

Felmy, A.R. and Weare, J.H., “Calculation of multicomponent ionic diffusion from zero to high concentration: I. The system Na-K-Ca-Mg-Cl-SO4-H2O at 25°C,” *Geochimica et Cosmochimica Acta* 55 (1991), 113–131. DOI: [10.1016/0016-7037(91)90405-T](https://doi.org/10.1016/0016-7037(91)90405-T).

The model extends empirical equations for Onsager phenomenological coefficients and combines them with Pitzer ion-interaction thermodynamics. The authors report that a large NaCl diffusive flux induces gradients in minor seawater species even where those species initially have no concentration gradients. This directly argues against assuming independent scalar diffusion of each ion or treating tracer coefficients as a mutual salt diffusivity.

### 2. Felmy & Weare (1991), associated species and temperature limitation

Felmy, A.R. and Weare, J.H., “Calculation of multicomponent ionic diffusion from zero to high concentration: II. Inclusion of associated ion species,” *Geochimica et Cosmochimica Acta* 55 (1991), 133–144. DOI: [10.1016/0016-7037(91)90406-U](https://doi.org/10.1016/0016-7037(91)90406-U).

The authors discuss significant differences between their association-aware model and simplified approaches, especially at high concentration. Crucially, they state that the data required by their formulation are unavailable at temperatures other than 25 °C. They describe an extended Nernst–Hartley approach as a possible more reliable extension of infinite-dilution data into slightly concentrated solutions, with agreement to existing six-component mutual-diffusion data below approximately 0.2 M. That dilute-domain statement must not be generalized to the current higher-salinity DCMD cases.

### 3. Miller, Lee & Rard: ternary seawater analogue

Miller, D.G., Lee, C.M. and Rard, J.A., “Ternary Isothermal Diffusion Coefficients of NaCl-MgCl2-H2O at 25 °C. 7. Seawater Composition.”

At simplified seawater composition (0.48877 mol/dm³ NaCl and 0.05110 mol/dm³ MgCl2), four mutual-diffusion coefficients were measured. The reported NaCl cross-term due to an MgCl2 gradient is 0.750 × 10^-9 m²/s, while the NaCl main-term is 1.432 × 10^-9 m²/s; the MgCl2 main-term is 0.728 × 10^-9 m²/s and its cross-term is 0.0185 × 10^-9 m²/s. This is a clear demonstration that a single scalar coefficient can conceal asymmetric cross-coupling. It is still only a 25 °C ternary analogue, not a full seawater closure.

### 4. Poisson & Papaud (1983): tracer data are not mutual diffusivity

Poisson, A. and Papaud, A., “Diffusion coefficients of major ions in seawater,” *Marine Chemistry* 13 (1983), 265–280. DOI: [10.1016/0304-4203(83)90002-6](https://doi.org/10.1016/0304-4203(83)90002-6).

The study measured self-diffusion coefficients of major ions in seawater of salinity 34.86 at 25 °C and examined temperature and salinity effects for Na+ and Cl−. These tracer measurements are valuable transport evidence but are not a mutual-diffusion matrix and cannot be inserted directly into a scalar salt film model.

### 5. Caldwell binary-electrolyte evidence

Caldwell's 1974 atmospheric-pressure NaCl expression is explicitly supported over 2–52 °C in 0.5 N NaCl. It can inform a bounded binary-electrolyte sensitivity at 40 and 50 °C only. The 60 and 70 °C sweep points are outside its stated range. It is not a natural-seawater mixture coefficient and must not be extrapolated or relabelled as one.

### 6. Thermodiffusion is a separate flux contribution

Xu and Torres (2025), “All-liquid thermal desalination and brine concentration via multichannel thermodiffusion,” *Nature Water* 3, 617–631. DOI: [10.1038/s44221-025-00428-5](https://doi.org/10.1038/s44221-025-00428-5).

Their multicomponent formulation contains both isothermal cross-diffusion and thermal-diffusion terms. Their natural-seawater effective Soret results are tied to distinct experimental configurations and an explicit simplification that neglects cross terms. This work motivates a future coupled sensitivity analysis but does not provide an isothermal Fickian salt diffusivity or a validated DCMD interface-Salinity closure.

## Recommended development path

1. **Preserve the current baseline.** No change to Wyon default or the existing Nayar three-model decomposition.
2. **Define the transported state.** Decide whether the CP layer is represented with independent ionic species, neutral electrolyte components, or a reduced collective salt coordinate. State the reference velocity frame and enforce electroneutrality / zero-current constraints as appropriate.
3. **Recover and reproduce the 25 °C reference model.** If full parameter tables and equations can be obtained, implement a separately tested Felmy–Weare/Pitzer reference calculation before attempting temperature extension. Do not reconstruct unavailable coefficients from abstracts.
4. **Establish temperature dependence.** Obtain or measure mutual/Onsager coefficients and relevant thermodynamic derivatives across 40–70 °C. A viscosity-only Stokes–Einstein scaling is not an adequate substitute for concentrated multicomponent electrolyte transport without validation.
5. **Reduce only after validation.** Derive an effective collective-salt coefficient from the matrix model under an explicitly stated composition-gradient path and reference frame. Quantify the reduction error over 15–38 g/kg.
6. **Close hydrodynamics independently.** Identify the exact channel/spacer geometry and select or validate a turbulent Sherwood correlation for that configuration. Do not pair a defensible diffusivity with an unvalidated mass-transfer coefficient and call the resulting CP prediction validated.
7. **Map to Nayar Reference Salinity.** Define the mapping from the transported composition state to Reference Salinity, including density and mass basis, before using interface salinity in Nayar's vapour-pressure expression.
8. **Treat Soret transport separately.** Add a thermal-diffusion term only in a clearly labelled research model with its own evidence and uncertainty. Do not fold it into an apparent Fickian diffusivity.
9. **Validation gates.** Require zero-flux equilibrium consistency; zero-flux CPC = 1; positive-flux monotonicity; bounded interface composition; electroneutrality; nonnegative entropy production / thermodynamic consistency; convergence tests; and sensitivity to diffusivity, Sherwood correlation, and composition-to-Reference-Salinity mapping.

## Final recommendation

**No numerical concentration-polarization implementation is approved at this stage.** The six-component Onsager/Pitzer model is the best theoretical route identified, but its high-concentration seawater parameterization is documented at 25 °C, not 40–70 °C. The next defensible step is to recover the full model and coefficient provenance, determine whether a temperature-dependent extension can be supported by primary data, and validate the reduced-order mapping. Until then, retain the no-CP baseline and report CP as an unresolved model limitation rather than filling the gap with tracer diffusivities, binary NaCl extrapolation, or Soret coefficients.

## References

1. Felmy, A.R. & Weare, J.H. (1991), Part I, DOI: 10.1016/0016-7037(91)90405-T.
2. Felmy, A.R. & Weare, J.H. (1991), Part II, DOI: 10.1016/0016-7037(91)90406-U.
3. Miller, D.G., Lee, C.M. & Rard, J.A., NaCl-MgCl2-H2O ternary mutual diffusion at seawater composition, OSTI record: https://www.osti.gov/servlets/purl/920867.
4. Poisson, A. & Papaud, A. (1983), DOI: 10.1016/0304-4203(83)90002-6.
5. Caldwell (1974), DOI: 10.1016/0011-7471(74)90041-2.
6. Xu, Y. & Torres, J. (2025), DOI: 10.1038/s44221-025-00428-5.
7. Nayar et al. (2016), DOI: 10.1016/j.desal.2016.02.024.
8. Wyon (2025), Lund University thesis, record 9198095.
