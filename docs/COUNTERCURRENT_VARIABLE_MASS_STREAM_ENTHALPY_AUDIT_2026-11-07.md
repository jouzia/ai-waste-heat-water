# Counter-current variable-mass stream enthalpy audit (2026-11-07)

## Scope

This audit follows the counter-current duration-invariance correction and the numerical water/salt/interface-energy conservation tests. It examines a separate question: whether the channel bulk-temperature marching equations constitute complete stream enthalpy balances when water crosses the membrane and both channel mass-flow rates change.

This is a model-form audit, not a claim that the current temperatures are experimentally wrong. The current equations are a reduced sensible-heat approximation. Their validity as an approximation must be stated separately from a full variable-mass enthalpy closure.

## Implemented equations

In `src/ai_water/md_channel_countercurrent.py`, the feed-forward sweep uses

```text
T_f,out = T_f,in - Q_feed / (m_dot_f,in cp_f)
m_dot_f,out = m_dot_f,in - m_dot_v
```

and the permeate-backward sweep uses

```text
T_p,out = T_p,in + Q_feed / (m_dot_p,in cp_p)
m_dot_p,out = m_dot_p,in + m_dot_v
```

where the implementation converts `q_w` in W to kJ/h using the factor 3.6. The co-current implementation in `md_channel.py` uses the analogous sensible-temperature updates and updates mass flow separately.

At the membrane interface, the solver closes

```text
Q_feed = Q_latent + Q_conductive
Q_permeate = Q_feed
```

per cell. The reporting-duration multiplier is applied to integrated water and heat quantities, not to steady-state temperatures or flow rates.

## What is established

- Water mass conservation is tested independently from the solver's temperature updates.
- Salt mass conservation is tested through the concentrate stream and cellwise feed salinity.
- The local membrane-interface heat balance is tested against feed-side, permeate-side, latent, and conductive terms.
- Integrated duty is tested against the sum of latent and conductive duties.
- These tests establish internal numerical invariants for the implemented reduced-order equations.

## What is not established

The current tests do not establish a complete enthalpy balance for either bulk stream. In particular, they do not independently evaluate the enthalpy carried across the membrane by the transferred water, with a consistent liquid/vapour reference state, and reconcile that term with the bulk stream enthalpy changes.

When `m_dot` changes across a cell, a full stream balance must be written in enthalpy-flow form rather than inferred solely from `Q/(m_dot cp)`. The required bookkeeping must identify:

1. the feed and permeate specific-enthalpy reference states;
2. the enthalpy of transferred water at the membrane-side state, including the phase-change contribution;
3. whether the latent term in the interface balance is defined relative to liquid water at the feed interface, permeate interface, or another stated reference temperature;
4. conductive heat transfer as a separate energy flux, counted exactly once;
5. the composition dependence of feed enthalpy and heat capacity as salinity changes; and
6. the direction-specific inlet and outlet mass-flow states in counter-current cells.

The present configuration uses constant user-supplied heat capacities and a specified latent heat. Those assumptions can support a transparent reduced-order closure, but do not by themselves define the transferred-water enthalpy reference or demonstrate exact variable-mass stream enthalpy conservation.

## Required equations before a solver change

For each cell, write explicit steady control-volume balances using one common enthalpy datum. In generic form:

```text
feed-side enthalpy in
  = feed-side enthalpy out
  + transferred-water enthalpy flux
  + conductive heat crossing the membrane

permeate-side enthalpy out
  = permeate-side enthalpy in
  + transferred-water enthalpy flux
  + conductive heat entering the permeate side
```

The transferred-water enthalpy flux must be defined consistently for vapour leaving the feed side and entering/condensing into the permeate side. The latent heat already used in the interface closure must not be added a second time. The two stream balances and membrane balance must sum to a global energy identity with no duplicated or missing latent/conductive term.

Only after the reference-state convention is fixed should the temperature updates be derived from the mass-weighted enthalpy equations. The implementation should then expose per-cell enthalpy residuals and test (a) zero-flux recovery, (b) nonzero permeation, (c) duration invariance, (d) feed/permeate flow reversal for counter-current indexing, and (e) global energy closure.

## Decision

Do not change the bulk-temperature solver in this audit. Do not describe the existing interface-energy tests as proof of complete stream enthalpy conservation. Retain the current equations as the documented reduced sensible-heat approximation pending an explicit transferred-water enthalpy convention and a derivation of the corresponding finite-volume equations.

This is a model-definition gap, not a failed CI check and not evidence that the membrane-interface energy closure is numerically inconsistent.
