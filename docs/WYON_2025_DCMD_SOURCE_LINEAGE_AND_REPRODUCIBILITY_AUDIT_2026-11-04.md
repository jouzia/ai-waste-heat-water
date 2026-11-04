# Wyon 2025 DCMD source-lineage and reproducibility audit

Date: 2026-11-04

## Purpose and status

This note traces the principal sources used by Annie Wyon's 2025 Lund University thesis, *Desalination utilizing data centre waste heat: A techno-economic study*, and records what can and cannot currently be reproduced from publicly accessible source material.

This is a literature and reproducibility audit only. It does not validate Wyon's model, reproduce its numerical results, or change the Research 2 physical model. The thesis itself reports a heat-flux discrepancy of up to approximately 11% against its selected experimental reference and states that the discrepancy was not resolved; it also notes that the experimental validation temperature range differs from the range used for case-study extraction.

## Source-lineage matrix

| Wyon reference | Role in thesis | What was independently checked | Reproducibility status / caution |
|---|---|---|---|
| [39] Qtaishat et al. (2008), DOI 10.1016/j.desal.2007.05.019 | Water-vapour diffusion coefficient in air; membrane/thermal-boundary-layer heat and mass transfer model context | Publisher abstract describes a numerical DCMD model for thermal boundary layers, interface temperatures, temperature-polarization coefficient, membrane mass-transfer coefficient and evaporation efficiency, solved against experimental observations | Abstract-level access only in this audit. Exact equation form, parameter definitions and validity range must be checked against full text before implementation. |
| [47] Sharqawy, Lienhard & Zubair (2010), DOI 10.5004/dwt.2010.1079 | Seawater thermophysical-property correlations used in the thesis appendix | MIT repository exposes the author manuscript; MIT's seawater-property site exposes a maintained code library (code version 7 Aug 2024; tables version 9 Dec 2023) with documented ranges and functions | Wyon's appendix records 2010-era correlations and states that pure-water vapour pressure was used for both pure water and seawater over the desired temperature range. The current MIT library includes a seawater vapour-pressure function over its stated range. This is a sensitivity/reproduction check, not proof the thesis implementation is erroneous: compare equations, salinity conventions, temperature scales, pressure assumptions and correlation validity before substituting. |
| [55] Termpiyakul, Jiraratananon & Srisurichan (2005), DOI 10.1016/j.desal.2004.11.019 | Initial DCMD module geometry and experimental validation reference | Publisher abstract confirms flat-sheet PVDF, 0.22 μm pore size, NaCl feeds 5,000–35,000 mg/L, feed 40–70°C, distillate 20°C, feed crossflow 1.85–3.7 m/s, distillate velocity 2.92 m/s; abstract reports membrane-distillation coefficient estimated from pure-water flux and reasonable agreement except at high feed concentration | Full article/raw experimental points were not obtained. The abstract confirms the membrane material/pore-size lineage but is insufficient to reproduce the plotted validation data or independently calculate Wyon's reported discrepancy. |
| [56] Phattaranawik, Jiraratananon & Fane (2003), DOI 10.1016/S0376-7388(02)00498-2 | Heat-transfer and membrane-distillation coefficient treatment | Publisher abstract and preview describe simultaneous heat/mass-transfer analysis, membrane thermal conductivity alternatives, and spacer effects | Full article and complete parameter tables not obtained. Do not infer the exact correlation or membrane-property implementation from the abstract alone. |
| [58] Ettouney, Almutairi & Aljuaidiyah (2025), DOI 10.1016/j.dwt.2025.100987 | Final PTFE DCMD module configuration used by Wyon | Open-access article/publisher-indexed full text confirms PTFE membrane: 77 μm thickness, 0.45 μm pore size, 89% porosity; channel length 0.5 m, width 0.2 m, height 0.002 m; system is a large-scale CSP/DCMD design for Kuwait | This is a different system boundary and heat source (CSP/power-plant thermal integration), not a data-centre waste-heat validation. Geometry transfer is traceable, but its use does not validate performance at Wyon's Barcelona operating conditions. |
| [61] Schock & Miquel (1987), DOI 10.1016/0011-9164(87)90107-X | Pressure-loss calculation cited by Wyon | Publisher abstract describes experimental pressure-drop and mass-transfer characteristics in spiral-wound elements and spacer-filled flow channels | Wyon applies a smooth-channel Blasius-type friction relation using hydraulic diameter. The source's spiral-wound/spacer-filled geometry is not automatically equivalent to Wyon's flat-channel module. Confirm friction-factor convention (Darcy vs Fanning), Reynolds-number range, hydraulic-diameter definition, spacer effects and applicability before treating pump duty as reproduced. |

