# Wyon initial DCMD channel geometry and hydraulic-diameter reconciliation

**Date:** 2026-11-06  
**Status:** source-data reconciliation; no solver changes  
**Related PR:** #81 — spacer-channel Sherwood correlation applicability

## Finding

A direct review of Wyon (2025), Section 3.2.2.1 and Table 6, resolves several geometry fields that were described too broadly as missing in the preceding audit. The initial Figure 9 validation configuration is specified as:

| Quantity | Wyon Table 6 |
|---|---:|
| Channel shape | Rectangular |
| Channel height | 0.005 m |
| Channel width | 0.05 m |
| Module length | 0.1 m |
| Reported hydraulic diameter | 0.003 m |
| Feed velocity | 1.85 m/s |
| Permeate velocity | 2.92 m/s |
| Flow classification | Turbulent |

Wyon states that the feed and permeate channel dimensions are the same and uses a turbulent-flow Nusselt relation in Eq. (10). The thesis identifies the initial setup as based on Termpiyakul et al. (2005) and Phattaranawik et al. (2003). The Table 6 description does not specify a spacer. That absence should be recorded as “not reported in this table/text,” not proof that the referenced experimental apparatus was spacer-free.

## Hydraulic-diameter consistency check

For a fully wetted rectangular duct, the standard geometric definition is:

`D_h = 4 A/P = 2wh/(w+h)`

Using the dimensions printed in Table 6:

`D_h,geometry = 2(0.05)(0.005)/(0.05+0.005) = 0.0090909 m`

This is not equal to the separately reported Table 6 value of 0.003 m. The geometry-derived value is approximately 3.03 times the tabulated hydraulic diameter.

This is an unresolved internal source-data inconsistency. Do not silently replace either value. Potential explanations (such as a different effective wetted perimeter, internal obstruction, or transcription/definition difference) require evidence from the cited experimental apparatus; none is established by the thesis table alone.

## Reynolds-number implications

The previous Reynolds table used the explicitly reported `D_h = 0.003 m` and the Wyon seawater density/viscosity correlations. Those values remain reproducible as the **reported-input Reynolds numbers**.

If the simple rectangular-duct geometric diameter of 0.0090909 m is used instead, Reynolds number scales linearly with hydraulic diameter at fixed `rho`, `u`, and `mu`, giving values approximately 3.03 times larger:

| Feed temperature | Re using reported 0.003 m, 15 g/kg | Re using geometric 0.00909 m, 15 g/kg | Re using reported 0.003 m, 38 g/kg | Re using geometric 0.00909 m, 38 g/kg |
|---:|---:|---:|---:|---:|
| 40 °C | 8,244 | 24,982 | 7,943 | 24,069 |
| 50 °C | 9,788 | 29,661 | 9,412 | 28,521 |
| 60 °C | 11,405 | 34,561 | 10,949 | 33,179 |
| 70 °C | 13,083 | 39,645 | 12,543 | 38,009 |

The geometry-derived values are diagnostic only; they are not a corrected baseline until the hydraulic-diameter definition is reconciled against the experimental source. Both calculations place the nominal case in a high-Reynolds-number regime under the respective definitions, but neither validates a salt Sherwood correlation.

## Spacer and correlation transfer

Wyon's Table 6 explicitly labels the flow turbulent and Eq. (10) applies a turbulent Nusselt correlation. The thesis does not list spacer dimensions or state in Table 6 that a spacer is present. References [55] and [56] should therefore be checked for apparatus details before treating spacer-filled-channel literature as directly representative.

Even if the channel is empty, the heat-transfer Nusselt closure does not automatically establish the salt Sherwood closure. A Chilton–Colburn analogy or empirical Sherwood relation would still need a justified diffusivity, matching geometry/flow regime, and an appropriate validation basis. If the original experimental channel used a spacer, the spacer-specific transfer evidence becomes essential.

## Required source reconciliation

1. Inspect the full methods/apparatus details in Termpiyakul et al. (2005), DOI 10.1016/j.desal.2004.11.019.
2. Inspect Phattaranawik et al. (2003), DOI 10.1016/S0376-7388(02)00498-2, for channel geometry and any spacer or effective hydraulic-diameter convention.
3. Determine why Wyon Table 6 lists 0.003 m while the tabulated rectangular dimensions yield 0.00909 m under `4A/P`.
4. Keep both Reynolds-number interpretations in the audit record until this discrepancy is resolved.
5. Do not use the discrepancy as a reason to modify the model silently or to select a Sherwood closure.

## Scope and model decision

This reconciliation changes no code, no model input, and no reported Nayar/Wyon flux. The Wyon default and three-model decomposition remain unchanged. The current bulk Reference Salinity remains a proxy; no membrane-interface salinity or CPC is calculated.

## Sources

1. Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*, Section 3.2.2.1, Table 6, Eqs. (9)–(11), and references [55]–[56]. https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf
2. Termpiyakul, P., Jiraratananon, R., & Srisurichan, S. (2005). *Heat and mass transfer characteristics of a direct contact membrane distillation process for desalination*. Desalination 177, 133–141. DOI: 10.1016/j.desal.2004.11.019.
3. Phattaranawik, J., Jiraratananon, R., & Fane, A. G. (2003). *Heat transport and membrane distillation coefficients in direct contact membrane distillation*. Journal of Membrane Science 212, 177–193. DOI: 10.1016/S0376-7388(02)00498-2.


