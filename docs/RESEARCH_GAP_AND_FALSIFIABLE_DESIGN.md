# Research gap, contribution boundary, and falsifiable study design

Version: 2026-10-11

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
| Dynamic MD behavior | Ali et al. (2020; DOI 10.1371/journal.pone.0230207) publish transient DCMD experimental responses and supporting data. Their approximately 3% model error follows a tuned heat-loss correction. | Do not reuse the tuned correction or count the same fitted conditions as held-out validation. |
| Data-center waste heat coupled to desalination | Yang et al. (2026), *Applied Energy*, DOI 10.1016/j.apenergy.2026.127428, couple flexible data-center waste heat to seawater preheating for temperature-/salinity-dependent reverse osmosis and co-optimize planning and operation. | Data-center-to-desalination thermal coupling and economic co-optimization are already published; the selected desalination process in this paper is RO, not MD. | Do not claim the first data-center/desalination integration or first thermo-electric co-optimization. The narrower candidate contribution is an experimentally grounded MD-specific thermal/hydraulic model joined to auditable net operational blue-water accounting, explicit cooling burdens, and substantiated counterfactual displacement. |
| Waste-heat-driven MD prior art | Arthur et al. (2023) integrate electrolyser waste heat and MD; Bahar and Ng (2020) model marine-engine waste heat with AGMD; Khalifa et al. (2025) experimentally drive AGMD with engine exhaust; Chen et al. (2026) report a CPU-waste-heat MD experiment. | Waste-heat-powered MD is established across multiple heat sources, including a CPU source in a 2026 paper. | Do not claim first integration of waste heat and MD, nor novelty from heat recovery alone. The present study's candidate contribution is a validated data-center-system assessment with time-resolved heat eligibility, full cooling/pumping and electricity-water burdens, and explicit counterfactual net-water accounting. |
| Industrial wastewater/heat reuse | Sulaiman et al. (2026; DOI 10.1007/s43832-026-00418-y) study DCMD for steel-industry wastewater and report experiments plus model comparisons. | Do not transfer hollow-fiber wastewater results directly to a data-center heat source or a different feed chemistry. |
| Membrane properties and scaling | Hu et al. (2025; DOI 10.1016/j.memsci.2025.124533) report membrane pore-size, temperature-polarization, salinity, and long-duration scaling trade-offs. | Do not assume constant membrane flux or ignore fouling/scaling uncertainty when moving from short benchmark runs to sustained operation. |
| CPU-waste-heat-driven MD experiment | Chen et al. (2026), Journal of Zhejiang Sci-Tech University (Natural Sciences), CNKI record ZJSG202601009; title translated as “Experimental study of a membrane-distillation desalination system based on CPU waste heat” | The bibliographic record and abstract report a CPU-heat-driven MD setup, with reported operation above 240 W and a 360 W / 55 °C case. This is direct prior art for the broad CPU-waste-heat-to-MD concept. | Do not claim first use of CPU/data-center waste heat to drive MD. The abstract's boundaries and metrics have not been independently reconstructed; it is not evidence of net freshwater benefit. |
| Integrated MD heat recovery | Sulaiman et al. (2026; DOI 10.1016/j.jwpe.2026.110673) report a validated hollow-fiber DCMD model and multi-objective optimization with integrated heat recovery. | Do not claim novelty for MD heat recovery or MD-level optimization alone; distinguish the data-center heat source, temporal eligibility, and counterfactual net-water accounting. |

The CPU-waste-heat MD experiment reported by Chen et al. (2026) materially narrows the novelty claim: waste-heat-driven MD itself is prior art, even though only its CNKI abstract and metadata have been verified here. The proposed work must not claim to be the first such concept. Its differentiator is not data-center/desalination integration or co-optimization alone: Yang et al. (2026) already cover data-center waste heat and RO feedwater preheating in an economic planning/operation framework. The narrower candidate contribution is experimentally grounded MD-specific thermal/hydraulic validation joined to time-resolved, counterfactual-aware net operational blue-water accounting. The exact CPU experiment boundary, cooling-water treatment, and full method remain unverified because the full text/data were not retrieved. These papers materially narrow the novelty claim. Neither “MD can use low-grade heat,” “data centers consume water,” nor “cooling and pumping matter” is a defensible stand-alone novelty claim.

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
- Yang et al. (2026), data-center waste heat and RO desalination co-optimization: https://doi.org/10.1016/j.apenergy.2026.127428
- Chen et al. (2026), CPU waste-heat-driven MD (full-text access/underlying data not audited here): https://xuebao.zstu.edu.cn/oa/darticle.aspx?id=20260109&type=view
- Arthur et al. (2023), electrolyser waste heat and MD: https://doi.org/10.1016/j.jwpe.2023.104426
- Bahar & Ng (2020), marine-engine waste heat and MD: https://doi.org/10.1016/j.seta.2020.100860
- Khalifa et al. (2025), engine-exhaust-driven MD: https://doi.org/10.1016/j.applthermaleng.2024.124839