## Important distinctions in the thesis model

1. **Two different membrane configurations appear.** The initial validation model is based on PVDF / 0.22 μm material lineage; the final case-study configuration is PTFE / 0.45 μm / 89% porosity. These must not be conflated when reconstructing validation or final production.
2. **Validation is not independent validation.** Wyon compares against the experimental source used to inform the initial model, reports an unresolved heat-flux discrepancy of up to about 11%, and acknowledges a mismatch between the experimental and case-study temperature ranges.
3. **The final module is literature-derived.** The PTFE geometry is consistent with the 2025 Ettouney et al. large-scale DCMD paper, but that paper's CSP/steam integration and 60°C/20°C design point differ from Wyon's data-centre case.
4. **Pump duty is especially sensitive to geometry.** A pressure-loss correlation sourced from spiral-wound/spacer-filled channels needs an explicit geometry/regime justification when applied to a flat-channel DCMD module.
5. **Seawater-property correlations need version control.** Wyon's appendix cites Sharqawy et al. (2010). MIT now publishes a maintained seawater-property package with updated tables and code. A faithful reproduction should first reproduce the thesis's stated equations, then run a separately labelled sensitivity case with the updated correlations; do not silently replace one with the other.
6. **Product water is not equivalent to net freshwater conserved.** Wyon's water output must remain distinct from seawater intake, brine/return flows, consumptive losses, auxiliary electricity water, and any demonstrable counterfactual freshwater displacement.

## Minimum reproduction protocol before any Research 2 engine change

- Transcribe the thesis's initial and final module tables separately, preserving units and source references.
- Reconstruct the heat-exchanger NTU calculation and verify hot/cold outlet temperatures and heat balance.
- Reconstruct the DCMD model in the same sequence: bulk-to-interface heat transfer, temperature polarization, vapour-pressure driving force, membrane mass transfer, latent plus conductive membrane heat flux, stream enthalpy balances, and salinity balance.
- Obtain the Termpiyakul experimental points or a traceable digitized dataset and compare only at matched feed salinity, inlet temperatures, flow velocities, membrane properties and module geometry.
- Report heat-flux and permeate-flux errors separately; do not treat a single heat-flux discrepancy as validation of every model subcomponent.
- Independently check the pressure-drop correlation and pump operating points using the actual flat-channel geometry and correct friction-factor convention.
- Reproduce the annual operating arithmetic under both 0.95 and 0.96 availability; preserve the thesis's stated 8,410 h/year as the 0.96-derived case, not as a universal value.
- Run a second, explicitly labelled property-correlation sensitivity case using the maintained MIT seawater-property library; document version, function, units, ranges and salinity/temperature conversions.
- Keep the output as a reproducibility audit until the calculations agree within a predeclared tolerance and all unresolved discrepancies are documented.

## Current conclusion

The source lineage is substantially clearer, but the numerical model is not yet independently reproducible. The most important open blockers are the unavailable raw/reference experimental data behind the Termpiyakul comparison, the applicability of the pressure-loss correlation to the flat-channel geometry, the exact property-correlation implementation/version, and the mismatch between validation and case-study operating ranges.

No Research 2 physical equations, coefficients, solver constraints or scenario outputs were changed by this audit.
