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
