# Prior-art search refresh and access log — 2026-11-03

## Status and scope

This is a dated search refresh and access log for Research 2, not a completed systematic review. Searches were run on 2026-11-03 using general scholarly/web indexing. The search interface and returned indexed records are not equivalent to a documented Scopus, Web of Science, Compendex, or Crossref database export. No claim of exhaustive coverage is made.

The purpose of this update is to (i) retry access to Kanbur et al. (2020), (ii) record newly surfaced closely related work, and (iii) sharpen the comparison boundary. Search terms included combinations of:

- "data center" OR "data centre" AND waste heat AND membrane distillation OR DCMD OR AGMD;
- data-center desalination AND RO OR MVC OR membrane distillation;
- data-center workload AND water consumption AND electricity-generation water;
- net operational blue-water accounting AND withdrawal AND consumption;
- dynamic workload/cooling coupling AND water use;
- waste-heat-driven membrane distillation AND cooling/pumping.

## Kanbur et al. (2020): publisher access retry

**Citation:** Kanbur, B. B., Wu, C., & Duan, F. (2020). "Multi-criteria thermoeconomic and thermodynamic assessments of the desalination-integrated two-phase liquid-immersion data center cooling system." *International Journal of Energy Research*, 44, 10453–10470. DOI: 10.1002/er.5677.

**Publisher record:** https://onlinelibrary.wiley.com/doi/abs/10.1002/er.5677

The Wiley record was opened on 2026-11-03. Its full-text and PDF links both redirected to the abstract record. The page explicitly reports that the full text hosted at iucr.org is unavailable due to technical difficulties. Therefore, the article body, equations, supplementary material, detailed water boundary, and validation procedure were not inspected in this access attempt.

