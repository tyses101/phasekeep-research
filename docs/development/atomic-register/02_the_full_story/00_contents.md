# The full story: contents

[← Start here](../README.md) · [Short version](../01_the_short_version.md)

Each chapter opens with **In plain words**, then gives the details, the key numbers and the evidence labels. Scripts are in [simulation source](https://github.com/tyses101/phasekeep-research/tree/main/code/atomic-register), and every experiment is listed in [experiments](../03_reference/experiments.md).

| # | Chapter | One-line summary |
|---|---|---|
| 1 | [Architecture](01_architecture.md) | How the PhaseKeep components fit together, with nothing renamed or retired |
| 2 | [Register geometry](02_register_geometry.md) | The four-site ring is two qubits on a square; hypercubes generalize it |
| 3 | [Physical development](03_physical_development.md) | From photons to atoms, including the ideas that were dropped and why |
| 4 | [Digital reference](04_digital_reference.md) | How to test the design on existing quantum computers |
| 5 | [RAMM instructions](05_ramm_instructions.md) | HOLD, ROTATE, COUPLE, and the exact echo |
| 6 | [Integrity checks (IQA)](06_iqa.md) | What our checks catch and what they miss |
| 7 | [Combined imperfections (P2-CIM)](07_imperfections_P2CIM.md) | The εα rule, and sixth-order suppression |
| 8 | [Drift (E5)](08_drift_E5.md) | Why changing hopping defeats the echo |
| 9 | [Finite control pulses (E6)](09_finite_control_E6.md) | Composite flips, and why the interaction must be off |
| 10 | [Echo timing (E7)](10_echo_timing_E7.md) | Each timing has a blind spot |
| 11 | [Envelope balance (E7-D)](11_envelope_balance_E7D.md) | The balance rule behind the failures |
| 12 | [Platforms (G0)](12_platforms_G0.md) | What real hardware could do it, and what's missing |
| 13 | [Pending research](13_pending.md) | Unfinished work, clearly marked |
| 14 | [Scientific framing](14_framing.md) | What is and isn't claimed |

**Standard model used in chapters 5–11** (unless stated otherwise):
- two four-site rings, one excitation each, zero flux, code = ring modes {0, 2} × internal {R1, R2}
- hopping J_A = 1.5, J_B = 1
- inter-ring interaction on R2–R2 pairs only, ∝ 1/d⁶, side-by-side spacing D = 2, mean strength v = 0.1
- gate = sin² envelope in two echo segments with ideal staggered flips, total time 2π/v ≈ 63/J_B
- metrics: leakage-aware average gate fidelity (d = 16) and worst-case code leakage
- physical units, where quoted, assume J_B/h = 1 MHz, so one time unit = 159 ns [ASSUMED]
