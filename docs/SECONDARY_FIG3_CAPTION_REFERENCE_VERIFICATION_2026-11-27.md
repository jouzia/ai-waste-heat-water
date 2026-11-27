# Keshavarzzadeh (2020) Figure 3 provenance audit

**Audit date:** 2026-11-27  
**Scope:** source attribution, operating-condition cross-check, and dimensional consistency for the experimental symbols in Figure 3 of the open-access secondary source.  
**Decision:** the Figure 3 caption's reference 25 is most likely a typographical miscitation of reference 37, because the article's Validation section explicitly attributes the Figure 3 comparison to reference 37 and gives matching experimental conditions. This is strong internal corroboration, not primary-source verification. No observation or validation gate is promoted.

## Sources inspected

1. Keshavarzzadeh, A. H. (2020), “Design and bio-inspired optimization of direct contact membrane distillation for desalination based on constructal law,” *Scientific Reports* 10, 16790, DOI: 10.1038/s41598-020-73964-7.
   - Full-text PMC record: https://pmc.ncbi.nlm.nih.gov/articles/PMC7545101/
   - Publisher PDF: https://www.nature.com/articles/s41598-020-73964-7.pdf
   - Figure 3 image: https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a9e6/7545101/d0502dbd9939/41598_2020_73964_Fig3_HTML.jpg
   - Open access under CC BY 4.0, subject to the article's third-party-material qualifications.
2. Martínez-Díez, L. & Vázquez-González, M. I. (1999), “Temperature and concentration polarization in membrane distillation of aqueous salt solutions,” *Journal of Membrane Science* 156, 265–273, DOI: 10.1016/S0376-7388(98)00349-4.
   - Publisher record: https://www.sciencedirect.com/science/article/pii/S0376738898003494
   - The publisher-indexed article text is accessible as search-extracted text, but a verified full primary-source PDF/figure has not been obtained for this audit.

## Citation discrepancy and new corroboration

The 2020 article's Figure 3 caption says the symbols indicate experimental data and cites reference 25. Reference 25 is:

- Keshavarzzadeh AH, Maleki A, Gharali K, Dusseault MB. “Multi-objective evolutionary-based optimization of a ground source heat exchanger geometry using various optimization techniques.” *Geothermics* (2020) 86:101861. DOI: 10.1016/j.geothermics.2020.101861.

That is bibliographically unrelated to the DCMD benchmark.

However, the same 2020 article's Validation section explicitly says its model is compared against experimental data reported by Martínez-Díez and Vázquez-González, reference 37. It then identifies the same flat-sheet module with nine feed and nine permeate channels and describes Figure 3 as the comparison at feed flow rates of 7 and 11 cm³/s and NaCl concentrations of 0, 0.55, 1.15, and 1.67 molar. Those operating conditions match the publisher-indexed description of the 1999 paper's experiments, which reports flat PTFE membrane tests, nine feed and nine permeate channels, and flux results across different recirculation rates and salt concentrations.

The bibliography identifies reference 37 as the 1999 Martínez-Díez and Vázquez-González paper. Taken together, this makes a caption typo (25 instead of 37) the most likely explanation. It is no longer appropriate to describe the Figure 3 marker provenance as wholly unexplained. Nevertheless, without direct inspection of the 1999 primary figure or its underlying measurements, point-by-point identity and the exact origin of every plotted symbol are not independently confirmed.

## Dimensional inconsistency requiring care

The 2020 Validation paragraph gives the PTFE nominal pore size as **0.2 mm**. The publisher-indexed 1999 article's Experimental section gives **0.2 μm**. The latter is also consistent with the same 2020 article's earlier description of the membrane and with the 1999 source's reported membrane specification. The 2020 value is therefore a likely unit typo by a factor of 1,000; do not copy 0.2 mm into the project parameter record.

The 1999 source's publisher-indexed Experimental text also reports a 60 μm membrane thickness and 80% void fraction, consistent with the 2020 article's validation description. These cross-checks support the intended source attribution but do not substitute for the primary source.

## Evidence classification

- **Verified:** the 2020 Figure 3 caption cites unrelated reference 25.
- **Verified:** the 2020 Validation section explicitly attributes the experimental comparison to reference 37, the 1999 DCMD paper.
- **Strongly supported inference:** reference 25 in the Figure 3 caption is a typographical miscitation; reference 37 is the intended experimental benchmark.
- **Likely unit error:** 0.2 mm in the 2020 Validation paragraph should be 0.2 μm, based on the 1999 publisher-indexed Experimental section.
- **Not verified:** exact point-by-point provenance of the plotted markers against the primary 1999 Figure 1/2/3 or raw measurements; exact series mapping and uncertainty for each marker; whether all plotted points were transcribed without alteration.

## Implications for the repository benchmark

