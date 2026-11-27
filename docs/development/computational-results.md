# Computational results at a glance

**Status: working development record, 2026-11-27.** A one-page index of the principal numerical results, each traced to its checkpoint. These are the outputs of simulations and exact calculations under stated assumptions. There are no physical experiments in this project; "experimental" in earlier planning documents means numerical experiments. Every number appears, with its model, on the checkpoint page named in the last column. For limits and negative results, read the linked pages, not just this table.

| Result | Model and assumptions | Evidence | Checkpoint |
|---|---|---|---|
| Of 24 relabellings of four Bell-type states, single-axis Cliffords give 4 and two-axis local Cliffords give all 24 | Ideal, noiseless | [DERIVED] | [V0](checkpoints/v0.md) |
| 108 of 225 basis pairs need an entangling gate | Ideal stabilizer bases | [DERIVED] | [V0](checkpoints/v0.md) |
| Accepted outputs are purer than unchecked exactly when the harmful ancilla fault rate is below 2x(1−x) | Independent Pauli faults | [DERIVED], rates [ASSUMED] | [V0.4](checkpoints/v0.4.md) |
| Conversion between local and joint geometry: 4 gates, 2 inter-photon | Assumed gate set, ideal | [DERIVED] | [V0.8](checkpoints/v0.8.md) |
| Adaptive switching: 6.6% fewer accepted-wrong results in the base profile, lost near 2e-4 conversion-fault probability | Assumed workloads | [DERIVED on ASSUMED] | [V0.8](checkpoints/v0.8.md) |
| Flagged joint extraction: zero first-order silent damage (196 single faults, M2; 460, M3) | Pauli fault models M2 and M3 | [DERIVED] | [V0.9](checkpoints/v0.9.md) |
| Second-order silent coefficient: 2.320 flagged, 2.427 conventional joint, 1.244 local | M2 | [DERIVED] | [V0.9](checkpoints/v0.9.md) |
| Flagged loses to conventional joint above *p* ≈ 1.1e-3 per location | M3 | [DERIVED on ASSUMED] | [V0.9](checkpoints/v0.9.md) |
| 119,829 reference runs for a 0.01 rad constant error, single gate | Exact click probability sin²(d/2), 95% | [DERIVED] | [V0.9](checkpoints/v0.9.md) |
| Inter-photon gates per round: 4, 8, 12, 18 (local, joint, flagged, verified cat); 8 with enough ancillary hosting | Destructive readout, K = 1 | [DERIVED on ASSUMED] | [V1.0](checkpoints/v1.0.md) |
| Completion $s^n$ at s = 0.5: 0.0625, 0.0039, 2.4e-4, 3.8e-6 | Failure aborts the round | [DERIVED on ASSUMED] | [V1.0](checkpoints/v1.0.md) |
| Unheralded ancilla loss raises silent damage about 10 times (local), about 60 times (flagged) at 1% | Loss per photon per gate | [DERIVED on ASSUMED] | [V1.0](checkpoints/v1.0.md) |
| X-bias reverses the V0.9 ranking | Bias weight 100 | [DERIVED on ASSUMED] | [V1.0](checkpoints/v1.0.md) |
| 119,829 runs reduced to 48 (50 gates) or 2 (256 gates) | Coherently accumulating constant error | [DERIVED on ASSUMED] | [V1.0](checkpoints/v1.0.md) |
| Data-touching gates: 4 local, 8 each joint round; ancilla-only 0, 0, 4, 10 | V1.0 circuits | [DERIVED] (annotation A01) | [Active-information exposure](active-vs-replaceable.md) |

See also [Negative results](negative-results.md) and [Reproducibility](reproducibility.md).
