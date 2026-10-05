# Recent literature evidence relevant to Research 2

Updated: 2026-09-30

This file records papers that materially affect the research design. It is a literature-screening record, not a claim that every cited study is an independent validation dataset.

## 1. Data-center waste heat + desalination

### Yang, Konstantinou & Hou (2026)
**Enabling grid-interactive data center-desalination coordination through thermo-electric coupling-based waste heat utilization**  
Applied Energy 408, 127428. DOI: 10.1016/j.apenergy.2026.127428.

Relevance:
- Directly couples data-center workload-driven waste heat to desalination.
- Uses a high-fidelity thermo-electric model and two-stage stochastic planning/operation optimization.
- Uses reverse osmosis rather than membrane distillation.
- Case study is based on Jubail Industrial City, Saudi Arabia.
- Important competitor to this project's system-level framing.

Implication for Research 2:
- Our novelty cannot be stated as merely "connecting data-center waste heat with desalination."
- Our differentiator must remain the **net freshwater-consumption accounting + MD physics + cooling burden + uncertainty + water-stress feasibility envelope**, validated against experimental MD data.

Source: https://doi.org/10.1016/j.apenergy.2026.127428

## 2. Data-center cooling + freshwater co-production

### Chen et al. (2026)
**A dual-purpose seawater evaporation system for data center cooling and freshwater production: design and performance analysis**  
Applied Thermal Engineering 287, 129458.

Relevance:
- Directly addresses simultaneous data-center cooling and freshwater production.
- Uses seawater evaporation and multi-effect distillation rather than DCMD.
- Reports system-level thermodynamic, energy, cost and emissions analysis.

Implication:
- The paper occupies the same broad data-center/water nexus but a different desalination architecture.
- Research 2 should explicitly position MD as a membrane-based thermal pathway and compare against alternative thermal pathways where useful.
- It reinforces the need to model cooling and water production jointly rather than treating cooling as an external penalty.

## 3. Cooling burden in membrane distillation

### Malaguti et al. (2026)
**Waste heat won't make membrane distillation cool: Thermodynamic analysis of cooling and pumping burdens**  
Desalination 628, 120039. DOI: 10.1016/j.desal.2026.120039.

Relevance:
- Reports cooling demand can reach 80–100% of heating demand in some MD configurations.
- Highlights cooling availability as a feasibility constraint.
- Quantifies pumping penalties and argues that free heat alone does not guarantee viability.

Implication:
- This strongly supports keeping cooling as a first-class subsystem in Research 2.
- The model must not report gross thermal-driven distillate without accounting for cold-side requirements, pumping and auxiliary electricity.

## 4. Waste-heat-driven MD experimental validation

### Al-Jariry et al. (2026)
**Analysis of high flux membranes for desalination in waste-heat driven vacuum membrane distillation plants: Experimental validation and techno-economic analysis**  
Desalination 620, 119627. DOI: 10.1016/j.desal.2025.119627.

Relevance:
- Experimental water-flux data were collected for multiple membrane materials, including ceramics.
- A one-dimensional model was validated against experimental flux data.
- Includes a waste-heat source at 90 °C and plant-level analysis.
- Data availability is stated as available on request.

Implication:
- Candidate quantitative validation source for a **waste-heat-driven MD subsystem**.
- Exact experimental boundary conditions must be extracted before inclusion in the held-out validation set.
- Do not use the reported fitted parameters as validation evidence for this repository.

## 5. Cross-system pilot MD model validation

### Bindels et al. (2026)
**Pilot-scale membrane distillation modeling: Validation, comparison, and consensus**  
Desalination 620, 119674. DOI: 10.1016/j.desal.2025.119674.

Relevance:
- Four pilot-scale AGMD models were compared using 2,716 experimental datapoints.
- The study covers broad salinity, module, membrane and spacer conditions.
- Model consensus uses empirical heat-transfer correlations, resistance-in-series membrane thermal conductivity, ePTFE support-layer treatment and air-gap distillate effects.
- Authors state the aggregated experimental data cannot be shared.

Implication:
- Strong methodological evidence for model-form uncertainty.
- Useful for correlation/model-structure comparison.
- Not suitable as a directly reproducible numerical held-out dataset unless legally available observations can be independently obtained.

## 6. Recent AI water-footprint context

### Barnett-Itzhaki et al. (2026)
**The water footprint of artificial intelligence: Emerging solutions and governance imperatives**  
Water Research 299, 125866. DOI: 10.1016/j.watres.2026.125866.

Relevance:
- Reviews operational and indirect water dimensions of AI infrastructure.
- Emphasizes cooling water, electricity-related water and water-stress context.
- Discusses waste-heat recovery among possible technical interventions.

Implication:
- Supports the research motivation and broader water-footprint framing.
- Does not replace facility-specific measurements or the present project's physical MD validation.

## 7. Data-center waste-heat recovery / exergy context

### Data centers waste heat recovery technologies: Review and evaluation (2025)
Applied Energy 384, 125489. DOI: 10.1016/j.apenergy.2025.125489.

Relevance:
- Reviews data-center waste-heat streams and recovery technologies.
- Uses exergy-based evaluation, reinforcing the distinction between heat quantity and heat quality.

