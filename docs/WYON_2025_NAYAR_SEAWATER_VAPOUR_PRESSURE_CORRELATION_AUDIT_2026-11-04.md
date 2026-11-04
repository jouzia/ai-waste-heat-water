# Wyon (2025): direct seawater vapour-pressure correlation audit

**Date:** 2026-11-04  
**Scope:** Documentation-only source and boundary-condition audit. No physical model code, equations, coefficients, solver constraints, or scenario outputs are changed.

## Executive finding

Wyon (2025) uses the pure-water saturation-pressure equation (Appendix A, Eq. A9) for both the seawater feed and pure-water permeate, explicitly stating that the seawater formulas available in the cited 2010 source were not valid over the model's desired 40–100 °C range.

A later and directly applicable seawater vapour-pressure correlation is available from Nayar et al. (2016), and is implemented in the MIT Seawater Properties Library as `SW_Psat(T,S)`. The correlation covers the temperature and salinity range relevant to Wyon's case study. It therefore provides a more direct candidate boundary condition than deriving seawater vapour pressure from the 2010 boiling-point-elevation correlation.

This is a literature-based correction candidate, not a reproduced Wyon model result. The flux impact must be evaluated only after the coupled DCMD surface-temperature and heat-transfer solution is independently reproduced.

## 1. Wyon source statements

Wyon's Table 2 reports Barcelona seawater salinity as approximately **38 g/kg**, noting that the value is converted from practical salinity according to Sharqawy et al. (2010). The Appendix states that salinities marked (S) are in kg/kg and that practical-salinity conversions are made when required.

Wyon's Appendix A, Eq. A9, gives pure-water vapour pressure as a function of absolute temperature and explicitly says this equation is used for both pure water and seawater because the seawater formulas provided in the cited 2010 reference were not valid over 40–100 °C.

The feed-side membrane vapour pressure is therefore not salinity-depressed in the published implementation described by Eq. A9. The same pure-water function is used for the permeate-side water.

## 2. Direct seawater correlation from Nayar et al. (2016)

