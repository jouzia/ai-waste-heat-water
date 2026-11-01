# Wyon (2025) full-text prior-art audit

**Audit date:** 2026-11-01  
**Source:** Annie Wyon, *Desalination utilizing data centre waste heat: A techno-economic study*, Lund University, June 2025, report LUTFD2/TFEM—25/5229--SE + (1–53), 53 pages.  
**Institutional record:** https://lup.lub.lu.se/student-papers/record/9198095  
**Readable copy consulted:** https://www.scribd.com/document/950751330/Desalination-Utilizing-Data-Centre-Waste-Heat-Jun25

## Access and evidence status

The Lund University record identifies the work as an open-access student thesis and provides the authoritative bibliographic metadata. The direct institutional PDF endpoint timed out during retrieval. A readable 53-page copy carrying the same title, author, report number, and pagination was available through Scribd and was used for this content audit. Because that copy is hosted by a third party, verify page-level details against the institutional file before quoting numerical results in a publication. This is a full-text content review of the readable copy, not an independently authenticated copy from the university repository.

## System scope and method

Wyon evaluates a hypothetical 1.5 MW direct-to-chip data centre in Barcelona, with no heat upgrade. The system couples a commercial heat exchanger, DCMD modules, and two hydraulic pumps. The model evaluates three product-water destinations: data-centre air-cooling, an electrolyser for backup hydrogen, and sale to the local water grid.

The heat exchanger uses a counter-current NTU/effectiveness formulation. The DCMD model is based on literature and an experimental module setup. Its stated simplifying assumptions include ideal-gas behaviour for water vapour/nitrogen/oxygen, no membrane wetting, no module heat losses, no feed-membrane fouling, and thermodynamic equilibrium. Membrane heat transfer includes both vapour transport and conductive heat transfer. The mass-flux model combines Knudsen and ordinary diffusion under a transitional-diffusion assumption. The final case-study setup uses PTFE membrane, 77 μm thickness, 89% porosity, 0.45 μm pore size, 0.1 m² membrane area per module, and 80 modules.

The two pumps are dimensioned from pressure losses through the DCMD modules and heat exchanger. At the stated standard conditions, the feed and permeate pump input powers are 4.053 kW and 2.564 kW, respectively; total is approximately 6.62 kW (reported in the discussion as about 7 kW).

## Validation and limitations explicitly reported

The thesis compares modelled total DCMD heat flux against experimental values from its source setup. It reports a small but significant discrepancy, suspects the mass-flux calculation, and states that the cause was not identified. It also notes that the experimental temperature range differs from the range used to extract case-study results. After this check, the final case-study membrane/module geometry is adjusted using another reference, retaining velocities from the initial reference to maintain turbulent flow.

Accordingly, this is a model check against a literature experiment with a documented unresolved discrepancy—not a clean validation across the full operating envelope. The thesis itself flags this limitation. Do not describe its DCMD model as fully validated without qualifying these points.

## Quantitative system accounting

The thesis estimates approximately 2 × 10^6 kg/year of product water and approximately 1816 × 10^6 kg/year of seawater requirement, with 8 m² effective membrane area. This corresponds to a very high seawater-feed-to-product-water ratio, which the discussion reports as varying approximately from 3500 to 300 across conditions. The study discusses brine salinity, discharge temperature, chemical additives, and electricity-related indirect environmental impacts.

The system's low product yield is central to its results: large seawater throughput and pumping are required relative to the water produced. The thesis identifies pump capital cost, pump electricity, heat-exchanger cost, and maintenance/service as important economic burdens. It finds grid-water sale unattractive at the assumed Barcelona water price, while on-site data-centre and electrolyser uses appear more promising in its scenario analysis.

## Water-accounting boundary: overlap and gap

Wyon explicitly treats data-centre water use and electricity-generation water use as distinct WUE concepts in the background discussion. It also models seawater feed, product water, and the three product-water destinations, and discusses reduced dependence on the local water grid.

However, the reviewed thesis does **not** establish a time-resolved net-blue-water ledger that consistently distinguishes freshwater withdrawal from consumption across:
- baseline data-centre cooling water;
- incremental MD feedwater withdrawal and brine discharge;
- pump and heat-exchanger electricity and its water intensity;
- marginal electricity-generation water consumption;
- product-water quality/treatment losses and end-use substitution;
- counterfactual freshwater displaced at the actual location and time.

It discusses environmental impacts and electricity mix, but the above integrated accounting boundary is not demonstrated in the reviewed methods/results. This is a bounded observation about this thesis, not a claim that no other literature provides such accounting.

## Implications for Research 2

### Established prior art — do not claim as novel
- Direct-to-chip data-centre waste heat driving DCMD.
- Heat-exchanger coupling and explicit hydraulic pump sizing.
- Parametric evaluation over data-centre waste-heat and seawater temperatures.
- Modelling product-water uses inside the data centre, for hydrogen production, and for sale.
- Recognition that low-grade heat, low water yield, pump energy/capital, and discharge impacts can undermine feasibility.
- Discussion of direct and indirect environmental impacts, including electricity mix and seawater/brine effects.

### Potentially differentiating research question — still unproven
A defensible candidate contribution remains a transparent, time-resolved counterfactual water-impact framework that separates withdrawal and consumption, tracks baseline versus incremental cooling/pumping/electricity burdens, accounts for location- and time-specific electricity water factors, and quantifies actual freshwater displacement by product-water end use with uncertainty and failure envelopes.

This thesis does not clear that contribution as novel. A systematic search and full-text comparison against other direct antecedents (including Kanbur et al. 2020, Yang et al. 2026, and the Malaguti et al. 2026 MD cooling/pumping analysis) remain necessary.

## Research status

- Wyon full-text content review: **completed from a third-party readable copy; institutional-PDF authentication outstanding**.
- Exact independent reproduction of Wyon's model/results: **not performed**.
- Research 2 novelty: **not established**.
- Research 2 empirical validation: **not established**.
- Issue #16 should remain open pending systematic search, remaining full-text reviews, and implementation-level comparison.

## Source references

1. Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University. Institutional record: https://lup.lub.lu.se/student-papers/record/9198095
2. Readable third-party copy consulted for this audit: https://www.scribd.com/document/950751330/Desalination-Utilizing-Data-Centre-Waste-Heat-Jun25
