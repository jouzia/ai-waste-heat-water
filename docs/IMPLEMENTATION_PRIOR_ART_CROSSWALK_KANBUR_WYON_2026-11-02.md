# Implementation-to-prior-art crosswalk: Kanbur (2020) and Wyon (2025)

**Audit date:** 2026-11-02  
**Repository ref inspected:** `main` after PR #42 merge  
**Purpose:** distinguish implemented behavior from intended contribution and map the current software boundary against the two direct data-centre/MD antecedents.

## Evidence boundary

The repository code and documentation were inspected directly. Kanbur's publisher and institutional records expose the abstract and bibliographic metadata, but its full article and supplement were not obtained. Wyon's full-text content was reviewed from a third-party readable copy matching the Lund institutional record; authentication against the institutional PDF remains outstanding. Accordingly, the literature-side comparison below is deliberately limited. This is a code/documentation crosswalk, not a replication study.

## 1. What the repository actually implements

| Capability | Code evidence | Current behavior | Important limit |
|---|---|---|---|
| Workload-to-heat approximation | `src/ai_water/workload_profile.py` | Integrates piecewise-constant IT power and duration; assumes IT electricity becomes heat on a first-order basis | No measured workload trace or server-specific power/temperature mapping is supplied by this module |
| Time-varying source eligibility | `src/ai_water/workload_engine.py` | Simulates each interval separately; gates recoverable heat by source-temperature threshold, positive IT power, and recoverable-heat fraction | Piecewise constant; no plant transient or thermal storage/controller model |
| Heat recovery | `src/ai_water/engine.py`, `models.py` | Applies recoverable-heat fraction, recovery efficiency, heat-exchanger effectiveness, usable-heat fraction, and a cooling heat penalty | Inputs are scenario parameters; no site-measured HX performance is embedded |
| MD production | `src/ai_water/md.py`, `md_thermal.py`, channel modules | Supports pressure-driving-force flux, optional explicit flux, heat duty, conductive leak, interface temperatures, salinity/activity options, and channel-level model variants | These alternatives are not a single validated, configuration-specific plant model; parameters and boundary conditions remain source-dependent |
| Hydraulic pumping | `src/ai_water/hydraulics.py`, `engine.py` | Computes pump electricity from distillate, recovery fraction, pressure drop and efficiency, or accepts a specific-energy input | No source-specific Kanbur/Wyon pump curve or module pressure-drop reproduction is established |
| Cooling burden | `models.py`, `engine.py` | Counts declared incremental facility electricity/water and MD cooling duty, electricity and water | No validated cooling-architecture response or site baseline is embedded; caller-supplied factors govern results |
| Direct feed and concentrate | `engine.py`, `models.py` | Calculates feed withdrawal as distillate divided by recovery fraction and concentrate as feed minus distillate | Simplified single-pass mass balance; does not itself model brine treatment, disposal, or reuse |
| Electricity-related water | `WaterFactors`, `engine.py` | Multiplies incremental intervention electricity by one supplied grid-water factor | One scalar factor only; no separate withdrawal and consumption factors, generation mix, geography/year join, or time-varying marginal factor |
| Counterfactual displacement | `WaterFactors`, `engine.py`, `workload_engine.py` | Requires explicit avoided consumption or a declared displacement fraction, capped at produced distillate; profile-level displacement is applied after interval aggregation | Does not prove the product water actually displaces potable/freshwater consumption at the destination |
| Uncertainty | `monte_carlo.py`, `global_sensitivity.py` | Provides seeded scenario sampling and sensitivity estimators | Evidence-backed joint distributions and site-specific factor distributions remain incomplete |

## 2. Critical distinction: withdrawal is not yet fully accounted as an impact ledger

The current `Result` model contains `feed_water_withdrawal_l` and `concentrate_discharge_l`, but the net-impact calculation is consumption-oriented:
- `direct_cooling_consumption_l`;
- `indirect_water_consumption_l`;
- `additional_water_consumption_l`;
- `avoided_freshwater_consumption_l`;
- `net_consumption_change_l`.

The current `WaterFactors` schema has a single `grid_water_l_per_kwh` value. It does not separately represent electricity-related water withdrawal and consumption. Nor does the current result schema calculate net withdrawal change, basin depletion, return-flow quality, or freshwater-equivalent impacts from brine discharge. Therefore, the project's intended distinction between withdrawal and consumption is only partially represented in the executable ledger: feed withdrawal is reported, while net change is calculated for consumption. The README and research design must not imply that a complete withdrawal-and-consumption impact ledger is already implemented.

