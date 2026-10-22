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


## Execution status

The geographic layer is a declared analysis interface, not yet an executed site study. Before any site-level result is reported, the study must ingest a versioned Aqueduct release, freeze site/basin mapping, attach a site-specific electricity-water factor with its system boundary, and preserve retrieval metadata. NASA POWER climate forcing is complementary and must not be substituted for Aqueduct water-stress indicators.


## Official Aqueduct source discovery (2026-10-13)

The official WRI landing page exposed the archive URL `https://files.wri.org/aqueduct/aqueduct-4-0-water-risk-data.zip`. A HEAD request reports 261,527,511 bytes, byte-range support, and a Last-Modified header of 2025-08-06. The ZIP central directory was inspected through HTTP range requests; the full archive was not downloaded.

The embedded geodatabase `Aqueduct40_waterrisk_download_Y2023M07D05/GDB/Aq40_Y2023D07M05.gdb` exposes three layers in EPSG:4326:

- `baseline_annual`: 68,506 multipolygons; includes `pfaf_id`, country/admin names, `bws_score/cat/label`, and `bwd_score/cat/label`.
- `baseline_monthly`: 16,395 multipolygons; includes monthly BWS/BWD/IAV fields.
- `future_annual`: 16,395 multipolygons; includes source-native `bau`, `opt`, and `pes` future water-stress fields for 2030/2050/2080.

The repository now has a reproducible remote-GDAL sampling script and six clearly labeled **city-centroid proxies** in `data/geography/site_proxies.csv`. They are not actual data-centre locations. Baseline and future layer basin IDs are recorded separately because the layers have different feature counts and must not be assumed to share identical geometry/resolution. Water stress remains contextual metadata, not a multiplier on water volume. Electricity-water factors and a defensible facility-site dataset remain missing; the geographic publication gate stays false until the site-sampling artifact, future-field semantics, and grid-water/carbon data are reviewed.


## First reproducible city-proxy sample (2026-10-13)

The workflow [Aqueduct discovery run #7](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38431293877) sampled both `baseline_annual` and `future_annual` through GDAL's remote ZIP access. Artifact ID `11830717527`, SHA-256 `ab2d0d47095c6dd7b9f18dfe02054511157d2f2181fb0b47d0e030c829d63699`, expires 2027-01-11. All six illustrative city-centroid proxies matched a polygon in both layers. The CSV output SHA-256 is `6ebdd18ecad452411dbac87fecd8fe1df274345f043fb3fc1a4221a796d66d23`.

| City proxy | Baseline BWS score | Source label | Baseline BWD label | Future annual BAU labels (2030/2050/2080) |
|---|---:|---|---|---|
| Barcelona | 4.544 | Extremely High (>80%) | Medium–High (25–50%) | Extremely high (>80%) / Extremely high (>80%) / Extremely high (>80%) |
| Chennai | 4.943 | Extremely High (>80%) | High (50–75%) | Extremely high (>80%) / Extremely high (>80%) / Extremely high (>80%) |
| Hyderabad | 5.000 | Extremely High (>80%) | Extremely High (>75%) | Extremely high (>80%) / Extremely high (>80%) / Extremely high (>80%) |
| Phoenix | 5.000 | Extremely High (>80%) | High (50–75%) | Extremely high (>80%) / Extremely high (>80%) / Extremely high (>80%) |
| Singapore | 0.000 | Low (<10%) | Low (<5%) | Low (<10%) / Low (<10%) / Low (<10%) |
| Frankfurt | 3.453 | High (40–80%) | Low–Medium (5–25%) | High (40–80%) / High (40–80%) / High (40–80%) |

These are basin indicators at **approximate city-centre points**, not facility locations. They are not multiplied into water volumes. The sample demonstrates the spatial extraction pipeline and variation in basin context, not that a real data centre at any city would experience the listed value. Future-field names were checked against source labels, but future scenario assumptions still need a complete README-backed semantic crosswalk before publication. The geographic gate remains false because site coordinates are illustrative and the electricity-water/carbon factors are not yet joined.


## Electricity–water factor audit (2026-10-22)

The factor-source review is recorded in [GEOGRAPHIC_ELECTRICITY_WATER_FACTOR_AUDIT_2026-10-22.md](GEOGRAPHIC_ELECTRICITY_WATER_FACTOR_AUDIT_2026-10-22.md). The key decision is that the openly available NREL/OpenEI technology factors are U.S.-scope and cannot be assigned as primary values to the non-U.S. city proxies. India-specific CEA reporting and peer-reviewed India water-for-electricity modeling are identified as candidate sources, but a compatible factor join has not been executed. Direct data-centre WUE, electricity-generation water intensity, and Aqueduct risk remain separate quantities. The geographic gate remains false.
