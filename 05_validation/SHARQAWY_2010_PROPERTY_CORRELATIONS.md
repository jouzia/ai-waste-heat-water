# Sharqawy (2010) property-correlation implementation

**Status:** source equations transcribed into callable functions; AGMD reproduction remains blocked by the article's unspecified property evaluation states and seawater salinity. These functions do not assign stream temperatures or salinity.

## Source and equations

Sharqawy, M.H., Lienhard V, J.H. & Zubair, S.M. (2010), “The thermophysical properties of seawater: a review of existing correlations and data,” *Desalination and Water Treatment* 16, 354–380. DOI: https://doi.org/10.5004/dwt.2010.1079. The MIT-hosted author manuscript was used for this transcription: https://web.mit.edu/lienhard/www/papers/journal/Thermophysical_properties_of_seawater-DWT-16-354-2010.pdf.

Implemented in `src/ai_water/sharqawy_2010.py`:

- **Eq. (3):** (S_R = 1.00472 S_P); implementation converts the article's reference-composition salinity (S_R) to the practical salinity (S_P) required by the Jamieson heat-capacity fit.
- **Eq. (4):** (T_{90}=T_{68}-0.00025(T_{68}-273.15)); implementation converts ITS-90 kelvin to IPTS-68 kelvin for Eq. (9).
- **Eq. (9), Table 3:** Jamieson et al. seawater heat capacity, returned in J/(kg K). The source's input range is (273.15<T_{68}<453.15) K and (0<S_P<180) g/kg; stated maximum deviation is ±0.28%.
- **Eq. (37):** (h_{fg,sw}=h_{fg,w}(1-S_R/1000)), returning latent heat per kg of total seawater solution rather than per kg of evaporated water.
- **Eq. (54), Table 11:** pure-water latent heat, returned in J/kg for 0–200°C.
- **Eq. (51), Table 11:** pure-water specific heat, returned in J/(kg K), with pressure supplied in MPa. The default 0.101325 MPa lies inside the table's stated (0.1<p<100) MPa validity interval.

The paper says the non-ideal correction in Eq. (39) is small and recommends Eq. (37) as an adequate estimate. The implementation therefore uses Eq. (37), and does not apply Eq. (39) a second time.

## Important mass-basis distinction

The AGMD article describes complete salt rejection and pure distillate. Therefore:
- hot/feed and cold/cooling saline-stream heat capacities must use the saline correlation at their explicitly chosen stream temperatures and salinity;
- distillate heat capacity must use the pure-water correlation;
- the latent-heat basis must be made consistent with the mass basis in the supplementary mass and energy balances.

Do not pass a pure-water latent heat per kg evaporated water into an equation whose latent heat is per kg of total saline solution, or vice versa. The new functions expose the two bases separately.

## What is still not specified

The Malaguti et al. (2026) main article and SI available to this audit do not identify:
1. the numerical seawater salinity used for the Config. 3 calculations;
2. the exact temperature at which (c_h) and (c_c) are evaluated (or whether the Jamieson fit is evaluated at inlet, mean, or another representative stream temperature);
3. the evaluation temperature for the pure distillate (c_d);
4. the temperature at which (h_{vap}) is evaluated;
5. whether any additional pressure convention beyond the near-atmospheric 2010 correlations is applied.

These are not recoverable uniquely from the four rounded recovery anchors. Do not fit salinity or property temperatures to those anchors. The solver continues to require explicit property inputs until the article authors clarify the missing states or a defensible, separately labelled scenario protocol is adopted.

## Verification boundary

Unit tests cover the published scale conversions, unit conversion, solution-mass latent-heat factor, representative physical ranges, and validity-range rejection. Passing these tests verifies the implementation against the transcribed equations; it does **not** demonstrate that the article's undocumented property evaluation states have been recovered or that the AGMD recovery results have been reproduced.
