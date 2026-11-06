# Reference Salinity and film-theory concentration-basis audit

**Date:** 2026-11-06  
**Status:** derivation and model-interface audit; no solver changes  
**Related work:** Nayar (2016) vapour-pressure variant; feed-side concentration-polarization applicability; seawater salt-diffusivity evidence audit; Caldwell binary-NaCl domain audit

## Executive finding

Nayar's salinity input is Reference Salinity in g/kg, a mass-per-mass quantity. The common DCMD film-theory concentration-polarization relation is often written using a volumetric salt concentration (e.g. kg/m³) and a solution density. These quantities are not numerically interchangeable.

For a seawater composition represented on the Reference Salinity scale, define the mass-fraction proxy

`w_R = S_R/1000`

where `S_R` is in g/kg. The corresponding salt-equivalent mass concentration is

`C_R = rho w_R = rho S_R/1000`

in kg/m³ when `rho` is in kg/m³. This is a basis conversion, not a claim that Reference Salinity is the exact mass of every dissolved constituent in composition-anomalous seawater. TEOS-10 distinguishes Reference Salinity from Absolute Salinity; Absolute Salinity includes a composition anomaly correction.

The conventional exponential CPC relation is derived under a specified film model and commonly assumes constant density across the concentration boundary layer. Under that approximation, the concentration ratio and mass-fraction ratio coincide. If density is allowed to vary from bulk to interface, the conversion must retain the density ratio; it is not valid to apply a volumetric concentration ratio directly to Reference Salinity without stating the density assumption.

No numerical CPC is introduced here. The mass-transfer coefficient, diffusivity, geometry-specific Sherwood closure, and interface composition are still unresolved.

## 1. Definitions and units

Let:
- `S_R`: Reference Salinity, g/kg seawater;
- `w_R = S_R/1000`: Reference-Salinity mass-fraction proxy, kg/kg;
- `rho`: local solution density, kg/m³;
- `C_R = rho w_R`: Reference-Salinity-equivalent salt concentration, kg/m³.

Thus,

`C_{R,b} = rho_b S_{R,b}/1000`

and

`C_{R,m} = rho_m S_{R,m}/1000`.

The ratio is

`C_{R,m}/C_{R,b} = (rho_m/rho_b)(S_{R,m}/S_{R,b})`.

This identity is exact for the defined proxy concentration. It shows why a volumetric concentration ratio equals a Reference-Salinity ratio only when the density ratio is unity (or when density variation is explicitly neglected).

TEOS-10 defines Absolute Salinity as the mass fraction of dissolved material and uses Reference Salinity as the reference-composition salinity scale. For natural seawater whose composition differs from Reference-Composition Seawater, Absolute Salinity may differ from Reference Salinity by an Absolute Salinity Anomaly. The current Nayar implementation uses Reference Salinity as its documented input variable; this audit does not silently replace it with Absolute Salinity.

## 2. Film-theory relation and the density assumption

A common DCMD film-theory expression is

`C_{R,m}/C_{R,b} = exp[J_v/(rho_b k_s)]`

where:
- `J_v` is water-vapour mass flux, kg m⁻² s⁻¹;
- `rho_b` is the chosen bulk-feed solution density, kg m⁻³;
- `k_s` is the salt-side film mass-transfer coefficient, m s⁻¹.

The exponent is dimensionless. With `k_s = Sh D_s/D_h`, the expression is only as defensible as the chosen salt diffusivity and Sherwood correlation.

If this expression is used with constant density across the film (`rho_m = rho_b`), then

`S_{R,m}/S_{R,b} = exp[J_v/(rho_b k_s)]`

and

`S_{R,m} = S_{R,b} exp[J_v/(rho_b k_s)]`.

This is the simplest consistent bridge from the volumetric concentration convention to Nayar's g/kg input. The same exponential multiplier applies to the mass-fraction proxy because constant density makes the two ratios equal.

If density is not assumed constant, the identity in Section 1 gives

`S_{R,m}/S_{R,b} = (rho_b/rho_m)(C_{R,m}/C_{R,b})`.

