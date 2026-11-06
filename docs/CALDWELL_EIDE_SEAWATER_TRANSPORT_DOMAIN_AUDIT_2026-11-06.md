# Caldwell–Eide Seawater Transport Data: Domain and Transferability Audit

**Date:** 2026-11-06  
**Scope:** Clarify the evidence supplied by Caldwell and Eide's 1981 and 1985 experiments for a possible DCMD feed-side transport closure.  
**Status:** Documentation-only audit. No diffusivity or Soret coefficient is added to the numerical model.

## Executive finding

Caldwell and Eide provide useful experimental evidence that is more composition-relevant than isolated NaCl measurements, but it does not supply the missing validated 40–70 °C natural-seawater mutual-diffusion closure.

Two studies must be distinguished:

1. **1981:** isothermal Fickian diffusivities and Soret coefficients were measured for five separate aqueous electrolyte solutions representing principal seawater salts. The reported temperature range is 0.5–40 °C. These are constituent-electrolyte solutions, not one mixed natural-seawater solution and not a multicomponent mutual-diffusion matrix.
2. **1985:** artificial seawater containing six major ions was subjected to thermogravitational (Clusius–Dickel column) separation at 5–40 °C and atmospheric pressure. Ionic Soret coefficients were inferred. The authors report a multicomponent effect relative to the binary-salt results. This is direct multicomponent thermodiffusion evidence, not an isothermal Fickian mutual-diffusion matrix.

Neither study covers the project's full 40–70 °C range. The 1981 Fickian data reach 40 °C only; the 1985 artificial-seawater Soret experiment also reaches 40 °C only. Neither supports extrapolation to 50–70 °C or a scalar natural-seawater mutual diffusivity.

## 1. Caldwell & Eide (1981): separate electrolyte solutions

