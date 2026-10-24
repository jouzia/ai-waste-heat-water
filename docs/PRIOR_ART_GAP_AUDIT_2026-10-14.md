# Prior-art gap audit — 2026-10-14

**Status:** Preliminary targeted audit, not a systematic review or novelty clearance.

## Decision

The broad project idea—using data-centre heat and/or desalination to reduce AI-infrastructure water impacts—is already represented in the literature. The manuscript must not claim to be the first data-centre desalination framework, first data-centre water-stress metric, first global data-centre water/heat-recovery analysis, or first waste-heat-assisted membrane-distillation study.

The narrow candidate contribution is an auditable counterfactual **operational blue-water consumption** ledger that explicitly couples (i) time-varying heat eligibility and membrane-distillation physics, (ii) incremental cooling and pumping burdens, (iii) electricity-related water factors with explicit consumption/withdrawal boundaries, and (iv) evidence-labelled uncertainty and failure envelopes. This is only a candidate contribution: it is not established until the complete model and source-validation gates pass.

## Directly relevant studies

| Study | Overlap with this project | Distinction / limit of comparison | Required response |
|---|---|---|---|
| Kanbur et al. (2020), DOI [10.1002/er.5677](https://doi.org/10.1002/er.5677) | Data-centre cooling coupled to direct-contact membrane distillation | Earlier DCMD/data-centre integration; must not be described as novel in itself | Compare assumptions, heat and cooling boundary, flux treatment, and water accounting against full text |
| Wyon (2025), data-centre waste-heat/DCMD techno-economic case study | Direct waste-heat-to-MD pathway | Potentially close engineering prior art; metadata and full method comparison need verification | Retrieve full paper, extract system boundaries and equations, record a claim-by-claim comparison |
| Chen et al. (2026), CPU-waste-heat MD | Waste heat from computing hardware used for MD | Different system scale/configuration may matter, but not enough to establish novelty without full text | Verify bibliographic details and compare heat-source temperature, flux model, recovery, and burdens |
| Yang et al. (2026), DOI [10.1016/j.apenergy.2026.127428](https://doi.org/10.1016/j.apenergy.2026.127428) | Data-centre waste heat used in seawater reverse-osmosis preheating | RO preheating differs from MD, but directly overlaps waste-heat/desalination integration | Compare useful-heat definition, displacement counterfactual, and water/energy boundary |
| Katakam et al. (online 2026; *Water Research* issue dated 2027), DOI [10.1016/j.watres.2026.126748](https://doi.org/10.1016/j.watres.2026.126748) | System-scale desalination for data-centre freshwater demand; RO/MVC/hybrids; recovery, energy, cost, and a water-stress metric | Publisher abstract says detailed thermal/operational integration between desalination and data centre is outside scope; full-text review still required | Do not claim the first data-centre desalination framework or first water-stress-linked metric; compare metric definitions and system boundary |
| Wang et al. (2026), DOI [10.1016/j.ese.2026.100702](https://doi.org/10.1016/j.ese.2026.100702) | Global data-centre/WWTP geospatial pairing, treated-effluent cooling, bidirectional thermal recovery, modeled water and emissions outcomes | Different pathway: water reuse and WWTP heat recovery rather than MD product-water generation | Do not claim the first global geospatial water/heat-recovery assessment; compare counterfactuals and what “freshwater conserved” means |
| Lei et al. (2025), DOI [10.1016/j.resconrec.2025.108310](https://doi.org/10.1016/j.resconrec.2025.108310) | Data-centre workload water use and determinants, including electricity-related factors | Review/assessment rather than MD intervention model | Use to justify workload-specific and grid-factor sensitivity; do not transfer universal water-use constants |
| Herrera et al. (2025), DOI [10.1016/j.jclepro.2025.146528](https://doi.org/10.1016/j.jclepro.2025.146528) | Probabilistic AI-infrastructure water-footprint scenarios, including direct, electricity-related, and embodied water | Global scenario forecast, not facility-specific MD coupling | Explain how the present study differs in operational counterfactual and engineering constraints; avoid claiming uncertainty-aware water accounting as wholly new |
| Malaguti et al. (2026), DOI [10.1016/j.desal.2026.120039](https://doi.org/10.1016/j.desal.2026.120039) | MD cooling and pumping burdens under different configurations | Thermodynamic MD analysis, not by itself data-centre net-water accounting | Explicitly model cooling and pumping; compare equations and configuration assumptions |

## Evidence quality and bibliographic cautions

- The rows above are a targeted direct-overlap screen, not a PRISMA-style systematic review. Search strings, database coverage, screening criteria, and full-text extraction are not yet archived.
- Katakam et al. has a DOI assigned in 2026 while the publisher page places the article in a 2027 *Water Research* issue. Cite it as online-first (2026; issue 2027) until final citation formatting is confirmed.
- The global data–water symbiosis article is open access under CC BY-NC-ND 4.0. Cite and link it; do not adapt/re-distribute its figures or tables without checking the license restrictions.
- Do not reproduce another paper's digitized experimental markers as primary data. Primary measurements, secondary reproductions, model curves, and our own digitization must remain separately labelled.
- The 1999 Martínez-Díez primary observation extraction and independent validation are still incomplete. Literature novelty cannot compensate for missing empirical validation.

## Required full-text comparison table

Before claiming novelty, complete one row per direct prior-art paper with:

1. exact system boundary and counterfactual;
2. heat source and temperature/availability model;
3. desalination technology and mass/energy equations;
4. measured versus simulated inputs;
5. calibration and independent validation protocol;
6. direct water withdrawal and consumption;
7. electricity-related water factor and boundary;
8. cooling, pumping, pretreatment, post-treatment, and brine treatment;
9. geographic data and whether locations are actual facilities or proxies;
10. uncertainty classes and sensitivity method;
11. open code/data and license;
12. exact residual gap left by that paper, supported by page/section citations.

## Permitted manuscript language until the audit is complete

> “We investigate whether a source-traceable, counterfactual operational blue-water ledger that explicitly includes MD heat-quality constraints and incremental cooling/electricity burdens can clarify when waste-heat-assisted MD may or may not reduce net operational water consumption. The distinctiveness of this combination remains subject to full-text comparison and independent model validation.”

Do not use “first”, “novel global framework”, “validated”, “net water positive”, or “water saving” as an established result unless the corresponding evidence is completed and cited.

## Sources consulted for this update (retrieved 2026-10-14)

- Katakam et al., *System-scale design and analysis of desalination systems for meeting water needs of data centers*: https://www.sciencedirect.com/science/article/pii/S0043135426014223
- Wang et al., *Global data–water symbiosis reduces AI infrastructure's carbon and water footprint*: https://pmc.ncbi.nlm.nih.gov/articles/PMC13147368/
- Lei et al., *The water use of data center workloads*: https://doi.org/10.1016/j.resconrec.2025.108310
- Herrera et al., *Sustainable AI infrastructure: A scenario-based forecast of water footprint under uncertainty*: https://doi.org/10.1016/j.jclepro.2025.146528
- Martínez-Díez & Vázquez-González (1999): https://doi.org/10.1016/S0376-7388(98)00349-4

## Addendum — targeted literature update (2026-10-24)

This addendum updates the targeted screen; it does not convert the review into a systematic review or establish novelty.

### Newly surfaced direct-overlap source

**Malaguti et al. (2026), “Waste heat won't make membrane distillation cool: Thermodynamic analysis of cooling and pumping burdens,” *Desalination* 628, article 120039. DOI: [10.1016/j.desal.2026.120039](https://doi.org/10.1016/j.desal.2026.120039).** The publisher record reports cooling loads reaching 80–100% of heating duty in some open-loop configurations, single-pass recovery typically around 2–6% (and below about 10% across the studied configurations), and pumping penalties of 0.2–0.5 kWh/m³ for stated pressure-loss conditions. It explicitly distinguishes theoretical thermal requirements from actual system energy consumption and treats cooling availability as a feasibility constraint. Source: publisher record and abstract, accessed 2026-10-24.

**Implication for this project:** cooling/pumping accounting and the warning that “free” heat alone does not guarantee feasibility are not novel contributions in isolation. The project must compare its actual equations and boundaries against this paper, including how it maps cooling duty to facility water consumption, whether pumping is represented, how heat eligibility and intermittent workload affect the system, and how electricity-related water impacts and freshwater displacement are counted. Do not claim that the current model fully captures these burdens unless the code and evidence demonstrate it.

A second close source is **Chen et al. (2026), “A dual-purpose seawater evaporation system for data center cooling and freshwater production: design and performance analysis,” *Applied Thermal Engineering*, article 129458**. The publisher abstract describes a coupled seawater-evaporation system that provides cooling and co-generates freshwater using data-centre waste heat. This is direct overlap with the broad dual-purpose cooling/freshwater concept. The current project must not claim that coupling data-centre cooling with freshwater generation is itself new. Full-text equation-by-equation comparison remains required.

### Updated research decision

The defensible candidate contribution remains narrow and conditional: an evidence-labelled counterfactual operational blue-water accounting framework that makes unresolved source data, model failure states, and break-even conditions explicit. This candidate is **not yet established as novel or empirically validated**. The primary source reconstruction, independent/unfitted validation, geographic integration, and final publication gates remain open. The new sources reinforce the need to prioritize full-text comparison and model-boundary auditing rather than adding more illustrative parameter sweeps.

### Follow-up checklist

- [ ] Add full-text extraction for Malaguti et al. (2026), including equations, configurations, cooling/pumping assumptions, and system boundary.
- [ ] Add full-text extraction for Chen et al. (2026), including whether the freshwater output is directly coupled to cooling and how net energy/water effects are counted.
- [ ] Compare both papers against the implemented model, not just the abstract; cite page/section numbers in the final comparison.
- [ ] Do not change scientific gates to true based on this literature update.

### Full-text / publisher-record extraction — 2026-10-24

#### Malaguti et al. (2026): full article text available on publisher page

The publisher page exposes the article text, so this comparison goes beyond the abstract. The study is a **lumped thermodynamic screening framework** for three representative membrane-distillation configurations: (1) DCMD with open feed and closed distillate circuits, (2) DCMD with external heat recovery, and (3) AGMD with internal heat recovery. It derives specific thermal energy requirement (STEC), specific cooling requirement (SCR), single-pass recovery, and pumping-energy estimates. It then maps those requirements to indicative actual energy consumption under selected heating and cooling technologies.

Relevant methodological details from the article:
- SCR is defined as cooling energy removed per unit distillate production; the article explicitly argues that the cold-side heat sink is a system constraint, not a free implicit resource.
- The model considers heating options including waste heat, solar thermal, resistive heating, natural gas, and heat pumps; cooling options include surface water, ambient air, and a cooling heat pump.
- Pumping energy is linked to module pressure drop, pump efficiency, and single-pass recovery. At a stated 300 mbar pressure drop, the reported illustrative pumping penalties are approximately 0.2–0.5 kWh/m³; typical single-pass recovery in the analyzed cases is low (roughly 2–6%).
- In some open-loop configurations, cooling demand approaches 80–100% of heating duty. The article stresses that theoretical energy requirements and actual energy consumption are different quantities.
- The authors describe the framework as a rapid screening/conceptual-design tool and note that the selected technology parameters are illustrative, not prescriptive design values.

**Direct comparison with this repository:** the current project already includes conditional net-water accounting, a cooling-water-intensity factor, incremental facility electricity, heat-recovery assumptions, and break-even/failure envelopes. However, those scenario inputs are not equivalent to the article's configuration-resolved SCR/STEC and hydraulic pressure-drop model. The current project should not imply that it has reproduced the article's MD thermal/hydraulic physics unless an explicit, tested implementation is added. In particular, a single cooling-water-intensity coefficient does not by itself resolve cooling duty, cooling technology, heat-sink temperature, or pump pressure drop. Conversely, the candidate project-level question is different: whether any water benefit remains after translating the desalination output and additional facility/electricity burdens into an explicit counterfactual operational water ledger. That distinction is a *candidate scope distinction*, not yet a demonstrated novelty claim.

Publisher source: https://www.sciencedirect.com/science/article/pii/S0011916426001955 (retrieved 2026-10-24).

#### Chen et al. (2026): publisher abstract and bibliographic record inspected; full text not extracted

Publisher record: **“A dual-purpose seawater evaporation system for data center cooling and freshwater production: design and performance analysis,” *Applied Thermal Engineering* 287, article 129458 (February 2026)**. The abstract describes a seawater-evaporation-based system that uses low-pressure phase-change absorption of data-centre waste heat, produces salt-free vapour that is condensed into freshwater, and co-generates refrigeration. The publisher highlights report two system configurations with power decreases of 41.5% and 40.0% and freshwater outputs of 10,004 and 10,744 t/day, respectively. These are publisher-reported abstract claims; their basis, assumptions, scale, and validation have not yet been checked against the full text.

**Comparison boundary:** this is direct prior art for coupling data-centre cooling and freshwater production with waste heat. It may differ materially from the present project in desalination mechanism, plant scale, energy integration, and evaluation objective, but those distinctions cannot be asserted as established until the full paper and supplement are reviewed. Do not compare its headline production values numerically with the present reduced-order screening outputs; the systems and boundaries have not been normalized.

Publisher source: https://www.sciencedirect.com/science/article/abs/pii/S1359431125040505 (retrieved 2026-10-24).

#### Updated evidence-based conclusion

The targeted review now establishes two things with different evidence strength:

1. **Established overlap:** MD cooling and pumping burdens are explicitly modeled in Malaguti et al.; dual-purpose data-centre cooling and freshwater generation from waste heat are explicitly described by Chen et al. Therefore, neither concept alone is a defensible novelty claim.
2. **Unresolved candidate contribution:** this repository's potential distinction is the explicit counterfactual *net operational blue-water* ledger and its evidence/failure accounting. Whether that combination is sufficiently distinct, correctly implemented, and useful is still unproven. Chen full-text extraction, equation-level model audit, source reconstruction, and independent validation remain outstanding.

No publication or scientific-validation gate is changed by this addendum.
