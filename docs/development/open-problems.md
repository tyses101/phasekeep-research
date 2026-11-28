# Open research problems

**Status: working development record, 2026-11-27.** What is unresolved, grouped by kind. Nothing here is a result.

## Priority list across all series (consolidated, 2026-11-28)

This is the single priority order for open work. The numbered problems below (1–20) and the [atomic-register pending list](atomic-register/02_the_full_story/13_pending.md) keep their detail; [roadmap v1.1](roadmap-v1.1.md) is kept as a historical plan.

| Priority | Open item | Origin |
|---|---|---|
| 1 | Confirm the pending E7-D reproduction checks; independent reproduction of V0 to V1.0 | [Atomic checkpoint](checkpoints/atomic-register-2026-11-28.md); problem 15 |
| 2 | Run the six-qubit two-register gate in noisy simulation, then on cloud hardware | Atomic register REF-03-I |
| 3 | Model atomic decay, dephasing and collective decay realistically | Atomic register G6 |
| 4 | Design control pulses and the interaction envelope together (E8) | Atomic register |
| 5 | Logical error protection, and Buddy encoded redundancy against [[4,2,2]] and repetition codes | Atomic register REF-05-L; problem 8 |
| 6 | What a failed two-photon gate does to the data; heralded loss; non-destructive parity | Problems 1–3 |
| 7 | Retrieve real platform parameters (ions, superconducting circuits, circular Rydberg emission inhibition) | Atomic register G0 |
| 8 | Full-text literature reading and prior-art review | Problems 12, 16 |
| 9 | Derive the observed sixth-order suppression | Atomic register P2-CIM |
| 10 | Terminology and provenance items | Problems 11–14 |

## Physical feasibility (the central block)

1. **What does a failed heralded two-photon gate do to the data?** Abort versus benign decides whether joint verification of unknown data is usable ([V1.0](checkpoints/v1.0.md)). The literature excerpt read did not say.
2. **Is there a non-destructive photon-presence or parity measurement at useful success probability?** Existing abstracts suggest it is probabilistic. If detection destroys the photon, the local geometry's advantage is a factor of 2.
3. **Can loss be heralded?** Heralding the ancilla is worth more than the flag in the model; unheralded data loss sets a floor.
4. **Can several ancillary axes be hosted in one photon?** Correlated loss, independent control and readout are unstudied.
5. **Geometry conversion under realistic loss and failures.** The conversion has two inter-photon gates; its physical-model behaviour is not computed.
6. **Time-dependent loss and scheduling.** V1.0 loss is per gate participation.
7. **Two entangled Tetragons.** The coupled polarization-OAM device is an open question inherited from Revision H (Volume 6, section 6.7).

## Architecture

8. Buddy's physical form. Whether verification, computation and characterization can share one coupler. Resource classes, the third encoding axis, and BUD-xx identifiers remain provisional.
9. The cost of adapting configuration to noise conditions, against the benefit.
10. The relationship between Docked Scheduling, PKC and DDQT, and whether offline ancilla preparation can change where failures occur. Requires the original DDQT documents.

## Terminology and provenance

11. Expansion of GEA in the publication instructions versus the frozen glossary (see [register](register-of-terms.md)).
12. Naming-conflict searches: SEE, NEE, CPE, EET, IEE, Convergent Entanglement, PALADIN, Docked Scheduling, IQA, "information checkpoint".
13. Definitions of the Buddy memory, execution, interface and resource branches: not supplied.
14. Reconciliation of historical A03 and A04 audit numbering with the R30 table (carried from Revision H; not renumbered).

## Verification and evidence

15. Independent numerical reproduction of V0 to V1.0. All execution so far is author-side.
16. Full-text reading of the literature in [Literature](literature.md).
17. Independent proof review of the B03 joint-bound proof, and sources for the memory-chain inputs (4%, 12.6%, 0.49, 23%), carried from Revision H.
18. Whether non-Pauli noise, correlated noise and leakage change the V0.9 and V1.0 rankings.

## Archival

19. Development archival completed: the tagged V1.0 repository snapshot is public on Zenodo with DOI [10.5281/zenodo.24589667](https://doi.org/10.5281/zenodo.24589667). See [Citing](citing.md). This is not a separate DOI for the original Revision H release.
20. B05 is completed for the V1.0 development source snapshot. Separate archival of the original release-asset bundles, including a standalone Revision H deposit, is not claimed. This administrative completion does not close scientific verification items.

## Not claimed

No experimental hardware validation, no demonstrated reduction of physical cost for equivalent logical operations, and no quantum or efficiency advantage.

## Atomic-register update, 2026-11-28

[PROPOSED] [Read the pending research priorities](atomic-register/05_whats_next.md). Model-based development; no hardware demonstration or novelty claim.
