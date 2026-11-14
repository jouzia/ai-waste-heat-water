# DCMD heat-transfer-coefficient uncertainty propagation

**Experiment ID:** `DCMD-HTC-UNCERTAINTY-PROPAGATION-2026-11-07`  
**Status:** Completed 600-scenario numerical stress test; archived artifact independently inspected on 2026-11-14.  
**Code:** PR [#106](https://github.com/jouzia/ai-waste-heat-water/pull/106), merged 2026-11-12 as `33a4d7c74dd32be4be26141987ccb83cb2fe1d1a`.

## Objective

Quantify how independent feed- and permeate-side heat-transfer-coefficient (HTC) perturbations propagate through the reduced-order counter-current DCMD channel model to outlet temperatures, freshwater production, hot-side thermal demand, latent duty, and conductive heat leak.

This is a deterministic factorial stress test. It is not a probabilistic uncertainty analysis and does not validate the underlying HTC correlation.

## Design

- 12 operating points: feed inlet temperatures 40, 50, 60, and 70 °C crossed with feed Reference Salinities 15, 35, and 38 g/kg.
- Permeate inlet temperature: 20 °C.
- Energy-balance modes: `sensible_cp` and `wyon_enthalpy`.
- Feed HTC and permeate HTC varied independently at factors 0.50, 0.75, 1.00, 1.25, and 1.50 relative to 500 W m⁻² K⁻¹.
- 25 HTC pairs per operating-point/mode block; 24 blocks; 600 simulations total.
- 80 finite-volume cells, the finest mesh used in the completed extended mesh study. This is a finest-mesh reference, not exact truth.
- Other numerical inputs held fixed: membrane area 0.23088 m²; permeance 100 kg m⁻² h⁻¹ bar⁻¹; latent heat 0.67 kWh kg⁻¹; membrane conductivity 0.0551 W m⁻¹ K⁻¹; thickness 110 μm; feed and permeate inlet mass flows 600 kg h⁻¹; heat capacities 4.18 kJ kg⁻¹ K⁻¹; duration 1 h; counter-current arrangement; concentration polarization disabled.

The nominal comparison for each operating point and energy mode is the 1.00/1.00 HTC pair. Temperature changes are reported as absolute °C; percentage changes are not computed for Celsius values.

## Artifact audit

The archived artifact contains:
- `htc_uncertainty_propagation.csv`: 600 data rows;
- `summary.json`: mode-specific extrema;
- `manifest.json`: design metadata and SHA-256 checksums.

Independent inspection confirmed:
- 600 rows and 600 unique scenario keys;
- 12 operating points and both energy modes (300 rows each);
- 24 complete operating-point/mode blocks, each containing all 25 HTC pairs;
- all 600 solver statuses are `success`;
- all numeric outputs are finite;
- nominal baseline rows exist for all 12 points in each mode;
- CSV and summary checksums match the manifest.

## Results

Ranges below are extrema across all 300 scenarios within each energy-balance mode, relative to that mode's corresponding nominal HTC baseline. These extrema may occur at different operating points and HTC pairs.

| Output | `sensible_cp` range | `wyon_enthalpy` range |
|---|---:|---:|
| Freshwater production | −43.096% to +33.009% | −43.108% to +33.032% |
| Hot-side thermal demand | −41.968% to +31.827% | −42.005% to +31.895% |
| Latent duty | −43.096% to +33.009% | −43.108% to +33.032% |
| Conductive heat leak | −41.609% to +31.331% | −41.640% to +31.388% |
| Feed outlet temperature | −0.954 to +1.257 °C | −0.947 to +1.247 °C |
| Permeate outlet temperature | −1.253 to +0.950 °C | −1.235 to +0.936 °C |

The two energy-balance modes produce similar HTC-response envelopes for this fixed numerical configuration. This is a robustness observation for the tested setup, not evidence that the modes are interchangeable in general.

## Interpretation

The tested HTC factors materially affect predicted freshwater production and thermal duties. In this model configuration, the full illustrative stress-test envelope spans approximately −43% to +33% for freshwater production and approximately −42% to +32% for hot-side thermal demand relative to nominal HTC.

The result supports explicitly reporting HTC assumptions and testing their influence rather than presenting one nominal prediction as insensitive to heat-transfer closure. It does not establish that the factor range is empirically plausible, that all combinations are physically correlated or attainable, or that any scenario has a particular probability.

The experiment propagates HTC variation through the reduced-order channel model using prescribed coefficients. It does **not** independently validate the hydrodynamic correlation used to obtain those coefficients, nor does it validate membrane permeance, vapour-pressure relations, thermodynamic properties, or the complete data-centre-to-water system. Concentration polarization is disabled, and the operating points are controlled numerical scenarios rather than a reproduction of a specific experiment.

## Reproducibility record

- Successful dedicated PR workflow: [run 42489865207](https://github.com/jouzia/ai-waste-heat-water/actions/runs/42489865207)
- Workflow head commit: `395fa3f5fff429e7083b87e9b4f0232e80e72ebb`
- Job: `128759679962` (`htc-uncertainty`, success)
- Artifact ID: `13621459958` (90-day retention; expiry 2027-02-06)
- Artifact SHA-256: `76169eaedf4152e0f4b0907aee80d09da72f2c6f6655773a67f8007c56fd3706`
- CSV SHA-256: `9f6c258d3887fd2dafae534bc7ff25c25e319fdf0c9f2d0b107f943a6341213a`
- Summary SHA-256: `983d951557f5c085bf9a8a8ad20bce05da96d71610e4808915165618c20279d3`
- Manifest SHA-256: `1668c4e69800f90454731a2a55d60cdcbf2e1171ef71424e8e4341e6f542d064`

The dedicated workflow triggered again on the merge commit was cancelled; the successful PR-head run above is the completed 600-case run for the merged implementation. On merge commit `33a4d7c`, repository CI, GDR validation, both enthalpy mesh workflows, sensible-versus-Wyon sensitivity, Nayar-versus-Wyon sensitivity, and Villa nominal-area sensitivity all completed successfully.

## Manuscript placement

Report this as a parameter-sensitivity/stress-test result in the uncertainty section. Do not describe it as a measured HTC uncertainty distribution, a Monte Carlo probability interval, an experimental validation, or a net-water-impact result. The system-level net-water analysis still requires its separate source-backed cooling, pumping, electricity-water, and displacement inputs.
