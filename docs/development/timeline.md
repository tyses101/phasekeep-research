# Timeline: V0 to V1.0

**Status: working development record, 2026-11-27.** Eleven checkpoints, in the order they were produced. Each original is preserved unchanged; later corrections are in [Errata](errata.md). All checks are author-side.

## The whole sequence at a glance (consolidated, 2026-11-28)

This is the single timeline from the first library edition to today. Detailed tables for each series follow below, unchanged.

| Date | Stage | What it is | Where |
|---|---|---|---|
| 2026-11-26 | Learning library, Edition 02 → Edition 03 (revisions a to h) | Plain-language book series; Revision H frozen, including its vocabulary | [Library](../../library/markdown/00-start-here.md), Appendix 6 |
| 2026-11-27 | Computational checkpoints V0 to V1.0 | Tetragon geometry, then Buddy verification and physical feasibility | Table below |
| 2026-11-27 | Exploration pack S01 to S31 | Idle faults, continuity geometry, logical handoff, adaptive policies (exploratory, not V1.1) | [Consolidated review](../../explorations/consolidated-review.md) |
| 2026-11-27 | QDE, QIJ and ASV documentation checkpoint | Relationships as a research framework | [Checkpoint](checkpoints/qde-2026-11-27.md) |
| 2026-11-27 | Optical constraints and pending terms | Linear-optics limits, contextuality and discord notes, PK-LMI, VOM | [QDE framework](qde-relational.md) |
| 2026-11-28 | Atomic-register update | From photons to atoms: four-atom ring, echo control, imperfection maps, platforms | [Checkpoint](checkpoints/atomic-register-2026-11-28.md) |
| 2026-11-28 | Consolidation and Edition 04 (working draft) | One-page story, consolidated indexes, new volumes 15 onward | [PhaseKeep from the beginning](phasekeep-from-the-beginning.md) |

## Computational checkpoints V0 to V1.0

| Checkpoint | Question | Main finding (inside its model) | Checks |
|---|---|---|---|
| [V0](checkpoints/v0.md) | What moves a Tetragon between entangled states and bases? | Single-axis operations reach 4 of 24 Bell relabellings; every product-to-entangled basis change needs an entangling gate | four-part program |
| [V0.1](checkpoints/v0.1.md) | Does entanglement persist usefully; what does switching encodings cost? | Persistence inside an entangled class is plain single-qubit composition; switching between product and entangled encodings always costs an entangling gate | seven parts |
| [V0.2](checkpoints/v0.2.md) | Does a free output geometry change the cost of a logical gate? | Only logical X gains; for one qubit adaptive switching cannot beat the fused baseline | nine parts |
| [V0.3](checkpoints/v0.3.md) | How much does leakage bias verification; how many equivalent routes exist? | Leakage bias bounded; redundancy exists for phase gates, not for X or H in the diagonal encoding | eleven parts |
| [V0.4](checkpoints/v0.4.md) | What does a Buddy parity check detect and miss? | Detects flips, misses phase errors; can lower reliability when its own faults are not small | 26 |
| [V0.5](checkpoints/v0.5.md) | Repeated checks, reusable ancilla, routers | Spacing matters; silence is not PASS; checking every segment can accept fewer correct runs | 33 |
| [V0.6](checkpoints/v0.6.md) | Is a check compatible with how the gate is built? | Implementation decides compatibility; commuting with the check is the necessary condition for concurrency | 33 |
| [V0.7](checkpoints/v0.7.md) | What is verified; do local checks survive across registers? | A PASS confirms only the checked property; a wrong-angle controlled phase passes | 33 |
| [V0.8](checkpoints/v0.8.md) | Local versus joint geometry, and conversion | Conversion costs 2 inter-photon gates; joint checks do not close the relative-phase gap; adaptive switching is workload-dependent | 48 |
| [V0.9](checkpoints/v0.9.md) | How reliable is the verifier itself? | Flagged extraction removes first-order silent damage but not second-order; not always best; cooperative variant tested fails | 33 |
| [V1.0](checkpoints/v1.0.md) | Is verification physically feasible? | Probabilistic inter-photon gates and unheralded loss may decide viability; bias can reverse the ranking | 29 |

The counts in the last column are the documented check counts of each program; V0 to V0.3 print their parts and a final `ALL PASS`. See [Reproducibility](reproducibility.md) for the recorded execution of every checkpoint.

## Two lines of work

1. **Tetragon map (V0 to V0.3):** ideal-state mathematics of one four-level photon. See [Tetragon](tetragon.md).
2. **Buddy verification (V0.4 to V1.0):** what a verifier detects, how reliable it is, and what it would physically take. See [Buddy](buddy.md) and [Physical feasibility](physical-feasibility.md).

## How the questions moved

Early checkpoints asked what the geometry can do. From V0.4 the question became whether verification makes a computation more reliable. V0.9 asked how reliable the verifier is. V1.0 asked whether it can exist. Each step found that the previous level of modelling had been too kind to the proposal, and each is reported with its negative results.

## Dates

The eleven archives were packaged on 2026-11-27 between about 03:57 (V0) and 06:03 (V1.0) by the build environment's file clock, after Revision H was committed (`8c39243`, 2026-11-27 00:09 −0600). These are packaging times recorded by the author's environment, not independent timestamps.

## 2026-11-27: QDE documentation checkpoint

[PROPOSED] [QDE, QIJ and ASV](checkpoints/qde-2026-11-27.md) extends the development research vocabulary and questions. This provisional documentation checkpoint is separate from the numbered computational series; it neither advances the release version nor changes prior results.

## Atomic-register update, 2026-11-28

[PROPOSED] [Read the dated checkpoint](checkpoints/atomic-register-2026-11-28.md). Model-based development; no hardware demonstration or novelty claim.
