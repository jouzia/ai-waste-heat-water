# Uncertainty and model-form prior register

Version: 2026-10-11

## Purpose

This register separates **measured variability**, **parameter uncertainty**, **model-form uncertainty**, **scenario uncertainty**, and **counterfactual uncertainty**. A probability distribution is not justified merely because a parameter is uncertain. Until a traceable empirical basis is available, use a deterministic scenario grid and label it as such.

## Register

| Quantity | Uncertainty class | Evidence required | Permitted treatment before evidence is complete | Prohibited shortcut |
|---|---|---|---|---|
| Membrane transport coefficient / flux | Parameter + model form | Source-matched membrane properties, operating conditions, and primary measured flux | Keep the source runner's explicit engineering closure separate from the modern model; run unfitted validation first | Fit to the same points later called held-out; report provisional flux as validated |
| Liquid properties, latent heat, vapor pressure | Parameter/model form | Traceable property source, unit convention, temperature range, salinity domain | Compare source-published correlations with a named authoritative property model; document domain and discrepancy | Mix equations from incompatible sources without an audit |
| Channel heat-transfer coefficient | Model form | Geometry and flow regime plus independent measurements or established correlation applicability | Compare source-specific entry-effect correlation against an alternative applicable correlation | Choose whichever correlation gives the lowest error on the held-out set |
| IT heat availability and temperature | Measured temporal variability | Site or openly documented time series with timestamp, load, temperature, and measurement context | Use explicitly labeled synthetic profiles only for software tests; otherwise state that the dynamic case is unparameterized | Infer recoverable heat from annual-average IT electricity alone |
| Heat-exchanger effectiveness / approach temperature | Parameter + scenario | Equipment datasheet or measured inlet/outlet temperatures and flows | Sweep an explicit engineering scenario grid and show the assumed range | Treat all IT waste heat as MD-eligible at the same temperature |
| MD cooling duty and heat sink | Model form + architecture | Configuration-specific energy balance and cooling architecture | Use the 2026 Malaguti analysis only to motivate configuration-specific cases; its reported 80–100% cooling/heating ratio applies to some open-loop cases, not universally | Assign one universal cooling ratio to all MD systems |
| Pumping energy | Parameter + model form | Geometry, flow, pressure-drop relation, pump curve/efficiency, and operating point | Calculate from explicit hydraulics; sweep pump efficiency only within a stated evidence range | Set pumping to zero because heat is free |
| Grid water intensity | Geographic/time variability | Traceable region, year, grid mix, and water-consumption/withdrawal definition | Use a site/year-specific factor or compare sourced alternatives as discrete scenarios | Use one global water-per-kWh factor without source and year |
| Water-stress indicator | Impact-assessment uncertainty | Named basin/geographic resolution, indicator version/year, and documented method | Report the physical water ledger separately; show stress-weighted results as secondary | Treat a stress score as physical liters or as a direct measure of local water availability |
| Freshwater displacement fraction | Counterfactual uncertainty | Evidence that the produced water displaces a named freshwater source and how much consumption is avoided | Run explicit cases such as 0, partial, and full displacement; the model bounds the fraction to [0, 1] | Treat distillate production as automatically avoided consumption |
| Cooling architecture / water source | Discrete scenario uncertainty | Explicit baseline and intervention architectures, source water, and boundary definitions | Compare named architectures side-by-side | Average mutually exclusive architectures into a fictitious single system |
| Membrane fouling/scaling and long-term drift | Temporal/model uncertainty | Long-duration measurements under matching feed chemistry and recovery | Mark as excluded or use explicit degradation scenarios until evidence is available | Extrapolate short steady-state tests to lifetime operation without caveat |
| Parameter dependence | Statistical structure | Joint measurements, physical constraints, or a justified dependency model | Preserve known dependence; otherwise perform dependency stress tests and label independent sampling as an assumption | Assume every uncertain input is independent by default |

## Probability-distribution policy

1. **Empirical distribution:** use only when the raw data, source, sample population, units, and observation window are recorded.
2. **Literature-derived distribution:** cite the exact study and configuration; do not transfer it across geometries or climates without justification.
3. **Engineering prior:** state the basis and bounds, and label the result as prior-driven.
4. **Scenario grid:** preferred when probabilities are unsupported. A grid demonstrates conditional behavior without pretending to know likelihoods.
5. **Sensitivity-only parameter:** if a plausible range cannot be defended, do not include it in a probability-weighted headline result.

The uniform `freshwater_displacement_fraction ~ U(0,1)` used in the Monte Carlo smoke test is a **software/test distribution only**. It is not an empirical prior and must not be used as the study's primary uncertainty model without evidence supporting that distribution.

## Analysis acceptance criteria

- Report the number of valid and invalid Monte Carlo draws, seed, sample size, and convergence check.
- Distinguish confidence/credible intervals from scenario envelopes.
- Check rank stability and convergence for global sensitivity indices before interpreting them.
- Preserve physically invalid samples as diagnostics; do not silently clip them into plausible values.
- Report the probability of `Delta W_net < 0` only when the input distributions are defensible and the counterfactual is specified.
- Show sign changes and failure regions, not only a mean or best case.
- Publish the complete input table, sources, transformations, and configuration-specific applicability domain.

## Links

- Research question and hypotheses: `docs/RESEARCH_GAP_AND_FALSIFIABLE_DESIGN.md`
- Transient benchmark audit: `docs/ALI_2020_TRANSIENT_SOURCE_AUDIT.md`
- Source-matched benchmark gate: `docs/PRIMARY_SOURCE_VALIDATION_GATE.md`
- Literature matrix: `01_literature/literature_matrix.csv`
