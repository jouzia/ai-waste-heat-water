# Ali et al. (2020) dynamic DCMD model reconstruction record

**Source:** Ali, Orfi, and Najib (2020), *Developing and validating a dynamic model of water production by direct-contact membrane distillation*, PLOS ONE 15(3): e0230207. DOI: https://doi.org/10.1371/journal.pone.0230207. Open access, CC BY 4.0.

**Purpose:** Reconstruct the published dynamic model as a prior-art baseline and validate its reported behavior against the publisher's supporting measurements. This is not a claim that dynamic DCMD modeling is new.

## What the paper already contributes

The paper derives a first-principles transient mass-production model in both lumped and spatial forms. The model couples hot- and cold-side outlet-temperature ODEs to an algebraic pseudo-steady membrane-interface solver and a dynamic membrane-flux equation. It uses measured step-response experiments on a 10 m² spiral-wound counter-current DCMD pilot plant, with nominal circulation flows of 50, 100, 200, and 300 L/h and nominal hot-inlet steps around 50–80 °C. Measurements of accumulated product mass were recorded at 10-second intervals.

Therefore, the project must not claim the first dynamic DCMD mass-production model, first transient mass-flux model, or first experimental transient validation. The useful role of this dataset is as a separately published benchmark for reproducing and stress-testing dynamic model behavior.

## Source-reported geometry and conditions

| Quantity | Source-reported value | Reconstruction note |
|---|---:|---|
| Effective membrane area | 10 m² | Geometric length × height is 14 × 0.7 = 9.8 m²; preserve this small source mismatch rather than silently changing the reported effective area. |
| Channel length | 14 m | Long module; spatial variation may matter. |
| Channel height/width | 0.7 m | The paper calls this channel height; record the source terminology. |
| Channel gap | 2 mm | Each side's geometric volume is approximately 14 × 0.7 × 0.002 = 0.0196 m³. |
| Membrane thickness | 230 μm | Source-reported. |
| Pore size | 0.2 μm | The setup text says “pore diameter”; Appendix B uses a pore-size symbol that appears to be a radius. Test both 0.1 μm and 0.2 μm as radius interpretations rather than choosing silently. |
| Porosity | 0.8 | Source-reported. |
| Water-entry pressure | 4.1 bar | Source-reported. |
| Salinity | 0.5% | The vapor-pressure activity expression requires a fraction (0.005), not the number 0.5; document the conversion. |
| Hot/cold circulation | Equal on both sides | Imposed by the pilot setup. |
| Cold-inlet temperature | Nominally 25 °C | Measured values fluctuate and are below 25 °C at some recorded times; use measured values where available and keep nominal substitution explicit where missing. |
| Time sampling | 10 seconds | Workbook time is stored in minutes, typically with increments near 0.1667 min. |

The main text does not fully specify every property correlation and membrane parameter required by Appendix B. Any adopted value for membrane tortuosity, solid/gas thermal conductivity, water-property correlations, or pressure-diffusivity product must be traced to its cited source or labeled as an engineering closure. Do not call such a reconstruction exact until those items are resolved.

## Published equations to reproduce

For the lumped model, the state includes the hot outlet temperature, cold outlet temperature, membrane mass-production rate, and accumulated distillate mass. The source defines the instantaneous mass-production rate through the membrane vapor-pressure difference:

\[
\dot m_w = C_m A(P_1-P_2), \qquad j_w=C_m(P_1-P_2).
\]

The source then differentiates this relation and couples it to the outlet-temperature derivatives. Its membrane bulk temperatures use geometric means in absolute temperature:

\[
T_{hb}=\sqrt{T_{h,in}T_{h,out}},\qquad
T_{cb}=\sqrt{T_{c,in}T_{c,out}}.
\]

The pseudo-steady interface-temperature relations are

\[
T_{hm}=a_hT_{hb}+a_cT_{cb}-c_hj_wH_v,\qquad
T_{cm}=b_hT_{hb}+b_cT_{cb}+c_cj_wH_v,
\]

where the coefficients depend on the hot-side, cold-side, and membrane heat-transfer coefficients. They are recalculated iteratively as the temperatures and flux change.

The source's lumped hot-side energy balance, including its empirical correction, is

\[
V\rho C_p\frac{dT_{h,out}}{dt}=
\dot m_{h,in}C_p(T_{h,in}-T_{ref})
-\dot m_{h,out}C_p(T_{h,out}-T_{ref})
-h_mA(T_{hm}-T_{cm})-j_wAH_v
-f_{los}\dot m_{h,in}C_p(T_{h,in}-T_{h,out}).
\]

The cold-side balance is

\[
V\rho C_p\frac{dT_{c,out}}{dt}=
\dot m_{c,in}C_p(T_{c,in}-T_{ref})
-\dot m_{c,out}C_p(T_{c,out}-T_{ref})
+h_mA(T_{hm}-T_{cm})+j_wAH_v.
\]

