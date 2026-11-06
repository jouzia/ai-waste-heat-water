# Feed-side concentration-polarization correlation audit

**Date:** 2026-11-06  
**Status:** literature and applicability audit; no solver coupling  
**Related experiment:** `NAYAR-WYON-TEMP-SALINITY-DECOMPOSITION-2026-11-06`

## Research question

Can the bulk Reference Salinity used by the Nayar (2016) vapour-pressure branch be replaced by a defensible feed-side membrane-interface Reference Salinity estimate for the local Wyon DCMD surface calculation?

## Executive finding

The standard DCMD film-theory expression provides a useful *candidate framework*, but the available project inputs do not justify selecting a unique salt mass-transfer correlation or a validated seawater mutual-diffusion coefficient. The correct next step is therefore not to couple a guessed Sherwood correlation into the production solver.

The Wyon initial validation configuration explicitly specifies a rectangular channel (height 0.005 m, width 0.05 m, length 0.1 m), reports a hydraulic diameter of 0.003 m, and labels the flow turbulent (Table 6). However, the standard rectangular-duct relation 4A/P gives 0.00909 m from the stated height and width. This unresolved factor-of-3.03 hydraulic-diameter discrepancy affects Reynolds number and must be reconciled against the cited apparatus sources before any new transfer closure is selected. The thesis does not specify a spacer in Table 6; spacer presence in the underlying experimental apparatus remains unverified. The laminar Graetz–Leveque Sherwood expression is not appropriate for the reported nominal flow. A turbulent Sherwood expression remains only a candidate, not a validated Wyon-specific salt-transfer closure.

The audit therefore recommends a separately labelled, bounded *model-form sensitivity* only after the missing transport-property and geometry choices are documented. Wyon's default branch and the existing three-model Nayar decomposition remain unchanged.

## 1. Film-theory formulation found in DCMD literature

A common expression for a retained, nonvolatile solute is

`C_{f,m}/C_{f,b} = CPC = \exp(J_w/(\rho_f k_s))`

where:

- `J_w` is water mass flux in kg m^-2 s^-1;
- `rho_f` is feed density in kg m^-3;
- `k_s` is a solute-side mass-transfer coefficient in m s^-1;
- `C_{f,m}` and `C_{f,b}` are consistently defined feed-side membrane-surface and bulk solute concentrations.

The exponent is dimensionless. This expression appears in DCMD modelling literature, including the high-salinity DCMD study by Alkhudhiri et al. / Water (2020) and the 2023 polystyrene-membrane DCMD study. The 2026 critical review defines CPC as the surface-to-bulk concentration ratio and discusses why its impact is often smaller than temperature polarization in DCMD.

This is a film-model estimate, not a direct measurement. The 2026 critical review emphasizes that reliable experimental validation is difficult because local membrane-interface concentration, temperature, and vapour flux are rarely measured together.

## 2. Candidate Sherwood closures and their limits

### Laminar Graetz–Leveque

A frequently reproduced entry-length expression is

`Sh = 1.86 (Re Sc D_h/L)^{1/3}`

with `k_s = Sh D_s/D_h`.

The cited DCMD papers explicitly identify this as a laminar-flow expression. It is not appropriate for the present nominal feed-channel Reynolds numbers and must not be used merely because the geometry resembles a flat channel.

### Turbulent smooth-duct candidate

A commonly used turbulent candidate is

`Sh = 0.023 Re^{0.8} Sc^{1/3}`

with `k_s = Sh D_s/D_h`.

This is a useful screening correlation, not an established fit for Wyon's exact channel. Its use would require evidence that the hydraulic-diameter representation, wall boundary condition, and flow development are appropriate. A spacer-filled channel or a non-circular rectangular duct can have materially different local mass transfer.

### Why the two correlations cannot be treated as a generic bracket

The laminar and turbulent expressions represent different flow regimes and underlying hydrodynamics. They are not interchangeable lower/upper uncertainty bounds. Applying the laminar formula to a turbulent case would create false precision rather than a defensible sensitivity interval.

## 3. Reynolds-number audit for the existing nominal feed configuration

The current sweep uses:

- feed velocity: 1.85 m s^-1;
- hydraulic diameter: 0.003 m;
- feed temperature: 40, 50, 60, and 70 °C;
- Reference Salinity: 15 and 38 g kg^-1 for the endpoint check.

Reynolds numbers were recalculated from the project's existing Wyon Appendix A density and viscosity correlations:

`Re = rho u D_h / mu`.

| Feed temperature | Re at 15 g/kg | Re at 38 g/kg |
|---:|---:|---:|
| 40 °C | 8,244 | 7,943 |
| 50 °C | 9,788 | 9,412 |
| 60 °C | 11,405 | 10,949 |
| 70 °C | 13,083 | 12,543 |

These are the **reported-input Reynolds numbers**, calculated using Wyon's tabulated hydraulic diameter of 0.003 m. Wyon explicitly labels the Table 6 flow turbulent and applies a turbulent Nusselt relation. However, the tabulated rectangular dimensions (0.005 m × 0.05 m) imply D_h = 0.00909 m under D_h = 4A/P, yielding Reynolds numbers 3.03 times larger if that geometric value is used. Both interpretations are high-Reynolds-number cases, but the discrepancy must remain visible rather than silently choosing one value.

The exact rectangular dimensions and module length are therefore known from Wyon Table 6; the hydraulic-diameter inconsistency is unresolved. Table 6 does not state whether a spacer is present. The Nusselt closure used for heat transfer does not automatically validate a Sherwood closure for salt transfer. A smooth-duct turbulent Sherwood equation remains a candidate only after the effective hydraulic diameter, wall condition, spacer state, and salt diffusivity are established.

