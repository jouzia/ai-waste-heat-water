# External Data Provenance Protocol

This project uses external datasets only for variables that the source actually measures or models. No external indicator is converted into a site-specific physical measurement without an explicit transformation and uncertainty statement.

## Required provenance fields

Every external parameter or dataset used in a published run must record:
- source_id
- provider/organization
- dataset name
- version or release
- retrieval date
- official source URL
- license/use terms
- variable definition and unit
- spatial and temporal resolution
- original value/file identifier
- transformation/calculation
- uncertainty or source-reported error
- model parameter receiving the value
- citation

## Prohibited shortcuts

- Do not treat WRI Aqueduct composite risk as a measurement of local freshwater availability.
- Do not treat NASA POWER/MERRA-2 grid values as on-site weather-station observations.
- Do not mix modeled climate forcing with measured hydrology without labeling the distinction.
- Do not use a universal electricity-water factor.
- Do not treat recovered distillate as avoided freshwater consumption unless the counterfactual displacement is explicitly demonstrated.

## Dataset handling

Large upstream datasets remain external. The repository stores metadata, retrieval manifests, extraction scripts, checksums, and small derived tables required for reproducibility. Raw files remain subject to the provider's applicable terms.

## Source selection hierarchy

For quantitative model inputs, prefer in order: (1) measurement or source-matched experiment, (2) official observational dataset, (3) validated physical model/reanalysis, (4) peer-reviewed parameter estimate, (5) explicitly labeled scenario assumption. A lower tier must never silently replace a higher tier.

## Geographic evidence chain

site coordinate -> climate forcing -> hydrological context -> basin water-risk screening -> operational water model

Each link remains separately identifiable in the experiment registry.
