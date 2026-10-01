# Free-source recovery update — 2026-10-01

## Confirmed no-cost source

Keshavarzzadeh (2020), “Design and bio-inspired optimization of direct contact membrane distillation for desalination based on constructal law,” Scientific Reports 10, 16790, DOI: 10.1038/s41598-020-73964-7, is openly available under CC BY 4.0.

- Publisher article: https://www.nature.com/articles/s41598-020-73964-7
- Free full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC7545101/
- DOI: https://doi.org/10.1038/s41598-020-73964-7

This is sufficient to inspect and implement the published equations legally. It is not sufficient by itself to establish independent validation because its Figure 3 experimental-marker provenance contains a citation mismatch that remains unresolved in this repository.

## Primary 1999 experimental paper

Martínez-Díez & Vázquez-González (1999), “Temperature and concentration polarization in membrane distillation of aqueous salt solutions,” Journal of Membrane Science 156(2), 265–273, DOI 10.1016/S0376-7388(98)00349-4.

- Publisher record/abstract: https://www.sciencedirect.com/science/article/pii/S0376738898003494
- DOI: https://doi.org/10.1016/S0376-7388(98)00349-4

The publisher page currently exposes the bibliographic record and abstract but not a free full-text copy. Do not pay for it solely to keep the project moving. The accessible 2020 open article, its supplementary material if any, and later legally accessible sources can support model development, but cannot be mislabelled as an independently recovered primary dataset.

## Legal recovery routes, in order

1. Check the college library's licensed ScienceDirect access while on campus or through its authorized remote-access route.
2. Search the authors' institutional repositories and university library catalogues for an accepted manuscript.
3. Request a personal research copy from the corresponding author through the publisher's “request article” or author contact route.
4. Use interlibrary loan/document delivery if the institution offers it.
5. If no lawful copy can be obtained, retain the 1999 source as a provenance lead and use only openly accessible datasets for quantitative validation.

Do not use unauthorized shadow libraries, bypass paywalls, or reproduce restricted article tables/figures without a lawful basis. Record the access route and licence for every extracted dataset.

## Validation consequence

Until the original experimental observations and exact operating conditions are lawfully accessible and crosswalked, the Keshavarzzadeh Figure 3 dataset remains a **development/reproduction target**, not independent held-out validation. The repository's source runner may be tested for numerical stability and conservation, but its output must not be described as experimentally validated.


## Newly identified open experimental dataset: Villa et al. (2018)

A publicly accessible NREL/Geothermal Data Repository dataset provides experimental DCMD and AGMD workbooks for 3M, Aquastill, and CLARCOR membranes, including co-current and counter-current configurations:

- Dataset title: *Membrane Specifications for Multi-Configuration Membrane Distillation Model*
- Authors: Villa, Vanneste, Cath, Turchi, and Akar
- DOI: 10.15121/1452747
- Record: https://gdr.openei.org/submissions/1016
- Size: 7 workbooks, approximately 95.97 MB
- Published record: 2018-03-01
- Conditions described in the record include 4 g/L NaCl, with configuration-specific flow and membrane area.

This is a promising legal alternative to the paywalled 1999 primary paper for **independent DCMD model validation**. It does not replace the 1999 source for reproducing the Keshavarzzadeh Figure 3 case because the membranes, geometry, salinity, and boundary conditions differ.

The repository search record displays a Creative Commons indicator, but the exact CC licence variant must be verified from the dataset's licence metadata before redistributing adapted data. The workbooks contain both experimental data and theoretical/calculated worksheets: only measured observations may be used as validation targets. The benchmark is registered as MD-OEDI-VILLA-2018; extraction, checksum capture, licence verification, and a held-out split remain pending.


## Newly identified open transient dataset: Ali, Orfi & Najib (2020)

The PLOS ONE article *Developing and validating a dynamic model of water production by direct-contact membrane distillation* is open access under CC BY 4.0 and includes five XLSX supporting-data files (S1–S5). The article reports a 10 m² spiral-wound counter-current DCMD pilot, 50/100/200/300 L/h feed-flow cases, 50–80 °C feed-temperature cases, nominal 25 °C cold inlet, 0.5% salinity, and 10-second sampling. The supporting files include experimental response data. The paper also reports that uncorrected dynamic models showed substantial mismatch, while a tuned heat-loss correction reduced the reported average relative error; that tuning is evidence of model-form risk, not an independent validation result for this project.

- Article and supporting-information links: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207
- DOI: 10.1371/journal.pone.0230207
- Licence: CC BY 4.0

This dataset is now registered as MD-DCMD-DYNAMIC-ALI-2020. It can support a future transient-validation track, but the current engine is not yet a transient MD model. Extract measured accumulated mass and actual input histories separately from the paper's extrapolated curves and model predictions. Do not claim transient validation until the time-dependent model and a held-out operating-condition split are in place.
