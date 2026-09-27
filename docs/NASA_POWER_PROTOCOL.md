# NASA POWER Climate Forcing Protocol

## Purpose

NASA POWER is used as a climate-forcing layer for cooling and heat-sink scenario analysis, not as a substitute for on-site instrumentation.

NASA documents that its meteorological parameters are based on GMAO MERRA-2 assimilation products. MERRA-2 provides hourly global estimates on a 0.5 degree x 0.625 degree grid; POWER exposes analysis-ready temporal products including hourly and daily data.

## Variables

Initial climate forcing should prioritize only variables with a documented role in the cooling model:
- near-surface air temperature
- dew-point temperature or humidity where required by the heat-rejection model
- wind speed at the documented height
- surface pressure where required
- precipitation only when used for a defined water-availability or operational context

## Retrieval metadata

Each extraction must record:
- dataset: NASA POWER
- source family: GMAO MERRA-2 for meteorological parameters
- parameter
- latitude and longitude
- start and end date
- temporal resolution
- retrieval date
- API/product version when exposed
- units
- source grid resolution
- transformation
- experiment_id

## Validation treatment

NASA documents comparisons of MERRA-2 meteorological parameters with NCEI surface observations, including bias and RMSE statistics. Those source-reported uncertainties must be preserved when climate forcing materially affects a result. For high-stakes site conclusions, an observational station dataset should be used as an independent contextual check where coverage permits.

## Modeling rule

Climate forcing modifies the heat-sink/cooling constraint. It must not directly modify membrane transport equations unless it is physically justified as a boundary condition.

Therefore:

climate forcing -> heat rejection boundary -> cooling burden

is kept separate from:

MD feed/permeate temperatures -> vapor pressure -> flux.

## API

The official POWER temporal APIs provide analysis-ready time series and machine-readable formats. Retrieval scripts must cache request metadata and a checksum of the resulting response.
