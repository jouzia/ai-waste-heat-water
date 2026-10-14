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