1. Keep the existing first-pass and colour-assisted 40-point CSVs unchanged as provisional secondary-source digitization artifacts.
2. Do not use either CSV for fitting, model scoring, or validation claims until the primary figure or measurements can be inspected and the extraction is independently repeated.
3. Keep the 1999 primary observation ledger separate and empty. Do not relabel secondary-source digitized points as primary observations.
4. Any future extraction from the 2020 Figure 3 must be labelled secondary-source-derived, preserve panel/pixel provenance, disclose the probable caption miscitation and pore-size unit typo, and distinguish graph-reading uncertainty from source measurement uncertainty.
5. A successful independent digitization would improve extraction reproducibility only; it would not by itself establish independent model validation.
6. Do not change `05_validation/FINAL_GATE_STATUS.yaml`. Source reconstruction, unfitted validation, held-out validation, and publication readiness remain blocked.

## Next admissible checks

- Continue seeking the primary 1999 article's original figures/tables or author-supplied data through lawful institutional or author-access routes.
- If primary evidence remains unavailable, retain the 2020 Figure 3 only as a secondary-source-derived sensitivity/extraction-quality artifact and exclude it from quantitative model evaluation.
- Do not infer or fabricate missing point values from the publisher-indexed prose or visual approximation.

## Reproducibility note

This audit combines direct inspection of the 2020 publisher PDF/PMC full text and Figure 3 with publisher-indexed text for the 1999 article. It is a source-attribution and dimensional-consistency audit, not a new point extraction, reconstruction of the primary experiment, or independent validation result.


## Independent secondary-source triangulation — Abdel-Rahman (2008)

A second, independently published DCMD modelling paper provides additional source-lineage evidence:

- Ali K. Abdel-Rahman (2008), “Modeling Temperature and Salt Concentration Distributions in Direct Contact Membrane Distillation,” *Journal of Engineering Sciences, Assiut University* 36(5), 1167–1188 (September 2008).
- Full PDF: https://jesaun.journals.ekb.eg/article_118726_da32ffe17fd391f214e6e2c75cb91678.pdf

The 2008 paper explicitly states in its Model Validation section that its numerical results are compared with the experimental results of Martínez-Díez and Vázquez-González [8]. It states that its Figure 2 plots the 1999 experimental permeate-flux data for **three recirculation rates**, expressed as feed/permeate average velocities of **25, 39 and 53 cm/s**, with distilled water as feed and a bulk temperature difference of **10 °C**. Its Figure 3 compares temperature-polarization coefficients against the same 1999 study. The 2008 reference list identifies [8] as Martínez-Díez and Vázquez-González, *Journal of Membrane Science* 156 (1999), 265–273; its shortened title omits the word “salt” but the authors, journal, volume, year and page range identify the same work.

The 2008 validation section also reports a 0.2 μm nominal pore size, 0.8 porosity and 0.6 × 10⁻⁴ m membrane thickness for its validation configuration. The publisher-indexed Experimental section of the 1999 paper independently reports the 0.2 μm pore size and 60 μm thickness. This triangulates the 2020 article's likely 0.2 mm unit typo; it is not evidence that the 1999 membrane was 0.2 mm.

### What this corroboration does and does not establish

- **Additional support:** the 1999 experiment was reused as an explicit experimental benchmark by a separate 2008 DCMD modelling study, not only by the 2020 paper.
- **Pure-water subset:** the 2008 paper's reproduced experimental series is for distilled-water feed at ΔT_b = 10 °C and three recirculation velocities. It is a secondary reproduction, not the primary 1999 figure or raw dataset.
- **Not a pointwise cross-check of the 2020 saline Figure 3:** the 2008 Figure 2 pure-water conditions do not match the 2020 Figure 3 NaCl concentration series. The 2020 paper's own Validation text remains the evidence tying its saline Figure 3 comparison to reference 37.
- **No new digitization:** no values were extracted from the 2008 Figure 2, and no values have been added to the repository observation ledger.
- **No primary-source recovery:** the original 1999 article's publisher-indexed text is accessible, but its original figure image/raw measurements have still not been obtained and independently inspected.

### Source locators

- 2008 article identification and description of prior 1999 experiments: PDF pages 1–3 (journal pages 1167–1169).
- 2008 validation against Martínez-Díez and Vázquez-González [8], three velocities, distilled-water feed, and ΔT_b = 10 °C: PDF page 11 (journal page 1177), lines 1394–1413 in the extracted text.
- 2008 Figure 2 labels and conditions: PDF page 12 (journal page 1178), lines 1433–1469.
- 2008 membrane properties (0.2 μm pore, 0.8 porosity, 60 μm thickness): PDF page 11 (journal page 1177), lines 1379–1385.
- 2008 bibliography entry [8]: PDF page 21 (journal page 1187), lines 2031–2034.

### Updated evidence classification

The Figure 3 caption's reference 25 is now best classified as a **high-confidence probable miscitation of reference 37**, because (i) the 2020 paper's own Validation section directly names reference 37 for the saline Figure 3 comparison and (ii) the 2008 paper independently uses the same 1999 experiment as a DCMD validation benchmark. It remains a probable caption error rather than a formally corrected publisher erratum. The precise marker-by-marker provenance of the 2020 saline series is still not independently verified.
