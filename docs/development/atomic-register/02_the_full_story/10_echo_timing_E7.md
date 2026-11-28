# 10. Echo timing (E7)

[← Finite control pulses](09_finite_control_E6.md) · [Next: envelope balance →](11_envelope_balance_E7D.md)

> **In plain words:** where you place the flips decides which kinds of drift get cancelled. Every arrangement has a "blind spot" frequency it can't handle. We also tried keeping the interaction on continuously across the flips. That leaked badly when the interaction is uneven, even with perfect flips.

**Script:** `code/e7_timing.py`. **Data:** `code/results/e7_timing.csv`. **Evidence:** SIMULATED. Ideal flips, drift amplitude 0.05.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## Sequences
| ID | Flip times (fraction of T) | Envelope |
|---|---|---|
| **E7-A** | 1/2, 1 | two sin² segments (original) |
| **E7-B** | 1/4, 3/4 | three sin² segments (T/4, T/2, T/4) |
| **E7-C** | 1/4, 3/4 | one continuous sin² |
| orig-cont | 1/2, 1 | one continuous sin² |
| CPMG-4 | 1/8, 3/8, 5/8, 7/8 | one continuous sin² |

## Uniform interaction (α = 0): drift rejection
| Drift | E7-A | E7-B | E7-C | CPMG-4 |
|---|---|---|---|---|
| Linear | 0.39 | **3.2e-4** | 3.2e-4 | 3.3e-4 |
| Step at T/2 | 0.88 | **exact** | exact | exact |
| ½ cycle per gate | **exact** | 0.43 | 0.43 | 2.1e-2 |
| 1 cycle per gate | 0.94 | **exact** | exact | 1.2e-4 |
| 2 cycles per gate | 1.2e-9 | 1.2e-9 | 1.2e-9 | exact |

Each sequence has a blind frequency. This is the standard filter-function behaviour of dynamical decoupling. The residual 3e-4 on linear drift is **leakage**, the same for every sequence.

## Uneven interaction (α = 0.5)
| Drift | E7-A | **E7-B** | E7-C | CPMG-4 continuous |
|---|---|---|---|---|
| None | 1.7e-6 | **1.4e-5** | 1.2e-3 (leak 0.6%) | 1.0e-2 (leak **10%**) |
| Linear | 0.39 | **3.3e-4** | 1.5e-3 | 1.0e-2 |
| Step | 0.88 | **1.5e-5** | 1.3e-3 | 1.0e-2 |
| 1 cycle | 0.94 | **1.4e-5** | 1.2e-3 | 1.0e-2 |
| ½ cycle | 1.9e-6 | 0.43 | 0.44 | 3.0e-2 |

## Verdicts
- **E7-B is the best tested compromise** for slow drift. It costs about 10× in the drift-free case, gains 3–4 orders of magnitude against linear drift, steps and 1-cycle oscillations, and keeps a ½-cycle blind spot.
- **E7-A is retained.** It is best when hopping is stable, and it handles ½-cycle drift.
- **E7-C and continuous CPMG-4 are negative results, kept.** With uneven V they leak heavily even with ideal flips. Chapter 11 explains why.