The ODE solver now integrates separately over each measured-input knot, using the interval's derivative consistently at its right endpoint. This avoids adaptive RK stages stepping across a derivative discontinuity in the piecewise-linear input. A synthetic regression test verifies interval-boundary integration.

For measured, piecewise-linear inlet-temperature histories, the derivative chain rule also includes inlet-temperature derivatives. In the spatial model, each cell's bulk-temperature derivative includes the neighboring upstream/downstream cell derivative (or the boundary-input derivative at the module edge). Omitting these terms is only defensible under constant boundary inputs; it is not consistent with a fluctuating measured-input trace.

The accumulated mass is the integral of the mass-production rate. The dynamic equation for the mass-production rate follows the paper's Eq. (1)/Appendix A Eq. (A.27); it depends on the derivatives of both outlet temperatures and the temperature derivatives of the membrane vapor pressures. The implementation must not replace this state equation with a purely steady-state \(j_w A\) calculation and then claim to reproduce the published transient model.

Appendix B specifies the following submodels:

- Vapor pressure at the hot membrane interface uses the source Antoine form with the salinity activity correction; the cold interface uses the corresponding pure-water form. The correlation is expressed in absolute temperature in the paper.
- \(j_w=C_m(P_1-P_2)\).
- The membrane coefficient \(C_m\) is selected from Knudsen, molecular-diffusion, or transition regimes according to the Knudsen number.
- The overall heat-transfer coefficient combines feed-side convection, membrane conduction plus latent transport, and permeate-side convection in series.
- \(h_m=((1-\epsilon)k_s+\epsilon k_g)/\delta\).
- The heat-transfer correlation is \(Nu=0.298Re^{0.646}Pr^{0.316}\).
- The source-reported vapor/latent-enthalpy correlation is \(H_v(T)=1850.7+2.8273T-1.6\times10^{-3}T^2\). Its unit convention must be checked against the source equations and implementation before use; do not silently mix kJ/kg and J/kg.
- The interface-temperature iteration terminates at a stated tolerance of \(10^{-7}\).

The exact Appendix A/B equations and their notation are in the source PDF. Equation transcription and units should be checked against the page images, not only OCR text.

## Equation-level ambiguities that must be handled explicitly

Two items require a reconstruction decision before any result can be called a faithful reproduction:

1. **Transition-regime membrane coefficient.** Appendix B's printed transition expression combines the reciprocal Knudsen-resistance term with a term involving (\tau\delta P_a/(\epsilon P_D)). Under the paper's nomenclature (P_D=P_aD) (pressure × diffusivity), those terms appear to have incompatible dimensions unless an additional factor or a different definition of (P_D) is intended. Do not implement the printed sum blindly. The first implementation should use the dimensionally consistent series-resistance relation (C_m=(C_{m,K}^{-1}+C_{m,MD}^{-1})^{-1}), retain the exact printed equation as a documented discrepancy, and test plausible interpretations of (P_D) separately.

2. **Pore radius and property closures.** The experimental description gives a 0.2 μm pore diameter, while the transport equations use a pore-size symbol that is conventionally a radius. The article does not fully enumerate tortuosity and all property correlations in the main text. Use the 0.1 μm and 0.2 μm radius interpretations as explicit sensitivity cases; do not silently tune the radius to match the paper's error table. The pressure-diffusivity product, water viscosity, heat capacity, conductivity, and membrane solid/gas conductivity must each have a source citation or be labeled as reconstruction assumptions.

The reported (H_v(T)=1850.7+2.8273T-1.6\times10^{-3}T^2) also needs a unit audit. With (T) in kelvin, its numeric scale is consistent with vapor enthalpy in kJ/kg, not J/kg. The energy balances use it as a vapor-enthalpy transport term relative to the stated reference temperature. Keep the source's symbol and physical interpretation distinct from a pure latent-heat-of-vaporization correlation until verified against the cited property source.

## Published error and correction values

The paper reports the following overall relative errors (lumped / spatial):

| Condition | Without correction | With correction |
|---|---:|---:|
| 50 L/h | 7.78% / 14.00% | 3.08% / 3.04% |
| 100 L/h | 10.01% / 15.97% | 3.78% / 2.90% |
| 200 L/h | 9.31% / 18.92% | 3.29% / 3.54% |
| 300 L/h | 16.99% / 25.19% | 2.71% / 3.51% |
| Overall | 11.02% / 18.52% | 3.22% / 3.25% |

The lumped model using terminal temperatures without correction has a reported overall error of 51.31%.

The correction factor \(f_{los}\) is not an independently measured physical heat-loss coefficient. The paper says its values were selected by trial and error/heuristics and acknowledges that the term may absorb both heat loss and other model errors.

| Flow | Lumped \(n=1\) \(f_{los}\) | Spatial \(n=10\) \(f_{los}\) |
|---:|---:|---:|
| 50 L/h | 0.077 | 0.15 |
| 100 L/h | 0.11 | 0.20 |
| 200 L/h | 0.10 | 0.22 |
| 300 L/h | 0.17 | 0.26 |

