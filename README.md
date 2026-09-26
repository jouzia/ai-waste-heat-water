# From AI Waste Heat to Water

Research 2 — Sustainable AI infrastructure, waste-heat recovery, membrane distillation, and net freshwater impact.

## Research question

Under what combinations of AI workload intensity, thermal conditions, waste-heat recovery efficiency, membrane-distillation operation, cooling burden, electricity-water intensity, and geographic water stress can waste-heat recovery produce a positive net freshwater benefit?

## Principle

Gross freshwater production is not treated as net water benefit. Cooling, pumping, auxiliary electricity, pretreatment, heat losses, and indirect water use are explicitly considered.

## Current implementation status

- Reproducible Python package skeleton established.
- Transparent baseline water/energy accounting engine implemented.
- Initial MD vapor-pressure transport primitive implemented using NIST water vapor-pressure data.
- Automated tests cover baseline limiting cases and MD temperature behavior.
- Source/provenance registry started.

## Scientific status

No scientific conclusion is claimed yet. The baseline model is not an industrial digital twin. Salinity effects, interface temperatures, detailed cooling, pumping, uncertainty distributions, geographic factors, and experimental validation remain required before quantitative deployment conclusions are reported.
