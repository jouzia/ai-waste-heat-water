# Property Provenance Gate for Malaguti AGMD Reference Solver (2026-10-28)

## Why the property source must be pinned

The Malaguti paper names Sharqawy et al. correlations for temperature- and salinity-dependent properties. The 2010 review is a relevant primary reference for the correlation family and includes a correction note for a coefficient in its specific-heat equation. The MIT seawater library now also cites the later review by Nayar et al. (2016), which incorporates pressure dependence, and lists its downloadable code archive as version 3.1.5 dated 2024-08-07.

Sources:
- Sharqawy, Lienhard & Zubair (2010), *Thermophysical properties of seawater: A review of existing correlations and data*, DOI 10.5004/dwt.2010.1079: https://doi.org/10.5004/dwt.2010.1079
- MIT Seawater Library, implementation/download page: https://web.mit.edu/seawater/
- MIT Seawater Library version history, version 3.1.5 (2024-08-07): https://web.mit.edu/seawater/Version_History_07Aug24-pdf-3a.pdf
- Nayar, Sharqawy, Banchik & Lienhard (2016), *Thermophysical properties of seawater: A review and new correlations that include pressure dependence*, DOI 10.1016/j.desal.2016.02.024.

## Provenance finding

The official MIT site confirms that a versioned library archive exists and that the library includes pressure-dependent seawater properties. The accessible code used in the exploratory solver was transcribed from a public mirror, not verified byte-for-byte against the official v3.1.5 archive. Therefore it must not be labeled “official MIT v3.1.5 implementation” or treated as exact source provenance.

The 2010 correlation review and 2016 pressure-dependent review are not interchangeable labels for an implementation. A reproduction must say which correlation equation/version was used, including pressure assumptions, temperature scale, salinity scale, validity range, and units. The code mirror's latent-heat expression also needs an explicit equation-level comparison against the chosen source before it is promoted to a trusted property function.

## Required property-call ledger

Complete this ledger from source evidence before closing the reproduction gate:

| Symbol | Fluid | Temperature argument | Salinity argument | Pressure | Source/version | Current status |
|---|---|---|---|---|---|---|
| c_h | Hot seawater | Inlet approximation supported for S2; exact AGMD call still to verify | Provisional 35 g/kg in diagnostic | Not independently fixed | Not version-verified | Open |
| c_c | Cold-channel seawater | Constant-channel assumption in SI; exact call still to verify | Provisional 35 g/kg in diagnostic | Not independently fixed | Not version-verified | Open |
| c_d | Pure distillate | Not explicitly fixed by the accessible SI text | 0 g/kg / pure water assumption | Not independently fixed | Placeholder constant used in diagnostic | Open |
| h_vap | Vaporization term | Evaluation temperature not explicitly fixed in accessible SI text | Seawater or pure-water interpretation needs equation context | Not independently fixed | Mirror formula only, not version-verified | Open |

## Solver verification requirements

The audit-only solver must remain separate from production thermodynamics. Before comparing computed recovery to the four Figure 4B read-offs, verify:

1. Equation residuals are small for every reported root.
2. The root satisfies physical bounds (positive recovery, valid temperature differences, no non-finite properties).
3. Multiple initial guesses converge to the same admissible root or all alternate roots are disclosed.
4. Units are tested at every boundary (J/kg, J/kg/K, °C, g/kg, dimensionless recovery).
5. The two source-text interpretations for ΔT_h,in (0.5 °C printed constraint vs 5 °C prose/main text) are reported as separate branches if both can be solved.
6. Source correlation code is compared against a versioned official source or independently evaluated published equations.
7. No parameter is adjusted to match the Figure 4B anchors.

## Gate decision

**Property provenance is not yet sufficient for a reproduction claim.** The published correlation family is identifiable, but the exact implementation/version and every property-call state are not established. The current solver is an algebra/numerical diagnostic only. Do not infer empirical validation, novelty, or net-water benefit from anchor proximity.
