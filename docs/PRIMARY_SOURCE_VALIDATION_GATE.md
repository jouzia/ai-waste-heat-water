# Primary-source validation gate: Martínez-Díez & Vázquez-González (1999)

## Current state

The 1999 Journal of Membrane Science paper is now registered as a distinct primary-provenance benchmark. It reports flat-sheet TF200 PTFE experiments with 0, 0.55, 1.15 and 1.67 M NaCl feeds, and provides the module geometry used in the validation lineage.

## What is established

- Primary publication and DOI identified.
- Membrane and module geometry extracted.
- Experimental stability constraints recorded.
- Primary benchmark is separated from the 2020 secondary reproduction.
- No parameter fitting is permitted before the first model-vs-data run.

## What remains blocking

1. Extract the actual primary experimental flux observations.
2. Reconstruct the corresponding bulk temperature and recirculation conditions.
3. Crosswalk those observations against the markers reproduced in Keshavarzzadeh (2020).
4. Digitize only where the source does not provide machine-readable values.
5. Repeat a subset of digitization independently and quantify extraction uncertainty.
6. Run the current model without fitted parameters.
7. Report MAE, RMSE, bias and relative error where mathematically appropriate.
8. Lock the development/held-out split before any parameter calibration.

## Scientific rule

A literature statement that a published model agrees with an experiment is not validation of this repository's implementation. The repository must reproduce the experiment under source-matched conditions with parameters fixed before comparison.

## Source note

The primary paper explicitly states that the measured flux results cover different temperatures, recirculation rates and solution concentrations, and that experimental conditions were maintained tightly. These constraints should be preserved rather than replaced by convenient defaults.


## Extraction ledger requirement

The machine-readable observation template is:
`04_experiments/literature_benchmarks/MD-DCMD-MARTINEZ-1999_observations.yaml`

The ledger intentionally starts empty. A populated row is admissible only when its source locator, boundary conditions, unit transformation, and extraction method are recorded. Figure-derived observations require archived pixel coordinates, axis calibration points, and an independent repeat extraction. Missing experimental boundary conditions remain blocking rather than being filled with repository defaults.

## Validation sequence

```text
Primary source
    -> observation extraction
    -> provenance/unit audit
    -> independent extraction check
    -> frozen unfitted model
    -> first comparison
    -> development/held-out split
    -> calibration only on development cases
    -> final held-out evaluation
```

This sequence prevents the common failure mode of treating a published model-to-data agreement as evidence that a new implementation is validated.

## Access recovery attempt (2026-10-14)

A fresh search reconfirmed the publisher landing page and abstract for the 1999 article, including the TF200 PTFE membrane description, but did not surface a verified legally accessible full-text copy or a publisher-provided machine-readable observation table. Search results include secondary descriptions and the open-access 2020 reproduction; neither is a substitute for primary-source observations. The observation ledger therefore remains empty, and this gate remains blocked rather than being populated from a secondary model figure.

### Owner assistance required if institutional access is available

Please provide **one** of the following, only if you can access it legally:
1. the publisher PDF for Martínez-Díez & Vázquez-González (1999), DOI 10.1016/S0376-7388(98)00349-4; or
2. clear screenshots of the experimental results figures/tables plus the pages stating each corresponding operating condition.

Do not purchase the article just for this project if that is unaffordable. We can still complete a transparently downgraded methods/scenario paper if the primary data remain inaccessible, but it cannot be described as independently validated. If you upload a PDF, I can extract the relevant tables/figures, preserve page/figure locators, and build the observation ledger; you should not manually transcribe numerical values unless asked.

### Sources checked

- Publisher record and abstract: https://www.sciencedirect.com/science/article/pii/S0376738898003494
- Secondary open-access model/reproduction to be cross-walked, not substituted for primary data: https://doi.org/10.1038/s41598-020-73964-7
- University of Málaga researcher publication record: https://portaldelainvestigacion.uma.es/unidades/19959/colaboracion/investigador/4323908?lang=en

## Owner access unavailable — fallback route (2026-10-15)

The researcher reports that their college is not listed for institutional access. No paid access is required and no purchase is requested.

A fresh web search found the publisher's indexed article page with the abstract and portions of the article text (including the experimental setup description), but this is not equivalent to verified access to the complete paper and its figures/tables. The next work should proceed without asking the researcher to solve institutional access:

