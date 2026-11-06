# Correction: provenance of Xu & Torres (2025) seawater Soret coefficients

**Date:** 2026-11-06  
**Purpose:** clarify experiment provenance in the Soret applicability audit  
**Scope:** documentation correction only; no solver changes

## Correction to the prior summary

The two reported aggregate natural-seawater Soret coefficients are **not simply two extraction methods applied to one experiment at two temperatures**. Table 1 of Xu and Torres (2025) separates results from two distinct experimental configurations:

| Experiment | Natural seawater, all-cation effective coefficient | Interpretation |
|---|---:|---|
| Single-channel TSU recirculation | (3.8_{-0.6}^{+0.4}	imes10^{-3} mathrm{K}^{-1}) | Single-channel thermodiffusion unit; the main text reports this value at 42 °C |
| Lab-scale liquid Burgers cascade (LBC) | (1.7_{-0.3}^{+0.4}	imes10^{-3} mathrm{K}^{-1}) | Separate multichannel apparatus and operating configuration; Table 1 reports this as a separate experiment |

These values must not be described as alternative reductions of the same natural-seawater dataset or as a temperature-only variation. The paper separately reports component-specific estimates (Na+, Mg2+, K+, Ca2+) and the effective all-cation estimate; those are different composition coordinates under the authors' stated simplifications.

The main text's (3.8	imes10^{-3} mathrm{K}^{-1}) value is explicitly associated with the single-channel TSU recirculation experiment at 42 °C. The (1.7	imes10^{-3} mathrm{K}^{-1}) value is the all-cation result for the lab-scale LBC experiment in Table 1. The article's LBC measurement is a different flow/device architecture, not an independent temperature point for a single material coefficient.

## Consequence for transfer to DCMD

The range 1.7–3.8 × 10^-3 K^-1 is only a cross-configuration spread in reported effective estimates. It is **not**:
- a confidence interval for one Soret coefficient;
- a calibrated temperature dependence;
- a concentration dependence across the project's 15–38 g/kg range;
- a validated uncertainty interval for DCMD feed-side Soret transport.

The earlier illustrative product (S_TDelta T) may remain as an order-of-magnitude scale calculation only, but it must be labelled as spanning two different apparatus datasets. It is not a prediction for the Wyon membrane channel.

The transfer limitations remain decisive: different channel geometry and flow regime, effective binary reduction of a multicomponent electrolyte, cation-only ICP-MS concentration basis, and no validated (S_T(T,S_R)) law for the Wyon temperature/salinity domain.

## Source

Xu, S. and Torres, J.F. (2025). *All-liquid thermal desalination and brine concentration via multichannel thermodiffusion*. Nature Water 3, 617–631. DOI: [10.1038/s44221-025-00428-5](https://doi.org/10.1038/s44221-025-00428-5). See the main-text discussion of the single-channel TSU result and Table 1, which separately labels “Single-channel TSU recirculation” and “Lab-scale LBC” experiments.
