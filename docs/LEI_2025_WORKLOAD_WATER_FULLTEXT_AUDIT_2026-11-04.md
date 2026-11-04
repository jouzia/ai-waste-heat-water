# Full-text audit: Lei et al. (2025) data-centre workload water use

**Audit date:** 2026-11-04  
**Status:** Main article read from the author-hosted eScholarship PDF; public supporting-code repository inspected at file-list and source-code level. This is a source audit, not an independent reproduction of the paper.

## Bibliographic record

Nuoa Lei, Jun Lu, Arman Shehabi, and Eric Masanet, “The Water Use of Data Center Workloads: A Review and Assessment of Key Determinants,” *Resources, Conservation and Recycling* 219 (June 2025), article 108310. DOI: [10.1016/j.resconrec.2025.108310](https://doi.org/10.1016/j.resconrec.2025.108310).

- Author-hosted full-text PDF: <https://escholarship.org/content/qt1vx545q7/qt1vx545q7_noSplash_d651596ddd2b9bd5a7dad5e9f0d83186.pdf>
- LBNL publication record: <https://eta-publications.lbl.gov/publications/water-use-data-center-workloads>
- Supporting code and data: <https://github.com/nuoaleon/The-Water-Use-of-Data-Center-Workloads-A-Review-and-Assessment-of-Key-Determinants>

## Research question and method

The article develops a workload-normalized measure of data-centre water consumption rather than relying only on WUE-site or WUE-source. It integrates server workload efficiency (SPECpower_ssj 2008 throughput), facility electricity use, site water use, and grid electricity water-consumption factors.

The central accounting identity (paper Eq. 1) is:

\[
W_{overall}=W_{site}+E_{facility}\times WCF
\]

where the facility-level site water and facility electricity are expressed per workload, and WCF is the freshwater-consumption factor for grid electricity. The paper further expresses site water per workload as WUE-site multiplied by server electricity per workload, and facility electricity per workload as PUE multiplied by server electricity per workload (paper Eqs. 2–4).

The paper's scope for direct water consumption includes humidification, direct adiabatic cooling, and cooling-tower consumption (evaporation, windage and blowdown/draw-off). Indirect consumption includes upstream fuel/equipment supply-chain water and water consumed at the point of electricity generation. The analysis considers ten cooling configurations and nineteen ASHRAE climate zones. The server model varies utilization, server vintage/refresh cycle, server efficiency quantile, and inactive-server fraction.

The abstract reports workload-level water-use variation exceeding 10,000-fold, with more than 1,000-fold differences in electricity-generation water-consumption factors and approximately 10-fold differences in server workload efficiency. These are the authors' reported scenario/model findings, not universal measured constants.

## Full-text limitations directly relevant to this project

1. **Consumption, not withdrawal.** The authors explicitly state that their workload-level water-use metric accounts for water consumption, not water withdrawals, and recommend adding electricity water-withdrawal factors for future total-site assessments (article Section 5, pp. 26–27).
2. **U.S.-weighted grid factors.** The electricity water-consumption factors use generation-weighted U.S. averages and do not resolve regional differences, power-plant cooling technology, prime-mover technology, or other factors.
3. **Server-centric workload representation.** Servers are the primary modeled IT load. The authors identify GPUs, storage, and network loads as extensions. The paper notes that its framework could be extended to AI training/inference metrics such as MLPerf when sufficient data exist; it does not directly establish an AI-workload-specific water factor.
4. **Benchmark representativeness.** The server-efficiency model uses SPECpower_ssj 2008. The authors warn that this benchmark may not represent the installed server population over time and that even its least-efficient servers may be more efficient than typical volume servers, potentially understating upper-bound water use.
5. **No time-resolved operational ledger established by this paper.** The published framework is scenario/decomposition based. The inspected article and supporting-code entry points do not establish an hourly, facility-level time series of water withdrawals and consumption or a temporally matched heat/desalination dispatch model.
6. **No counterfactual freshwater-displacement test.** The article quantifies workload water consumption; it does not evaluate the marginal freshwater displaced by a specific saline-feed desalination system, the additional source-water withdrawals and brine consequences of that system, or a net-water-benefit counterfactual of the type required by this repository's research question.

## Reproducibility and supporting materials inspected

The article points to a public GitHub repository containing:
- `SI Supporting Code.Rmd`
- `SI Supporting Code 2 (WaterSensitivity).ipynb`
- `data/SPEC_2024.xlsx`
- `data/UEs_16cases.csv`
- Sobol/sensitivity result CSV files.

The R Markdown code exposes scenario dimensions including refresh cycle (1–8 years), server-efficiency quantiles (5th/95th), utilization (10–80%), and inactive-server fraction (5%/30%). It uses SPECpower server power/performance data and local smoothing/regression functions to estimate server electricity per workload. This inspection confirms that supporting code and input/result files are publicly listed; it is **not** a clean-environment execution or independent numerical reproduction. The supporting repository's README provides only a brief contact line, and the complete supporting package was not independently executed in this audit.

## Implications for the present Research 2 framework

This paper is a strong source for defining the **data-centre baseline consumption ledger** and for avoiding simplistic workload-to-water assumptions. It supports keeping server efficiency, utilization, cooling configuration, climate, facility efficiency, and grid water-consumption factors explicit rather than collapsing them into a single universal WUE or litres-per-workload constant.

It does **not** close the repository's withdrawal-accounting gap. A Research 2 net-water comparison must keep at least the following terms distinct and source-specific:

- direct facility water withdrawal and consumption;
- electricity-generation water withdrawal and consumption (using region- and technology-appropriate factors);
- saline feedwater withdrawal and freshwater product recovery;
- desalination process electricity and associated upstream water impacts;
- brine/concentrate discharge or MLD/ZLD management;
- the counterfactual freshwater source and the amount of freshwater actually displaced;
- temporal matching between available waste heat, desalination operation, and data-centre water demand where operational claims are made.

Care is needed not to double-count grid water: if facility electricity is already multiplied by a source-based water factor, the site and upstream components must be defined consistently with the selected boundary. The Lei et al. WCF is a **consumption** factor and cannot be substituted for a withdrawal factor.

## Bounded prior-art assessment

Lei et al. (2025) is prior art for workload-normalized direct-plus-indirect data-centre water **consumption** and for decomposing its determinants. It is not, on the evidence inspected, prior art for a time-resolved withdrawal-versus-consumption ledger coupled to waste-heat-driven membrane distillation with explicit counterfactual freshwater displacement.

This is a bounded distinction, not a novelty claim. Other literature may address parts or all of those components; Issue #16 remains open pending the remaining systematic search and full-text comparisons.

## Unresolved work

- Independently execute the published supporting code in a clean environment and record exact versions, input hashes, and outputs before relying on any numerical reproduction.
- Audit the supplementary information and source data more deeply, including the provenance and boundary of each WCF and the construction of the cooling-system PUE/WUE scenarios.
- Obtain full methods/equations/tables and supplementary information for Katakam et al. (2026 online / 2027 issue) and compare its SWUI boundary with this project's accounting boundary.
- Continue the Kanbur (2020) full-text and supplement access attempt; no paid purchase or author contact is authorized by this audit.
- Continue database-specific prior-art searching and screening; this single-paper audit does not constitute a systematic review.

## Source access log

| Source | Accessed | Evidence level |
|---|---|---|
| Lei et al. main article PDF via eScholarship | 2026-11-04 | Full text read |
| LBNL publication record | 2026-11-04 | Bibliographic record and abstract |
| Lei et al. public GitHub repository | 2026-11-04 | Repository file list and R Markdown source inspected; no clean execution |
| Lei et al. supplementary information | 2026-11-04 | Supporting code inspected; separate SI PDF not independently obtained in this audit |
| Katakam et al. publisher/PubMed records | 2026-11-04 | Abstract and extended indexed publisher text only; full methods/SI not verified |
