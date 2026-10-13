# Prior-art audit: Wyon (2025) data-centre waste-heat desalination thesis

**Source:** Annie Wyon, *Desalination utilizing data centre waste heat: A techno-economic study*, Lund University, June 2025.  
**Institutional record:** https://lup.lub.lu.se/student-papers/record/9198095  
**Full open-access PDF:** https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf  
**Report number:** LUTFD2/TFEM—25/5229--SE.

## Scope already covered by the thesis

- Hypothetical 1.5 MW direct-to-chip data centre in Barcelona, Spain.
- Data-centre waste heat transferred to seawater through a commercial heat exchanger, followed by direct-contact membrane distillation (DCMD).
- Two commercial pumps are explicitly modeled.
- Three distillate use cases: data-centre air-cooling, electrolyser feed for backup hydrogen production, and sale to the local water grid.
- Performance outputs include water production, electricity consumption, cost of water, and space requirements.
- The thesis concludes that production is technically possible, but low-grade heat and pump investment/operating electricity create substantial economic challenges.

## Model and validation details

The final DCMD model uses literature-derived properties and an 80-module case. The thesis lists rectangular channels of 0.002 m height and 0.2 m width, module length 0.5 m, hydraulic diameter approximately 0.004 m, feed velocity 1.85 m/s, permeate velocity 2.92 m/s, PTFE membrane thickness 77 μm, porosity 89%, pore size 0.45 μm, membrane area 0.1 m², and membrane conductivity 0.031 W m⁻¹ K⁻¹.

On printed thesis page 16, Figure 9 compares modeled and experimental total heat flux at feed inlet temperatures of 40, 50, 60, and 70 °C. The plot annotates relative discrepancies of approximately +6.5%, −8.1%, −11.0%, and −8.4%, respectively. These are secondary-source figure annotations, not raw experimental observations. The thesis explicitly states that the discrepancy remains, the cause has not been identified, and the validation temperature range differs from the case-study extraction range.

Do not digitize this figure and describe it as primary data. If it is used as a secondary cross-check, archive the source locator, axis calibration, pixel coordinates, digitization uncertainty, and a clear secondary-source label; do not use it to replace the original experiment.

## Implication for the present project

The broad system concept is not novel: a data-centre waste-heat/DCMD/heat-exchanger/pump system and several water end uses have already been modeled. A different location, a larger hypothetical facility, or another cost estimate is not enough to establish a publishable contribution.

A potentially defensible distinction would require all of the following, rather than simply extending the thesis case study:

1. **Source-matched physical validation:** independently reconstruct and test the MD model against primary observations; preserve discrepancies and uncertainty.
2. **Boundary-consistent water accounting:** separate gross distillate from avoided freshwater consumption, quantify incremental cooling/pumping and electricity-related water, and state the displacement counterfactual.
3. **Time-resolved heat eligibility:** match workload-driven heat quantity and temperature to the MD operating envelope, not only annual or steady-state averages.
4. **Uncertainty and failure regimes:** quantify when the intervention is neutral or water-negative; do not assume a positive result.
5. **Prior-art comparison:** compare the full Kanbur et al. (2020) data-centre/DCMD paper and Wyon (2025) thesis directly before asserting novelty.

This audit is based on the full thesis text and the displayed validation figure. It is a literature comparison, not evidence that the current repository's model is validated or that the proposed contribution is novel.
