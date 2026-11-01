# Research 2 scope decision under primary-source access constraint

**Decision date:** 2026-10-15  
**Project:** From AI Waste Heat to Water: A Net-Water-Impact Framework for Sustainable AI Infrastructure  
**Status:** Provisional scope control; empirical validation gate remains blocked.

## Decision

Do not hold all remaining work hostage to institutional access, and do not manufacture or infer experimental observations from article snippets. Run two parallel tracks:

1. **Source-recovery track:** continue checking lawful author-shared copies, institutional records, and explicitly secondary reproductions. A secondary transcription may be used only as secondary-source-derived evidence, with its own provenance and uncertainty.
2. **Evidence-bounded manuscript track:** continue reproducible model verification, accounting-boundary tests, sensitivity/convergence, break-even and failure-envelope scenarios, and open-dataset analyses. Frame these as methods, scenario analysis, and conditional decision support—not as independent physical validation or proof that the system yields net freshwater.

## Scope and claim rules

- The 1999 Martínez-Díez & Vázquez-González paper remains the intended primary DCMD benchmark, but its observation ledger must stay empty until values and operating conditions can be traced to a lawful source.
- The publisher-indexed abstract/article snippets establish bibliographic and selected textual facts, not a complete experimental dataset. Do not reconstruct unseen figure/table values from snippets.
- The 2000 paper by Martínez-Díez, Florido-Díaz, and Vázquez-González is a related publication, not automatically an interchangeable copy of the 1999 dataset. Do not merge or substitute it without checking the actual methods, runs, and overlap.
- The open-access Keshavarzzadeh (2020) study may support a crosswalk only where its source attribution and exact experimental conditions are inspectable. Its model reproduction is not primary data and is not independent validation of this repository.
- Report the current 16-observation, four-fold flow-level comparison only as within-source model-form evidence; report Sobol convergence only as numerical stability under illustrative input distributions.
- Keep Ali et al. transient mass-error metrics withdrawn while the meaning of the nonmonotonic `mw (kg)` field is unresolved. Do not treat outlet-temperature diagnostics as a substitute for mass validation.
- Keep geographic Aqueduct indicators as contextual basin-risk screening. Do not multiply risk scores into water volumes, and do not claim a site-specific electricity-water join until factors, boundaries, geography, and provenance are auditable.
- No positive net-water-benefit claim, deployment prediction, or “independently validated” claim is allowed unless the corresponding scientific gate passes.

## Minimum deliverables for the fallback manuscript

1. A reproducible counterfactual accounting specification that distinguishes withdrawals from consumption and gross product water from net operational blue-water impact.
2. Unit tests and conservation/boundary checks, with explicit handling of negative net benefit and physically inadmissible scenarios.
3. Reproducible sensitivity/convergence and break-even/failure-envelope analyses, with uncalibrated assumptions clearly marked.
4. Separate, provenance-preserving analyses of the open GDR/NREL and Ali datasets, retaining known limitations and excluding invalid mass metrics.
5. A complete limitations section, executable reproduction instructions, source manifest, and a claim-to-evidence table.
6. A final novelty audit against direct prior art before asserting a contribution.

## Source-recovery queue (no paid access)

- Publisher article record: https://www.sciencedirect.com/science/article/pii/S0376738898003494
- University of Málaga publication record: https://portaldelainvestigacion.uma.es/unidades/19959/colaboracion/investigador/4323908?lang=en
- ResearchGate record for the exact 1999 article: https://www.researchgate.net/publication/221910876_Water_Desalination_by_Membrane_Distillation (the page exposes the article abstract among related works; this is not confirmed full-text access)
- ResearchGate record for the related 2000 paper, which offers an author-request route but is not the same publication: https://www.researchgate.net/publication/233056529_Study_of_Polarization_Phenomena_in_Membrane_Distillation_of_Aqueous_Salt_Solutions
- Open secondary reproduction to inspect carefully: https://doi.org/10.1038/s41598-020-73964-7

## Exit criteria

The paper can be prepared for a methods/scenario-oriented submission only after its own reproducibility, source audit, accounting, prior-art, and manuscript-package gates are complete. It must be described as **not independently empirically validated** unless a defensible empirical validation route is completed. The project-level hard gate in `05_validation/FINAL_GATE_STATUS.yaml` remains authoritative and must not be manually forced to complete.


## New actionable source route found (2026-10-15)

The open-access Keshavarzzadeh (2020) article is available at https://www.nature.com/articles/s41598-020-73964-7 (also indexed at https://pmc.ncbi.nlm.nih.gov/articles/PMC7545101/). Its validation section explicitly says Fig. 3 compares model curves with experimental data attributed to Martínez-Díez & Vázquez-González (1999), with panels for 7 and 11 cm³/s and concentrations 0, 0.55, 1.15 and 1.67 M NaCl. This means the next source-recovery action is not merely a scenario-only pivot: digitize only the experimental symbols in that open-access figure into a separate secondary-source-derived ledger, preserve figure/axis/pixel provenance, and perform an independent repeat extraction. The model lines must not be treated as experimental observations.

This route can support a transparent **secondary-source-derived benchmark comparison**, not a claim that the original 1999 primary paper was directly inspected. The empty primary ledger and independent-validation gate stay unchanged until the primary evidence and boundary conditions are independently resolved.