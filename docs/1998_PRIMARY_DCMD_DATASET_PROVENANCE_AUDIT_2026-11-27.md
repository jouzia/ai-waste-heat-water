# 1998 Primary DCMD Dataset Provenance Audit (2026-11-27)

## Disposition

A second primary experimental paper by Martínez-Díez and Vázquez-González has been located in accessible full text:

- Martínez-Díez, L.; Vázquez-González, M.I. (1998), “Effects of Polarization on Mass Transport through Hydrophobic Porous Membranes,” *Industrial & Engineering Chemistry Research*, 37(10), 4128–4135.
- DOI: 10.1021/ie970911q
- Publisher record: https://pubs.acs.org/doi/10.1021/ie970911q
- Accessible full-text PDF: https://citeseerx.ist.psu.edu/document?doi=a77be3eade26facb51c0ddcc6a7b3a792da6e582&repid=rep1&type=pdf

This is a primary experimental source, not a secondary model comparison. It is registered as `MD-DCMD-POLARIZATION-1998`. Its plotted observations have not yet been digitized. It is not merged with the 1999 observation ledger and does not change the validation gate.

## Experimental design recovered from the paper

The paper reports experiments using a flat Gelman TF200 PTFE membrane with:

- 80% void fraction;
- 60 μm thickness;
- 0.2 μm nominal pore size;
- nine prismatic feed channels and nine permeate channels, each approximately 0.45 × 7.0 × 55.0 mm;
- effective membrane area 34.6 × 10⁻⁴ m².

The warm feed was water or aqueous NaCl at 0.55, 1.15, and 1.67 M; the cold side initially contained pure water. The bulk temperature difference was 10°C. Average hot-side temperature varied from approximately 20°C to 50°C in increments of about 7°C. The recirculation rates were 7, 11, and 15 × 10⁻⁶ m³/s, corresponding to channel velocities of approximately 0.25, 0.39, and 0.53 m/s. Both sides used the same recirculation rate in each experiment.

The paper's source locators are:

| Figure/table | Reported content | Evidence class |
|---|---|---|
| Figures 4–6 | Measured water flux against feed temperature for the three recirculation rates; symbols distinguish water and NaCl feed concentrations | Primary experimental observations plotted as figures |
| Figures 8–12 | Temperature-polarization and vapour-pressure-polarization coefficients | Experimental-data-derived/analytical results; confirm the exact definition before use |
| Table 1 | Heat-transfer coefficient and membrane coefficient estimates with reported uncertainties | Inferred coefficients from the paper's analysis, not independent measurements |

The article states that water flux was measured by timing and weighing distillate collected from the cold reservoir. It reports feed/permeate temperature measurements at module inlets and outlets, small temperature fluctuations, and high salt rejection.

## Relationship to the 1999 benchmark: unresolved

The later 1999 *Journal of Membrane Science* paper by the same authors uses the same nominal TF200 membrane specification and channel dimensions, and its experimental discussion also covers water and NaCl feeds, temperature, and recirculation-rate effects. However, the 1999 paper reports an effective membrane area of 33.7 × 10⁻⁴ m², versus 34.6 × 10⁻⁴ m² in the 1998 paper.

A 2008 paper by Abdel-Rahman reproduces water-only flux and temperature-polarization comparisons and explicitly attributes the plotted experimental series to the 1999 paper. Its conditions (25, 39, and 53 cm/s; ΔT_b = 10°C) closely match the 1998 paper's reported velocities and temperature difference. This is strong evidence of related experimental conditions, but it does not prove that the 1998 and 1999 plotted datasets are identical. The 1998 paper is therefore retained as a separate candidate primary dataset until pointwise overlap can be assessed.

Do not:
- combine the 1998 and 1999 series;
- treat the 2008 reproduction as an independent experiment;
- use the 1998 inferred Table 1 coefficients as independent validation of a model calibrated to the same flux data;
- infer that the small membrane-area discrepancy is a typographical error without author or source clarification.

## Recommended extraction protocol

1. Preserve the accessible PDF and record its SHA-256 hash, retrieval date, page count, and exact page numbers for Figures 4–6 and 8–12.
2. Digitize only the experimental symbols in Figures 4–6. Keep model curves, if any, in separate series and never label them as observations.
3. Record the feed concentration, recirculation rate, average bulk feed temperature, bulk temperature difference, flux units, and figure locator for every point.
4. Calibrate both axes from at least three major ticks and retain pixel coordinates, calibration parameters, and digitizer/software version.
5. Perform an independent second extraction before accepting any values. Report pointwise differences and an uncertainty envelope that includes marker width, line overlap, and axis calibration.
6. Compare candidate 1998 points with the 1999 and 2008 reproductions only after checking temperature definitions, flux units, feed concentration, flow-rate mapping, and membrane-area treatment.
7. Keep all extracted values in a clearly labelled secondary/provisional ledger until the overlap and provenance questions are resolved. The primary 1999 ledger remains unchanged.

## Validation status

No extraction, fitting, parameter calibration, validation score, or gate transition is claimed here. The new source creates a credible path to a primary experimental benchmark independent of the ambiguous 2020 Figure 3 caption, but the data still require controlled extraction and overlap analysis.
