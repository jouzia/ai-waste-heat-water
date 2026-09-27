# Model Card

## Intended use

Screening, sensitivity analysis, literature reproduction, and scenario exploration for the question of whether AI/data-centre waste heat can support membrane distillation without producing a larger operational freshwater burden elsewhere.

## Model type

Deterministic reduced-order coupled energy/water model with optional literature fluxes, membrane thermal properties, hydraulic pressure-drop calculations, cooling-burden inputs, and an IAPWS-08 standard-seawater thermodynamic pathway.

## Outputs

The model reports IT energy, facility energy, recoverable heat, MD thermal duty, latent duty, conductive membrane heat leak, cooling duty, cooling electricity/water, product water, feed withdrawal, concentrate discharge, concentrate salinity, pumping electricity, auxiliary electricity, indirect electricity-related water, and an explicit net-consumption-change screening metric.

## Known limitations

- Current interface-temperature treatment is reduced-order unless measured interface temperatures are supplied.
## Salinity and thermodynamics\n\nFor the primary standard-seawater benchmark, IAPWS-08 supplies the seawater thermodynamic pathway. IAPWS describes the formulation as applicable to IAPSO standard seawater and gives documented validity limits; the model treats those limits as constraints rather than silently extrapolating.\n\nThe single-pass concentration layer assumes complete salt retention and uses water-removal-weighted bulk salinity. Concentration polarization, local channel gradients, precipitation, and recycle remain outside this layer.\n\n## Known limitations
- The model does not yet resolve channel-level mass/energy balances.\n- Concentration polarization is not explicitly resolved.
- Cooling is parameterized rather than solved from a detailed heat-sink model.
- Electricity-water factors are external site parameters.
- Embodied water and full life-cycle impacts are outside the current operational boundary.
- Numerical outputs are not evidence of industrial feasibility.

## Validation hierarchy

1. Unit/equation tests.
2. Literature reproduction using source-matched configurations.
3. Sensitivity and qualitative trend checks.
4. Physical validation of selected transfer relationships where feasible.

A desktop prototype, if constructed, will not be described as validation of an industrial AI data centre.

## Reproducibility

Every empirical parameter used in a published result should be traceable through parameters/parameter_registry.yaml and SOURCES.yaml. Scenario-only assumptions must remain visibly identified.
