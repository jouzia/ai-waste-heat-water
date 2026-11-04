# Wyon (2025): fixed-interface vapour-pressure driving-force sensitivity

**Date:** 2026-11-04  
**Scope:** Equation-level diagnostic only. No coupled solver, mass-transfer coefficient, physical model code, or scenario output changed.

## Purpose

The prior audits identified (i) a difference between the pure-water vapour-pressure coefficient sets printed in Wyon (2025) Eq. A9 and Nayar et al. (2016) Eq. 6, and (ii) the availability of Nayar's direct natural-seawater Eq. 5. This note combines those two property formulations to quantify their effect on the **vapour-pressure driving force only**, while holding membrane-interface temperatures fixed.

This is not a reproduction of Wyon's coupled interface-temperature solver and is not a mass-flux or freshwater-production estimate.

## Method

Historical Wyon pressure function, evaluated exactly as printed in Appendix A Eq. A9:

~~~text
ln(p_v,w) = a1/T + a2 + a3*T + a4*T^2 + a5*T^3 + a6*ln(T)
a1=-5800; a2=1.391; a3=-4.846e-2
a4=4.176e-5; a5=-1.445e-8; a6=6.545
T = t + 273.15 K
~~~

Alternative Nayar 2016 property pair:

~~~text
ln(p_v,w) = a1/T + a2 + a3*T + a4*T^2 + a5*T^3 + a6*ln(T)
a1=-5800; a2=1.3915; a3=-4.8640e-2
a4=4.1765e-5; a5=-1.4452e-8; a6=6.5460

p_v,sw(T,S) = p_v,w(T) * exp(-4.58180e-4*S - 2.04430e-6*S^2)
~~~

For the feed-side salinity, use the 2020 Port of Barcelona open-water station MA20B: 37.743 PSU, converted with Sharqawy Eq. 3 to S_R = 37.92114696 g/kg. This is a provenance-backed example, not proof that Wyon selected this station.

At each fixed pair of interface temperatures:
- Wyon baseline: Δp_W = p_v,w,Wyon(T_f,m) − p_v,w,Wyon(T_p,m)
- Nayar alternative: Δp_N = p_v,sw,Nayar(T_f,m,S_R) − p_v,w,Nayar(T_p,m)

The interface temperatures are held identical between the two calculations. No change is made to the mass-transfer coefficient c, pore-air partial pressure, membrane temperature, heat-transfer coefficients, or any solver state.

## Results

| Feed interface | Permeate interface | Wyon Δp | Nayar Δp | Change in Δp |
|---:|---:|---:|---:|---:|
| 40 °C | 30 °C | 3.308 kPa | 2.992 kPa | −9.56% |
| 45 °C | 30 °C | 5.642 kPa | 5.159 kPa | −8.55% |
| 45 °C | 35 °C | 4.185 kPa | 3.776 kPa | −9.78% |
| 50 °C | 30 °C | 8.555 kPa | 7.863 kPa | −8.09% |
| 55 °C | 30 °C | 12.163 kPa | 11.207 kPa | −7.86% |
| 60 °C | 30 °C | 16.594 kPa | 15.311 kPa | −7.73% |

Across these illustrative interface-temperature pairs, the Nayar alternative reduces the same-state vapour-pressure driving force by approximately **7.7–9.8%**. For closer interface approaches, the percentage difference can be larger because the absolute driving force is smaller.

## Interpretation limits

1. This is not a predicted DCMD mass-flux change. In Wyon Eq. 14, flux is J = c Δp, and c itself depends on membrane temperature, pore-air partial pressure, diffusion coefficient, tortuosity, membrane geometry and other quantities. This diagnostic holds c fixed and changes only Δp.
2. The actual membrane-interface temperatures are unknown until Wyon's iterative surface-temperature / heat-transfer solution is independently reproduced.
3. The 2020 Port MA20B salinity is a plausible open-water reference, not a verified match to Wyon's exact feed sample.
4. The Nayar correlation is the main natural-seawater fit. Its reported maximum absolute deviation is 0.26% over its primary 20–180 °C dataset and 0–160 g/kg salinity range.
5. The Wyon/Nayar pure-water equation comparison is based on coefficients as printed. The thesis's unpublished Python implementation has not been inspected.
6. No result here should be propagated into module production, annual water output, pumping, economics or environmental impact without a coupled model reproduction.

## Next reproduction gate

1. Reconstruct the Wyon historical baseline from the thesis equations and final DCMD module dimensions.
2. Verify pure-water saturation pressure independently and preserve both the Wyon printed baseline and Nayar 2016 alternative.
3. Reproduce the coupled interface-temperature energy balance and mass-flux coefficient, including pore-air partial pressure.
4. Only after matching the published heat-flux validation curve should the Nayar property pair be run as a separate sensitivity.
5. Report changes in interface temperatures, Δp, c, flux and total heat flux separately.

## References

1. Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University. [Official thesis PDF](https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf).
2. Nayar, K.G., Sharqawy, M.H., Banchik, L.D., and Lienhard V, J.H. (2016). “Thermophysical properties of seawater: A review and new correlations that include pressure dependence.” *Desalination*, 390, 1–24. [DOI: 10.1016/j.desal.2016.02.024](https://doi.org/10.1016/j.desal.2016.02.024).
3. Port de Barcelona. *Water and sediment quality of the Port of Barcelona — Summary 2020*. Table 9, station MA20B salinity. [Official PDF](https://www.portdebarcelona.cat/sites/default/files/content/file/2021/09/28/1/valoracion-aguas_-2020.pdf).
4. Sharqawy, M.H., Lienhard V, J.H., and Zubair, S.M. (2010). “The thermophysical properties of seawater: A review of existing correlations and data.” Eq. 3 salinity conversion. [DOI: 10.5004/dwt.2010.1079](https://doi.org/10.5004/dwt.2010.1079).
