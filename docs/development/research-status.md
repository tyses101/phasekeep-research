# Research status and evidence classes

**Status: working development record, 2026-11-27.**

This page separates five things that are easy to confuse. A statement on any development page belongs to exactly one of them.

## The five levels

| Level | Question it answers | Current state |
|---|---|---|
| 1. Mathematical derivation | Does the result follow from the stated assumptions? | Many results, all inside stated ideal or Pauli-noise models. |
| 2. Computational validation | Does a program reproduce the derived numbers? | Eleven checkpoint programs, run author-side from clean copies. No independent reproduction yet. |
| 3. Proposed architecture | What could be built, in what roles? | Buddy (open), IQA (provisional), PALADIN, Docked Scheduling, shared ancillary hosting: proposals only. |
| 4. Unresolved physical feasibility | Can the required gates, readout and loss budgets exist? | **Unresolved.** V1.0 identifies probabilistic photon-photon gates and undetected loss as the bottlenecks. |
| 5. Hardware measurement | Has anything been measured on a device? | **None.** |

A modelled improvement is not a physical advantage. Every table of probabilities on these pages is a calculation under assumed fault rates, not an observation.

## Evidence classes

| Class | Meaning here |
|---|---|
| [DERIVED] | Follows from the stated model by mathematics, and was checked by a program. Says nothing about whether the model is physical. |
| [ASSUMED] | A noise value, gate set, workload or hosting arrangement chosen as an example, not measured. |
| [PROPOSED] | A design idea or name, not tested or demonstrated. |
| [UNVERIFIED] | A claim or source not yet checked against its full text or by anyone other than the author. All literature on these pages is UNVERIFIED unless a page says otherwise. |
| [MEASURED] | Reserved for project hardware measurements. None exist. |
| [BLOCKED] | Cannot proceed without missing evidence or capability. |

The frozen library also uses REPORTED (a result stated by a cited source, with its reading scope recorded) and SIMULATED (output of a model). The checkpoint pages fold simulation into DERIVED or ASSUMED, and say which.

## Rules the checkpoints follow

- Gate counts, weights, photon spans and similar counts are *structural proxies*, not costs. Physical cost fields stay empty (audit item A02).
- No combined score is formed across incompatible units. Where a choice is shown, it is a feasible set and a Pareto set over separate metrics.
- The conventional local round is kept as the baseline in comparisons; the joint geometry is never presented as a replacement.
- Negative results and mistakes are kept on the page that found them, and in [Errata](errata.md).
- A passing program shows numerical consistency inside the model. It does not show physical validity, hardware feasibility or superiority.