1. Extract only explicitly visible, source-attributed textual facts from the publisher-indexed page, recording the exact URL and section; do not infer unseen table values.
2. Search for a legally shared author manuscript or repository copy, and send a concise, polite request to the corresponding author if a public contact address can be verified.
3. Check whether a legally accessible secondary paper reports a clearly identified digitization or transcription of the same original experimental data. If so, label those values as **secondary-source-derived**, retain page/figure/table locators, and keep them separate from primary observations.
4. Continue the existing open-source GDR/NREL and Ali et al. analyses as separate evidence tracks. They can support a transparently downgraded paper, but they cannot be relabelled as validation against Martínez-Díez et al. (1999).
5. If the primary figures cannot be legally obtained, replace the planned primary-source validation claim with a limitation and a reproducible model-verification/scenario analysis. The publication gate must remain blocked for any claim requiring independent empirical validation.

No gate is passed by this fallback plan. This is a project-side task; the researcher does not need to find or pay for the paper.



## Additional access-route audit (2026-10-15)

The follow-up search did not establish a verified free full-text copy of the exact 1999 article. It did identify:
- The University of Málaga publication record listing the 1999 article, but no verified full-text file on the surfaced record.
- A ResearchGate page for a related 2000 article, *Study of Polarization Phenomena in Membrane Distillation of Aqueous Salt Solutions*, with an author-request option. This is a related publication, not proof that the 1999 observations are identical or that it can replace the 1999 source.
- The publisher-indexed 1999 article text provides selected setup details and descriptive claims, but no verified complete observation table or figure set suitable for source-audited digitization.

Accordingly, the source-recovery track remains open and the primary observation ledger remains empty. The parallel fallback scope is documented in [RESEARCH2_SCOPE_DECISION_PRIMARY_ACCESS_2026-10-15.md](RESEARCH2_SCOPE_DECISION_PRIMARY_ACCESS_2026-10-15.md). The study may proceed as a reproducible methods/scenario analysis only if its remaining gates pass; it must not be described as independently empirically validated without a defensible validation dataset.


## Secondary-figure extraction route identified (2026-10-15)

A full open-access article is available at https://www.nature.com/articles/s41598-020-73964-7 and its PubMed Central record https://pmc.ncbi.nlm.nih.gov/articles/PMC7545101/. Keshavarzzadeh (2020), *Scientific Reports* 10, 16790, explicitly states that its Fig. 3 compares model curves with experimental symbols attributed to Martínez-Díez & Vázquez-González (1999), for feed concentrations 0, 0.55, 1.15 and 1.67 M NaCl and recirculation rates of 7 and 11 cm³/s. This is a concrete, lawful secondary-source figure route, even though it is not the primary article.

**Permitted next step:** digitize the experimental symbols from the open-access secondary paper's Fig. 3 into a separate ledger, named and tagged as *secondary-source-derived digitization of data attributed to Martínez-Díez & Vázquez-González (1999)*. Archive the figure image, exact panel, axis calibration points, pixel coordinates, digitization software/version, extraction uncertainty, and an independent repeat extraction. Cross-check figure axes, temperature definition, concentrations, and flow rates against the primary publisher text. Keep this ledger separate from the empty primary-source ledger.

**Not permitted:** silently relabel secondary-digitized points as directly extracted primary data; infer missing operating conditions; treat the 2020 model curve as experimental data; claim that this route resolves all primary-source questions; or fit model parameters before the frozen unfitted comparison.

This improves the fallback evidence route but does not by itself pass the primary-source, independent-validation, or publication gate.

## Secondary-source figure audit findings (2026-10-15)

The open-access Keshavarzzadeh (2020) PDF text confirms Fig. 3 panels for 7 and 11 cm³/s and NaCl concentrations 0, 0.55, 1.15 and 1.67 M; the plotted x-variable is average feed bulk temperature, defined as the mean of feed inlet and outlet bulk temperatures. This confirms a candidate source route, not numerical observations.

The audit found two material unresolved discrepancies before digitization: (1) the 2020 validation paragraph says nominal pore size 0.2 **mm**, while the indexed 1999 source description says 0.2 **μm** (a factor of 1,000); and (2) the Figure 3 caption's extracted superscript citation appears as reference 25, while the validation paragraph cites the 1999 source as reference 37. The plot's flux-axis units and calibration also remain unverified from text alone. These discrepancies are documented in [SECONDARY_BENCHMARK_FIG3_SOURCE_AUDIT_2026-10-15.md](SECONDARY_BENCHMARK_FIG3_SOURCE_AUDIT_2026-10-15.md).

**Current decision:** do not populate either observation ledger yet. Numerical digitization requires visual inspection of the actual Figure 3 image, confirmation of its axis units and symbol-series mapping, and a documented independent repeat. Do not configure the model using the disputed pore-size value.
