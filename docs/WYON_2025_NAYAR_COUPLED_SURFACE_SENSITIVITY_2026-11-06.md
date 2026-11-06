# Nayar 2016 coupling in the Wyon local DCMD surface solver

**Implementation note — 2026-11-06**

## Purpose and scope

The surface solver now exposes an opt-in `vapour_pressure_model="nayar_2016"` sensitivity mode. The default remains `"wyon_2025"`; no baseline equations or default inputs have been changed.

This is a local, steady membrane-surface calculation coupled to the existing Wyon channel-film iteration. It is not a full axial DCMD module model, and it does not reproduce Wyon Figure 9.

## Correlation pairing

The Nayar branch consistently uses both Nayar equations:

- Pure-water saturation pressure, Nayar et al. (2016) Eq. (6), for the permeate-side interface.
- Natural-seawater vapour pressure, Nayar et al. (2016) Eq. (5), for the feed-side interface:
  `p_v,sw(T,S) = p_v,w(T) exp(-4.58180e-4 S - 2.04430e-6 S^2)`.

The same natural-seawater correlation is used for the mean-membrane-temperature vapour pressure in the pore-gas air-partial-pressure term of the Wyon combined Knudsen/molecular diffusion expression. The paired Nayar pure-water correlation is used as the reference pressure inside Eq. (5). The branch does not combine the Nayar salinity factor with Wyon's different pure-water coefficients.

The input `feed_salinity_sr_g_kg` is Reference Salinity in g/kg, consistent with the Nayar correlation. Its use as the channel-property salinity and as the Nayar pressure salinity is explicit.

## Important interface and pore assumptions

The current model does not solve concentration polarization or a membrane-interface salinity field. For this sensitivity branch, the supplied bulk feed Reference Salinity is used as a proxy for:

1. feed-side membrane-interface salinity in the feed-interface vapour pressure; and
2. salinity associated with the mean-membrane-temperature pore vapour pressure used to estimate air partial pressure.

These are modelling assumptions for a bounded property sensitivity, not claims that bulk and interface salinity are physically identical. The code does not resolve salt accumulation, salt rejection, pore wetting, or local pore composition.

## Preserved Wyon baseline

- `vapour_pressure_model` defaults to `"wyon_2025"`.
- Wyon's source-faithful pure-water vapour-pressure convention remains in force in the default path.
- Existing Wyon sensitivity regression fixtures remain unchanged and exercise the default path.
- The alternative branch requires an explicit feed salinity; it cannot silently assume zero salinity.

## Interpretation limits

Nayar et al. report the natural-seawater vapour-pressure correlation as valid over 0–180 °C and 0–160 g/kg, with maximum uncertainty ±0.26% within its stated range. The implemented local Wyon surface solver retains its own 0–100 °C bulk-temperature guard. Correlation uncertainty is not the same as uncertainty in predicted DCMD flux.

A change in local flux or heat flux under this branch is a model-form sensitivity result. It is not experimental validation, does not establish the exact salinity used in Wyon's Figure 9 comparison, and does not substitute for the missing axial stream enthalpy/outlet calculations (Wyon Eqs. 18–20).

## References

Nayar, K. G., Sharqawy, M. H., Banchik, L. D., & Lienhard V, J. H. (2016). Thermophysical properties of seawater: A review and new correlations that include pressure dependence. *Desalination, 390*, 1–24. https://doi.org/10.1016/j.desal.2016.02.024

Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University, report LUTFD2/TFEM--25/5229--SE.
