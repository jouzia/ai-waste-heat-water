# Wyon (2025): Nayar seawater vapour-pressure and pure-water coefficient audit

**Date:** 2026-11-04  
**Scope:** Documentation-only. No physical model code, solver constraints, coefficients or scenario outputs changed.

## Executive finding

Wyon (2025), Appendix A Eq. A9, applies the pure-water saturation-pressure equation to both seawater feed and pure-water permeate, stating that the seawater formulae in Sharqawy et al. (2010) were not valid over the desired 40–100 °C range.

Two equation issues are now documented:

1. Wyon Eq. A9 copies the Sharqawy 2010 pure-water coefficient a3 = -4.846e-2. Nayar et al. (2016), Eq. 6, later use a3 = -4.8640e-2, with slightly updated precision for the other coefficients. Direct evaluation of the printed coefficient sets gives a **+5.09% to +6.20%** Wyon-over-Nayar difference in pure-water vapour pressure from 40 to 100 °C.
2. Nayar et al. (2016), Eq. 5, provide a direct salinity-dependent seawater vapour-pressure relation based on natural-seawater primary data. At Wyon's rounded nominal salinity of 38 g/kg, it gives a seawater/pure-water pressure ratio of **0.979843**, or a 2.0157% depression at the same temperature.

These are property-boundary findings, not DCMD flux errors. The paired Nayar pure-water Eq. 6 and natural-seawater Eq. 5 should be treated as one alternative property formulation for a future matched-condition sensitivity run. Do not change the model until Wyon's coupled DCMD solution is independently reproduced.

## 1. Wyon source

Wyon Table 2 reports Barcelona seawater salinity as approximately **38 g/kg**, converted from practical salinity according to Sharqawy et al. (2010). Appendix A states that salinities marked S are in kg/kg.

Wyon Appendix A Eq. A9 explicitly uses the pure-water vapour-pressure equation for both seawater and pure water because the seawater formulae in the cited 2010 reference were considered invalid over 40–100 °C. Thus the published boundary condition does not apply a salinity depression to feed-side vapour pressure.

## 2. Pure-water coefficient discrepancy

Wyon Eq. A9 / Sharqawy 2010 Eq. 53 print:

~~~text
a1=-5800; a2=1.391; a3=-4.846e-2
a4=4.176e-5; a5=-1.445e-8; a6=6.545
~~~

Nayar 2016 Eq. 6 prints:

~~~text
a1=-5800; a2=1.3915; a3=-4.8640e-2
a4=4.1765e-5; a5=-1.4452e-8; a6=6.5460
~~~

Direct evaluation, T = t + 273.15 K:

| Temperature | Wyon Eq. A9 | Nayar 2016 Eq. 6 | Wyon relative to Nayar |
|---:|---:|---:|---:|
| 40 °C | 7.767 kPa | 7.391 kPa | +5.09% |
| 60 °C | 21.053 kPa | 19.963 kPa | +5.46% |
| 80 °C | 50.223 kPa | 47.456 kPa | +5.83% |
| 100 °C | 107.805 kPa | 101.511 kPa | +6.20% |

This establishes a discrepancy between the equations as printed. It does not establish whether Wyon's unpublished code exactly implements the printed coefficients. It also does not imply a corresponding percentage error in DCMD flux.

## 3. Direct natural-seawater correlation

Nayar et al. (2016), Eq. 5:

~~~text
p_v,sw(T,S) = p_v,w(T) * exp(-4.58180e-4*S - 2.04430e-6*S^2)
~~~

Here S is Reference Salinity in **g/kg**, not kg/kg. The paired pure-water function is Nayar Eq. 6.

The main Eq. 5 is fitted to Grunberg's **natural-seawater** primary data. Nayar report validity 0–180 °C and 0–160 g/kg, maximum absolute deviation 0.26%, and average absolute deviation 0.06%. The primary data span 20–180 °C; extrapolation below 20 °C has a separately estimated uncertainty of 0.91%. Wyon's 40–100 °C case-study range is within the primary-data temperature range.

