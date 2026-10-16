# Secondary benchmark source audit — Keshavarzzadeh (2020), Figure 3

**Audit date:** 2026-10-16  
**Status:** First-pass figure digitization completed (40 marker estimates); independent repeat extraction and unit/series audit remain outstanding. This is not yet an admissible validation dataset.

## Source

Keshavarzzadeh, A. H. (2020). “Design and bio-inspired optimization of direct contact membrane distillation for desalination based on constructal law.” *Scientific Reports*, 10, 16790. DOI: https://doi.org/10.1038/s41598-020-73964-7. Open-access PDF: https://www.nature.com/articles/s41598-020-73964-7.pdf. The article is CC BY 4.0, subject to the article's third-party-material qualifications.

## Verified by inspecting the uploaded PDF and actual Figure 3 image

- The validation paragraph attributes the experimental comparison to Martínez-Díez and Vázquez-González (1999), reference 37.
- Figure 3 compares water mass flux against average feed bulk temperature, (T_{b1}), which the text defines as the average of feed-channel inlet and outlet bulk temperatures.
- Panel (a) is (Q=7\,\mathrm{cm^3/s}); panel (b) is (Q=11\,\mathrm{cm^3/s}).
- The four stated NaCl concentrations are 0, 0.55, 1.15, and 1.67 mol/L.
- The figure caption says symbols are experimental data and lines are model results. The first-pass CSV is intended to capture symbol locations only.
- The text describes the original membrane as PTFE, with 80% void fraction and 60 μm thickness.

## First-pass digitization artifact

- CSV: `04_experiments/literature_benchmarks/MD-DCMD-MARTINEZ-1999_SECONDARY-FIG3_first_pass.csv`
- 40 estimated marker locations: 2 panels × 4 concentration series × 5 points.
- Coordinates are pixel estimates on a 3× raster render of PDF page 6. Axis calibration uses the visible tick labels in each panel and a linear fit.
- Raster crop SHA-256: `f351ce4ea1f7cd27aea4359266a6e17c0feac6d383f37793327235304a452c2d`
- The cropped figure image was created from the user-provided open-access PDF. It is available in the current conversation as `MD-DCMD-Keshavarzzadeh2020-Fig3-crop.png`.
- Provisional extraction uncertainty: ±0.7 K and ±0.06 in plotted flux units. These are working estimates, not measured confidence intervals.
- Flux-axis interpretation is provisional: the vertical label appears to plot (J_m\times10^3\,[\mathrm{kg\,m^{-2}\,s^{-1}}]); the CSV stores both plotted values and the corresponding (10^{-3}\) SI conversion. Confirm this reading before using the values in model scoring.
- Marker overlap and small symbol size make some nearby concentration series hard to distinguish in the first pass. The 1.15 M series is particularly provisional where stars and triangles nearly overlap. No independent second pass has been completed.
- Treat the file as a traceable *draft digitization*, not as final data and not as primary-source observations.

## Material source discrepancies / unresolved checks

1. **Pore-size discrepancy:** the 2020 validation paragraph reports “0.2 mm nominal pore size,” whereas the indexed description of the 1999 source reports 0.2 μm. This is a factor of 1,000 and may be a typographical/transcription error. Do not silently resolve it or use it to configure the model until checked against the primary source or another authoritative source.
2. **Figure-caption citation error:** visual inspection confirms that the Figure 3 caption points to reference 25 for the experimental symbols, but the validation paragraph points to reference 37 for Martínez-Díez and Vázquez-González. Reference 25 is a ground-source heat-exchanger optimization paper, while reference 37 is the 1999 membrane-distillation paper. This appears to be a real citation mismatch in the caption, not merely a text-extraction artefact.
3. **Axis calibration and units:** the image has temperature ticks from 290 to 330 K and plotted flux ticks from 0.5 to 3.5. The physical-unit interpretation is provisionally (10^{-3}\,\mathrm{kg\,m^{-2}\,s^{-1}}) per plotted unit and still requires an explicit second check.
4. **Operating conditions:** only average feed bulk temperature and recirculation rate are explicit in the figure/text inspected here. Do not invent permeate temperatures or other unreported boundary conditions.

## Next gate

Before using this benchmark for fitting or validation:
1. Independently digitize all points (preferably with WebPlotDigitizer or a second scripted/manual pass) and compare pointwise disagreement.
2. Verify the flux-axis multiplier and concentration-to-marker mapping, especially the overlapping 0.55 M and 1.15 M series.
3. Freeze the final secondary-source CSV and checksum; retain this first-pass file as an audit trail rather than silently replacing it.
4. Seek the 1999 primary paper or author-supplied data to verify membrane specifications and boundary conditions.
5. Keep this dataset separate from the primary observation ledger. Any eventual use must be labelled secondary-source-derived and must not be described as direct primary-source validation.

## Decision

Figure 3 can support a *provisional secondary-source benchmark candidate*, not independent validation of the project's model. The project's overall final gate remains INCOMPLETE.


## Color-assisted review pass — 2026-10-16

A second *review pass* was generated from the raster using color-separated marker detections plus manual review of the plotted symbols. It is not an independent extraction because it uses the same figure image and same analyst workflow.

- Review CSV: `04_experiments/literature_benchmarks/MD-DCMD-MARTINEZ-1999_SECONDARY-FIG3_review_pass.csv`
- First pass retained as audit trail: `04_experiments/literature_benchmarks/MD-DCMD-MARTINEZ-1999_SECONDARY-FIG3_first_pass.csv`
- The review pass contains 40 approximate marker centres and pixel coordinates. Its flux values remain in plotted-axis units; do not interpret them as final SI observations.
- This review exposed that several first-pass series assignments were too rough. The review CSV is the current provisional extraction, but close marker overlap—especially between the 0.55 M and 1.15 M series—still requires independent extraction.
- No fit, model score, or physical-validation claim is admissible from either CSV at this stage.
