# Research gap, contribution boundary, and falsifiable study design

Version: 2026-10-13

## 1. Research question

**Under what combinations of time-varying AI data-center heat availability, membrane-distillation (MD) performance, cooling and pumping burden, electricity-related water intensity, and local water context does an MD heat-recovery intervention reduce net operational blue-water consumption relative to an explicit counterfactual?**

This is a conditional systems question, not a presumption that waste heat creates a water benefit.

## 2. What the current literature already establishes

| Evidence strand | Source-grounded implication | What this project must not claim |
|---|---|---|
| Workload-level data-center water use | Lei et al. (2025; DOI 10.1016/j.resconrec.2025.108310) report very large variation across workloads and identify server efficiency, grid water factors, utilization, cooling, infrastructure efficiency, climate, inactive servers, and refresh cycle as determinants. | Do not assign a universal liters-per-AI-query factor or infer site water use from compute alone. |
| Probabilistic AI-infrastructure water accounting | Herrera et al. (2025; DOI 10.1016/j.jclepro.2025.146528) distinguish facility, electricity-related, and embodied water and use scenario-based uncertainty. | Do not present a few deterministic cases as a global forecast or treat embodied water as operational water. |
| MD cooling and pumping | Malaguti et al. (2026; DOI 10.1016/j.desal.2026.120039) show that cooling can approach heating duty in some configurations and that pumping can materially affect system consumption. | Do not treat heat as free, assume a free heat sink, or omit hydraulic/cooling penalties. |
| Source-matched DCMD transport | Keshavarzzadeh (2020; DOI 10.1038/s41598-020-73964-7) provides a one-dimensional DCMD formulation and a secondary-reproduced experimental comparison. Martínez-Díez and Vázquez-González (1999; DOI 10.1016/S0376-7388(98)00349-4) are the primary experimental provenance target. | Do not treat the 2020 paper's reported model agreement as validation of this repository; primary observations and boundary conditions must be reconstructed. |
| Dynamic MD mass-production model | Ali et al. (2020; DOI 10.1371/journal.pone.0230207) publish lumped and spatial first-principles transient mass-production models, a coupled outlet-temperature ODE system, and measured accumulated-mass step responses. Untuned overall errors are 11.02%/18.52%; reported 3.22%/3.25% errors require a flow-dependent heuristic correction explicitly selected by trial and error. Five supporting XLSX files are now hash-pinned and extracted into 17,385 transient records plus 16 steady-state conditions. | Dynamic DCMD modeling and transient validation are prior art. Reproduce untuned and tuned cases separately; do not claim the first dynamic model, and do not use heuristic-corrected conditions as held-out evidence. |
| Direct data-center waste heat to MD techno-economic case | Wyon (2025), open-access Lund University thesis, models a hypothetical 1.5 MW direct-to-chip data center in Barcelona coupled to DCMD, a commercial heat exchanger, and two pumps; it compares distillate use for cooling, electrolysis, or sale to the water grid. The thesis reports a remaining model–experiment heat-flux discrepancy with unidentified cause and notes that the validation temperature range differs from the case-study range. It identifies low-grade heat and pumping costs as key limitations. | Do not claim novelty from a hypothetical data-center/MD case, heat-exchanger integration, pump modeling, or comparing water end uses alone. A journal contribution needs independent experimental validation and a rigorous net-consumption counterfactual with source-linked uncertainty, including cooling-water changes and electricity-water burdens. |
| Data-center cooling integrated with DCMD | Kanbur, Wu, and Duan (2020), *International Journal of Energy Research*, DOI 10.1002/er.5677, already model two-phase liquid-immersion data-center cooling whose waste heat heats a DCMD module, including thermodynamic/thermoeconomic analysis and multiobjective optimization. | Data-center-to-MD integration and thermoeconomic optimization are direct prior art; neither may be claimed as new. The remaining candidate contribution must be proven through independent MD validation and boundary-consistent net-water accounting. |
| System-scale data-center desalination and water-stress metric | Katakam et al. (2026, online ahead of print; *Water Research*, DOI 10.1016/j.watres.2026.126748) compare RO/MVC/hybrid desalination and brine management and introduce SWUI for data-center desalination impacts on regional water stress. | Do not claim the first system-level data-center desalination assessment or first water-stress metric. This study focuses on RO/MVC, not MD driven by data-center waste heat; any proposed metric must be distinct and secondary to the physical net-water ledger. |
| Data-center waste heat coupled to desalination | Yang et al. (2026), *Applied Energy*, DOI 10.1016/j.apenergy.2026.127428, couple flexible data-center waste heat to seawater preheating for temperature-/salinity-dependent RO and co-optimize planning and operation. | Do not claim the first data-center/desalination integration or first thermo-electric co-optimization. The potential contribution is narrower: validated MD transport joined to auditable, counterfactual net operational blue-water accounting and sourced incremental burdens. |
| Waste-heat-driven MD prior art | Arthur et al. (2023) integrate electrolyser waste heat and MD; Bahar and Ng (2020) model marine-engine waste heat with AGMD; Khalifa et al. (2025) experimentally drive AGMD with engine exhaust; Chen et al. (2026) report a CPU-waste-heat MD experiment. | Waste-heat-powered MD is established across several heat sources. Do not claim first integration of waste heat and MD or novelty from heat recovery alone. |
| Industrial wastewater/heat reuse | Sulaiman et al. (2026; DOI 10.1007/s43832-026-00418-y) study DCMD for steel-industry wastewater and report experiments plus model comparisons. | Do not transfer hollow-fiber wastewater results directly to a data-center heat source or a different feed chemistry. |
| Membrane properties and scaling | Hu et al. (2025; DOI 10.1016/j.memsci.2025.124533) report membrane pore-size, temperature-polarization, salinity, and long-duration scaling trade-offs. | Do not assume constant membrane flux or ignore fouling/scaling uncertainty when moving from short benchmark runs to sustained operation. |
| CPU-waste-heat-driven MD experiment | Chen et al. (2026), *Journal of Zhejiang Sci-Tech University (Natural Sciences)*, official record ZJSG202601009, report a CPU-heat-driven MD setup; the abstract reports stable operation above 240 W and a 360 W / 55 °C case. | Do not claim first use of CPU/data-center waste heat to drive MD. The full method and dataset have not been independently reconstructed, and the abstract does not establish net freshwater benefit. |
| Integrated MD heat recovery | Sulaiman et al. (2026; DOI 10.1016/j.jwpe.2026.110673) report a validated hollow-fiber DCMD model and multi-objective optimization with integrated heat recovery. | Do not claim novelty for MD heat recovery or MD-level optimization alone; distinguish the data-center heat source, temporal eligibility, and counterfactual net-water accounting. |

