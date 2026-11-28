# 4. Digital reference: testing on existing quantum computers

[← Physical development](03_physical_development.md) · [Next: RAMM instructions →](05_ramm_instructions.md)

> **In plain words:** before anyone builds the atomic hardware, the design's *logic* can be tested on today's cloud quantum computers. The intended two-ring operation is just one standard gate (CZ) on six qubits. We keep a second, much more expensive version that imitates the physical imperfections. That version is for studying the physics, not for running the logic.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## Encodings (both kept)
| | One-hot | Compact |
|---|---|---|
| One ring | 8 qubits | 3 qubits |
| Two rings | 16 qubits | 6 qubits (logical code subspace: dimension 16) |
| Strength | Free excitation-count check (loss detection) | Cheapest. Hopping needs no entangling gates |

## REF-01: single register [SIMULATED `ref01_onehot.py`, `ref01_diagnostics.py`]
- **Accuracy:** one-hot, 200 random code superpositions. Fidelity is 1 to about 1e-14 even with **one** Trotter step.
- **The test isn't vacuous:** omitting hopping gives F = 0.03; omitting the flip gives F = 0.89.
- **Negative controls:**
  - internal-state-dependent hopping stays exact
  - a site detuning of 0.8 J creates Trotter error that converges as n⁻⁴ (7.7e-4 → 5.4e-10, from 1 to 32 steps)
- **Gate count:** the sequence in the script counts **16** two-qubit gates at one step. It reduces to **12** when the commuting layers are merged.
- **Corrected metric:** the earlier "code fidelity" for the detuned case used a non-unitary projected target. Use **W = C†U_exact†U C, F = (|Tr W|² + Tr W†W)/(m(m+1))** instead. The exact detuned evolution itself leaks **6.49%** (worst case).

## REF-03-I: ideal logical execution (PROPOSED for hardware; logic SIMULATED)
- **The gate:** for a conditional phase of π, the intended inter-register gate is **one CZ between the two internal qubits**. That's 6 compact qubits, excluding preparation, readout and other logical gates.
- **Confirmed in simulation:** the intended-gate target is a pure diagonal phase on the code. [SIMULATED `echo_combined.py`]
- **Not yet done:** noisy-circuit validation, and any hardware run.

## REF-03-P: physical-interaction emulation [REPORTED, separate AI re-run (REPORTED)]
| Item | Value |
|---|---|
| Interaction Pauli-Z terms (including identity) | 32 |
| RZ rotations per slice | 31 |
| CNOTs per slice, independent gadgets | 130 |
| CNOTs per slice, shared-parity network | 36 |
| Phase reconstruction residual | ~5.6e-16 |
| 64-slice logical fidelity | ~99.99759% |
| Full 64-slice echo cost | 2,304 CNOTs, 1,984 RZ |

**This cost reproduces the physical interaction's *imperfections*.** It isn't needed to implement the intended gate. The audit scripts for REF-03-P are **not included** in this package (see handoff).

Slice-count behaviour [REPORTED]:
- 16 and 32 slices fail catastrophically (worst leakage 98% and 73%).
- 64 or more slices converge towards the continuous model's 99.98868%.
- 64 slices showing *higher* fidelity than the continuous result probably reflects error cancellation. It isn't a better implementation.

## REF-03-N: controlled imperfection injection (PROPOSED)
- **Purpose:** inject chosen amounts of unevenness, drift and detuning into REF-03-I, then compare against the tolerance models in chapters 7–11.
- **Status:** **no noisy hardware execution has been performed.**
