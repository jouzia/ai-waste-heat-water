# Keshavarzzadeh (2020) Figure 3 caption-reference verification

**Audit date:** 2026-11-27  
**Scope:** bibliographic verification of the Figure 3 experimental-symbol citation in the open-access secondary source.  
**Decision:** provenance discrepancy confirmed; no observation or validation gate is promoted.

## Direct source inspected

Keshavarzzadeh, A. H. (2020), “Design and bio-inspired optimization of direct contact membrane distillation for desalination based on constructal law,” *Scientific Reports* 10, 16790, DOI: 10.1038/s41598-020-73964-7.

- Full-text PMC record: https://pmc.ncbi.nlm.nih.gov/articles/PMC7545101/
- Figure 3 image: https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a9e6/7545101/d0502dbd9939/41598_2020_73964_Fig3_HTML.jpg
- Article metadata identifies the article as open access under CC BY 4.0, subject to the article's third-party-material qualifications.

## Verified citation mismatch

The article's Validation paragraph (PMC full-text lines 208–210) says the model is compared with experimental data reported by Martínez-Díez and Vázquez-González and cites reference 37.

The Figure 3 caption (lines 211–217) says the symbols indicate experimental data and cites reference 25.

The bibliography identifies:
- **Reference 25:** Keshavarzzadeh AH, Maleki A, Gharali K, Dusseault MB. “Multi-objective evolutionary-based optimization of a ground source heat exchanger geometry using various optimization techniques.” *Geothermics* (2020) 86:101861. DOI: 10.1016/j.geothermics.2020.101861.
- **Reference 37:** Martínez-Díez L, Vázquez-González MI. “Temperature and concentration polarization in membrane distillation of aqueous salt solutions.” *Journal of Membrane Science* (1999) 156:265–273. DOI: 10.1016/S0376-7388(98)00349-4.

Reference 25 is bibliographically unrelated to the stated DCMD experimental benchmark. This confirms a real internal citation mismatch in the secondary article. It does **not** establish whether the caption contains a typographical citation error or whether the plotted symbols have a different provenance. The mismatch must not be silently corrected by assuming reference 37 is certainly the source of every marker.

## Implications for the repository benchmark

1. Keep the existing first-pass and colour-assisted 40-point CSVs unchanged as provisional audit artifacts.
2. Do not use either CSV for fitting, model scoring, or validation claims while marker provenance, series mapping, and flux-axis interpretation remain unresolved.
3. Keep the 1999 primary observation ledger separate and empty until the primary source itself supplies traceable observations and operating conditions.
4. Any future Figure 3 extraction must be named secondary-source-derived, preserve panel and pixel provenance, and disclose this citation mismatch.
5. A successful independent digitization would improve extraction reproducibility only; it would not resolve the source citation or establish independent validation.
6. Do not change `05_validation/FINAL_GATE_STATUS.yaml`. Source reconstruction, unfitted validation, held-out validation, and publication readiness remain blocked.

## Next admissible checks

- Seek a direct primary-source figure/table or author-supplied data to verify the plotted experimental series.
- If that remains inaccessible, document the figure as an unresolved secondary-source candidate and exclude it from quantitative model evaluation.
- Continue the independent digitization protocol only as an extraction-quality exercise, with no model fitting or scoring until provenance and units are resolved.

## Reproducibility note

This audit is a bibliographic/source-attribution check based on the accessible PMC full text and the rendered Figure 3 image. It is not a new point extraction, a reconstruction of the 1999 experiment, or an independent validation result.