The literature review materially narrows the claim. Kanbur et al. (2020) already couple data-center immersion-cooling heat to DCMD and optimize thermoeconomic performance; Wyon (2025) models a 1.5 MW data-center-to-DCMD case with heat exchanger, pumps, and multiple distillate uses; Chen et al. (2026) report a CPU-waste-heat MD experiment. Yang et al. (2026) couple data-center waste heat to RO, while Katakam et al. (2026, online ahead of print) analyze system-scale data-center desalination and introduce a water-stress metric. These are direct prior-art constraints, not incidental adjacent papers. The project must not claim the first data-center-to-MD integration, first waste-heat-driven MD system, first thermoeconomic optimization, first data-center desalination water-stress metric, or first dynamic DCMD mass-production model/transient validation. A potentially defensible contribution would require source-matched and independent MD validation plus a rigorously bounded, time-resolved net operational blue-water ledger with cooling, pumping, electricity-water, and substantiated counterfactual displacement. The Ali 2020 dynamic model is an explicit prior-art baseline: reproduce its published equations and reported error levels before claiming a new validation or workload-response method. Whether that contribution is sufficiently novel remains unresolved until the full Kanbur (2020) and Wyon (2025) methods are compared and a systematic literature search is completed. The CPU experiment's full boundary and dataset remain unverified because only the official abstract/metadata have been retrieved. Neither “MD can use low-grade heat,” “data centers consume water,” nor “cooling and pumping matter” is a defensible stand-alone novelty claim.
## 3. Bounded contribution

The intended contribution is a **validated, counterfactual-aware coupling of time-resolved data-center thermal availability to MD and net operational freshwater accounting**, with the following linked elements:

1. Time-matched recoverable heat rather than annual-average heat alone.
2. Explicit heat-exchanger approach temperature, source-temperature eligibility, and heat-recovery losses.
3. Coupled MD heating, cooling/heat-sink availability, pressure-drop and pumping electricity.
4. Separate ledgers for direct withdrawal, direct consumption, electricity-related water, distillate recovered, and freshwater consumption demonstrably displaced.
5. Site-specific electricity-water factors and basin water-stress context, with source resolution and uncertainty preserved.
6. Uncertainty-aware break-even envelopes showing where the intervention helps, is neutral, or harms net freshwater consumption.
7. Source-matched and independent validation before quantitative claims.

This contribution is a candidate research gap, not a claim that no prior paper has considered any of these components. A final novelty claim requires a systematic database search and citation chasing immediately before manuscript submission.

## 4. Primary estimand and counterfactual

Define, for the same service demand and study period:

`Delta W_net = W_consumption,intervention - W_consumption,counterfactual`

where the intervention increment includes all included direct operational consumption and electricity-related water attributable to the intervention (heat recovery, MD feed handling, pumping, cooling, pretreatment, and auxiliary loads). Report withdrawals separately from consumption. A negative `Delta W_net` means lower modeled consumption under the declared counterfactual.

Recovered distillate is a physical output, **not automatically avoided freshwater consumption**. Count avoided consumption only when the displaced water source and actual displacement fraction are stated and supported. If that counterfactual cannot be substantiated, report gross distillate and net added consumption separately, and do not claim a net freshwater benefit.

A water-stress-weighted indicator may be reported as a secondary impact metric, but it must not replace the unweighted physical water ledger. Do not equate a basin-risk score with liters of water.

