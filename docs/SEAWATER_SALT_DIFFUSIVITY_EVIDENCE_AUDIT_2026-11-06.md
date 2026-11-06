# Seawater salt-diffusivity evidence and scalar-closure applicability audit

**Date:** 2026-11-06  
**Status:** literature evidence audit; no solver changes  
**Related audits:** feed concentration-polarization applicability; spacer-channel transfer correlation; Wyon Table 6/Table 7 hydraulic-diameter provenance

## Executive finding

The literature located so far does not justify selecting one scalar salt mutual/effective diffusivity for the current Wyon/Nayar concentration-polarization model over the full 40–70 °C and 15–38 g/kg Reference Salinity domain.

The available studies measure different transport quantities and different solution systems:

- self-diffusion coefficients of individual ions in seawater;
- self-diffusion coefficients of Na+ and Cl− in concentrated binary NaCl solutions;
- mutual diffusion coefficients in selected ternary electrolyte mixtures;
- Fickian diffusion of NaCl in an approximately oceanic-concentration binary solution, with the full experimental validity range not exposed in the available abstract;
- multicomponent thermodiffusion (Soret transport), which is not the isothermal Fickian diffusivity needed by the conventional film-theory CPC equation.

These values cannot be substituted for one another without a thermodynamic/transport model that defines the concentration variable and maps multicomponent ionic transport to the chosen scalar salt flux.

## Evidence matrix

| Study | Solution / measurement | Temperature and composition coverage | What it can support | Why it is not yet the CPC input |
|---|---|---|---|---|
| Caldwell (1973), DOI 10.1016/0011-7471(73)90073-9 | Fickian NaCl diffusivity in 0.5-normal aqueous NaCl; reports a temperature expression | Abstract identifies 0.5 N; accessible abstract does not establish the full temperature validity range | Candidate binary-NaCl reference, subject to full-text range and units verification | Binary NaCl, not natural seawater; temperature-domain and mass/molar concentration basis need verification |
| Poisson & Papaud (1983), DOI 10.1016/0304-4203(83)90002-6 | Self-diffusion coefficients of five major ions in natural seawater; Na+ and Cl− studied versus temperature and salinity | Natural seawater S=34.86 at 25 °C; Na+ and Cl− temperature/salinity dependence investigated | Ion-specific mobility context for seawater | Self-diffusion is not the mutual salt diffusivity governing a bulk salinity gradient |
| Poisson & Gadhia / related five-salt work (1981), DOI 10.1016/0198-0149(81)90100-X | Fickian diffusivity of five principal salts in separate aqueous electrolyte solutions | 0.5–40 °C; NaCl 28.5 g/kg, Na2SO4 5.0 g/kg, MgCl2 5.0 g/kg, MgSO4 5.0 g/kg, CaCl2 5.0 g/kg | Component-specific electrolyte diffusivity evidence and temperature trends | Separate salt solutions are not one multicomponent seawater mixture; temperature range does not cover 50–70 °C |
| Miller et al. (1986), DOI 10.1016/0016-7037(86)90021-9 | Mutual diffusion matrix for ternary NaCl–MgCl2–H2O seawater analogue | 25 °C; NaCl 0.489 M and MgCl2 0.051 M | Direct evidence that a seawater-like ternary electrolyte requires multiple main- and cross-diffusion coefficients | Single-temperature result; ternary analogue, not full seawater chemistry; scalar reduction requires justification |
| ACS (2023), DOI 10.1021/acs.jpcb.3c03863 | Simulated Na+ and Cl− self-diffusion in binary NaCl aqueous solution | 273–433 K, 1–5 mol/kg | Temperature- and salinity-dependent ion self-mobility in concentrated NaCl brines | Self-diffusion rather than mutual salt diffusion; 1–5 mol/kg is above the approximate NaCl-equivalent molality of the current 15–38 g/kg seawater domain |
| J. Chem. Phys. (2025), DOI 10.1063/5.0272445 | Molecular-dynamics self-diffusion of major ions in model standard seawater | Standard seawater S_R=35.166 g/kg; tabulated values 2–25 °C | Ion-specific self-diffusion in a realistic multicomponent composition | Low-temperature range and self-diffusion observable; does not provide a 40–70 °C mutual salt coefficient |
| Nature Water (2025), DOI 10.1038/s44221-025-00428-5 | Thermodiffusion/Soret response in NaCl brine and natural-seawater experiments | NaCl and natural seawater near 41 °C; thermal gradients and multichannel experiments | Shows multicomponent thermodiffusive behaviour and effective collective response under temperature gradients | Soret/thermodiffusion is an additional transport term, not the isothermal Fickian coefficient in the standard CPC film equation |

## Quantitative notes

### 1. Approximate concentration-domain comparison

For a rough NaCl-equivalent conversion only (not a claim that seawater is NaCl), a Reference Salinity range of 15–38 g/kg corresponds approximately to:

`m_{NaCl,eq} = (S/58.44)/(1-S/1000)`

where S is expressed in g/kg solution and the result is mol/kg water.