## 3. Comparison against direct antecedents

### Kanbur, Wu & Duan (2020)

The accessible abstract establishes a two-phase liquid-immersion data-centre cooling system whose waste heat heats a DCMD feed, with thermodynamic, economic, thermoeconomic and multiobjective assessment. This overlaps with the project's heat-source/desalination integration and thermoeconomic framing.

The abstract does not establish whether Kanbur models a time-varying workload trace, water withdrawal/consumption, electricity-generation water, counterfactual freshwater displacement, or uncertainty in these quantities. These dimensions remain **unknown**, not absent, until full text and supplementary material are inspected.

### Wyon (2025)

The readable thesis copy describes a 1.5 MW direct-to-chip data-centre/DCMD case with a heat exchanger, two pumps, and three product-water use cases. It explicitly models pump burdens and identifies a model-to-experiment heat-flux discrepancy whose cause is not resolved.

The reviewed thesis content does not demonstrate the repository's exact piecewise-constant workload-to-MD coupling or an integrated withdrawal/consumption/electricity-water/displacement ledger. This is a bounded comparison of the inspected thesis copy, not a global novelty claim. Institutional-PDF authentication remains outstanding.

## 4. What can and cannot be claimed now

### Implemented and testable
- Piecewise-constant workload intervals can be simulated independently and aggregated.
- Declared source-temperature eligibility controls heat recovery.
- A reduced-order MD and thermal-duty model can be coupled to those intervals.
- Pumping, incremental cooling, a single indirect electricity-water factor, feed withdrawal, concentrate discharge, and declared avoided consumption can be reported.
- Software tests cover code behavior; they do not establish empirical model validity.

### Not yet demonstrated
- Source-matched reproduction of Kanbur or Wyon.
- Validation of the complete workload-to-heat-to-MD-to-water chain against independent data.
- Measured data-centre workload and heat traces.
- A complete water-withdrawal and water-consumption impact ledger with separate electricity factors.
- Site/year-specific marginal electricity water impacts.
- Verified freshwater displacement at actual end-use locations.
- A robust comparative claim that the proposed accounting method is novel.

## 5. Required engineering/research work before claiming the candidate contribution

1. Add explicit, separately named electricity-water withdrawal and consumption factors, each with source, geography, year, generation mix, and applicable boundary.
2. Define the net-withdrawal and net-consumption equations separately; do not collapse them into a single water number.
3. Define treatment of brine discharge, return flows, water quality, and any freshwater-equivalent impact separately from gross feed withdrawal.
4. Make counterfactual displacement evidence-bearing by end use, quality requirement, location, and time; a user-supplied fraction alone is a scenario assumption.
5. Connect workload intervals to a provenance-backed measured or validated modeled heat trace.
6. Validate the MD submodel against primary observations with predeclared held-out conditions before evaluating the coupled system.
7. Obtain Kanbur full text/supplement and authenticate the Wyon institutional PDF; complete the equation/boundary crosswalk.
8. Complete a documented systematic literature search and claim-to-evidence matrix.

## 6. Decision

The current code implements a useful screening model with time-resolved workload coupling and a consumption-oriented counterfactual ledger. It does **not** yet implement the full intended operational blue-water accounting boundary, and the complete coupled model is not empirically validated. Kanbur and Wyon establish that data-centre waste heat coupled to DCMD/MD, pumps, and technoeconomic analysis are prior art. The candidate distinction remains an unproven hypothesis: source-matched validated MD coupled to a time-resolved, boundary-consistent ledger with separately reported withdrawal and consumption, incremental cooling/pumping/electricity water, and defensible freshwater displacement.

Issue #16 should remain open. No novelty, reproduction, or positive net-water-benefit claim is cleared.

## References

- Kanbur, B. B., Wu, C., & Duan, F. (2020). *International Journal of Energy Research*, 44(13), 10453–10470. https://doi.org/10.1002/er.5677
- Wyon, A. (2025). *Desalination utilizing data centre waste heat*. Lund University. https://lup.lub.lu.se/student-papers/record/9198095
- Repository implementation inspected at `main`: `src/ai_water/engine.py`, `models.py`, `workload_profile.py`, `workload_engine.py`, `cooling_scenarios.py`, and associated documentation.