## 5. Falsifiable hypotheses

- **H1 — Heat eligibility:** nominal IT heat overstates usable MD heat when source temperature, heat-exchanger approach, and temporal mismatch are enforced.
- **H2 — Cooling constraint:** under some plausible configurations, the cooling and pumping burden offsets the benefit of recoverable heat; there is no universal positive-benefit result.
- **H3 — Counterfactual dependence:** the sign and magnitude of `Delta W_net` change with the actual displaced water source and displacement fraction.
- **H4 — Geographic heterogeneity:** the same physical water change can imply different water-stress-weighted impacts across locations; this must be shown without mislabeling risk scores as physical availability.
- **H5 — Model uncertainty:** uncertainty in membrane transport, heat transfer, cooling burden, and electricity-water factors can change whether a scenario is classified as beneficial. Report the probability of each sign, not just a mean.

Each hypothesis can be rejected by the results. Do not write the discussion as if any hypothesis has already been supported.

## 6. Pre-specified comparisons

At minimum compare:

1. Baseline data-center operation with its declared cooling architecture.
2. Waste-heat recovery without MD, to isolate the heat-recovery/cooling-system effect.
3. Waste-heat-to-MD intervention with cooling and pumping fully included.
4. The same intervention with time-varying source-temperature eligibility enforced.
5. Counterfactual sensitivity cases with zero, partial, and substantiated full displacement of the selected freshwater source.
6. Alternative electricity-water factors and geographic contexts, with all sources and years recorded.

Do not silently mix facility-level direct water consumption, electricity-generation water, and embodied supply-chain water. If embodied water is excluded from the primary estimand, state that scope boundary explicitly.

## 7. Validation and analysis sequence

1. Verify package tests, lint, and CI status on the exact final commit.
2. Reconstruct primary DCMD experimental observations and source-matched boundary conditions; archive raw files, checksums, units, transformations, and digitization coordinates where relevant.
3. Run source-matched predictions without fitting and report MAE, RMSE, bias, and uncertainty-aware residuals.
4. Freeze a development/held-out split by experimental condition before calibration. Never split adjacent samples from one transient trace across train and test.
5. Validate transient behavior separately using measured inputs and accumulated-mass observations; keep differentiated/smoothed rate curves separate.
6. Compare plausible heat-transfer/property closures as model forms rather than selecting one solely for best fit.
7. Build the time-resolved coupling only after its state variables and conservation equations are explicit; check time-step and spatial-grid convergence.
8. Calibrate empirical distributions only from traceable evidence. Demonstrate Monte Carlo convergence and Sobol/sensitivity stability.
9. Map the break-even surface across heat eligibility, cooling, pumping, electricity-water factors, and counterfactual displacement.
10. Publish the full negative and null results alongside positive cases.

## 8. Release rule

No net-benefit headline is permitted until primary validation, independent/held-out evaluation, time-varying coupling, source-linked uncertainty, and counterfactual water accounting are complete. If the evidence shows no beneficial operating region, that is a valid and reportable result.

## References and source URLs

- Lei et al. (2025): https://doi.org/10.1016/j.resconrec.2025.108310
- Herrera et al. (2025): https://doi.org/10.1016/j.jclepro.2025.146528
- Malaguti et al. (2026): https://doi.org/10.1016/j.desal.2026.120039
- Keshavarzzadeh (2020): https://doi.org/10.1038/s41598-020-73964-7
- Martínez-Díez & Vázquez-González (1999): https://doi.org/10.1016/S0376-7388(98)00349-4
- Ali et al. (2020): https://doi.org/10.1371/journal.pone.0230207
- Sulaiman et al. (2026), steel-wastewater DCMD: https://doi.org/10.1007/s43832-026-00418-y
- Hu et al. (2025): https://doi.org/10.1016/j.memsci.2025.124533
- Sulaiman et al. (2026), integrated MD heat recovery: https://doi.org/10.1016/j.jwpe.2026.110673
- Kanbur et al. (2020), data-center immersion cooling integrated with DCMD: https://doi.org/10.1002/er.5677
- Katakam et al. (2026, online ahead of print), system-scale data-center desalination and SWUI: https://doi.org/10.1016/j.watres.2026.126748
- Wyon (2025), *Desalination utilizing data centre waste heat* (open-access Lund University thesis): https://lup.lub.lu.se/student-papers/record/9198095
- Yang et al. (2026), data-center waste heat and RO desalination co-optimization: https://doi.org/10.1016/j.apenergy.2026.127428
- Chen et al. (2026), CPU waste-heat-driven MD (full-text access/underlying data not audited here): https://xuebao.zstu.edu.cn/oa/darticle.aspx?id=20260109&type=view
- Arthur et al. (2023), electrolyser waste heat and MD: https://doi.org/10.1016/j.jwpe.2023.104426
- Bahar & Ng (2020), marine-engine waste heat and MD: https://doi.org/10.1016/j.seta.2020.100860
- Khalifa et al. (2025), engine-exhaust-driven MD: https://doi.org/10.1016/j.applthermaleng.2024.124839
