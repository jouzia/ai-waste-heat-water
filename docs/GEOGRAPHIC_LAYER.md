# Geographic Layer

The geographic layer maps the operational water result to site conditions without
turning a water-stress score into a universal threshold.

## Primary external source

WRI Aqueduct 4.0 is the primary water-stress screening dataset. The current
WRI Data Explorer entry was updated 22 September 2026 and provides basin-level
baseline indicators plus future projections for 2030, 2050 and 2080 under CMIP6
scenarios.

Source:
- WRI Aqueduct 4.0 Current and Future Global Maps Data
- https://datasets.wri.org/datasets/aqueduct-global-maps-40-data
- https://www.wri.org/data/aqueduct-global-maps-40-data

## Legal and provenance rule

WRI states that Aqueduct 4.0 may be shared, reproduced, and adapted with attribution under CC BY 4.0. Public outputs using the dataset must preserve attribution and the dataset version/retrieval date. If WRI registration is required for adaptation/sharing, complete that registration through the official WRI process rather than through research tooling. See `docs/EXTERNAL_DATA_LEGAL.md`.

Required attribution: `Source: WRI Aqueduct, accessed on [insert date]. Licensed under Creative Commons Attribution International 4.0.`

## Required fields

Each modeled site should record:

- site_id
- latitude / longitude or HydroBASINS identifier
- country / administrative region
- Aqueduct version and retrieval date
- baseline water-stress indicator and unit/scale
- relevant future scenario/year when used
- electricity-water factor
- electricity-water-factor source and boundary
- climate/heat-sink assumptions
- source IDs for every transformed parameter

## Boundary rule

Aqueduct is a screening/prioritization dataset. Its composite risk indicators
must not be treated as direct measurements of local freshwater availability.
Site-level conclusions should preserve the basin indicator, source version,
spatial mapping method, and uncertainty.

## Data policy

Do not commit the full WRI ZIP or derived geospatial database to the repository.
Store acquisition metadata and small derived tables only. Record the exact
source version and retrieval date so another researcher can reconstruct the
analysis.