This gives approximately 0.261–0.676 mol/kg water. This is below the 1–5 mol/kg range of the ACS (2023) NaCl ion self-diffusion table. That dataset therefore cannot be directly interpolated into the current salinity range without extrapolation and a change of observable (self- to mutual diffusion).

### 2. Why a single ion coefficient is not a salt mutual coefficient

In multicomponent electrolytes, individual ionic fluxes are coupled by electroneutrality, activity gradients, and cross-diffusion. Miller et al. (1986) measured a ternary NaCl–MgCl2–H2O analogue and found significant cross terms; four coefficients were required to describe the ternary diffusion system. A scalar effective coefficient could be constructed only after defining the salt-composition coordinate and the boundary conditions, and then deriving or fitting the effective response.

Poisson & Papaud (1983) report tracer/self-diffusion coefficients for individual seawater ions. These are useful mobility data but do not, by themselves, give the collective Fickian salt flux down the bulk salinity gradient.

### 3. Thermodiffusion is a separate term

The Nature Water (2025) work reports Soret/thermodiffusive transport in NaCl brine and natural seawater around 41 °C. Its flux framework includes both Fickian and thermal-gradient terms. The existence of this effect is relevant because the DCMD feed boundary layer has a temperature gradient, but it does not mean the conventional isothermal film-theory relation can simply be assigned the Soret coefficient or a self-diffusion coefficient. If thermal diffusion is later included, it must be an explicitly separate term and supported by an appropriate coupled model.

## Consequence for the current CPC model

The conventional film relation used in the prior applicability audit,

`C_{f,m}/C_{f,b} = exp(J_v/(k_s rho))`,

requires a defensible salt concentration variable, solution density convention, and a salt mass-transfer coefficient `k_s = Sh D_s/D_h`. Selecting `D_s` is not merely choosing a convenient value in the 10^-9 m²/s range. It defines the transport observable and solution chemistry represented by the model.

The current evidence does not establish a single `D_s(T,S)` for natural seawater over 40–70 °C and 15–38 g/kg. The laminar/turbulent and empty/spacer channel-correlation questions also remain configuration-specific. Consequently:

1. Do not implement a default CPC correction.
2. Do not average Na+ and Cl− self-diffusion coefficients and call the result a measured seawater mutual diffusivity.
3. Do not extrapolate the 0.5–40 °C electrolyte data to 70 °C without labelling the extrapolation and quantifying uncertainty.
4. Do not use the 1–5 mol/kg NaCl self-diffusion data directly for 0.26–0.68 mol/kg NaCl-equivalent seawater.
5. Keep the Nayar bulk Reference Salinity proxy and all Wyon baseline results unchanged.

## Defensible next research options

A future numerical study can proceed only after one of the following routes is selected and labelled:

- **Binary-NaCl approximation:** define the solution as NaCl rather than natural seawater, identify a mutual/Fickian diffusivity correlation valid over the full temperature and molality range, and quantify the composition approximation.
- **Multicomponent seawater model:** obtain a validated multicomponent Maxwell–Stefan or Onsager diffusion matrix for representative seawater composition and temperature, then derive the effective salt transport response under electroneutrality.
- **Empirical effective coefficient:** obtain DCMD feed-channel data for membrane-interface concentration or a validated concentration-polarization coefficient under matching geometry, temperature, salinity, and flow conditions.

Any exploratory sensitivity using a prescribed `D_s` should be explicitly named an assumed-coefficient sensitivity, not a predictive seawater CPC model.

## References

1. Caldwell, D. R. (1973). *Thermal and Fickian diffusion of sodium chloride in a solution of oceanic concentration*. Deep-Sea Research and Oceanographic Abstracts 20(11), 1029–1039. DOI: 10.1016/0011-7471(73)90073-9.
2. Poisson, A. & Papaud, A. (1983). *Diffusion coefficients of major ions in seawater*. Marine Chemistry 13(4), 265–280. DOI: 10.1016/0304-4203(83)90002-6.
3. *Soret coefficient and isothermal diffusivity of aqueous solutions of five principal salt constituents of seawater* (1981). Deep-Sea Research Part A 28(12), 1605–1618. DOI: 10.1016/0198-0149(81)90100-X.
4. Miller, D. G., Ting, A. W., Rard, J. A. & Eppstein, L. B. (1986). *Ternary diffusion coefficients of the brine systems NaCl (0.5 M)-Na2SO4 (0.5 M)-H2O and NaCl (0.489 M)-MgCl2 (0.051 M)-H2O (seawater composition) at 25°C*. Geochimica et Cosmochimica Acta 50(11), 2397–2403. DOI: 10.1016/0016-7037(86)90021-9.
5. *Transport Properties of NaCl in Aqueous Solution and Hydrogen Solubility in Brine* (2023). Journal of Physical Chemistry B. DOI: 10.1021/acs.jpcb.3c03863.
6. *Large-scale simulations of a detailed molecular model of seawater: ionic conductivity and diffusion coefficients of CO2* (2025). Journal of Chemical Physics 163, 034505. DOI: 10.1063/5.0272445.
7. *All-liquid thermal desalination and brine concentration via multichannel thermodiffusion* (2025). Nature Water. DOI: 10.1038/s44221-025-00428-5.
