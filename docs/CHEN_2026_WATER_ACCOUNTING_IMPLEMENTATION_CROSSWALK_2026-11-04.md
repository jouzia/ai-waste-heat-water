# Chen et al. (2026) water-accounting and implementation crosswalk — 2026-11-04

**Source:** Longxiang Chen et al., “A dual-purpose seawater evaporation system for data center cooling and freshwater production: design and performance analysis,” *Applied Thermal Engineering* 287 (2026), article 129458. DOI: [10.1016/j.applthermaleng.2025.129458](https://doi.org/10.1016/j.applthermaleng.2025.129458). [Publisher article record](https://www.sciencedirect.com/science/article/pii/S1359431125040505).

**Audit scope:** comparison of publisher-indexed article text with the current Research 2 implementation in `src/ai_water/engine.py`, `src/ai_water/models.py`, and `scripts/run_break_even_failure_envelope.py`.

**Evidence boundary:** publisher-indexed abstract, introduction, methodology assumptions, selected results/conclusion and system description were accessible. The complete PDF, full equation set, detailed parameter tables, validation data and supplementary information were not obtained. The implementation statements below are source-code observations; they do not validate the physical model. This is not a complete full-text audit or independent reproduction.

## 1. Chen system boundary supported by accessible text

The publisher describes a seawater evaporation-driven data-centre cooling and freshwater cogeneration system:

1. Low-pressure seawater phase change absorbs data-centre waste heat and provides cooling.
2. The evaporation produces salt-free vapour.
3. A multi-stage compressor maintains the low-pressure evaporation condition and raises vapour pressure/temperature.
4. Compressor-discharge vapour is integrated with multi-effect distillation (MED), recovering condensation heat to increase freshwater output.
5. Two configurations are compared: SEFDS and the water-injection heat-exchange variant SEFDS-WI.
6. Conventional comparison systems include an indirect evaporative cooling system for data centres (IECS) and an MVC-MED desalination system.

**Technology classification:** this is a seawater low-pressure evaporation + mechanical vapour compression + MED architecture. It is not identified as membrane distillation (MD), DCMD or AGMD. A process distinction does not, by itself, establish novelty for Research 2.

The publisher highlights say the system enables year-round utilization of data-centre waste heat. The accessible methodology also states steady-state thermodynamic modelling of each device. These statements do not establish a time-resolved workload-to-heat simulation, hourly/seasonal dispatch validation, or measured year-round operation. Those details remain unknown pending full methods/SI inspection.

## 2. Publisher-visible outputs and their limits

The publisher abstract reports:

| Metric | SEFDS | SEFDS-WI |
|---|---:|---:|
| Freshwater production | 10,004.20 t/day | 10,744.12 t/day |
| Freshwater production increase | 13.9% | 21.6% |
| Reported power | 6,095.49 kW | 6,349.08 kW |
| Power reduction | 41.5% | 40.0% |
| Capital-cost reduction | 13.1% | 9.1% |
| Operating-expense reduction | 37.0% | 34.9% |
| CO2 reduction | 41.6% | 40.0% |
| Payback period | 3.33 years | 3.30 years |

These are author-reported model outputs and comparisons against conventional standalone systems, not independently reproduced measurements. The accessible abstract does not provide enough information to normalize the reported power values or reductions to Research 2's functional unit. Do not interpret the power reductions as a reduction in total data-centre electricity without the detailed baseline and boundary definitions.

Publisher-indexed methodology text states steady-state device modelling, adiabatic component assumptions, isenthalpic throttling, MATLAB implementation, and REFPROP 9.1 property calculations. The page says the MVC-MED, IECS, SEFDS and SEFDS-WI systems are validated, but the accessible text does not expose the validation cases, data, error metrics, or validation scope.

## 3. Research 2 implementation crosswalk

The following describes what the inspected code currently computes. It is not a claim that the inputs are empirically sourced or that the model has passed physical validation.

| Accounting / physical term | Research 2 implementation observed | Chen publisher-text evidence | Comparison decision |
|---|---|---|---|
| IT electricity / heat generation | `it_energy = it_power_kw × duration_h`; `heat_generated = it_energy` | Data-centre waste heat is the driving resource; accessible text does not expose the complete IT-to-heat equation | Similar high-level coupling only; do not claim equation-level equivalence |
| Recoverable heat | Workload recoverable fraction × recovery efficiency × HX effectiveness × usable fraction, less cooling heat penalty | Low-pressure seawater evaporation absorbs waste heat; detailed recoverable-heat and heat-exchanger equations not visible | Different architectures and unverified boundaries |
| Cooling service | MD cooling demand is MD thermal duty × a scenario cooling-to-heating ratio | Seawater phase change itself provides data-centre cooling | Not the same cooling mechanism; Research 2 coefficient is not a Chen model |
| Cooling electricity | MD cooling duty × a fixed electricity-per-thermal-duty factor, plus incremental facility electricity | Compressor and other component power are part of Chen's reported system power; detailed breakdown not visible | No numerical comparison without complete component and baseline boundaries |
| Direct cooling water | Incremental facility electricity × facility cooling-water intensity + MD cooling duty × MD cooling-water intensity | Seawater evaporation is the cooling and vapour-generation mechanism; total intake/evaporation/loss terms not visible | Research 2's coefficient-based water burden is not a reproduction of Chen's seawater mass balance |
| Pumping / compression | Optional pressure-drop/pump-efficiency MD calculation; default scenario runner uses fixed pump kWh/m3. MD cooling electricity is separate | Multi-stage vapour compressor is explicitly part of Chen's process; complete compressor stages, pressure ratios and efficiencies not visible | Not equivalent. Research 2's pump term is not Chen's vapour-compressor work |
| Feedwater withdrawal | `feed_water_withdrawal_l = freshwater_l / feed_recovery_fraction` | Seawater is evaporated; full seawater intake and stream flow rates not visible | Research 2 computes an idealized MD feed flow from a specified recovery fraction; Chen withdrawal cannot be inferred from abstract freshwater production |
| Concentrate / brine | `concentrate_discharge_l = feed_water_l - freshwater_l`; concentrate salinity is estimated from feed salinity and recovery fraction | MED integration and seawater evaporation are described; complete brine/concentrate streams, blowdown and disposal are not visible | Do not assume equivalent salt balance, brine discharge or environmental boundary |
| Electricity-related water | `(incremental_facility_electricity_kwh + auxiliary_electricity_kwh) × grid_water_l_per_kwh` | Abstract reports power and CO2 outcomes; grid-water factors and water-consumption boundary are not visible | Candidate ledger dimension in Research 2; Chen comparison remains unknown |
| Freshwater displacement | Explicit avoided-consumption volume capped at produced distillate, or produced distillate × user-set displacement fraction | No counterfactual displaced freshwater source or displacement fraction visible | Research 2 models an explicit counterfactual assumption not established in accessible Chen text |
| Net water outcome | Additional direct and electricity-related water burden minus avoided freshwater consumption | Publisher abstract reports freshwater production, not a comparable net operational blue-water ledger | No claim of net-water superiority or direct numerical comparison |
| Time dependence | Scalar workload power and duration; scenario sweeps are conditional assumptions, not empirical probabilities | Publisher highlight says year-round waste-heat utilization; visible device methodology is steady-state | Year-round claim is not evidence of hourly workload coupling or temporal validation |
| Geography / water stress | No basin-specific water factor in the inspected core engine schema | Coastal/water-stressed application is stated generally; accessible text does not establish a basin-resolved water-stress method | Geographic net-water comparison remains open |

### 3.1 Important code-level accounting qualifications

1. **The feed and concentrate outputs are simplified model quantities.** The engine derives feed volume from distillate and a user-specified recovery fraction, then defines concentrate as the difference. The inspected code does not expose a complete intake, pretreatment reject, cleaning, blowdown, leakage, post-treatment, or disposal model.
2. **The grid-water factor needs explicit metadata.** The code labels the result `indirect_water_consumption_l`, but `grid_water_l_per_kwh` itself does not encode geography, time period, generation technology, source-water type, or whether the factor represents withdrawal or consumption. Until the factor's provenance and definition are fixed, this is a conditional factor-based burden, not a fully characterized consumption inventory.
3. **The facility cooling factor also needs explicit boundary metadata.** The field name says consumption, but its source, geography, technology and withdrawal/consumption definition must be documented before a water-accounting claim is made.
4. **Avoided water is counterfactual, not automatically equal to product water.** The code correctly makes displacement an explicit fraction or capped volume. Its physical interpretation still requires evidence that the product quality and use actually displace freshwater consumption.
5. **The current model does not implement Chen's seawater evaporation/MVC/MED train.** It models MD flux/thermal demand, a simplified cooling burden, and MD pumping/auxiliary electricity. It does not implement the multi-stage vapour compressor, MED effects, water-injection heat exchanger, or Chen's integrated process balances.
6. **Software tests are not physical validation.** Passing CI, unit tests, or a deterministic scenario sweep does not validate MD flux, energy balances against independent experiments, or water factors.

## 4. What can and cannot be concluded

### Established overlap

Chen et al. is direct prior art for:
- using data-centre waste heat in a seawater-derived freshwater system;
- combining cooling and freshwater production in one integrated system;
- thermodynamic and thermoeconomic evaluation of that coupled architecture;
- integrating evaporated seawater vapour with compression and MED heat recovery.

Research 2 must not claim those broad ideas as new. Nor can it claim that data-centre cooling/freshwater cogeneration is unprecedented.

### Candidate distinction, not novelty clearance

Research 2's potential distinction is not the broad co-production concept. It is the conditional, source-traceable accounting question: under what explicit counterfactual and water-factor definitions does MD product water offset freshwater consumption after incremental cooling, pumping and electricity-related water burdens are counted?

That candidate distinction is **not yet cleared as novel**. Chen's complete water/energy boundaries and other direct prior art must be checked. Research 2 also still needs source reconstruction and independent, unfitted validation.

### Unknown from accessible Chen text (not proof of omission from the paper)

- Total seawater withdrawal and all intake streams.
- Complete evaporated-vapour, freshwater, concentrate, brine and blowdown mass balance.
- Salt balance and brine concentration/discharge destination.
- Whether product-water quality is measured, assumed or calculated.
- Source-water withdrawal versus consumptive use.
- Cooling duty and freshwater production functional-unit normalization.
- Component-level compressor and MED electricity/thermal breakdown.
- Whether IT electricity is inside or outside each reported power boundary.
- Grid electricity water factors and their geography/time/source definitions.
- Counterfactual freshwater displacement and end-use substitution.
- Basin-specific water stress.
- Time-resolved workload/heat matching and seasonal operational evidence.
- Validation data, calibration/validation separation, errors, and uncertainty treatment.
- Open code/data and supplementary parameter provenance.

## 5. Required full-text/SI extraction if an authorized copy becomes available

1. Process-flow diagram, all streams and component boundaries.
2. Seawater intake, evaporation, condensate, MED feed/product, concentrate and brine mass balances.
3. Salt balance, water quality and discharge handling.
4. Compressor stage pressures, efficiencies, mass flows and electricity.
5. MED effect count, temperature levels, heat-recovery equations and performance ratio.
6. Data-centre load, heat rejection, waste-heat temperature and annual/seasonal operating profile.
7. Baseline configurations and exact denominators for power, cost and emissions comparisons.
8. Direct and indirect water withdrawal/consumption definitions and factors.
9. Validation data, model errors, uncertainty ranges and sensitivity protocol.
10. Code/data availability and licensing.

No purchase or author contact is authorized by this audit. Until an authorized full text/SI is available, retain the evidence limitation rather than filling gaps by inference.

## 6. Manuscript-safe comparison wording

> Chen et al. have already demonstrated, through a publisher-reported thermodynamic and thermoeconomic model, an integrated seawater-evaporation, vapour-compression and MED architecture that co-produces data-centre cooling and freshwater. Our current reduced-order MD screening model represents a different process configuration and evaluates a conditional counterfactual water ledger. The available publisher text does not permit a quantitative comparison of withdrawal, consumption, brine, electricity-related water, or freshwater displacement. Accordingly, we do not claim superiority or novelty of the broader cooling–freshwater integration concept.

This wording is deliberately limited to the evidence currently available. It should be revised after full methods/SI extraction and the remaining prior-art comparison.

## 7. Decision and next actions

- [x] Re-inspect the current Research 2 engine, schema and break-even scenario runner.
- [x] Record the Chen process boundary and publisher-visible methods/results.
- [x] Map code terms to the evidence-supported and unknown Chen terms.
- [x] Identify water-factor provenance and withdrawal/consumption semantics as unresolved model requirements.
- [ ] Obtain and inspect complete Chen methods and SI through an authorized route.
- [ ] Compare the same water-accounting terms against Katakam, Wang, Lei, Herrera and the remaining direct prior art.
- [ ] Decide whether Research 2's factor schema needs explicit metadata for source, geography, year, technology, and withdrawal/consumption type.
- [ ] Keep Issue #16, novelty, source-reconstruction and independent-validation gates open.

**Decision:** the crosswalk confirms broad prior-art overlap and identifies exactly where the present MD ledger differs from Chen's seawater evaporation/MVC/MED architecture. It does not establish a novel contribution, validate the current model, or justify a quantitative net-water comparison.
