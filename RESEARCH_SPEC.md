# Research Specification

## Primary question
Under what combinations of AI workload intensity, data-center thermal conditions, waste-heat recovery efficiency, membrane-distillation operating conditions, cooling requirements, electricity-water intensity, and geographic water stress can waste-heat recovery produce a positive net freshwater benefit?

## Objectives
1. Build a transparent AI-workload-to-water model.
2. Parameterize it from peer-reviewed literature and documented datasets.
3. Include cooling, pumping, auxiliary electricity, and water accounting.
4. Determine break-even and failure regimes.
5. Quantify uncertainty and sensitivity.
6. Evaluate geographic variation.
7. Validate equations and selected literature cases.
8. Publish a reproducible research package.

## Hypotheses
- H1: Higher recoverable heat temperature expands the feasible MD operating envelope.
- H2: More AI workload generally increases heat availability, but not necessarily net water benefit.
- H3: Cooling can materially reduce or eliminate gross benefit.
- H4: Geography and electricity-water intensity materially affect results.
- H5: Integrated thermal-hydraulic optimization can improve water efficiency.
- H6: Results form a feasibility envelope rather than a universal threshold.

## Validation hierarchy
1. Unit/equation tests.
2. Literature reproduction.
3. Qualitative behavior and sensitivity checks.
4. Selected physical measurements where feasible.

A prototype will not be treated as industrial-scale proof without scaling justification.
