# Wyon 2025: water-boundary and model-reproducibility addendum

**Date:** 2026-11-04  
**Parent audit:** `docs/PRIOR_ART_WYON_2025_DCMD_AUDIT_2026-11-04.md`  
**Primary source:** Annie Wyon (2025), *Desalination utilizing data centre waste heat: A techno-economic study*, Lund University. [Full thesis PDF](https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf).

This addendum records details verified against the complete thesis PDF and corrects one ambiguity in the earlier audit.

## 1. Water-throughput boundary: freshwater output is small relative to seawater intake

Wyon's standard case uses a 60 kg/s seawater feed to 80 DCMD modules. The operating table reports approximately 2 × 10^6 kg/year freshwater production and approximately 1,816 × 10^6 kg/year seawater requirement. The implied product-to-feed mass ratio is approximately 0.110%, assuming the reported annual quantities are comparable and seawater density is treated on the same mass basis.

This is not a measured recovery ratio; it is a derived ratio from the thesis's modelled annual quantities. The thesis also describes freshwater production across the tested temperature envelope as less than 0.1 to 0.7 m³/h. These values make feed intake and discharge a first-order part of any environmental assessment, not a negligible auxiliary flow.

The thesis's environmental discussion says the product system has a very high seawater-to-freshwater ratio, approximately 3,500:1 to 300:1, compared with around 10–20 for MED/MSF. It notes chemical treatment and post-treatment are not fully included in the economic estimate.

## 2. Thermal discharge is a major environmental constraint

The thesis identifies thermal discharge as a potentially dominant direct impact. It reports discharge temperatures up to 50°C above ambient seawater, compared with a cited recommendation to limit discharge to 10°C above ambient. It suggests alternative MD configurations with heat exchange between outlet and incoming feed as possible mitigation.

This finding is important for Research 2: a model that credits waste-heat reuse and freshwater production but does not account for the temperature and location of the returned seawater/brine would have an incomplete environmental boundary. Thermal pollution must be tracked separately from blue-water consumption; they are related operational impacts but not interchangeable metrics.

## 3. Auxiliary electricity and energy boundary

The two selected commercial pumps are reported at 4.053 kW and 2.564 kW, approximately 6.62 kW total (rounded in the discussion to 7 kW). The thesis's variable electricity cost is dominated by pump electricity. Thermal energy is priced at zero because the heat is treated as waste heat.

The thesis does discuss indirect environmental impact from electricity generation and the Spanish electricity mix, but it does not quantify an explicit water-consumption factor for the electricity used by the two pumps. This leaves an opening for a more complete operational water ledger, but not a basis for claiming that indirect electricity impacts themselves are novel.

## 4. Availability inconsistency to preserve in reproduction

The methodology's annual production calculation sets operational availability Γ = 0.96 and reports 8,410 operating hours/year. The critical-evaluation section later describes operational availability as 95%. These are inconsistent (0.96 × 8,760 = 8,409.6 hours, whereas 0.95 × 8,760 = 8,322 hours). A faithful reproduction should retain the methodology value for reproducing the reported annual operating hours, document the later 95% statement as an internal inconsistency, and test both values in sensitivity analysis rather than silently choosing one.

## 5. Validation qualification

The thesis explicitly says the membrane heat-flux model differs from experimental values by up to 11%, that the cause was not identified, and that the experimental temperature range does not match the range used for extracting the case-study results. The later critical evaluation reiterates the up-to-11% error. It is therefore more precise to call this a model checked against experimental heat-flux data with a reported discrepancy, not a fully validated system model.

## 6. Reproduction implications for Research 2

Before using Wyon as a numerical benchmark:
1. Reproduce the 60 kg/s heat-exchanger feed and 80-module configuration.
2. Reproduce the heat-exchanger NTU/effectiveness calculation and the selected HX assumptions.
3. Reproduce the DCMD surface-temperature iteration and mass-flux relation with the stated initial and final module geometries distinguished.
4. Reproduce pump pressure drops and selected pump operating points.
5. Match the experimental validation temperature range before computing validation error; then separately quantify extrapolation to the case-study range.
6. Reproduce annual product and feed quantities under both 0.96 and 0.95 availability assumptions.
7. Report seawater intake, freshwater product, brine flow, outlet temperature, chemicals, post-treatment, and auxiliary electricity independently.
8. Keep the counterfactual freshwater displacement question separate: produced water is not automatically an equal volume of freshwater conserved unless it displaces a specified marginal freshwater source and its associated treatment/distribution burdens.

## Source locations in the thesis

- Case study and stream flow: pp. 11–12 (PDF pp. 20–21).
- Heat exchanger and DCMD model: pp. 13–17 (PDF pp. 22–26).
- Pump sizing and operating power: pp. 17–18 (PDF pp. 26–27).
- Annual production and seawater requirement: p. 18 (PDF p. 27).
- Production, electricity and cost results: pp. 22–28 (PDF pp. 31–39).
- Environmental impacts and thermal discharge: pp. 34–35 (PDF pp. 43–44).
- Critical evaluation and 95% availability statement: p. 36 (PDF p. 45).
