# Wyon Table 6/Table 7 hydraulic-diameter provenance audit

**Date:** 2026-11-06  
**Status:** source reconciliation; no solver changes  
**Related records:** `FEED_CONCENTRATION_POLARIZATION_CORRELATION_AUDIT_2026-11-06.md`, `WYON_INITIAL_CHANNEL_GEOMETRY_RECONCILIATION_2026-11-06.md`, `SPACER_CHANNEL_TRANSFER_CORRELATION_ADDENDUM_2026-11-06.md`

## Executive finding

A closer reading of Wyon (2025) Section 3.2.2 resolves an important source-provenance ambiguity:

- **Table 6 is the initial thermodynamic model / Figure 9 validation configuration**, based on the experimental setup described in references [55] and [56].
- **Table 7 is the later final case-study configuration**, based on references [55] and [58]. Wyon explicitly states that the setup and membrane characteristics are based on [58], while the velocities are the only remaining characteristics from [55], retained to maintain turbulent flow.

These are distinct configurations and must not be conflated in the research code or in the CPC audit. The existing 12-case Wyon/Nayar local-solver sweep uses the Table 6 PVDF configuration; it is a local sensitivity experiment tied to the initial/validation setup, not a simulation of Wyon's final Table 7 case-study module.

## Table 6: initial / validation configuration

Wyon Table 6 reports:

| Parameter | Value |
|---|---:|
| Shape | Rectangular |
| Height | 0.005 m |
| Width | 0.05 m |
| Module length | 0.1 m |
| Hydraulic diameter | 0.003 m |
| Feed velocity | 1.85 m/s |
| Permeate velocity | 2.92 m/s |
| Flow label | Turbulent |
| Membrane | PVDF |
| Thickness | 126 µm |
| Porosity | 75% |
| Pore size | 0.22 µm |
| Area | 0.0003 m² |
| Membrane thermal conductivity | 0.041 W/(m K) |

For an unobstructed rectangular duct, `D_h = 4A/P = 2wh/(w+h)`. With `h=0.005 m` and `w=0.05 m`, this gives:

`D_h = 2(0.005)(0.05)/(0.005+0.05) = 0.0090909 m`.

This differs from Wyon's reported 0.003 m by a factor of approximately 3.03. The thesis does not explain this discrepancy in the Table 6 description. Because Table 6 is explicitly a theoretical input configuration based on two references, the discrepancy should be recorded as an unresolved input/provenance inconsistency—not treated as proof of an unreported spacer or a measured channel geometry.

The Table 6 flow label “Turbulent” and the 1.85 m/s velocity are attributed to a combined setup based on [55,56]. However, reference [56] reports that flow in its spacer-filled channel was probably transitional rather than turbulent. Reference [55] independently describes its experimental velocity range (1.85–3.7 m/s) as turbulent. These statements concern different experimental conditions/configurations and should not be merged into one universal regime classification.

## Table 7: final case-study configuration

Wyon Table 7 reports:

| Parameter | Value |
|---|---:|
| Shape | Rectangular |
| Height | 0.002 m |
| Width | 0.2 m |
| Module length | 0.5 m |
| Hydraulic diameter | approximately 0.004 m |
| Feed velocity | 1.85 m/s |
| Permeate velocity | 2.92 m/s |
| Membrane | PTFE |
| Thickness | 77 µm |
| Porosity | 89% |
| Pore size | 0.45 µm |
| Area | 0.1 m² |
| Membrane thermal conductivity | 0.031 W/(m K) |

The unobstructed rectangular-duct hydraulic diameter from the Table 7 dimensions is:

`D_h = 2(0.002)(0.2)/(0.002+0.2) = 0.0039604 m`,

which rounds to the approximately 0.004 m value reported in Table 7. Thus Table 7 is internally consistent with the standard empty-rectangular-duct definition, unlike Table 6.

Wyon explicitly says that the final setup and membrane characteristics are based on [58], while only the velocities are retained from [55] to maintain turbulent flow. This is a model-design decision, not evidence that the Table 7 channel geometry reproduces the apparatus of [55].

## Implications for the current repository