MIT's Seawater Properties Library exposes SW_Psat(T,S) and documents a function range of 0–180 °C and 0–160 g/kg; posted code version 3.1.5 is dated 7 August 2024.

**Important correction:** the ~1.5% natural-vs-Ca-free difference in Nayar concerns the separate Ca-free artificial-seawater correlation in Appendix C. It must not be added as an uncertainty term to the main natural-seawater Eq. 5.

## 4. Salinity convention and calculation

Wyon's rounded Table 2 value (~38 g/kg) is the nominal reproduction input unless the underlying Port of Barcelona measurement is recovered at higher precision.

~~~text
p_v,sw / p_v,w
  = exp(-4.58180e-4*38 - 2.04430e-6*38^2)
  = 0.9798431
~~~

Thus Nayar Eq. 5 estimates seawater vapour pressure 2.0157% below pure-water vapour pressure at the same temperature.

If 38 were instead a raw Practical Salinity value S_P, TEOS-10 gives S_R = (35.16504/35)S_P = 38.1792 g/kg, which yields a 2.0265% depression. Do not substitute this for Wyon's already-converted rounded 38 g/kg without the original unrounded observation.

## 5. Relation to BPE route

Sharqawy 2010 Eq. 36 provides a broad-range boiling-point-elevation correlation. It remains a useful independent cross-check, but the direct Nayar Eq. 5 is the preferred seawater pressure relation. The earlier BPE-derived estimate (~2.01–2.02%) is numerically close to Nayar's 2.0157% at 38 g/kg.

## 6. Limits and reproduction sequence

Established:
- Wyon uses pure-water pressure for both streams in Eq. A9.
- The printed Wyon/Sharqawy 2010 pure-water equation differs from Nayar 2016 Eq. 6 by +5.09% to +6.20% over 40–100 °C.
- Nayar 2016 Eq. 5 is a natural-seawater correlation applicable to Wyon's temperature and salinity range.
- At 38 g/kg, Eq. 5 gives p_v,sw/p_v,w = 0.979843.

Not established:
- Neither vapour-pressure difference is a DCMD flux-error estimate.
- Impacts on membrane-surface temperatures, heat flux, mass flux, module production, annual production or pump sizing have not been calculated.
- Wyon's complete DCMD solver has not been independently reproduced or experimentally validated.

Next sequence:
1. Recover the unrounded Port of Barcelona salinity observation and its original scale.
2. Reproduce Wyon's salinity conversion and printed Eq. A9 as the historical baseline.
3. Independently verify pure-water pressure against Nayar Eq. 6 and a recognised pure-water reference.
4. Reproduce the coupled DCMD surface-temperature and heat-transfer solver.
5. Add paired Nayar Eq. 6 + Eq. 5 as a separate sensitivity case, using g/kg Reference Salinity.
6. Compare membrane-surface vapour pressure, mass flux and heat flux at matched conditions; keep the historical baseline unchanged.

## References

1. Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University. [Official thesis PDF](https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf).
2. Nayar, K.G., Sharqawy, M.H., Banchik, L.D., and Lienhard V, J.H. (2016). “Thermophysical properties of seawater: A review and new correlations that include pressure dependence.” *Desalination*, 390, 1–24. [DOI: 10.1016/j.desal.2016.02.024](https://doi.org/10.1016/j.desal.2016.02.024).
3. MIT. *Thermophysical properties of seawater*, code version 3.1.5 (7 August 2024). [Library](https://web.mit.edu/seawater/).
4. Millero, F.J., Feistel, R., Wright, D.G., and McDougall, T.J. (2008). “The composition of Standard Seawater and the definition of the Reference-Composition Salinity Scale.” *Deep-Sea Research Part I*, 55, 50–72. [DOI: 10.1016/j.dsr.2007.10.001](https://doi.org/10.1016/j.dsr.2007.10.001).
5. Sharqawy, M.H., Lienhard V, J.H., and Zubair, S.M. (2010). “The thermophysical properties of seawater: A review of existing correlations and data.” *Desalination and Water Treatment*, 16, 354–380. [DOI: 10.5004/dwt.2010.1079](https://doi.org/10.5004/dwt.2010.1079).
