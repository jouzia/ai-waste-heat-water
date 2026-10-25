# Malaguti MD thermodynamic equations and model-extension gate — 2026-10-24

**Status:** Literature-derived equation extraction plus a partial equation evaluator. The STEC/SCR equations and module-pumping expression have been transcribed into an optional helper module, but the complete supplementary derivation, independent numeric reproduction, empirical validation, and novelty assessment remain incomplete. This is not a validation result or a novelty claim.

## 1. Primary source

Malaguti, M. et al. (2026), “Waste heat won't make membrane distillation cool: Thermodynamic analysis of cooling and pumping burdens,” *Desalination* 628, 120039. DOI: [10.1016/j.desal.2026.120039](https://doi.org/10.1016/j.desal.2026.120039). The publisher record states that the theoretical derivation and variable definitions are in the Supplementary Information. The accessible article text includes the equations below.

Related prior art: Chen, L. et al. (2026), “A dual-purpose seawater evaporation system for data center cooling and freshwater production: design and performance analysis,” *Applied Thermal Engineering* 287, 129458. DOI: [10.1016/j.applthermaleng.2025.129458](https://doi.org/10.1016/j.applthermaleng.2025.129458). This establishes that coupling data-centre cooling and freshwater production is already proposed in a different seawater low-pressure evaporation/compression/MED architecture.

## 2. Definitions and equations transcribed from Malaguti et al.

The article defines specific thermal energy consumption as a **thermal requirement**, not necessarily the final energy consumption of the plant:

- \(STEC = \dot Q_h / \dot m_d\)
- \(SCR = \dot Q_c / \dot m_d\)

Here \(\dot m_d\) is distillate production rate; \(\dot Q_h\) is heating duty and \(\dot Q_c\) is cooling duty. The article reports three configurations:

1. DCMD with open feed and closed distillate.
2. DCMD with external heat recovery.
3. AGMD with internal heat recovery.

Let \(h_{vap}\) denote latent heat of vaporization, \(\eta\) vaporization efficiency, \(\Delta T = T_{h,in}-T_{c,in}\), \(\Delta T_{h,in}=T_{h,in}-T_{c,out}\), \(\Delta T_{h,out}=T_{h,out}-T_{c,in}\), and \(\Delta T_{HX}\) the temperature difference across the heat exchanger. The article states the cold-stream inlet is fixed at 20 °C and sets \(\Delta T_{h,in}=\Delta T_{HX}=5\ ^\circ C\) for the paper's explored conditions; these are paper-specific assumptions, not universal constants.

### Configuration 1

\[
SCR_1 = \frac{h_{vap}}{\eta}
\frac{\Delta T-\Delta T_{h,in}}{\Delta T-\Delta T_{h,out}}
\]

\[
STEC_1 = \frac{h_{vap}}{\eta}
\frac{\Delta T}{\Delta T-\Delta T_{h,out}}
\]

### Configuration 2

\[
SCR_2 = \frac{h_{vap}}{\eta}
\frac{\Delta T_{HX}}{\Delta T-\Delta T_{h,out}}
\]

\[
STEC_2 = \frac{h_{vap}}{\eta}
\frac{\Delta T_{h,in}+\Delta T_{HX}}
{\Delta T-\Delta T_{h,out}}
\]

### Configuration 3

\[
SCR_3 = \frac{h_{vap}c_c}{\eta c_h}
\frac{\Delta T_{h,out}}{\Delta T-\Delta T_{h,out}}
\]

\[
STEC_3 = \frac{h_{vap}}{\eta}
\frac{\Delta T_{h,in}}{\Delta T-\Delta T_{h,out}}
\]

The article gives specific module pumping energy as:

\[
E_{pump,module} = \frac{\Delta P}{R\,\eta_{pump}}
\]

where \(\Delta P\) is module pressure drop, \(\eta_{pump}\) is pump efficiency and \(R=\dot m_d/\dot m_{feed}\) is single-pass water recovery. Unit conversion and consistency checks are required before comparing this expression with kWh/m³ outputs. Do not assume the formula can be inserted unchanged without confirming the article's unit conventions and the code's basis.

### Translating thermal requirements into system electricity

The article separates auxiliary circulation pumping from module pumping. Its equations are:

\[
\dot w_h = \dot w_{h,pump} + STEC/\tau_h
\qquad
\dot w_{h,net}=k_{h1}\dot w_{h,pump}
+k_{h2}STEC/\tau_h
\]

\[
\dot w_c = \dot w_{c,pump} + SCR/\tau_c
\qquad
\dot w_{c,net}=k_{c1}\dot w_{c,pump}
+k_{c2}SCR/\tau_c
\]

Here \(\tau_h\) and \(\tau_c\) represent heating/cooling conversion efficiencies, while the \(k\) factors represent the share supplied by paid energy carriers. Exact symbols, units, assumptions, and the full derivation must be checked against the Supplementary Information before implementing this layer. These are not water-intensity factors: converting energy consumption into water burden requires separately sourced, geographically appropriate water-intensity factors and explicit accounting boundaries.

## 3. Required inputs and provenance checklist

| Input | Unit / basis | Evidence needed before model implementation |
|---|---|---|
| Configuration | categorical | Explicitly select one of the three configurations; do not mix equations across configurations |
| Hot/cold inlet temperatures | °C or K differences | Published benchmark or documented scenario; retain source and operating boundary |
| \(\Delta T_{h,in}\), \(\Delta T_{HX}\) | K or °C difference | Source values or explicit sensitivity ranges; avoid treating paper settings as universal |
| \(h_{vap}\) | J/kg or equivalent | Temperature-dependent property source and stated evaluation temperature |
| Vaporization efficiency \(\eta\) | dimensionless | Published range or calibration with independent data; never silently fit to validation targets |
| \(c_h,c_c\) | J/(kg K) | Fluid identity, salinity/temperature basis, and property source |
| \(R\) | fraction | Derived by the specified configuration equations or independent measurements; not an arbitrary constant if pump burden is coupled to recovery |
| Module pressure drop \(\Delta P\) | Pa | Measured or documented hydraulic model, including operating flow |
| Pump efficiency \(\eta_{pump}\) | fraction | Pump curve or cited assumption and sensitivity range |
| Auxiliary loop pumping | kWh/m³ product or consistent specific basis | Separate circuit and calculation; do not merge with membrane-module pumping |
| \(\tau_h,\tau_c\) | dimensionless | Technology-specific efficiencies/COPs and clear energy-carrier boundary |
| \(k_{h1},k_{h2},k_{c1},k_{c2}\) | fractions | Explicitly documented energy-source shares; sum/interpretation checked against source |
| Cooling-sink feasibility | temperatures, duty, flow/capacity | Evidence that a real sink can reject the calculated load at the assumed temperature |
| Water-intensity factors | L/kWh or m³/MWh | Source, geography, time period, and whether withdrawal or consumption |
| Avoided-water counterfactual | L or m³ per functional unit | Explicit displaced source/process and displacement fraction, with a justified boundary |

## 4. What the current project can and cannot claim

The existing scenario runner's fixed MD cooling-to-heating ratio, fixed cooling electricity/water factors, and default fixed pumping factor are useful for **screening conditional scenarios**. They do not reproduce the three configuration-specific equations above, derive single-pass recovery from temperature and efficiency, or jointly resolve pressure drop, pump efficiency, cooling-sink availability, and technology-dependent conversion efficiencies.

The current net-water ledger remains a counterfactual accounting calculation conditional on its inputs. A computed positive or negative result is not evidence of real-world water savings unless the water boundary, displaced supply, operational feasibility, and input factors are defensible.

## 5. Minimum benchmark and implementation gate

Do not implement all three configurations at once. Proceed only after obtaining and recording the supplementary derivation and a benchmark table with, at minimum:

1. A source-defined case and exact configuration.
2. Every input and its units, including property evaluation conventions.
3. Reported intermediate values where available (STEC, SCR, recovery, module pumping).
4. Reported tolerance/rounding and a documented independent hand calculation or second implementation.
5. Dimensional checks and limiting-case tests.
6. A clear distinction between equation verification and empirical validation.

A comparison against the same equations used by the implementation is an analytical verification, not independent empirical validation. If the paper does not provide a reproducible numeric benchmark for a quantity, mark that benchmark unavailable rather than inventing a target.

### Proposed first extension

If the supplement and benchmark support it, implement **one** configuration (preferably the one whose required inputs can be documented most completely) as an optional module, leaving the existing screening baseline unchanged. Add tests for units, physically invalid temperature differences, efficiencies outside (0, 1], recovery bounds, and positive pressure drop. Compare outputs against a separately transcribed reference table before coupling results into the net-water ledger.

## 6. Current status

- Prior art for coupled cooling and freshwater production: established.
- Malaguti equations transcribed from accessible article text: yes, preliminary extraction.
- Supplementary Information independently audited: not yet.
- Published numeric benchmark fully reconstructed: not yet.
- Partial configuration-specific STEC/SCR equation evaluator implemented: yes; full model with derived outlet temperature/recovery and coupled energy/water accounting: no.
- Independent empirical validation: no.
- Novelty established: no.
- Net-water benefit demonstrated: no.


## 7. Full-text numeric anchors extracted on 2026-10-24

A full-text version-of-record PDF was accessible through the Politecnico di Torino institutional repository. This improves on the earlier publisher-page-only extraction, but it does **not** mean the supplementary PDF was independently audited.

Source: [institutional repository PDF](https://iris.polito.it/retrieve/handle/11583/3009010/c2612a47-ce66-4dfc-9742-367e56ec3f6d/1-s2.0-S0011916426001955-main.pdf). The article states that generated data are included in the article and supplementary information.

Published reference anchors (not a complete benchmark table):
- For configuration 3 (AGMD with internal heat recovery), at vaporization efficiency η=0.5, reported single-pass recovery is 2.2% at ΔT=30 °C and 3.9% at ΔT=50 °C.
- At η=0.7, reported recovery is 3.0% at ΔT=30 °C and 5.6% at ΔT=50 °C.
- Figure 4 evaluates module pressure-drop cases of 100, 300, and 1000 mbar. The article reports typical pumping penalties around 0.2–0.5 kWh/m³ at 300 mbar and low single-pass recovery (typically 2–6%).
- Cold-stream inlet temperature is fixed at 20 °C; ΔT_h,in=5 °C and ΔT_HX=5 °C for the explored cases. Technology conversion values are illustrative, not prescriptive.

These values can anchor a recovery/pumping test once supplementary definitions (especially equations deriving ΔT_h,out and R) are transcribed exactly. They do not independently verify STEC/SCR, and graph-read values must not be presented with source-table precision.

### Revised next gate
1. Retrieve and audit the supplementary PDF, including equations S1 onward and variable conventions.
2. Transcribe exact equations deriving ΔT_h,out and recovery R.
3. Build a reference table for the four recovery anchors and available pumping values; distinguish article text from graph-read estimates.
4. Independently implement the equations in a test-only reference script with dimensional checks.
5. Port equations to the production model only after the reference script reproduces source anchors within stated precision.

### Time estimate, scoped
Planning estimate: **6–10 focused hours** if the supplement is accessible and sufficiently complete; allow **another 2–4 hours** if retrieval or interpretation is difficult. This covers source reconstruction, reference calculations, tests, and one optional configuration—not remaining publication work or empirical validation.


## 8. Equation evaluator added (2026-10-24)

Two code artifacts have now been added:
- `src/ai_water/md_thermodynamics.py`: explicit equation-level STEC/SCR evaluators for the three published configurations when the outlet temperature difference and fluid properties are supplied, plus the pressure-drop/recovery/pump-efficiency pumping equation.
- `tests/test_md_thermodynamics.py`: unit and invalid-input tests for equation selection, required configuration inputs, physical bounds, and pressure-unit conversion.

This is deliberately a **partial equation evaluator**, not a full implementation of Malaguti's thermodynamic model. It does not derive `delta_t_h_out_k`, single-pass recovery, temperature-dependent seawater properties, or heat-sink feasibility. The code accepts these required values explicitly and labels the outlet temperature difference as requiring an independent source or validated calculation. It is not connected to the project's main simulation engine or net-water ledger.

The pumping test uses 300 mbar = 30,000 Pa, recovery 0.03, and pump efficiency 0.75, yielding 0.37037 kWh/m³ from the published expression. This is a dimensional/unit-conversion test, not an empirical measurement or a reproduction of a complete paper operating point.

**Verification caveat:** both files were fetched back from the default branch after creation. This confirms repository contents, not successful test execution. The repository CI workflow runs pytest and Ruff on pushes; a passing run must be checked before the implementation is described as tested. The supplementary equations and exact benchmark reconstruction remain open gates.


## 9. Equation-level test strengthening (2026-10-25)

The equation tests were strengthened to compare each configuration's returned STEC/SCR values against separately expanded numerical expressions using the same documented equations, plus an explicit pumping-expression conversion check. These are useful implementation-regression and unit-conversion checks.

They are **not** an independent implementation of the supplementary model and are **not** empirical or published-output validation: the expected values are calculated from the same published equations, with illustrative inputs. The 4 recovery anchors (η = 0.5 and 0.7 at ΔT = 30 °C and 50 °C) remain un-reproduced because the supplementary derivation of ΔT_h,out and R has not been obtained. No test execution or passing CI run is claimed here.

The supplementary file is listed by the publisher as a 618 KB PDF, but direct retrieval through the currently available web route was blocked. The accessible article text confirms that Eq. S8 constrains ΔT_h,out and that recovery depends on η and ΔT; it does not provide the full algebra needed to reconstruct that dependency in this audit. Do not back-solve the equation from the four plotted anchors and then present the result as source-derived.