Caldwell, D.R. and Eide, S.A. (1981), “Soret coefficient and isothermal diffusivity of aqueous solutions of five principal salt constituents of seawater,” *Deep Sea Research Part A* 28(12), 1605–1618. DOI: [10.1016/0198-0149(81)90100-X](https://doi.org/10.1016/0198-0149(81)90100-X).

The abstract reports measurements for:
- NaCl at 28.5 g/kg
- Na2SO4 at 5.0 g/kg
- MgCl2 at 5.0 g/kg
- MgSO4 at 5.0 g/kg
- CaCl2 at 5.0 g/kg

The measurements span 0.5–40 °C and pressures from atmospheric to 620 bar. Interpolation equations are reported for each electrolyte's Soret coefficient and isothermal Fickian diffusivity as functions of temperature and pressure.

**Applicability:**
- The data are valuable as constituent-electrolyte transport evidence.
- The salts were measured in separate aqueous solutions, not together as a full seawater mixture.
- A salt-specific Fickian coefficient is not automatically a component of a natural-seawater mutual-diffusion matrix.
- The temperature domain ends at 40 °C, so the 50, 60 and 70 °C DCMD cases are outside it.
- The broad pressure range does not solve the temperature or composition mismatch. For the current atmospheric-pressure DCMD model, the atmospheric-pressure branch would be the relevant subset, if the full interpolation equations and experimental uncertainties are obtained.

**Decision:** May be cited as a low-temperature constituent-level evidence source or future sensitivity input at the 40 °C boundary only. Do not combine the five scalar coefficients into a seawater diffusivity by arithmetic, mass-fraction, or mole-fraction averaging.

## 2. Caldwell & Eide (1985): artificial-seawater thermodiffusion

Caldwell, D.R. and Eide, S.A. (1985), “Separation of seawater by Soret diffusion,” *Deep Sea Research Part A* 32(8), 965–982. DOI: [10.1016/0198-0149(85)90039-1](https://doi.org/10.1016/0198-0149(85)90039-1).

The abstract reports artificial-seawater samples separated in a Clusius–Dickel thermogravitational column at 5–40 °C and atmospheric pressure. The represented ions were Na, Mg, K, Ca, Cl and sulfate. Positive ions were measured by atomic absorption and negative ions by titration; ionic Soret coefficients were calculated from the separations.

The authors report a multicomponent effect: ionic coefficients were not identical to those previously measured for the same ions in binary salts. They state that, except for sulfate, the Soret coefficients were similar to the binary-salt values and that the difference was moderate for their artificial-seawater composition.

**Applicability:**
- This is direct evidence that a multicomponent seawater-like mixture can alter thermodiffusive response relative to isolated binary electrolytes.
- It concerns Soret/thermodiffusive separation in a thermogravitational column, not isothermal Fickian salt transport through a DCMD feed boundary layer.
- The 5–40 °C range does not cover the 50–70 °C operating cases.
- The column's thermal and hydrodynamic conditions are not the Wyon rectangular membrane channel.
- The abstract alone does not provide a validated coefficient set or uncertainty model for conversion to Nayar Reference Salinity.

**Decision:** Use as qualitative, multicomponent Soret evidence only. It strengthens the decision to keep thermodiffusion separate from isothermal CP closure; it does not provide a Fickian diffusivity or DCMD Soret closure.

## 3. Consequence for the current DCMD model

The current DCMD sweep uses feed temperatures 40, 50, 60 and 70 °C and Reference Salinities 15, 35 and 38 g/kg. The evidence coverage is therefore:

| Source | Transport quantity | Composition | Temperature range | What it can support |
|---|---|---|---:|---|
| Caldwell & Eide (1981) | Isothermal Fickian diffusivity and Soret coefficient | Five separate aqueous salt solutions | 0.5–40 °C | Constituent-level evidence, at most a 40 °C sensitivity with correct species/basis |
| Caldwell & Eide (1985) | Ionic Soret coefficients | Artificial six-ion seawater mixture | 5–40 °C | Qualitative multicomponent thermodiffusion evidence |
| Felmy & Weare (1991), Part I | Coupled multicomponent ionic diffusion model | Six-component seawater system | 25 °C | Best structural model architecture at the reference temperature |
| Felmy & Weare (1991), Part II | Associated-species multicomponent model | Six-component seawater system | 25 °C | Highlights association and the lack of required data beyond 25 °C |

No listed source validates a natural-seawater mutual-diffusion closure over 40–70 °C and 15–38 g/kg.

## 4. Required safeguards

1. Do not call the 1981 separate-electrolyte values “natural-seawater diffusivity.”
2. Do not call the 1985 Soret coefficients Fickian diffusivities.
3. Do not average the five 1981 salt coefficients to create an effective scalar seawater coefficient without a derivation and validation.
4. Do not extrapolate either 1981 or 1985 data above 40 °C.
5. Do not infer a temperature trend from the 1981/1985 results and extend it to 70 °C.
6. Keep thermal-diffusion terms distinct from isothermal concentration-driven transport.
7. Retain the current no-CP baseline until a suitable closure and hydrodynamic Sherwood relation are independently justified.

## References

- Caldwell, D.R. & Eide, S.A. (1981). “Soret coefficient and isothermal diffusivity of aqueous solutions of five principal salt constituents of seawater.” *Deep Sea Research Part A*, 28(12), 1605–1618. DOI: 10.1016/0198-0149(81)90100-X.
- Caldwell, D.R. & Eide, S.A. (1985). “Separation of seawater by Soret diffusion.” *Deep Sea Research Part A*, 32(8), 965–982. DOI: 10.1016/0198-0149(85)90039-1.
- Felmy, A.R. & Weare, J.H. (1991). “Calculation of multicomponent ionic diffusion from zero to high concentration: I. The system Na-K-Ca-Mg-Cl-SO4-H2O at 25°C.” *Geochimica et Cosmochimica Acta*, 55, 113–131. DOI: 10.1016/0016-7037(91)90405-T.
- Felmy, A.R. & Weare, J.H. (1991). “Calculation of multicomponent ionic diffusion from zero to high concentration: II. Inclusion of associated ion species.” *Geochimica et Cosmochimica Acta*, 55, 133–144. DOI: 10.1016/0016-7037(91)90406-U.
