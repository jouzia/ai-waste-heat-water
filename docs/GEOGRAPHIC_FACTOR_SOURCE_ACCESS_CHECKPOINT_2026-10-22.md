# Geographic factor source-access checkpoint — 2026-10-22

## Purpose

Record what could be verified during the next geographic-accounting pass, and prevent a reporting template or modeled scenario from being silently promoted to observed grid-water data.

## Verified findings

### CEA thermal-station water reporting

The official Central Electricity Authority (CEA) site indexes an annual water-consumption format for all thermal power stations and a monthly environmental-data format. The public landing page is:

- https://www.cea.nic.in/divisionPage/510?lang=en
- https://cea.nic.in/monthly-annual-environmental-data-format-for-thermal-power-stations/?lang=en

During this review, the second URL redirected to the CEA login page. Search-indexed content exposed the names of the downloadable XLSX templates, but the template/landing-page evidence does **not** provide a public, complete, machine-readable collection of observed plant-level water consumption values. Therefore no plant observations were extracted and no CEA-derived factor is populated in the factor ledger.

The CEA data discovery result is a source-access limitation, not evidence that the CEA does not hold or collect the records.

### Matching electricity generation

The Government of India's Open Government Data catalog describes a station-wise monthly power-generation dataset with station location, fuel, installed capacity, programmed generation, and actual generation:

- https://data.gov.in/catalog/power-generation

This is a candidate denominator source, but it cannot be paired with the water reporting template until compatible observed water records are available and station identifiers, reporting periods, units, and generation boundaries are reconciled.

### India multi-model scenario source

Srinivasan et al. (2018), *Water for electricity in India: A multi-model study of future challenges and linkages to climate change mitigation*, reports modeled India-level projections through 2050 from five energy-economic modeling teams:

- DOI: https://doi.org/10.1016/j.apenergy.2017.04.079
- CEEW overview: https://www.ceew.in/publications/water-electricity-india
- Publisher record: https://www.sciencedirect.com/science/article/abs/pii/S0306261917304725

This is appropriate for a clearly labeled India-specific **scenario range** only after the relevant numerical tables, definitions, model scenario, year, and denominators are extracted and checked. It is not a measured Chennai grid factor. The paper itself emphasizes that results depend on generation mix and cooling technology and that uncertainty is high.

## Decision for this repository

1. Leave `data/geography/electricity_water_factors.csv` header-only until a source-backed row can be fully documented.
2. Do not use regulatory water-consumption limits as observed plant performance or a national average.
3. Do not divide a national annual water total by electricity generation unless both totals cover matching plant populations, reporting periods, water metrics, and system boundaries.
4. If plant-level observations remain inaccessible, use a separate, explicit modeled-scenario analysis derived from a source table; do not describe it as observed or city-specific.
5. Keep direct facility WUE, upstream electricity-generation water, and Aqueduct basin stress as distinct terms. Do not multiply water-stress scores into physical water volumes.
6. Geographic integration remains an open publication gate.

## Next executable data task

Acquire the actual CEA annual reporting workbook/data and a compatible station-generation table from a lawful public source or direct request. If actual observations cannot be obtained, extract the India multi-model paper's scenario table(s) with exact page/table references and build a scenario-only factor ledger. The paper's full methods and supplementary data must be checked before assigning numerical factors.

## Claim boundary

This checkpoint confirms source discovery and the present access limitation. It does not confirm a completed factor join, a physical validation result, or a net-water benefit.
