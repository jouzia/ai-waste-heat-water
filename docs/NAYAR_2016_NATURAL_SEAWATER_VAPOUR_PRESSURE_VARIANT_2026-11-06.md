# Nayar (2016) Natural-Seawater Vapour-Pressure Variant

**Date:** 2026-11-06  
**Status:** Isolated property-correlation implementation with reference-value tests. Not yet coupled into the Wyon DCMD solver and not an experimental DCMD validation.

## Purpose

Wyon (2025), Appendix A Eq. (A9), applies a pure-water saturation-pressure correlation to both the saline feed and pure-water permeate. This preserves the historical Wyon baseline, but it does not represent the reduction in water vapour pressure caused by dissolved salts.

Nayar et al. (2016) provide a direct natural-seawater vapour-pressure relation over a range that includes Wyon's 40-100 °C use case. This PR adds the paired Nayar pure-water and natural-seawater equations as a separate, independently tested property formulation. It does not change Wyon's existing implementation.

## Equations

Nayar et al. (2016), Eq. (6), calculate pure-water vapour pressure:

`p_{v,w}(T)=\exp(a_1/T+a_2+a_3T+a_4T^2+a_5T^3+a_6\ln T)`

with T in kelvin and coefficients:

| Coefficient | Value |
|---|---:|
| a1 | −5800 |
| a2 | 1.3915 |
| a3 | −4.8640 × 10⁻² |
| a4 | 4.1765 × 10⁻⁵ |
| a5 | −1.4452 × 10⁻⁸ |
| a6 | 6.5460 |

Nayar et al. (2016), Eq. (5), calculate natural-seawater vapour pressure:

`p_{v,sw}(T,S)=p_{v,w}(T)\exp(-4.58180\times10^{-4}S-2.04430\times10^{-6}S^2)`

Here S is **Reference Salinity in g/kg**. It is not practical salinity, a mass fraction in kg/kg, or NaCl concentration in mg/L.

The stated validity range is 0-180 °C and 0-160 g/kg. Nayar report maximum uncertainty of ±0.26% for the natural-seawater correlation within its stated range.

## Reference checks

The new implementation is tested against direct evaluations of the published coefficient set:

| Temperature | Nayar pure-water pressure |
|---:|---:|
| 0 °C | 0.611871 kPa |
| 20 °C | 2.341217 kPa |
| 40 °C | 7.390799 kPa |
| 60 °C | 19.962948 kPa |
| 80 °C | 47.455945 kPa |
| 100 °C | 101.511238 kPa |

At S = 38 g/kg:

`p_{v,sw}/p_{v,w}=0.9798431127`

This is a 2.0157% seawater vapour-pressure depression relative to Nayar's paired pure-water equation at the same temperature. At 60 °C, the resulting natural-seawater pressure is approximately 19.5606 kPa.

## Model boundary and integration plan

- The Wyon pure-water Eq. (A9) baseline remains unchanged.
- The Nayar implementation is an alternative property correlation, not a retroactive correction to the source transcription.
- No DCMD flux, membrane-interface temperature, total heat flux, module production, or Figure 9 error is inferred from the pressure ratio alone.
- The Nayar pure-water equation differs from Wyon's printed Eq. (A9) coefficients. Therefore, a coupled Nayar sensitivity run must use the paired Nayar pure-water and natural-seawater equations consistently, not combine the Nayar salinity multiplier with Wyon's pure-water coefficients without labelling that hybrid.
- A subsequent integration must define how salinity is applied at the feed membrane interface and within the mean-pore-pressure term. The bulk salinity must not be silently treated as membrane-surface salinity; concentration polarization is not represented by this property correlation.
- Before comparing to Figure 9, recover the exact Termpiyakul experimental concentration and distinguish Wyon's model output from the reference experiment.

## Reproduction

`pytest -q tests/test_nayar_2016_vapour_pressure.py`

## Sources

1. Nayar, K.G., Sharqawy, M.H., Banchik, L.D. & Lienhard V, J.H. (2016). “Thermophysical properties of seawater: A review and new correlations that include pressure dependence.” *Desalination*, 390, 1-24. DOI: 10.1016/j.desal.2016.02.024. The authors' final manuscript is available through MIT DSpace: https://dspace.mit.edu/entities/publication/f41d977b-998b-425d-8c56-4fbc645084ec.
2. MIT Seawater Properties Library, code version 3.1.5 (7 August 2024): https://web.mit.edu/seawater/.
3. Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University, Appendix A Eq. (A9): https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf.
