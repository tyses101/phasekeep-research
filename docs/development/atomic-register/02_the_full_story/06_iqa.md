# 6. Integrity checks (IQA)

[← RAMM instructions](05_ramm_instructions.md) · [Next: combined imperfections →](07_imperfections_P2CIM.md)

> **In plain words:** we have two cheap checks:
> - **counting excitations** catches loss
> - **a parity measurement** catches some errors that push the register out of its allowed states
>
> Neither catches every error that corrupts the information itself. Catching and *fixing* those needs redundancy across registers, and that hasn't been demonstrated.

[ASSUMED] Scope: numerical statements apply only to the stated model, sequence and sampled parameters. They are not hardware guarantees.

## Three protection levels (PROPOSED organization)
| Level | Mechanism | Status |
|---|---|---|
| 1. Physical integrity | Excitation count (one-hot) | SIMULATED / REPORTED |
| 2. Code-space integrity | X₁X₂ stabilizer parity (compact) | REPORTED, separate AI re-run (REPORTED) |
| 3. Logical integrity | Redundant-register encoding and correction | **Not demonstrated** |

## Parity check [REPORTED, separate AI re-run (REPORTED)]
- **Circuit:** one ancilla, **2 CNOTs + 4 Hadamards**, excluding preparation and measurement.
- **Accuracy:** the projectors P± = (I ± X₁X₂)/2 match to about 8.9e-16.

| Injected error | Detected | Accepted-state fidelity |
|---|---|---|
| None | 0% | 100% |
| Single compact spatial Z | 100% | rejected |
| **Double spatial ZZ** (acts as logical X) | **0%** | 0% |
| **Single compact X** | **0%** | 0% |
| **One-hot single-mode phase error** | **50%** | **50%** |

The one-hot phase error contains a Z₁Z₂ (logical) component, which parity cannot see.

## Excitation count [REPORTED, separate AI re-run (REPORTED)]
- **Uniform amplitude damping:** every actual loss is flagged.
- **Unequal damping:** accepted states are distorted (p = 0.01–0.2 gave conditional fidelity 0.9986).
- **Phase errors pass:** one tested phase error passed the count at 25% fidelity.

## The hidden-error problem
- **Drift corrupts logic without leaving the code.** In E5 (ch. 8), drift produces up to 94% logical infidelity with leakage around 1e-5 or lower.
- **So both checks would report "valid"** while the operation is almost entirely wrong.
- **Levels 1 and 2 are necessary but nowhere near sufficient.**

## Buddy System and level 3 (PROPOSED)
- **Buddy role in this proposal:** an encoded-redundancy investigation; the frozen Buddy definition is not replaced. It **never** copies unknown quantum states (no-cloning).
- **What to benchmark it against:**
  - repetition codes, for one error type
  - **[[4,2,2]]**, a four-qubit code encoding two logical qubits and detecting any single-qubit error. It can correct a single error **only when its location is known** (an erasure).
- **Location knowledge** could come from excitation counting or flagged decay (erasure conversion: UNVERIFIED reference).
- **Open question:** whether the location can be identified without disturbing the surviving encoded information.
- **No logical recovery mechanism is claimed.**

## Dual-species verification (PROPOSED, provisional name IQA-DS)
- **Idea:** separate the failure mechanisms of the register and its verifier, for example with different atomic species.
- **Caveat:** different species don't guarantee independent errors, and a non-destructive verification interaction is still needed.
