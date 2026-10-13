# Ali et al. (2020) held-out-flow flux-law diagnostic

**Source:** Ali, Orfi & Najib (2020), PLOS ONE, DOI [10.1371/journal.pone.0230207](https://doi.org/10.1371/journal.pone.0230207).  
**Run:** [Ali data ingestion run #17](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38429359577).  
**Artifact:** `ali-2020-dynamic-dcmd-source-data`, ID `11830272697`, SHA-256 `e0237d13ef46bbb703a8503630b27cc0bad1a1ba62981be70bff635069e03320`, expires 2027-01-11.  
**Input:** 16 source-linked steady-state S1 observations; input ledger SHA-256 `87e338a4ac7868d380d6948025ff83b50061212894bb1c35dcf193ac4d363e27`.

## Split and models

- Development flows: 50, 100, and 200 L/h (12 observations).
- Held-out flow: 300 L/h (4 observations).
- Fixed model: one permeance fit on development flows, with TPC fixed at 0.8.
- Alternative: permeance plus a bounded logistic TPC function of log flow, fitted on the same development rows.
- Two feed-salinity interpretations are reported separately: article-stated 0.5% (5 g/kg) and the S1 TDS_E column as a lower-salinity proxy. The source inconsistency is not resolved by this analysis.

## Results

| Salinity interpretation | Model | Train MAE | Held-out MAE | Held-out RMSE | Held-out MARE |
|---|---|---:|---:|---:|---:|
| 0.5% stated salinity | Fixed TPC=0.8 | 0.274 | 0.828 | 0.861 | 73.93% |
| 0.5% stated salinity | Flow-dependent TPC | 0.069 | 0.181 | 0.214 | 17.33% |
| TDS_E proxy | Fixed TPC=0.8 | 0.273 | 0.825 | 0.858 | 73.64% |
| TDS_E proxy | Flow-dependent TPC | 0.062 | 0.210 | 0.284 | 17.15% |

<text>Flux errors are in kg m⁻² h⁻¹; MARE is mean absolute relative error.</text>

The fixed-TPC model underpredicts the 300 L/h observations with a held-out bias of approximately −0.828 kg m⁻² h⁻¹ under the 0.5% interpretation. The flow-dependent model substantially improves the held-out result, but it uses three fitted parameters and only four held-out observations from the same source study. Under the TDS_E proxy, the fitted permeance reaches the configured upper bound of 200 kg m⁻² h⁻¹ bar⁻¹; that boundary solution is a warning about parameter identifiability and source-property ambiguity.

## Interpretation and limits

This is a **model-form diagnostic**, not a publication-grade validation result. It only tests the vapor-pressure flux submodel against a source-derived steady-state ledger. It does not validate the dynamic outlet-temperature ODEs, channel energy balance, membrane conduction, pumping, cooling, or net-water accounting. TPC is not measured in the source and the flow-dependent form was selected as an exploratory alternative. No claim of novelty is warranted: the source paper itself publishes a dynamic DCMD model.

The default dynamic reconstruction also failed a physical admissibility check for the source geometry at 50 L/h and a 60/25 °C inlet step: the numerical solver returned an outlet below the inlet/initial-state temperature envelope. The implementation now rejects such trajectories. This failure remains a blocking model-reconstruction issue rather than something to be tuned away with held-out data.