Implication:
- Supports the exergy layer already implemented in Research 2.
- Research 2 should retain source-temperature/exergy reporting instead of treating all kWh-th as equivalent.

## 8. Primary MD foundation

### Martínez-Díez & Vázquez-González (1999)
**Temperature and concentration polarization in membrane distillation of aqueous salt solutions**  
Journal of Membrane Science 156(2), 265–273. DOI: 10.1016/S0376-7388(98)00349-4.

Relevance:
- Primary experimental provenance for flat-sheet PTFE DCMD.
- Studies water and NaCl feeds and evaluates temperature and concentration polarization.

Implication:
- Remains a primary validation target.
- Experimental observations must be extracted from the primary source before model calibration.

## 9. Literature-positioning rule

The existence of 2025–2026 papers directly coupling data centers and desalination means the manuscript must **not** claim that this research is the first to propose data-center waste-heat desalination.

The defensible contribution is narrower:

> A source-traceable, uncertainty-aware framework for determining when data-center waste heat coupled to membrane distillation produces a positive net freshwater-consumption benefit after accounting for thermal quality, cooling, hydraulic/auxiliary burdens, electricity-related water, counterfactual displacement and geographic water stress.

This contribution remains subject to quantitative validation and comparison against the recent literature above.


## 2026 evidence refresh — 2026-10-02

### Malaguti et al. (2026), Desalination 628, 120039

DOI: 10.1016/j.desal.2026.120039.

This open-access study explicitly evaluates heating, cooling, and pumping burdens together. It reports that cooling demand can reach 80–100% of heating in some open-loop MD configurations and that pumping penalties of 0.2–0.5 kWh/m3 arise under representative low-recovery/high-pressure-loss conditions. The paper also emphasizes that free heat alone does not establish system viability.

**Model implication:** cooling is a first-class constraint in the coupled water model; the study must not report a heat-only water benefit.

### Barnett-Itzhaki (2026), Water Research 299, 125866

DOI: 10.1016/j.watres.2026.125866.

This 2026 review frames AI water use as a combination of direct cooling water, indirect electricity-related water, and other upstream components. It reports a wide global footprint estimate and emphasizes the role of siting and water stress.

**Model implication:** preserve direct and indirect operational water accounting and keep basin-level water stress as a contextual deployment layer rather than converting it into a universal threshold.

### DOE data-center design guidance

The U.S. Department of Energy's data-center design guide states that higher server-exit temperatures improve opportunities for useful heat reuse and that heat reuse can reduce or eliminate some chiller/cooling-tower operation when a suitable heat host exists.

**Model implication:** source temperature, heat-host availability, and counterfactual cooling displacement must be represented separately.

### IEA 2026 data-center electricity update

IEA reports that global data-center electricity consumption increased around 17% in 2025 and that AI-focused data-center demand grew faster than the overall data-center segment.

**Model implication:** workload scenarios should cover both sustained/high-utilization and intermittent/low-utilization regimes rather than assuming a single steady IT load.

### Evidence-status rule

These literature findings are contextual/methodological evidence. They are not measurements of this project's integrated AI-waste-heat-to-water system and must not be presented as model validation.


## 2026 evidence additions verified 2026-10-05

### Malaguti et al. (2026) — cooling and pumping are explicit MD burdens
Malaguti, M., Morciano, M., Viano, G., Achilli, A., Ali, A., Quist-Jensen, C. A., & Tiraferri, A. (2026). *Waste heat won't make membrane distillation cool: Thermodynamic analysis of cooling and pumping burdens*. Desalination, 628, 120039. DOI: 10.1016/j.desal.2026.120039. Open access under CC BY 4.0.

Verified findings relevant to this study: cooling loads can reach 80–100% of thermal input in some open-loop MD configurations; pumping penalties of 0.2–0.5 kWh/m³ arise under representative low single-pass recoveries and pressure losses; and feasibility depends on heat-sink effectiveness and hydraulic resistance, not heat availability alone.

Research consequence: cooling and pumping remain first-class terms in the integrated AI-waste-heat-to-MD model. These published values are contextual evidence and are not inserted as universal parameter defaults.

### Barnett-Itzhaki (2026) — AI water footprint and governance boundary
Barnett-Itzhaki, Z. (2026). *The water footprint of artificial intelligence: Emerging solutions and governance imperatives*. Water Research, 299, 125866. DOI: 10.1016/j.watres.2026.125866.

The review frames AI water demand as including direct evaporative cooling and indirect electricity-related water use, emphasizes water-stressed siting and facility-level transparency, and discusses waste-heat recovery among potential technical responses. Its global projections are treated as contextual literature, not as direct parameter values for this study.

### Lei et al. (2025) — workload-level water heterogeneity
Lei, N., Lu, J., Shehabi, A., & Masanet, E. (2025). *The water use of data center workloads: A review and assessment of key determinants*. Resources, Conservation and Recycling, 219, 108310. DOI: 10.1016/j.resconrec.2025.108310.

The study identifies server efficiency, grid water factors, utilization, cooling system type, infrastructure efficiency, climate, inactive-server share, and refresh cycle as important determinants of workload-level water use. This supports the study's separation of workload, cooling architecture, geography, and indirect electricity-water accounting rather than using a single universal WUE factor.
