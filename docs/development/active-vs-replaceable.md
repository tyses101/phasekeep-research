# Active-information versus replaceable-resource exposure

**Status: working development record, 2026-11-27. The gate counts below are DERIVED from the V1.0 circuit definitions by a post-V1.0 annotation ([A01](#traceability)); the interpretation is PROPOSED. Nothing is measured.**

:::plain In plain words
Not every failed operation is equally costly. If a failure only wastes a helper photon, it is like a spoiled sheet of scrap paper: replace it and try again. If it disturbs the photon that carries the actual information, it may be unrecoverable. This page counts, for each verification round, how many interactions touch the information and how many touch only helpers.
:::

## The engineering question

*Can we arrange the system so that unsuccessful operations predominantly consume replaceable resources rather than irreplaceable quantum information?*

A failed operation is not necessarily catastrophic. An **unrecoverable** failed operation is. That distinction may matter more than the raw success probability of the equipment.

## The counts [DERIVED]

Two-qubit gates per round in the V1.0 circuits, one ancilla qubit per ancilla photon (K = 1, destructive readout). A gate is *data-touching* if one of its two qubits is a data axis, and *ancilla-only* if both are ancilla qubits.

| Round | Total inter-photon gates | Touch data | Ancilla only |
|---|---|---|---|
| Local conventional | 4 | 4 | 0 |
| Joint conventional | 8 | 8 | 0 |
| Joint flagged | 12 | 8 | 4 |
| Joint verified cat | 18 | 8 | 10 |
| Joint cooperative, verified | 14 | 8 | 6 |
| ZZZZ only (partial joint) | 4 | 4 | 0 |

At *s* = 0.5, a round in which all eight data-touching gates must succeed completes with probability $0.5^8$ = 0.00390625, however many ancilla-only gates are added.

## What this does and does not say

- **Extra verification machinery adds ancilla-only gates, not data-touching ones.** Under the (ASSUMED) condition that an ancilla-only failure consumes only ancilla photons and leaves data untouched, those failures are the replaceable kind. The data-touching count stays at 4 for the local geometry and 8 for every full joint round.
- **The floor of 8 is the joint geometry's price**, set by the data-touching gates. Hosting several ancilla axes in one photon (a [hypothesis](physical-feasibility.md)) lowers the *total* count toward that floor; it cannot go below it.
- **Preparing resources ahead of demand does not remove the eight data-path gates**, because they act on the data when it is present. In the flagged round the flag gates are interleaved with the data couplings, so they are not offline-preparable either. Whether offline preparation of ancilla resources, as in the frozen DDQT inventory-based mode, could change where the *ancilla-only* failures occur is a **proposed research direction requiring source reconciliation**. No integration with DDQT is claimed.
- **A data-touching failure is not automatically destructive.** Whether it leaves the data intact (benign) or disturbs it is exactly what V1.0 leaves open. The counts above say how often the question arises, not what the answer is.
- **The count is of exposure events, not of damage.** The abort model in [V1.0](checkpoints/v1.0.md) is one assumption; a model in which data-touching failures are benign and retried gives attempt counts of 8 and 16 at *s* = 0.5 for local and joint conventional.

## Traceability

The totals match the V1.0 page's K = 1 column and its program output. The split was not part of the V1.0 package; it is [annotation A01](../../annotations/a01-active-exposure/count_gate_exposure.py), which reads the unmodified V1.0 program's circuit definitions and counts gates, with a [recorded execution](../../annotations/a01-active-exposure/execution-record.txt). It runs no new simulation, and it is author-side re-execution of an existing implementation, not independent reproduction.

## Limits

Gate-level behaviour of a real heralded gate is not modelled, and nothing about timing, correlated loss on shared photons or detector effects. The counts are structural, not costs.