## 4. Salt diffusivity is a separate unresolved input

The mass-transfer coefficient requires a suitable mutual/effective salt diffusivity:

`Sc = mu/(rho D_s)`, `k_s = Sh D_s/D_h`.

The audit did not identify a sufficiently justified single `D_s(T,S)` for natural seawater over the entire 40–70 °C and 15–38 g/kg sweep.

The following distinctions matter:

1. Individual Na+ and Cl- tracer/ionic diffusion coefficients are not automatically the mutual diffusion coefficient of an electrically neutral salt mixture.
2. NaCl solution data are not identical to natural seawater, which contains multiple principal ions.
3. Infinite-dilution values are not automatically applicable at seawater concentrations.
4. A room-temperature value cannot be carried unchanged across the 40–70 °C range.
5. The 2023 NaCl transport-property study reports temperature- and molality-dependent ionic diffusion data, but these are ion-specific data and do not by themselves provide the natural-seawater mutual diffusivity required by this model.

Accordingly, no ionic diffusivity from that study has been silently substituted for a natural-seawater mutual diffusion coefficient.

## 5. Reference Salinity conversion is not a cosmetic detail

Nayar Eq. (5) expects Reference Salinity in g kg^-1. The film-theory concentration ratio must use a consistent concentration basis.

The implementation must not assume without derivation that a concentration ratio expressed in kg m^-3 is numerically identical to a ratio of Reference Salinity in g kg^-1. Density changes between bulk and membrane interface can matter. The conversion should be formulated through a salt mass fraction / solution mass balance, with the exact definition of the concentration variable stated and tested.

The current Nayar branch uses bulk Reference Salinity as an explicit proxy for the feed-interface and mean-pore salinity. This audit does not alter that behaviour.

## 6. Implications for the current Nayar–Wyon result

The previous 12-case decomposition found that, at 60 °C and 38 g kg^-1, the Nayar natural-seawater branch was 2.304% lower in mass flux than the Nayar pure-water diagnostic, under the bulk-salinity proxy. That is a conditional local-solver sensitivity result.

The present audit does not establish whether concentration polarization increases the magnitude of that correction. Higher feed-interface salinity would generally further depress water activity / vapour pressure, but the magnitude depends on the salt mass-transfer coefficient and the salinity-basis conversion. The 2026 critical review also cautions that concentration polarization is often a smaller contribution than temperature polarization in DCMD.

No numerical CPC, interface salinity, or revised Nayar flux is reported here because the inputs needed to support such a number are not yet established.

## 7. Required inputs before a coupled implementation

| Required item | Current status | Why it matters |
|---|---|---|
| Feed channel cross-section / aspect ratio | Wyon Table 6: rectangular, 5 mm × 50 mm, length 100 mm | Known dimensions; reconcile reported D_h = 3 mm against 4A/P = 9.09 mm |
| Spacer presence, geometry, and porosity | Not specified in Wyon Table 6; apparatus state unverified | Can alter mixing and local transfer substantially |
| Natural-seawater mutual/effective salt diffusivity over T/S range | Not selected | Required for Schmidt and Sherwood numbers |
| Applicable turbulent Sherwood correlation and validity range | Candidate only | Must match flow regime and channel geometry |
| Concentration variable and conversion to Reference Salinity | Needs explicit derivation | Avoids mixing mass concentration and mass-fraction bases |
| Local axial development / bulk salinity evolution | Not represented in the local solver | A local element cannot represent module-wide concentration rise |

## 8. Recommended next experiment

After reconciling the Table 6 hydraulic diameter and checking the cited apparatus for spacer details, and once the missing diffusivity/closure inputs are resolved, implement an opt-in research-only interface-salinity calculation with:

1. a clearly named diffusivity model and source domain;
2. at least one geometry-appropriate turbulent Sherwood closure;
3. a separately reported CPC and membrane-interface salinity;
4. explicit conversion to Nayar Reference Salinity;
5. tests for units, zero-flux limit (`CPC -> 1`), positive-flux monotonicity, and physical salinity bounds;
6. a sensitivity analysis over defensible correlation/property uncertainty;
7. no change to the default Wyon baseline.

If the channel geometry and seawater diffusivity cannot be established, retain an explicitly parameterized CPC sensitivity rather than claiming a predictive concentration-polarization model.

## Sources

1. *Direct Contact Membrane Distillation: A Critical Review of Transmembrane Heat and Mass Transfer Models* (2026), Sections 5.2 and relevant transport-property discussion. https://pmc.ncbi.nlm.nih.gov/articles/PMC12942289/
2. *Highly Saline Water Desalination Using Direct Contact Membrane Distillation (DCMD): Experimental and Simulation Study* (2020), Eqs. (12)–(18), film model and laminar Graetz–Leveque closure. https://www.mdpi.com/2073-4441/12/6/1575
3. *Porosity Effect of Polystyrene Membranes on Desalination Performance* (2023), Eqs. (11)–(18), CPC film model and laminar correlation. https://doi.org/10.3390/polym15081821
4. *Transport Properties of NaCl in Aqueous Solution and Hydrogen Solubility in Brine* (2023), temperature- and molality-dependent ion diffusion data. https://pmc.ncbi.nlm.nih.gov/articles/PMC10591480/
5. Wyon (2025), *Desalination utilizing data centre waste heat: A techno-economic study*, Appendix A and initial DCMD configuration. https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf
6. Nayar et al. (2016), *Thermophysical properties of seawater: A review and new correlations that include pressure dependence*, Eq. (5), DOI: 10.1016/j.desal.2016.02.024.