Publisher-visible abstract facts:
- two-phase liquid-immersion data-centre cooling;
- cooling load range 0.7–1.5 kW;
- waste heat heats the feed side of a DCMD module;
- membrane area range 5–75 cm²;
- reported maximum thermal and exergy efficiencies 64.5% and 53.7%;
- reported maximum daily distillate production 6.13 kg;
- the hybrid has higher capital and operating costs than stand-alone data-centre cooling;
- reported payback period 3.72 years;
- reported levelized product cost range 2.69–5.33 SGD/h (preserve the publisher's printed unit; do not convert it to SGD/m³);
- multiobjective optimum reported at 1.1 kW cooling load and membrane area 5.12–5.19 cm².

**Evidence boundary:** these facts are abstract-level only. They establish direct integration and thermoeconomic analysis as prior art. They do not establish the paper's precise water withdrawal/consumption treatment, brine boundary, pumping model, or validation quality. Those cells remain unknown pending full text and supplement.

The publisher record identifies Fei Duan as corresponding author and displays a contact email. No email has been sent. Author contact or interlibrary-loan requests require a separate deliberate action.

## Additional records surfaced in this refresh

### Katakam et al. (2026): system-scale desalination for data centres

**Citation:** Katakam, V. S. S., Arzumanyan, M., Lin, N., & Bahadur, V. (2026). "System-scale design and analysis of desalination systems for meeting water needs of data centers." *Water Research*, 308, Part B, 126748. DOI: 10.1016/j.watres.2026.126748. PMID: 42731480.

Sources:
- PubMed: https://pubmed.ncbi.nlm.nih.gov/42731480/
- ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0043135426014223

PubMed abstract reports two-stage RO, mechanical vapour compression (MVC), and hybrid configurations for brackish water (5,000 ppm), seawater (35,000 ppm), and produced water (at least 50,000 ppm), with conventional brine disposal or minimum/zero liquid discharge. It reports freshwater recovery, input energy, and water cost comparisons. The indexed ScienceDirect text additionally discusses prior data-centre desalination studies, transient supply-demand mismatch, simplified first-principles assumptions, constant-flux/area-normalized production, salinity and recovery limitations, and incomplete treatment of pretreatment/brine/post-treatment costs in some prior studies.

**Evidence boundary:** the publisher full-text request returned HTTP 403 in this search session. The comparison is based on the PubMed abstract and indexed publisher text, not a complete independent reading of the paper or its supplement. Its evaluated technologies are RO/MVC/hybrids; do not misstate it as a membrane-distillation study.

### Waste-heat DCMD using a reverse Brayton cycle (2026)

A newly surfaced open-access *Energy Conversion and Management* article, "Waste heat driven direct contact membrane desalination coupled with reverse Brayton cycle: Techno-economic analysis and multi-objective optimization" (2026), DOI 10.1016/j.enconman.2026.121727, evaluates reverse-Brayton-cycle waste heat from a hydrogen-liquefaction plant coupled to DCMD. The indexed abstract reports permeate cooling as a material share of waste-heat-recovery capital cost and gives optimized production/cost outputs.

This is adjacent process-integration prior art, not data-centre prior art. It reinforces that waste-heat/DCMD coupling, permeate cooling, and multiobjective techno-economic optimization are established beyond data centres. Full methods and supplementary material have not been reviewed in this refresh.

### Data-centre water accounting definitions

A 2026 ACM conference paper, "Balancing Bits and Drops: Stress-Adjusted Water Management for Data Centers" (DOI 10.1145/3744255.3811726), surfaced in the search. Its indexed text explicitly distinguishes withdrawal, discharge, and consumption and separates direct on-site consumption from indirect electricity-generation consumption. The publisher page could not be opened in this session (HTTP 403); this is an indexed-text lead, not a full-text audit. It should be evaluated for metric overlap and its stress-adjustment method in the next full-text pass.

### Workload-level water determinants

Lei et al. (2025), "The water use of data center workloads: A review and assessment of key determinants," *Resources, Conservation and Recycling* 219, 108310, DOI 10.1016/j.resconrec.2025.108310, has a public institutional record and abstract. It reports workload water-use variation exceeding 10,000-fold and identifies server efficiency, grid water factors, utilization, cooling type, infrastructure efficiency, climate, inactive-server share, and refresh cycle as determinants. This is directly relevant to workload-level water attribution, but it does not by itself validate a data-centre-to-MD intervention.

## Updated prior-art interpretation

The combined evidence now clearly rules out novelty claims based on:
1. coupling data-centre waste heat to DCMD (Kanbur et al., 2020; Wyon, 2025);
2. data-centre-scale desalination assessment or RO/MVC/brine-management comparison (Katakam et al., 2026);
3. data-centre waste heat coupled to RO preheating and thermo-electric operation (Yang et al., 2026);
4. workload-level data-centre water-use determinants (Lei et al., 2025);
5. waste-heat-driven DCMD and cooling/permeate-cooling optimization in other industrial energy systems (2026 reverse-Brayton/DCMD study);
6. the general distinction between direct and electricity-related water consumption, and between withdrawal, discharge, and consumption (the 2026 ACM record is a further lead).

A defensible candidate contribution, if it survives the full review and empirical tests, remains narrower: a source-traceable and independently validated MD model coupled to time-matched data-centre heat eligibility and a counterfactual operational blue-water ledger that reports withdrawal, discharge, and consumption separately; includes cooling, pumping, and geographically/time-resolved electricity-water burdens; and tests whether product water demonstrably displaces freshwater under uncertainty.

This is a candidate gap, not an established novelty result. The current repository implementation does not yet implement all of those components (see the implementation crosswalk merged in PR #43). Issue #16 remains open.

## Next actions

1. Obtain the complete Kanbur article and any supplement through an authorized library route or author-provided copy; then map its equations, heat-source model, DCMD model, water boundary, cooling/pumping, and validation.
2. Obtain and read the full Katakam paper and supplement; compare system boundary, feedwater sources, brine management, recovery, cost, and water-stress treatment.
3. Retrieve the ACM 2026 paper and inspect its stress-adjusted metric against the proposed physical ledger.
4. Complete a reproducible multi-database search with database-specific syntax, date/time, exported records, duplicate removal, screening decisions, and citation chasing. This web-index refresh is not a substitute.
5. Keep the novelty claim conditional until primary-source comparison and independent MD validation are complete.

## Search/access log

| Date | Source/route | Query or target | Result | Evidence level |
|---|---|---|---|---|
| 2026-11-03 | Wiley Online Library | DOI 10.1002/er.5677, full text and PDF links | Both redirect to abstract; Wiley reports full text unavailable due to technical difficulties | Publisher abstract only |
| 2026-11-03 | PubMed | PMID 42731480 | Abstract and bibliographic metadata available | Abstract |
| 2026-11-03 | ScienceDirect | PII S0043135426014223 | Indexed discussion available; direct page returned 403 | Abstract/indexed text |
| 2026-11-03 | ScienceDirect | Reverse-Brayton/DCMD article, DOI 10.1016/j.enconman.2026.121727 | Indexed abstract and highlights available | Abstract/indexed text |
| 2026-11-03 | ACM Digital Library/DOI index | DOI 10.1145/3744255.3811726 | Indexed text available; direct page returned 403 | Indexed text |
| 2026-11-03 | LBL/UC eScholarship | DOI 10.1016/j.resconrec.2025.108310 | Institutional abstract/metadata available | Abstract |

