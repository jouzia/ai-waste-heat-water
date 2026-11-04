# Wyon 2025 seawater vapour-pressure treatment: correction and sensitivity audit

Date: 2026-11-04

## Finding

Wyon's Appendix A states that the pure-water saturation-pressure equation A9 was used for both pure water and seawater because the seawater vapour-pressure formulas in Sharqawy et al. (2010) were not valid over the desired 40–100 °C range. This is documented explicitly in the thesis (Appendix, Eq. A9).

The first part of the explanation is understandable: the direct seawater-vapour-pressure correlations tabulated in Sharqawy et al. (2010) have limited ranges:
- Eq. (30): one temperature (25 °C) and a restricted chlorinity range;
- Eq. (31): 100–180 °C and 35–170 g/kg;
- Eq. (32): 0–40 °C and 0–40 g/kg;
- Eq. (33): 0–40 °C and 0–40 g/kg.

However, the same Sharqawy et al. paper also provides Eq. (36), a boiling-point-elevation (BPE) correlation with stated validity of 0–200 °C and 0–0.12 kg/kg salinity, with reported accuracy ±0.018 K. The paper identifies Eq. (36) as a best-fit correlation based on Bromley et al.'s measured BPE data. This does not make Eq. (36) a direct seawater-vapour-pressure equation, but it provides a route to estimate seawater vapour pressure consistently from pure-water saturation pressure and BPE:
`p_v,sw(T,S) = p_v,w(T - BPE(T,S))`
where the temperature/salinity conventions and the BPE definition must be applied consistently. For rigorous implementation, solve the corresponding saturation-temperature relation rather than silently treating BPE as a direct vapour-pressure multiplier.

## Equation and range check

Sharqawy et al. (2010), Table 7, Eq. (36):

`BPE = A S^2 + B S`

`A = -4.584 × 10^-4 t^2 + 2.823 × 10^-1 t + 17.95`

`B = 1.536 × 10^-4 t^2 + 5.267 × 10^-2 t + 6.56`

Stated validity: `0 ≤ t ≤ 200 °C`, `0 ≤ S ≤ 0.12 kg/kg`; reported accuracy ±0.018 K. Here the source's salinity convention and temperature scale must be respected; Wyon's practical-salinity-to-mass-fraction conversion should be checked before direct substitution.

For an illustrative screening calculation at `S = 0.038 kg/kg` (38 g/kg, before any reference-composition conversion), Eq. (36) gives:
- 40 °C: BPE ≈ 0.380 K
- 45 °C: BPE ≈ 0.394 K
- 50 °C: BPE ≈ 0.409 K
- 55 °C: BPE ≈ 0.423 K
- 60 °C: BPE ≈ 0.438 K
- 65 °C: BPE ≈ 0.454 K

Using Wyon's Eq. A9 pure-water saturation-pressure expression at `T` and at `T - BPE` gives an illustrative seawater saturation-pressure depression of approximately 2.01–2.02% relative to pure water across 40–65 °C (about 0.156–0.534 kPa in absolute pressure over these paired points). This is a diagnostic of the vapour-pressure boundary condition, not a measured result and not a direct estimate of the resulting permeate-flux error.

## Why this matters to Wyon's DCMD calculation

Wyon's Eq. (14) calculates membrane vapour flux from the difference between feed-side and permeate-side membrane-surface vapour pressures. Appendix Eq. A9 is used for the vapour pressures. Applying pure-water saturation pressure to the saline feed side therefore overstates the feed-side vapour-pressure boundary condition relative to a salinity-aware calculation.

The exact change in predicted flux cannot be inferred from the 2.01–2.02% saturation-pressure comparison alone. It depends on the solved membrane-surface temperatures, permeate-side pressure, membrane mass-transfer coefficient, and the coupled heat/mass-transfer iteration. The model must be rerun with the salinity-aware boundary condition before quantifying a production or validation impact.

## Reproduction actions

1. Preserve Wyon's published pure-water-for-both-sides implementation as the baseline.
2. Reconstruct Eq. (36) exactly from the original PDF, including temperature scale and salinity convention.
3. Convert Wyon's local salinity from practical salinity to the source's reference-composition salinity where required; document the conversion and units.
4. Implement the BPE-derived seawater vapour-pressure relation as a separate sensitivity branch, with an explicit saturation-temperature inversion.
5. Compare feed-side interfacial vapour pressures at every converged operating point.
6. Rerun the coupled surface-temperature and flux solver; report changes in feed-side pressure, permeate flux, latent heat transfer, total heat flux, and annual product water separately.
7. Compare against the same experimental dataset and conditions used by Wyon. Do not call the sensitivity case validated merely because it uses a more salinity-aware correlation.
8. Keep uncertainty and correlation validity visible. The ±0.018 K BPE correlation accuracy does not include uncertainty from salinity-scale conversion, extrapolation of other properties, membrane parameters, or model structure.

## Research 2 implications

- This is a specific, traceable boundary-condition limitation in the Wyon DCMD baseline, not proof that the whole thesis model is invalid.
- It is a useful reproduction and sensitivity test for Research 2, but it does not establish novelty.
- Research 2 must not silently inherit the pure-water vapour-pressure approximation for saline feed.
- No Research 2 physical model equations, coefficients, solver constraints, or scenario outputs were changed by this audit.