Reproducing the tuned errors is a source-reconstruction check, not independent validation. Report untuned and published-tuned cases separately. Do not refit \(f_{los}\) on the same traces and then describe those traces as held out.

## Supporting data now extracted

The source XLSX files S1–S5 are available from the publisher under CC BY 4.0. Their SHA-256 values are pinned in scripts/extract_ali_2020_observations.py and 01_literature/derived/ali_2020_supplementary_acquisition_ledger.csv.

- Raw nonblank worksheet-row ledger: 17,430 rows.
- Structured transient ledger: 17,385 records, of which 16,837 have both time and cumulative mass.
- 548 temperature-only rows in S5 50/60/70 sheets have no timestamps; they are preserved but excluded from time-domain fitting.
- Steady-state table: 16 valid flow/temperature observations.
- Two non-condition S1 rows are preserved in a separate exclusion ledger.
- The derived 25%/10% tail-slope comparison contains 34 rows and is a within-paper consistency diagnostic only.

The current 90-day artifact and per-file/ledger checksums are recorded in 04_experiments/literature_benchmarks/MD-DCMD-DYNAMIC-ALI-2020_observations.yaml and docs/ALI_2020_SUPPORTING_DATA_AUDIT_2026-10-13.md.

## Data-quality flags that must remain visible

1. **S2 sheet 55:** the first cumulative-mass observation is nonzero (about 1.75 kg) and the measured hot-inlet temperature does not reach the sheet label. Treat this as a partial/nonstandard trace unless the source methods resolve it.
2. **S5 sheets 50/60/70:** trailing temperature-only values lack timestamps. Preserve them as untimed measurements; do not invent a time axis.
3. **S5 sheet 80:** the final measured hot-inlet temperature is about 72.5 °C, not 80 °C. It is not an attained 80 °C steady-state condition, although its measured input trajectory may still be useful for a transient comparison.
4. **S1 table:** two non-condition rows are excluded from the 16 valid steady-state conditions and archived with source row locators.
5. The S2–S5 file-to-flow crosswalk (50/100/200/300 L/h) is based on the observed circulation-flow series and the source operating matrix. \(FR\) is circulation flow, not distillate production.

## Reproduction/validation protocol

1. Implement the lumped model first with the paper's stated equations, source-pinned inputs, and no refitting.
2. Reproduce the untuned Table 1 errors before applying the published \(f_{los}\) values. If the errors do not reproduce, report the exact discrepancy and identify the unreported property/parameter assumptions.
3. Run the published-tuned \(f_{los}\) values as a separate source-reproduction case. Do not describe the tuned fit as an independent predictive result.
4. Use condition-level separation, not random splitting of adjacent time points. Preserve complete traces as units.
5. Treat the extra 40 °C/55 °C traces and the 80R replicate as diagnostics, with explicit data-quality flags. Do not silently relabel 55 °C as 50 °C or the S5 80 °C trace as a fully attained setpoint.
6. Evaluate accumulated-mass error, production-rate error, and response-lag error separately. Report errors on the original time grid and retain the source's reported metric as a separate reproduction statistic.
7. Only after the source model reproduces its own benchmark should the repository's alternative model be compared against this independent study. Keep the GDR/NREL dataset and Ali dataset distinct; neither may be used for both fitting and held-out evaluation without an explicit leakage analysis.

## What this does and does not establish

The data acquisition, hashes, source row locators, and structured extraction are complete. This document establishes a reproducible prior-art benchmark and a clear test protocol. It does **not** establish that the repository's current model matches the Ali experiment, that the published model's heuristic correction is physically identified, or that data-center waste heat yields a net freshwater benefit.


## 2026-10-13 admissibility check and held-out-flow diagnostic

The first transient smoke test on the default 10 m² configuration (50 L/h, 60 °C hot inlet, 25 °C cold inlet, both outlets initialized at 25 °C) numerically converged but predicted a hot outlet of **11.714 °C** after one minute—below the global inlet/initial-state temperature envelope. This is thermodynamically inadmissible for the declared passive system. The implementation now rejects such trajectories with an explicit error instead of returning them as successful predictions. The generic integration smoke test uses a deliberately reduced 0.1 m² area; that test is only an integrator sanity check and is **not** the source geometry. The default source-geometry/low-flow case remains a known structural mismatch and must not be treated as a successful reconstruction.

The separate S1 flux-law diagnostic fits permeance on the 50/100/200 L/h observations and holds out all four 300 L/h observations. A fixed-TPC model (α=0.8) has held-out MAE 0.828 kg m⁻² h⁻¹ and RMSE 0.861. An exploratory logistic TPC-versus-log-flow model reduces held-out MAE to 0.181 and RMSE to 0.214 under the 0.5% salinity interpretation. This is a within-paper, fitted, held-out-flow diagnostic—not independent validation. Under the alternative measured-TDS proxy, fitted permeance hits the optimizer's upper bound (200 kg m⁻² h⁻¹ bar⁻¹), signalling parameter/boundary sensitivity. Both the salinity discrepancy and model-form issue remain unresolved.
