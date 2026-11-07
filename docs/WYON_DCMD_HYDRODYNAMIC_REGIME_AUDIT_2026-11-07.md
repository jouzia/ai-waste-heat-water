# Wyon DCMD hydrodynamic-regime and correlation-applicability audit

**Audit date:** 2026-11-07  
**Scope:** Wyon (2025) Section 3.2.2, Tables 6–7, Eqs. (9)–(12), and Eq. (22).  
**Status:** Evidence and applicability audit; no transport correlation or baseline parameter changed.

## Executive finding

The source-faithful implementation reproduces Wyon's stated turbulent-channel Nusselt expression and the Reynolds-number definition. However, the label "turbulent" alone is not enough to establish that the selected heat-transfer correlation is quantitatively applicable across every operating point.

For the initial Table 6 geometry, calculated feed Reynolds numbers span approximately 7.94×10^3–1.31×10^4 across 40–70 °C and Reference Salinity 15–38 g/kg. The permeate-side Reynolds number at 20 °C is approximately 8.73×10^3. These values straddle or fall below the commonly stated Re ≥ 10,000 lower bound for Dittus–Boelter/Colburn-type fully turbulent smooth-tube correlations. The source's Eq. (10) is a modified expression attributed to Termpiyakul et al. (2005), so the generic smooth-tube range is a diagnostic comparator, not proof that Eq. (10) is invalid.

The later Table 7 geometry increases hydraulic diameter to approximately 4 mm. At the same velocities, the calculated feed Reynolds range is approximately 1.06×10^4–1.74×10^4 and the 20 °C pure-water permeate Reynolds number is approximately 1.16×10^4. This shifts the nominal cases above 10,000, but does not establish transferability to a different rectangular-channel geometry or prove the correlation's range.

## Source configuration distinction

Wyon Table 6 describes the initial validation setup:
- Rectangular channel: 5 mm × 50 mm; length 0.1 m; hydraulic diameter 3 mm.
- Feed/permeate velocities: 1.85/2.92 m s⁻¹.
- PVDF, 126 μm thick, 75% porosity, nominal pore size 0.22 μm, membrane area 0.0003 m², membrane conductivity 0.041 W m⁻¹ K⁻¹.
- The source labels the flow turbulent.

Wyon Table 7 describes the later case-study configuration:
- Rectangular channel: 2 mm × 200 mm; length 0.5 m; hydraulic diameter approximately 4 mm.
- The velocities are retained from the earlier setup.
- PTFE, 77 μm thick, 89% porosity, nominal pore size 0.45 μm, membrane area 0.1 m², membrane conductivity 0.031 W m⁻¹ K⁻¹.

These are distinct configurations. They must not be combined into a single experimental validation geometry. The Table 7 setup retains selected velocities from the earlier source while changing channel dimensions and membrane properties.

## Correlation transcription

Wyon Eq. (10) is implemented as:

\[
Nu = 0.023\left(1+6\frac{D_h}{L}\right)Re^{0.8}Pr^{1/3}.
\]

Wyon Eq. (9) then gives:

\[
\alpha = \frac{Nu\,k}{D_h}.
\]

The code's implementation in `wyon_nusselt_number` matches this transcription. The exponent 1/3 is retained as printed; it should not be silently replaced by 0.3 or 0.4 from a different Dittus–Boelter convention. Wyon attributes Eq. (10) to Termpiyakul et al. (2005), not as an independently fitted correlation in this repository.

Reynolds numbers are calculated from Wyon Appendix A seawater/pure-water density and viscosity correlations and the source's velocities and hydraulic diameters:

\[
Re=\frac{\rho vD_h}{\mu}.
\]

### Calculated regime screen

| Configuration | Stream | Temperature | Reynolds number |
|---|---|---:|---:|
| Table 6, 3 mm hydraulic diameter | Feed, salinity 15–38 g/kg | 40–70 °C | 7,943–13,082 |
| Table 6, 3 mm hydraulic diameter | Pure-water permeate | 20 °C | 8,727 |
| Table 7, approximately 4 mm hydraulic diameter | Feed, salinity 15–38 g/kg | 40–70 °C | 10,591–17,443 |
| Table 7, approximately 4 mm hydraulic diameter | Pure-water permeate | 20 °C | 11,636 |

The ranges above are calculated from the stated Wyon Appendix A property equations, the stated velocities, and the stated hydraulic diameters. The range endpoints need not correspond to identical salinity-temperature pairs on both sides.

The length-to-diameter ratios are approximately 33.3 for Table 6 and 125 for Table 7. Published textbook treatments commonly state Re ≥ 10,000 for Dittus–Boelter-type fully developed turbulent flow, with Prandtl and L/D restrictions that vary by reference. This flags the Table 6 low-Re cases and the Table 6 permeate side for caution. The Table 6 L/D also falls below the stricter L/D ≥ 60 criterion sometimes reported, although it exceeds the L/D ≥ 10 criterion in other standard references.

## Interpretation and model decision

1. **Keep the Wyon Eq. (10) baseline unchanged.** Source fidelity is preferable to silently swapping in a different correlation.
2. **Do not describe the heat-transfer coefficients as independently validated.** The regime screen identifies cases where generic fully turbulent smooth-tube applicability criteria are not clearly satisfied.
3. **Do not infer spacer/channel effects.** The source configurations are rectangular channels, but the available dimensions do not establish spacer geometry, roughness, entrance conditions, or a validated spacer-specific Nusselt relation.
4. **Do not promote the current heat-transfer coefficients to universal DCMD correlations.** Their applicability is bounded by the source geometry, property correlations, and stated velocities.
5. **Keep a correlation-sensitivity study separate from the source-faithful baseline.** A defensible alternative requires a source with a documented geometry, Reynolds/Prandtl range, and comparable boundary conditions. A generic correlation comparison is a model-form sensitivity, not validation.
6. **Treat the Blasius pressure-drop calculation separately.** Wyon Eq. (22) uses a smooth-channel turbulent friction-factor expression. Its use also depends on the smooth-channel assumption and cannot represent unreported spacers, fittings, headers, or manifold losses.

## Reproduction notes

The Reynolds-number audit can be reproduced using the Appendix A correlations in `src/ai_water/wyon_2025_fluid_properties.py`, the Table 6 and Table 7 geometries and velocities in Wyon (2025), and the definition in Eq. (11). No empirical measurement has been added and no source parameters have been tuned.

## References

- Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University, report LUTFD2/TFEM--25/5229--SE, Section 3.2.2, Tables 6–7, Eqs. (9)–(12), (22), Appendix A. Official record: https://lup.lub.lu.se/student-papers/record/9198095
- Termpiyakul, P., Jiraratananon, R., & Srisurichan, S. (2005). Heat and mass transfer characteristics of a direct contact membrane distillation process for desalination. *Desalination*, 177, 133–141. DOI: 10.1016/j.desal.2004.11.019.
- Tosun, I. (2007). *Modeling in Transport Phenomena*, 2nd ed., Elsevier, discussion of Dittus–Boelter applicability. This is cited only for generic correlation applicability criteria, not as evidence validating Wyon Eq. (10).
