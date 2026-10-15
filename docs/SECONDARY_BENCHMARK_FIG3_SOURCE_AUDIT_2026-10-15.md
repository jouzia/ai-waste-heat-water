# Secondary benchmark source audit — Keshavarzzadeh (2020), Figure 3

**Audit date:** 2026-10-15  
**Status:** Figure metadata verified from the open-access PDF text; numerical digitization not yet performed.

## Source

Keshavarzzadeh, A. H. (2020). “Design and bio-inspired optimization of direct contact membrane distillation for desalination based on constructal law.” *Scientific Reports*, 10, 16790. DOI: https://doi.org/10.1038/s41598-020-73964-7. Open-access PDF: https://www.nature.com/articles/s41598-020-73964-7.pdf. The article is licensed CC BY 4.0, subject to the article's third-party material qualifications.

## Verified from the accessible article text

- The validation section says the experimental data were reported by Martínez-Díez and Vázquez-González (1999), cited there as reference 37.
- Figure 3 compares mass flux (J_m) against (T_{b1}), described as the average of the feed-channel inlet and outlet bulk temperatures.
- Panels correspond to recirculation rates (Q=7) and (Q=11) cm³/s.
- The four stated NaCl concentrations are 0, 0.55, 1.15, and 1.67 mol/L.
- The caption says symbols represent experimental data and lines represent the 2020 model results. Only symbols may be digitized as observations.
- The article describes the original membrane as PTFE, with 80% void fraction and 60 μm thickness.

## Material source discrepancies / unresolved checks

1. **Pore-size discrepancy:** the 2020 paper's validation paragraph reports “0.2 mm nominal pore size.” The 1999 publisher-indexed description available in the source audit reports 0.2 μm nominal pore size. These differ by a factor of 1,000. This could be a typographical or transcription error, but the discrepancy must not be silently resolved. Do not use this pore-size value to configure the model until the primary source or another authoritative source clarifies it.
2. **Figure-caption citation discrepancy:** the Figure 3 caption text surfaced by the PDF extraction says “experimental data25,” while the validation paragraph cites the Martínez-Díez and Vázquez-González paper as reference 37. The reference list must be inspected visually / against the publisher HTML to determine whether this is a layout/extraction issue or a source citation error. The plot should not be treated as source-secure until the attribution is confirmed.
3. **Flux-axis unit and calibration:** the article text calls the plotted quantity water mass flux but does not state the figure axis tick values or unit in the extracted text. Read the actual figure image and record exact axis calibration before digitization; do not infer units from other figures or from model equations.
4. **Operating conditions:** only the average feed bulk temperature is explicitly defined in the visible text. Do not invent permeate inlet/outlet temperatures or other unreported boundary conditions.

## Decision

The figure is a viable candidate for a secondary-source-derived benchmark, but not yet an admissible numerical dataset. The observation ledger remains empty until the actual image can be inspected, units and axis calibration verified, experimental-symbol series mapped, and an independent repeat extraction archived. Any eventual comparison must be labelled secondary-source-derived and must not be described as direct primary-source validation.