1. Keep the existing Table 6-based local surface-solver benchmark and Nayar/Wyon decomposition unchanged. They are tied to the initial PVDF/validation configuration.
2. Do not replace the Table 6 hydraulic diameter with 0.00909 m without identifying whether the 0.003 m value was intended to represent a different effective geometry or was a source/transcription error.
3. Do not use Table 7's approximately 0.004 m hydraulic diameter together with Table 6's PVDF membrane properties and call the result Wyon's final case-study configuration. Table 7 is a different configuration with PTFE and different dimensions.
4. If a separate final-case-study model is later added, implement Table 7 as a separate named configuration, preserving its PTFE properties, geometry, length, and hydraulic diameter.
5. A salt Sherwood closure still requires its own justified diffusivity and transfer-correlation basis. Wyon's use of a turbulent Nusselt correlation and smooth-channel pressure-drop relation does not itself validate a concentration-polarization closure.
6. Keep both the reported Table 6 Reynolds values (using 0.003 m) and geometry-derived diagnostic values (using 0.00909 m) visible in the audit record. They answer different assumptions and must not be silently interchanged.

## Literature and source notes

- Wyon (2025), Section 3.2.2, Table 6, Table 7, Eqs. (9)–(11), and the paragraph immediately preceding Table 7. The thesis states that Table 6 is the initial thermodynamic setup based on [55,56], and that Table 7 is the final case-study setup based on [55,58], with velocities retained from [55].
- Termpiyakul, Jiraratananon & Srisurichan (2005), [55], *Heat and mass transfer characteristics of a direct contact membrane distillation process for desalination*, Desalination 177, 133–141, DOI: 10.1016/j.desal.2004.11.019. The abstract identifies 1.85–3.7 m/s as its turbulent-flow region.
- Phattaranawik, Jiraratananon & Fane (2003), [56], *Heat transport and membrane distillation coefficients in direct contact membrane distillation*, Journal of Membrane Science 212, 177–193, DOI: 10.1016/S0376-7388(02)00498-2. Its abstract identifies the spacer-filled-channel flow pattern as probably transitional rather than turbulent.
- Ettouney, Almutairi & Aljuaidiyah (2025), [58], *Modeling and analysis of large-scale direct contact membrane distillation and parabolic trough concentrated solar power*, Desalination and Water Treatment 321, 100987. Wyon cites this as the basis for the Table 7 final configuration.
- Wyon thesis official record: https://lup.lub.lu.se/student-papers/record/9198095
- Wyon thesis PDF: https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf

## Decision

This audit resolves configuration provenance and identifies a Table 6 hydraulic-diameter inconsistency. It does not establish a corrected Table 6 hydraulic diameter, prove spacer presence in Table 6, or justify a Sherwood correlation. No source-faithful default, numerical result, or existing experiment is changed.


## Further distinction: Table 7 is a hybridized configuration, not a verbatim reproduction of reference [58]

The cited Ettouney et al. (2025) paper [58] gives the same Table 7 membrane/channel dimensions (PTFE, 77 µm, 89% porosity, 0.45 µm pore size, 0.5 m length, 0.2 m width, 0.002 m height). However, its own DCMD model specifies feed and permeate flow rates of 10 L/min per element and explicitly assumes laminar one-dimensional channel flow because its Reynolds numbers are below 2300.

Wyon states that the Table 7 geometry and membrane characteristics are based on [58], but the velocities 1.85 m/s and 2.92 m/s are retained from [55] to maintain turbulent flow. Therefore Table 7 is a **hybridized design point**: [58] supplies the channel/membrane geometry and [55] supplies the higher velocities. It is not a reproduction of the complete operating condition or flow regime in [58].

This distinction matters for transfer-correlation selection. The fact that the Table 7 rectangular geometry yields a consistent (D_happrox4) mm does not mean the [58] laminar-flow correlations or the [55] turbulent-flow correlations can be transferred without qualification to Wyon's hybrid point. The actual Reynolds number must be calculated from the chosen geometry, velocity, temperature, and salinity, and the Sherwood closure must be justified separately.

For the current repository, this reinforces the decision to retain Table 6 and Table 7 as distinct named configurations if both are ever represented. It does not justify changing the current Table 6 local-solver benchmark.
