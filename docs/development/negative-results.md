# Negative results

**Status: working development record, 2026-11-27. Kept prominent on purpose.** A negative result is a calculation that went against a proposal, or a limit of what a calculation can show. They are listed with the checkpoint that found them. All are inside the stated models.

| # | Result | Found in | Evidence |
|---|---|---|---|
| 1 | Moving between product and entangled bases always needs an entangling gate in the ideal model; conversion has a price. | [V0](checkpoints/v0.md), [V0.1](checkpoints/v0.1.md) | [DERIVED] |
| 2 | For one logical qubit, adaptive switching of geometry cannot save operations against the fused single-axis baseline. | [V0.2](checkpoints/v0.2.md) | [DERIVED] |
| 3 | The diagonal encoding is not uniformly more robust; X and H have no alternative single-axis route in it. Equivalent routes are not independent routes. | [V0.3](checkpoints/v0.3.md) | [DERIVED] |
| 4 | A Buddy parity check misses phase errors and can lower reliability: a harmful ancilla fault between the two CNOTs becomes an undetected logical error and a PASS. | [V0.4](checkpoints/v0.4.md) | [DERIVED], parameters [ASSUMED] |
| 5 | Dephasing-dominated noise defeats the two-axis parity check. | [V0.4](checkpoints/v0.4.md) | [DERIVED] |
| 6 | Checking every segment can accept fewer correct runs than checking at an intermediate spacing, and sometimes than no checking. | [V0.5](checkpoints/v0.5.md) | [DERIVED] |
| 7 | Silence from a detector is not PASS once loss exists. | [V0.5](checkpoints/v0.5.md) | [DERIVED] |
| 8 | A PASS confirms the checked property only: a controlled phase with the wrong angle passes every local check. | [V0.7](checkpoints/v0.7.md) | [DERIVED] |
| 9 | The joint checks do not close the relative-phase gap either. | [V0.8](checkpoints/v0.8.md) | [DERIVED] |
| 10 | The joint code is not a superset of the local code's coverage; joint extraction creates correlated errors with the same number of silent logical cases. | [V0.8](checkpoints/v0.8.md) | [DERIVED] |
| 11 | Adaptive switching rejects slightly more than staying joint in every profile, and its benefit disappears at a conversion-fault probability near 2e-4 in the base profile. | [V0.8](checkpoints/v0.8.md) | [DERIVED on ASSUMED workloads] |
| 12 | Flagging does not remove silent damage, only moves the leading term from *p* to *p*²; under M3 it loses to the conventional joint round above *p* ≈ 1.1e-3. | [V0.9](checkpoints/v0.9.md) | [DERIVED on ASSUMED fault model] |
| 13 | The cooperative two-cat-qubit round tested is not fault tolerant, even with a verified cat. | [V0.9](checkpoints/v0.9.md) | [DERIVED] |
| 14 | Extra verification machinery increases the number of fault cases that leave some damage on the data. | [V0.9](checkpoints/v0.9.md) | [DERIVED] |
| 15 | With destructive readout the local geometry still needs inter-photon gates (4 per round); its advantage is a factor of 2. | [V1.0](checkpoints/v1.0.md) | [DERIVED on ASSUMED rule] |
| 16 | If a failed inter-photon gate aborts the round, completion falls to $s^n$ (for example 0.0039 for the joint round at s = 0.5); if failure disturbs the data, joint verification of unknown data is not usable below s ≈ 0.75. | [V1.0](checkpoints/v1.0.md) | [DERIVED on ASSUMED s] |
| 17 | Unheralded ancilla loss raises silent damage about 10 times (local) and about 60 times (flagged). Unheralded data loss sets a floor about 400 times the loss-free value for the flagged round. | [V1.0](checkpoints/v1.0.md) | [DERIVED] |
| 18 | The V0.9 ranking reverses under X-biased noise; the best configuration depends on the noise model. | [V1.0](checkpoints/v1.0.md) | [DERIVED on ASSUMED bias] |
| 19 | Repeated verification slows damage accumulation but does not stop it, and it costs runs. | [V1.0](checkpoints/v1.0.md) | [DERIVED] |
| 20 | Under some physical profiles the feasible set of verification configurations is empty. | [V1.0](checkpoints/v1.0.md) | [DERIVED on a toy profile] |

## All negative results in one place (consolidated index, 2026-11-28)

The table above covers V0 to V1.0. Later series keep their own detailed lists; their headline negatives are indexed here so this page is the single entry point. Numbering continues from the table above; the source lists keep their own identifiers.

| # | Result | Series and original identifier |
|---|---|---|
| 21 | V0.9's single flagging crossing is really a boundary in two parameters (error rate and idle-to-gate ratio) | [Explorations](../../explorations/consolidated-review.md) S26 |
| 22 | V1.0's ordering of damage among accepted runs does not survive idle faults; the chosen metric decides the ranking | Explorations S28 |
| 23 | Under four qubits, no register holding two logical qubits detects every single error | Explorations S29 |
| 24 | Handing information to a separate register helps only with a quieter memory and near-perfect two-photon gates | Explorations S30, S31 |
| 25 | Microwave plus Raman control cannot fully control the atom-cloud Tetragon, and it leaks | [Atomic register](atomic-register/03_reference/evidence_and_failures.md) N1 |
| 26 | Energy confinement fixes leakage but leaves phase errors, is not universal, and has no physical source in a frozen ensemble | Atomic register N2 |
| 27 | Without hopping, a four-atom ring reaches only 7 of 63 control directions | Atomic register N3 |
| 28 | "Chiral" splitting at flux 2π is a gauge relabelling | Atomic register N4 |
| 29 | Equal hopping (ratio 1) and ratio 2 between rings cause complete leakage | Atomic register N5 |
| 30 | Combined hopping error and uneven interaction are only quadratically suppressed | Atomic register, P2-CIM |
| 31 | Drifting hopping defeats the echo (up to about 94% infidelity), invisibly to the checks | Atomic register N11 |
| 32 | Composite flips fail with an uneven interaction left on | Atomic register N9 |
| 33 | Continuous and notched interaction envelopes underperform segmented ones; suppression drops from sixth to fourth order | Atomic register N12, N13 |
| 34 | Parity and excitation counting miss some logical errors | Atomic register N14 |
| 35 | Rydberg dressing does not improve the interaction-to-decay ratio, and introduces collective decay; an earlier mixed-source estimate also ranked circular Rydberg states lower, which is not an established platform ranking | Atomic register N15, N16 |

## What these results do not mean

They do not show that PhaseKeep cannot work, and they do not show that it can. They show where the modelled proposal is fragile. Several rest on assumptions (destructive readout, abort versus benign failure) that the project has not yet tested. A model-dependent ranking is not a general statement about architectures.

## Atomic-register update, 2026-11-28

[PROPOSED] [Read all retained negative results](atomic-register/03_reference/evidence_and_failures.md). Model-based development; no hardware demonstration or novelty claim.
