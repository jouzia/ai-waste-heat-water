# Seawater property-source audit for Malaguti AGMD reproduction

**Audit date:** 2026-10-27  
**Status:** Source identified; implementation not yet accepted.

## Decision

Use the official MIT Seawater Thermophysical Properties Library as the primary implementation reference for seawater properties, rather than transcribing isolated polynomial coefficients from OCR. The library page identifies code version 7 August 2024 and tables version 9 December 2023. It lists `SW_SpcHeat(T, S, P)` in J/(kg K) and `SW_LatentHeat(T, S)` in J/kg, with separate validity ranges. The library's overall advertised temperature/salinity envelope is not a substitute for checking each individual function's range.

Official source: https://web.mit.edu/seawater/  
Library page and function list: https://web.mit.edu/seawater/  
Primary references:
- Nayar, Sharqawy, Banchik & Lienhard (2016), *Desalination* 390, 1–24, DOI: https://doi.org/10.1016/j.desal.2016.02.024
- Sharqawy, Lienhard & Zubair (2010), *Desalination and Water Treatment* 16, 354–380, DOI / author manuscript record: https://dspace.mit.edu/entities/publication/0c55d19d-eb62-4e5f-8a12-a71c2b53f36a

## Important specific-heat correction

The MIT library explicitly warns that the original Jamieson et al. coefficient contains a typo. It states that the (b_3) coefficient should be (-3.15\times10^{-6}), not positive, and that the corrected Nayar et al. coefficient is:

```text
B = -6.913 + 7.351e-1*S - 3.15e-3*S^3
```

This is the correction as documented by MIT; do not substitute an OCR-transcribed coefficient set without checking the full equation's variable definitions and units in the source code.

The 2010 review's Table 3 gives a Jamieson specific-heat polynomial in (T_{68}), with output in kJ/(kg K), and a stated range (273.15<T_{68}<453.15) K and (0<S_P<180) g/kg. Its convention uses the ITS-68 temperature scale and reference-composition salinity. Those conventions must be applied exactly if implementing that older correlation. The newer MIT library's callable function instead documents temperature in °C, salinity in g/kg, pressure in MPa, and output in J/(kg K). These two interfaces must not be mixed.

## Latent heat

The MIT library lists `SW_LatentHeat(T, S)` in J/kg, valid for 0–200 °C and 0–240 g/kg, at its defined pressure convention (P_0). The 2010 review proposes a seawater latent-heat relation based on pure-water latent heat and salinity. Before choosing between that older expression and the current library function, inspect the exact property method used by Malaguti et al.; match the source method rather than selecting whichever gives a closer result.

## Retrieval status and next action

The official MIT webpage is accessible and exposes the archive link, but the available retrieval interface did not return the ZIP archive contents. No MIT library source code has therefore been locally inspected or vendored in this audit. No correlation implementation or numerical result should be described as verified yet.

Next gate:
1. Obtain the official archive through a browser/download route and record its version and license.
2. Inspect the exact implementation of `SW_SpcHeat` and `SW_LatentHeat`.
3. Determine from Malaguti's paper whether (c_h), (c_c), and (h_{vap}) are evaluated at inlet, outlet, or representative temperatures, and what salinity each represents.
4. Implement only the documented source conventions and test known table values or official library outputs.
5. Proceed to the AGMD coupled solver only after the property layer has independent reference tests.

## Scope guard

This is a source-selection and convention audit, not validation of the thermodynamic model. No recovery anchor has been reproduced. No empirical validation, net-water benefit, or novelty claim follows from this note.