Nayar et al. (2016), *Thermophysical properties of seawater: A review and new correlations that include pressure dependence*, DOI [10.1016/j.desal.2016.02.024](https://doi.org/10.1016/j.desal.2016.02.024), provide a direct seawater vapour-pressure relation:

```text
p_v,sw(T,S) = p_v,w(T) * exp(-4.58180e-4*S - 2.04430e-6*S^2)
```

where:
- (p_{v,sw}) is seawater vapour pressure;
- (p_{v,w}) is pure-water vapour pressure;
- (S) is salinity in **g/kg**, not kg/kg.

The source reports the correlation for approximately 20–180 °C and 0–160 g/kg. The MIT Seawater Properties Library exposes the corresponding `SW_Psat(T,S)` function and documents a function range of 0–180 °C and 0–160 g/kg. Its current posted code version is 3.1.5 (7 August 2024). The 40–100 °C and nominal ~38 g/kg Wyon case-study conditions are within the correlation's stated range.

The Nayar paper reports a maximum deviation of approximately 0.29% for the fitted primary dataset. It also cautions that natural-seawater data can differ from the Ca-free seawater fit by as much as approximately 1.5% at the same salinity. The correlation should therefore be treated as a literature-based engineering estimate, not as a composition-exact value for Barcelona seawater.

## 3. Salinity convention and nominal calculation

Wyon reports the already-converted and rounded value **~38 g/kg** in Table 2. That rounded table value is the appropriate nominal input for reproducing the thesis unless the underlying Port of Barcelona measurement is recovered at higher precision.

For (S=38 mathrm{g/kg}):

```text
p_v,sw / p_v,w
  = exp(-4.58180e-4*38 - 2.04430e-6*38^2)
  = 0.9798431
```

Thus the direct correlation estimates seawater vapour pressure to be **2.0157% lower** than pure-water vapour pressure at the same temperature.

A separate convention check: if a raw value of 38 were a Practical Salinity (S_P), rather than Wyon's already-converted rounded g/kg value, the TEOS-10 reference-salinity conversion would be:

```text
S_R = (35.16504 / 35) * S_P
    = 38.1792 g/kg
```

Using 38.1792 g/kg in the Nayar relation gives a 2.0265% depression. This is shown only to distinguish the two salinity conventions; it must not be substituted for Wyon's reported rounded 38 g/kg without recovering the original unrounded measurement.

## 4. Relation to the earlier boiling-point-elevation route

Sharqawy et al. (2010) Eq. 36 provides a BPE correlation with a broad temperature and salinity range. The earlier audit considered using BPE plus pure-water saturation pressure as an indirect seawater-vapour-pressure estimate. That remains a possible independent cross-check, but it is not the preferred correction now that the direct Nayar correlation and MIT `SW_Psat` implementation have been identified.

The earlier BPE-derived estimate of approximately 2.01–2.02% is numerically close to the direct Nayar result at nominal 38 g/kg. The direct correlation should be the primary candidate in subsequent work; BPE should be retained as a separate consistency check, with its own salinity-scale and temperature-inversion conventions documented.

## 5. What this does and does not establish

Established:
- Wyon applies pure-water vapour pressure to seawater feed and pure-water permeate in Eq. A9.
- A direct salinity-dependent correlation is available over Wyon's operating temperature range.
- At nominal 38 g/kg, the direct correlation gives a same-temperature seawater/pure-water vapour-pressure ratio of 0.979843.
- The Nayar correlation has a reported fit uncertainty and a separate natural-seawater composition caveat.

Not established:
- A 2.0157% change in vapour pressure is **not** a 2.0157% change in DCMD mass flux.
- The correction's impact on local membrane-surface temperatures, heat flux, mass flux, module production, annual freshwater production, or pump sizing has not been calculated.
- No claim is made that the Nayar correlation exactly represents the ionic composition of Barcelona seawater.
- No independent reproduction or experimental validation of Wyon's complete DCMD solver has been completed.

## 6. Reproduction sequence

1. Recover the unrounded Port of Barcelona salinity observation and confirm whether the source quantity is Practical Salinity, a mass concentration, or a mass fraction.
2. Reproduce Wyon's stated salinity conversion and preserve the units at every property-function boundary.
3. Reproduce the published pure-water Eq. A9 implementation and Wyon's coupled DCMD surface-temperature / heat-transfer calculation before changing the vapour-pressure boundary condition.
4. Add the Nayar 2016 direct seawater vapour-pressure correlation as a separate sensitivity case, using g/kg input.
5. Compare the resulting local membrane-surface vapour-pressure difference, mass flux and heat flux at matched conditions. Keep the original Wyon baseline unchanged.
6. Report the Nayar fit uncertainty and the natural-seawater composition caveat separately; do not fold them into an unsupported single confidence interval.

## References

1. Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University. [Official thesis PDF](https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf).
2. Nayar, K.G., Sharqawy, M.H., Banchik, L.D., and Lienhard V, J.H. (2016). “Thermophysical properties of seawater: A review and new correlations that include pressure dependence.” *Desalination*, 390, 1–24. [DOI: 10.1016/j.desal.2016.02.024](https://doi.org/10.1016/j.desal.2016.02.024).
3. MIT. *Thermophysical properties of seawater*, library code version 3.1.5 (7 August 2024). [Library and property-function ranges](https://web.mit.edu/seawater/).
4. Millero, F.J., Feistel, R., Wright, D.G., and McDougall, T.J. (2008). “The composition of Standard Seawater and the definition of the Reference-Composition Salinity Scale.” *Deep-Sea Research Part I*, 55, 50–72. [DOI: 10.1016/j.dsr.2007.10.001](https://doi.org/10.1016/j.dsr.2007.10.001).
5. Sharqawy, M.H., Lienhard V, J.H., and Zubair, S.M. (2010). “The thermophysical properties of seawater: A review of existing correlations and data.” *Desalination and Water Treatment*, 16, 354–380. [DOI: 10.5004/dwt.2010.1079](https://doi.org/10.5004/dwt.2010.1079).
