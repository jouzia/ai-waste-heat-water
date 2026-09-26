# Parameter Extraction Protocol

A literature number is not entered into the model merely because it looks plausible.

For every candidate parameter record the exact definition, symbol, value, unit,
operating conditions, MD configuration, feed composition, membrane properties,
measurement/calculation status, source identifier, exact table/figure/equation
location, uncertainty, transformation, and validation status.

## Priority parameters

### MD transport
- membrane permeance or mass-transfer coefficient
- flux
- feed/permeate interface temperatures
- temperature polarization coefficient
- concentration polarization coefficient
- membrane thermal conductivity
- latent and conductive heat transfer

### Thermal integration
- waste-heat source and return temperature
- heat availability profile
- exchanger effectiveness and approach temperature
- recoverable heat fraction
- cooling duty and heat-sink temperature

### Hydraulics
- channel pressure drop
- flow rate
- pump efficiency
- pumping electricity
- single-pass recovery

### Water accounting
- cooling withdrawal and consumption
- MD feed withdrawal
- electricity-generation water factor
- site/source WUE
- water-stress indicator

## Evidence classes

A = measured or independently reproduced peer-reviewed primary result.
B = peer-reviewed synthesis with traceable provenance.
C = authoritative dataset or standard.
D = engineering/scenario assumption.

Classes A-C may support empirical parameterization when applicability is
documented. D remains scenario-only unless independently validated.

## Reproduction rule

A literature reproduction benchmark must preserve the source boundary,
configuration, units, operating conditions and uncertainty. Parameters from
incompatible MD configurations must not be mixed simply to construct a
convenient case.
