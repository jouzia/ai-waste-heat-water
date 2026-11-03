# Full-text prior-art audit: Talukder et al. (2026) stress-adjusted data-centre water management

**Audit date:** 2026-11-03  
**Source:** Talukder, Z., Bin Rahim, I., Sen Gupta, P., Ren, S., & Islam, M. A. (2026). “Balancing Bits and Drops: Stress-Adjusted Water Management for Data Centers.” *Proceedings of the 17th ACM International Conference on Future and Sustainable Energy Systems (E-Energy '26)*, 386–398. DOI: https://doi.org/10.1145/3744255.3811726.  
**Access status:** ACM DOI landing page exposes the open-access article and substantial full text. CC BY 4.0 is stated on the publisher record. This audit uses publisher-visible article text; it is not an independent replication of code or data.

## 1. Why this paper is a direct novelty constraint

This is not a membrane-distillation or waste-heat desalination paper. It is direct prior art for data-centre operational water accounting that:
- distinguishes water withdrawal, discharge, and consumption;
- separates on-site cooling water from off-site electricity-generation water;
- applies spatially and temporally resolved water-stress characterization;
- traces indirect electricity-water impacts to upstream power-plant geography using eGRID subregions and generation-weighted plant data;
- evaluates workload scheduling, rainwater harvesting, and dry cooling as water-management strategies.

Research 2 cannot claim to introduce stress-adjusted data-centre water accounting, the direct/indirect split, or electricity-generation provenance-aware stress accounting in general.

## 2. Source-grounded methods and claims

### Water boundary

The paper explicitly defines withdrawal as water taken from a source, discharge as water returned to the environment, and consumption as the portion not returned to the original watershed. It gives consumption = withdrawal − discharge and warns that these terms are not interchangeable. Its principal impact metric is stress-adjusted consumption, not an undifferentiated water-volume total.

### Spatial and temporal stress

The paper uses AWARE-US county-level monthly characterization factors. On-site consumption is weighted by the factor at the data-centre county and month. Off-site electricity-related consumption is weighted using water-stress factors associated with upstream power plants.

For off-site attribution, the authors use EPA eGRID subregions as a practical approximation of electricity provenance and calculate a generation-weighted average of plant-level water-stress factors. The paper acknowledges that exact power-flow tracing is difficult and that this regional generation portfolio is an approximation.

### Workload and operational strategies

The study evaluates workload scheduling across time and locations, rainwater harvesting, and dry cooling. It uses offline optimization with perfect future knowledge as an upper bound, rather than claiming an online scheduling algorithm. The publisher text reports up to 25% reductions in stress-adjusted water consumption for stress-aware workload scheduling under its evaluated settings. This is the paper's reported result, not a result reproduced by Research 2.

### Data and limitations stated by the authors

The paper reports a dataset of 4,147 US data-centre locations and makes it available through the Open Science Framework. Stated limitations include dependence on AWARE-US, possible omission of small or recently commissioned power plants in public EPA data, a single precipitation year (2023) for rainwater analysis, an offline scheduling upper bound, and a snapshot of data-centre locations.

The geographic scope is US-specific. Its stress factors and grid-provenance method should not be transferred to another country without appropriate local hydrological and electricity-system data.

## 3. Claim-by-claim comparison with Research 2

| Dimension | Talukder et al. (2026) | Research 2 repository status | Consequence |
|---|---|---|---|
| Data-centre water accounting | Explicit withdrawal, discharge, consumption definitions | Feed withdrawal and concentrate discharge are reported; net impact is consumption-oriented | Definitions are prior art; Research 2 still needs a more complete boundary and separate net-withdrawal treatment |
| Direct/on-site water | Explicit on-site consumption | Direct cooling consumption is represented through declared factors | General direct-water accounting is not novel |
| Indirect electricity water | Explicit off-site electricity-generation consumption | One scalar grid_water_l_per_kwh factor | Research 2 does not yet match the paper's geographic/temporal granularity |
| Electricity provenance | eGRID subregion and generation-weighted power-plant water-stress attribution | No generation-plant provenance or time-varying marginal electricity-water factor | A scalar grid factor is materially less resolved |
| Water stress | AWARE-US county/month characterization | No implemented stress characterization layer | Stress-adjusted accounting is established prior art; repository implementation remains incomplete |
| Workload dynamics | Time-slotted workload scheduling and spatial/temporal flexibility | Piecewise-constant workload intervals gate heat recovery | Dynamic workload modelling is prior art in broader data-centre water literature |
| Cooling interventions | Rainwater harvesting and dry cooling; water-energy trade-offs | Cooling penalty and declared incremental facility cooling factors | Cooling-water/energy trade-off is prior art |
| Desalination technology | No MD/RO desalination plant producing product water is evaluated | Reduced-order MD model is coupled to recoverable heat | Desalination coupling is a meaningful difference, not proof of novelty by itself |
| Waste-heat recovery | Not the studied intervention | Data-centre heat eligibility and heat recovery are central | Different physical intervention |
| Product-water counterfactual | No desalinated-product-water displacement analysis identified in the reviewed text | Declared avoided freshwater consumption/displacement fraction, capped by distillate | Product-water displacement may remain distinct, but must be evidence-backed |
| MD empirical validation | Not applicable to the paper's scope | Independent validation remains incomplete | Research 2 must validate its MD subsystem separately |
| Geography | US counties and US eGRID | Factors are caller-supplied; no country-specific provenance model | Any case study requires location-appropriate hydrology and grid data |

## 4. Revised interpretation of the candidate contribution

The following are not defensible novelty claims: first data-centre water accounting framework; first separation of withdrawal, discharge, and consumption; first direct/indirect operational water accounting; first stress-adjusted data-centre water metric; first geographic attribution of electricity-generation water impacts; or first workload-aware water-management analysis.

The candidate distinction, if it survives the remaining prior-art search and validation, is substantially narrower:

> An empirically audited membrane-distillation subsystem coupled to time-matched data-centre waste-heat eligibility, evaluated through an explicit product-water counterfactual and a boundary-consistent operational water ledger that separates withdrawal, discharge, and consumption, includes cooling and pumping, and attributes electricity-related water to the relevant location and time.

This is a research hypothesis, not an established novelty result. Talukder et al. already supply much of the water-accounting and stress-attribution layer. Research 2 must demonstrate that its desalination/product-water counterfactual creates a distinct, useful and validated extension rather than simply appending an MD calculator to an existing stress-adjusted ledger.

A defensible implementation should consider a modular accounting design: (1) physical volume ledger for withdrawal, discharge, consumption, and transfers; (2) electricity-water ledger with separate withdrawal and consumption factors, generation geography, time, and provenance; (3) location/time-specific stress characterization; (4) desalinated-product-water counterfactual tied to end-use quality, location, time, and verified freshwater displacement; (5) independently validated MD physical model; and (6) evidence-backed uncertainty propagation. Do not implement or merge such a design merely from this literature comparison; first define the accounting boundary and identify compatible data sources for the intended case-study geography.

## 5. Adjacent evidence update: Katakam et al. (2026)

The current ScienceDirect article preview exposes the abstract and highlights for Katakam et al., “System-scale design and analysis of desalination systems for meeting water needs of data centers,” *Water Research* 308, 126748, DOI 10.1016/j.watres.2026.126748. It reports two-stage RO, MVC, and hybrid systems; brackish (5,000 ppm), seawater (35,000 ppm), and produced-water (at least 50,000 ppm) feeds; conventional brine disposal and MLD/ZLD; freshwater recovery, energy consumption, and water cost; and a Saline Water Utilization Intensity (SWUI) metric for data-centre water-stress impact.

The publisher preview reports a seawater hybrid RO-MVC/MLD example with 736 L freshwater per 1,000 kg feed, 9.4 kWh/m³ permeate, and $3.2/m³ permeate. The publisher preview identifies the article as dated 1 January 2027 in Volume 308, while PubMed lists an ahead-of-print date of 17 August 2026. Record this bibliographic date discrepancy rather than silently selecting one date.

The preview is not the full article or supplement; equations, detailed system boundary, validation and complete SWUI construction remain to be audited. This paper rules out claims to first system-scale desalination assessment for data centres or first data-centre desalination water-stress metric. It evaluates RO/MVC/hybrid systems, not the MD configuration in Research 2.

## 6. Remaining evidence gaps and actions

1. Obtain and inspect the full Kanbur et al. (2020) article and supplement through authorized access. The Wiley page identifies Fei Duan as corresponding author (feiduan@ntu.edu.sg), but no author email has been sent.
2. Obtain the full Katakam et al. article and supplement; the current publisher preview is abstract/highlights-level evidence.
3. Obtain the reverse-Brayton/DCMD article's full methods and data; the publisher identifies it as open access and reports data available on request, but no request has been made.
4. Complete the multi-database search and screening log; this audit does not satisfy systematic-review acceptance criteria.
5. Finish primary experimental MD data extraction and independent validation before presenting the coupled framework as validated.
6. Keep issue #16 open. Do not freeze novelty language or claim a positive net-water benefit.

## References

- Talukder, Z., Bin Rahim, I., Sen Gupta, P., Ren, S., & Islam, M. A. (2026). Balancing Bits and Drops: Stress-Adjusted Water Management for Data Centers. *E-Energy '26*, 386–398. https://doi.org/10.1145/3744255.3811726
- Katakam, V. S. S., Arzumanyan, M., Lin, N., & Bahadur, V. (2026). System-scale design and analysis of desalination systems for meeting water needs of data centers. *Water Research*, 308, 126748. https://doi.org/10.1016/j.watres.2026.126748
- Current implementation crosswalk: docs/IMPLEMENTATION_PRIOR_ART_CROSSWALK_KANBUR_WYON_2026-11-02.md
- Prior-art search/access log: docs/PRIOR_ART_SEARCH_REFRESH_ACCESS_LOG_2026-11-03.md