## Additional distinction from the two cited apparatus studies

The two references behind Wyon Table 6 should not be collapsed into one flow-regime claim:

- Termpiyakul et al. (2005), Wyon reference [55], reports feed crossflow velocities of 1.85–3.7 m/s and explicitly describes the investigated range as turbulent. The 1.85 m/s Wyon feed velocity is consistent with the lower end of that range.
- Phattaranawik et al. (2003), Wyon reference [56], studies both laminar and turbulent modules and reports that the flow pattern in its **spacer-filled channel** was probably transitional rather than turbulent.

This is a material apparatus distinction. It does not prove that Wyon's Table 6 configuration is spacer-filled, nor that the 2003 spacer-filled channel is geometrically identical to the 2005 apparatus. It does show why the shared velocity value alone cannot identify the flow regime or spacer state. The original apparatus details and the hydraulic-diameter discrepancy still need to be reconciled before a Sherwood closure is selected.

The 2023 spacer-channel review independently defines the hydraulic diameter for an empty non-circular channel as (4A/P), while a net-type spacer requires a different effective hydraulic-diameter expression based on spacer voidage, thickness, and filament diameter. This reinforces the need to establish whether the quoted 3 mm value is an empty-duct or spacer-adjusted diameter.


## Primary-source cross-check: Phattaranawik et al. (2003) module table

A further check of the full-text Phattaranawik, Jiraratananon & Fane (2003) paper cited by Wyon resolves the origin of a particularly important geometry mismatch. Its Table 1 reports **two distinct PMMA modules**, not one geometry with a single hydraulic diameter:

| Source module | Width | Length | Height | Hydraulic diameter | Effective membrane area |
|---|---:|---:|---:|---:|---:|
| Laminar-flow module | 0.050 m | 0.100 m | 0.005 m | 0.00909 m | 0.005 m² |
| Turbulent-flow module | 0.003 m | 0.100 m | 0.003 m | 0.003 m | 0.0003 m² |

These entries are transcribed from the source paper's Table 1. The laminar module's hydraulic diameter is exactly the value obtained from the rectangular-duct relation (4A/P=2wh/(w+h)) using 50 mm × 5 mm. The turbulent module is a separate, much narrower 3 mm × 3 mm channel; its 3 mm hydraulic diameter and 0.0003 m² area are internally consistent with its own listed geometry.

The Wyon Table 6 combination previously transcribed in this audit—50 mm width, 100 mm length, 5 mm height, but 3 mm hydraulic diameter and 0.0003 m² area—matches a **cross-combination of the laminar module's dimensions and the turbulent module's hydraulic diameter/effective area** in Phattaranawik et al. (2003).

This is stronger than a generic discrepancy between a rectangular duct formula and a tabulated value. It suggests a possible source-table row/column or module-identity conflation. It is not yet proof of how the Wyon table was assembled: Wyon also cites Termpiyakul et al. (2005), and the precise provenance of each Table 6 field must be checked against that study's apparatus. The correct scientific status is therefore **probable cross-module geometry conflation, pending independent confirmation from Termpiyakul et al.**, not a silently corrected Wyon input.

### Consequences

1. Do not use the mixed Wyon geometry tuple as if it described one physically consistent rectangular channel.
2. Preserve both source module rows as distinct configurations.
3. Do not substitute the 3 mm turbulent-module hydraulic diameter or 0.0003 m² active area into a 50 mm × 5 mm × 100 mm channel.
4. Recalculate Reynolds numbers only after choosing and documenting the actual source module; the reported 1.85 m/s velocity must also be associated with the correct module and cross-sectional flow area.
5. The original 2003 paper's discussion says its spacer-filled channel was probably transitional rather than turbulent. This classification pertains to that study's spacer-filled apparatus and must not be assigned automatically to the separate empty-channel or Termpiyakul configuration.
6. No Nusselt or Sherwood closure, solver input, or reported Nayar/Wyon result is changed by this audit.

### Source record

- Phattaranawik, J., Jiraratananon, R. & Fane, A.G. (2003). “Heat transport and membrane distillation coefficients in direct contact membrane distillation.” *Journal of Membrane Science*, 212, 177–193. DOI: 10.1016/S0376-7388(02)00498-2. The accessible full-text source contains Table 1 module dimensions and the experimental discussion of the spacer-filled channel flow classification: https://elibrary.tsri.or.th/fullP/BGJ4380027/BGJ4380027_s02.pdf
- Wyon (2025), thesis cited above, Table 6 and Section 3.2.2.1: https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf
- Termpiyakul et al. (2005), DOI 10.1016/j.desal.2004.11.019. The accessible abstract confirms the PVDF membrane and operating velocity/temperature range, but does not resolve the Table 6 channel-dimension tuple or spacer state: https://www.lenntech.com/abstracts/1434/heat-and-mass-transfer-characteristics-of-a-direct-contact-membrane-distillation-process.html
