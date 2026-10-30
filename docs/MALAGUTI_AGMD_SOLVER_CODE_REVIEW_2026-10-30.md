# AGMD Reference Solver Review: Root Admissibility and Test Scope (2026-10-30)

## Scope

Reviewed `src/ai_water/malaguti_agmd_reference.py` and `tests/test_malaguti_agmd_reference.py` on branch `research2/agmd-reference-solver-2026-10-27`. This is a code review of the isolated reference solver, not a source-validated reproduction.

## Confirmed strengths

- Property inputs are explicit caller arguments; the solver does not silently import provisional property correlations.
- Units are documented at the function boundary.
- It reports residuals for both coupled equations.
- It rejects non-finite and non-positive inputs and requires exactly one root under its current admissibility filter.
- The test fixture clearly labels the property values as provisional and distinguishes saline cold-channel water from pure distillate.

## Finding: root upper bound is not yet source-justified

The solver accepts only roots satisfying:

`minimum_delta_t_h_out_c <= delta_t_h_out <= delta_t_h_in_c`.

The SI text available in this audit specifies a minimum outlet terminal difference of 0.5 °C. It does not clearly establish the upper bound `delta_t_h_out <= delta_t_h_in` as a general mathematical constraint. The bound may be an intended operating-domain restriction, but it must not be encoded as a source-derived universal constraint without further textual evidence.

Recommendation: expose the admissibility interval as an explicit caller-supplied/model-policy choice or remove the upper bound from the generic solver. If retaining it for a specific Figure 4B case, label it as a case-specific assumption and test its effect.

## Finding: current tests are regression checks, not independent validation

The four expected recovery values are generated from the same provisional property set and the implementation's equations. These tests are useful to detect accidental code changes, but they do not independently validate the equation transcription, property values, or paper reproduction.

Recommendation: add independent algebra checks with hand-constructed inputs, direct residual substitution, and tests that distinguish no root, one admissible root, and multiple admissible roots. Keep figure-read anchor comparisons in a separate validation layer with digitization uncertainty.

## Finding: no alternate-initial-guess test is applicable to the current algorithm

The implementation uses polynomial root calculation, not an iterative nonlinear solver initialized from a starting guess. Therefore a “multiple initial guesses converge” test is not meaningful for this implementation. The relevant robustness test is enumeration and classification of all real roots, followed by admissibility filtering and explicit handling of zero, one, or multiple physical roots.

## Property-source update

The official MIT page confirms code version 3.1.5 dated 2024-08-07, while the publicly indexed property tables identify library version 3.1.3. The table PDF is therefore suitable only for carefully matched spot checks; it is not a version-matched validation oracle for v3.1.5. The official source page describes the separate function contracts: specific heat takes temperature, salinity, and pressure; latent heat takes temperature and salinity. Do not collapse these into a single generic property call.

Official references:
- https://web.mit.edu/seawater/
- https://web.mit.edu/seawater/Version_History_07Aug24-pdf-3a.pdf
- https://web.mit.edu/seawater/2017_MIT_Seawater_Property_Tables_r2b_2023c.pdf

## Decision

The isolated solver is a useful algebraic diagnostic, but the current admissible-root upper bound and regression-test interpretation require clarification. No production thermodynamics changes are warranted. The reproduction gate remains open.
