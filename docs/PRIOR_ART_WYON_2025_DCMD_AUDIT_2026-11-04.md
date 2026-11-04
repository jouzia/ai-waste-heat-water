# Wyon (2025) DCMD and data-centre waste-heat prior-art audit

**Audit date:** 2026-11-04  
**Source:** Annie Wyon, *Desalination utilizing data centre waste heat: A techno-economic study*, Master thesis, Lund University, June 2025. [Institutional record](https://lup.lub.lu.se/student-papers/record/9198095) · [Full 53-page PDF](https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf)

## Executive finding

This is direct and highly relevant prior art. Wyon models a hypothetical 1.5 MW direct-to-chip data centre in Barcelona coupled to direct-contact membrane distillation (DCMD), including a heat exchanger, two pumps, thermodynamic calculations, pump power, cost of water, space, and three freshwater-use cases. It predates this project and prevents claims that data-centre waste heat + MD/DCMD integration, a thermodynamic system model, pump-aware energy accounting, or techno-economic assessment are new.

The thesis is a student master's thesis and a modelled case study, not an operational demonstration. Its existence is nevertheless sufficient to establish conceptual and modelling prior art.

## Scope and system boundary

- No heat upgrading: the thesis explicitly limits scope to direct use of data-centre waste heat.
- Hypothetical 1.5 MW direct-to-chip data centre in Barcelona.
- DCMD modules based on literature, a commercial heat exchanger and two commercial pumps.
- Product-water cases: data-centre air-cooling, electrolyser feed for backup hydrogen production, and sale to the local water grid.
- Reported production varies with source heat and seawater temperature; the thesis describes a range below 0.1 to 0.7 m³/h for the case-study system.
- The thesis evaluates water production, electricity, simplified water cost and space requirement.

## Reconstructable physical model

The thesis gives an equation-level DCMD formulation, not merely a black-box yield coefficient:

1. **Heat balance across the membrane:** neglecting heat losses, feed-side convection, membrane heat transfer and permeate-side convection are set equal: q_f = q_m = q_p = q_total.
2. **Boundary-layer heat transfer:** q_f = alpha_f (T_f - T_f,m) and q_p = alpha_p (T_p,m - T_p), with convective coefficients from Nusselt correlations.
3. **Membrane heat flux:** q_m = q_v + q_c = J H_v + (k_m/delta_m)(T_f,m - T_p,m), explicitly including latent heat carried by vapour and conductive heat leakage.
4. **Mass flux:** J = c (p_f,m - p_p,m), with a combined Knudsen/molecular diffusion coefficient. The thesis assumes transitional diffusion with Knudsen number 0.5.
5. **Iterative solution:** membrane-surface temperatures are iterated to satisfy heat-flux consistency; enthalpy rates then determine feed/permeate outlet temperatures.
6. **Salt balance:** feed salinity is updated from inlet/outlet mass flow and density.
7. **Hydraulics:** module and heat-exchanger pressure drops are used to size feed and permeate pumps; module pressure drop uses a smooth-channel turbulent friction correlation.

This is a useful independent reconstruction target. It also means our existing fixed cooling-to-heating and fixed water-per-thermal-energy coefficients are materially less mechanistic than this prior model.

## Validation and limitations recorded by Wyon

- The DCMD heat-flux model is compared against experimental values from its cited reference.
- Wyon reports a discrepancy of up to 11%; the thesis says the apparent error may originate in the mass-flux calculation, but its exact cause was not identified.
- Wyon also notes that the experimental temperature range does not match the range used for extracting the case-study results.
- The thesis characterises its components as simplified estimates. It notes that production and cost estimates may be affected by model discrepancy and assumed 95% operational availability.
- The thesis suggests exploring alternative MD configurations (including water-gap MD) and heat recovery as future work.

Thus it is inaccurate to call the thesis model experimentally validated without qualification. It is a model checked against experimental heat-flux data, with a documented residual discrepancy and a temperature-range mismatch.

## Water accounting: what it does and does not establish

Wyon discusses data-centre WUE and the potential to use produced water for cooling, hydrogen production or grid sale. It compares the modelled cost of produced water with local freshwater pricing and discusses local water availability and public opposition.

The thesis does **not** present a full net-blue-water counterfactual ledger in the sense required by this project. In particular, the inspected thesis does not formulate a source-specific freshwater displacement fraction, quantify the incremental upstream water burden of all auxiliary electricity under an explicit grid-water factor, or provide a spatially resolved water-stress-weighted net water impact. Do not infer that these dimensions are absent from every possible supplementary dataset; they are not established in the thesis text reviewed here.

## Implications for Research 2

### Novelty claims ruled out

Do not claim:
- first integration of data-centre waste heat with membrane distillation/DCMD;
- first thermodynamic model of this coupled system;
- first DCMD system assessment including pumps and pressure drops;
- first study of data-centre cooling, hydrogen or external sale as product-water uses;
- first techno-economic or space assessment of DCMD using direct-to-chip waste heat.

### Potentially differentiating work, still unproven

A defensible extension would need to demonstrate something substantive beyond Wyon, for example:
- a reproducible, independently tested MD model with source-traceable equations and parameter provenance;
- a transparent, time-resolved heat-availability/temperature/flow eligibility model linked to real or defensible data-centre operating profiles;
- an explicit operational blue-water balance that distinguishes seawater intake, freshwater product, brine/return flows, consumptive losses, auxiliary electricity water, and counterfactual freshwater displacement;
- location- and time-specific water-stress weighting and uncertainty propagation;
- a rigorous comparison against Wyon's DCMD baseline and other published DCMD configurations, with validation error reported on matched experimental conditions.

These are candidate research directions, not a novelty or contribution claim. The current reduced-order screening engine is not equivalent to Wyon's equation-level DCMD model and must not be presented as if it were.

## Reproduction checklist before any model upgrade

1. Extract Wyon's complete standard-condition tables and module geometry.
2. Trace each DCMD equation to its cited source and retrieve the underlying experimental dataset/reference where lawfully accessible.
3. Reconstruct heat-exchanger effectiveness and terminal-temperature constraints.
4. Reconstruct module pressure-drop and pump-efficiency assumptions, including pump curves and commercial equipment data.
5. Reproduce the thesis's reported heat-flux comparison and quantify error over the same temperature range before extrapolating.
6. Reproduce at least one complete case-study operating point and water-production result before using it as a benchmark.
7. Preserve the distinction between freshwater production and net freshwater benefit.

## References

- Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University. [Institutional record](https://lup.lub.lu.se/student-papers/record/9198095).
- Kanbur, B. B., Wu, C., & Duan, F. (2020). Multi-criteria thermoeconomic and thermodynamic assessments of the desalination-integrated two-phase liquid-immersion data center cooling system. *International Journal of Energy Research*, 44, 10453–10470. DOI: [10.1002/er.5677](https://doi.org/10.1002/er.5677). (Separate direct-prior-art audit: PR #56.)