Therefore, if the conventional volumetric CPC expression is retained as written, its conversion to Reference Salinity requires the interfacial-to-bulk density ratio. One must not multiply Reference Salinity by the volumetric CPC and omit this factor while simultaneously claiming variable-density consistency.

A more rigorous variable-density film model should be derived from the salt mass balance using a clearly specified mass-average velocity, concentration coordinate, and composition-dependent density/diffusivity. The simple exponential relation should not be patched with an arbitrary density correction without deriving the governing equation and boundary conditions.

## 3. Consequences for the Nayar vapour-pressure model

The Nayar (2016) natural-seawater vapour-pressure relation uses Reference Salinity in g/kg in its salinity-depression factor:

`p_{v,sw}(T,S_R)=p_{v,w}(T)\exp(-4.58180\times10^{-4}S_R-2.04430\times10^{-6}S_R^2)`.

Therefore, the interface salinity supplied to Nayar must remain in g/kg Reference Salinity units. Do not pass:
- `C_R` in kg/m³;
- `w_R` as kg/kg;
- Practical Salinity as a dimensionless number;
- NaCl molality or NaCl-equivalent concentration;

without an explicitly justified conversion to the Reference Salinity scale.

For the present research implementation, bulk Reference Salinity is still only a proxy for the feed-interface and mean-pore salinity. The pore-side composition field is not independently resolved, and the Nayar salinity factor is not a concentration-polarization model.

## 4. Recommended implementation contract if CPC is later enabled

Any future CPC feature must make its concentration basis explicit in names, documentation, and tests. Minimum contract:

1. Input bulk salinity is `reference_salinity_g_per_kg`, not a generic `concentration`.
2. Convert to a mass-fraction proxy with `w_R = S_R/1000`.
3. If the chosen film correlation is written in kg/m³, construct `C_R = rho w_R` using a density correlation valid for the stated temperature and composition.
4. State whether the film model assumes constant bulk density. Under that approximation, apply the exponential CPC multiplier directly to `S_R`.
5. If variable density is claimed, use `S_{R,m}/S_{R,b}=(rho_b/rho_m)(C_{R,m}/C_{R,b})` and derive the variable-density film balance rather than applying the constant-density exponential formula unchanged.
6. Validate units and dimensional consistency; ensure zero flux gives `S_{R,m}=S_{R,b}`; positive retained-salt flux gives nondecreasing interface salinity under the stated model.
7. Enforce the validity domains of density, diffusivity, and Sherwood correlations independently. Do not extrapolate the Caldwell (1974) binary-NaCl coefficient above 52 °C or label it natural-seawater diffusivity.
8. Keep this entire CPC path opt-in and research-only. The Wyon baseline and the existing Nayar bulk-salinity comparison remain unchanged.

## 5. Open items

- Determine whether Nayar's exact salinity convention in the 2016 correlation is Reference Salinity or a closely related seawater salinity scale from the full paper's definitions and cited equation source; current project documentation uses Reference Salinity and must preserve that stated convention unless primary-source review requires correction.
- Select a composition-dependent seawater density formulation consistent with the salinity scale used.
- Resolve the binary-NaCl versus natural-seawater transport-property mismatch.
- Establish a geometry-appropriate feed-side Sherwood relation for the Wyon apparatus.
- Derive and validate a variable-density film model if density variation across the film is to be retained.

## References

1. Nayar, K. G. et al. (2016). *Thermophysical properties of seawater: A review and new correlations that include pressure dependence*. Desalination 390, 1–24. DOI: 10.1016/j.desal.2016.02.024.
2. IOC, SCOR and IAPSO (2010). *The International Thermodynamic Equation of Seawater – 2010: Calculation and Use of the Thermodynamic Properties of Seawater*. TEOS-10 Manual, UNESCO.
3. TEOS-10 Gibbs SeaWater (GSW) documentation: `gsw_SR_from_SP` and `gsw_uPS`, which define Reference Salinity output in g/kg.
4. Suleman, M. et al. (2021). DCMD review discussion of concentration polarization and the film-theory relation for interfacial concentration, *Desalination and Water Treatment* 229, 52–68.
5. Open Membrane Database, concentration-polarization film-theory description, including the role of solute rejection and film mass-transfer coefficient.
