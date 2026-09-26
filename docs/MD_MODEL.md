# Membrane-distillation model: staged implementation

## Stage 1 — pressure-driving-force module

The transport model starts from the standard MD relationship:

J = C_m (p_hot - p_cold)

where J is membrane mass flux, C_m is membrane permeance, and the pressure
terms are water-vapor pressures at the membrane interfaces.

Published MD reviews describe vapor-pressure difference as the fundamental
mass-transfer driving force and identify heat transfer, temperature
polarization, concentration polarization, membrane properties, and
configuration as important parts of a realistic model.

The repository therefore treats C_m as an explicit parameter. It must not be
silently inferred from an unrelated experiment.

## Stage 1 limitation

The current implementation uses pure-water saturation pressure only.
It does not yet model salinity/activity effects, membrane-interface
temperature polarization, concentration polarization, membrane pore-scale
transport, conductive heat leak, configuration-specific cold-side behavior,
or fouling/wetting.

Consequently, the MD module is a transport primitive, not a complete digital twin.

## Validation source

Water saturation-pressure coefficients are taken from NIST Chemistry WebBook
SRD 69. The implemented coefficient ranges are 304–333 K and 334–363 K.

Before saline-feed simulations are reported, a validated activity or
vapor-pressure correction and an interface-temperature model must be added.
