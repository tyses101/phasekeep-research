# Checking Without Breaking, Part 2

::: plain
Edition 03's Volume 7 taught the central lesson of verification: **detection is not verification**. This volume carries that lesson into the atomic register. It describes:
- two cheap checks the register offers for free
- what each catches, and what slips through
- why catching an error is not the same as fixing it
- where the Buddy System fits now

Nothing here demonstrates error correction. It maps what has and hasn't been shown.
:::

## 21.1 What we already know

Three facts from Edition 03 still frame everything:
- **Looking destroys.** Measuring a quantum state directly usually wrecks the information it holds.
- **Copying is impossible.** An unknown quantum state cannot be duplicated (the no-cloning rule, Volume 2), so "keep a backup and compare" is not available.
- **A check tests one property.** A parity check asks a yes/no question about the data without reading the data. A PASS confirms that one property only. A wrong rotation angle, for example, can pass every check (Volume 7).

## 21.2 Three levels of integrity

It helps to separate three things that can go wrong, from the most physical to the most logical:

| Level | The question | Example of failure |
|---|---|---|
| **1. Physical** | Is the carrier still there? | An atom decayed; the excitation vanished |
| **2. Code** | Is the register still inside its allowed states? | The ring slipped into a travelling mode |
| **3. Logical** | Is the information the *right* information? | The phase drifted, so the register holds the wrong state |

Each level needs its own kind of check. A register can pass levels 1 and 2 and still fail level 3. Volume 20's drift results are exactly that case.

PhaseKeep's working organization of **Integrated Quantum Assurance (IQA)** uses these three levels. [[PROPOSED]]

## 21.3 Check 1: count the excitations

In the physical-style encoding (one qubit per atom-and-level, Volume 19), a healthy register always holds **exactly one** excitation. None of the register's operations change that number. So counting the excitations at the end is a free check: any other count means something went wrong. [[DERIVED]]

[[REPORTED]] An independent re-run tested this against simple noise models:

| What went wrong | Does counting catch it? |
|---|---|
| Excitation lost, same probability for every state | Yes: every real loss is flagged |
| Excitation lost, more likely for some states than others | Loss is flagged, but the *surviving* states are subtly distorted |
| A phase error (nothing lost) | **No.** In one test, the state's fidelity fell to 25% while the count stayed perfect |

## 21.4 Check 2: the parity check

In the compact encoding, the ring's two standing waves form the X₁X₂ = +1 code (Volume 18). Measuring the parity X₁X₂ with one helper qubit tells you whether the register is still inside the code, without reading which code state it holds. [[REPORTED]] The circuit needs two two-qubit gates and four single-qubit gates, and was checked to about 10⁻¹⁵.

[[REPORTED]] What it catches:

| Injected error | Detected? |
|---|---|
| A single phase flip on one compact qubit | Yes, every time |
| A phase flip on **both** compact qubits | **No.** It is the code's logical NOT, so it stays inside the code |
| A bit flip on one compact qubit | **No** |
| A phase error on one atom in the physical encoding | **Only half the time.** Part of it acts like a logical operation |

::: watch
**A check tells you about the property it measures, and nothing else.** Counting finds loss; parity finds escapes from the code. Neither can see an error that keeps the register inside the code while changing its information.
:::

## 21.5 The hidden-error problem

Volume 20 found the clearest example. When hopping drifts during an operation, the register can end up almost entirely wrong (up to 94% infidelity) while its leakage stays tiny. Both checks above would report "fine".

That is the strongest argument for level 3: **some errors can only be caught by redundancy**, by encoding the same logical information across more than one register so that a disagreement reveals the error.

## 21.6 From detecting to correcting

Correction needs more than detection: you must know *what* went wrong and *where*, without destroying the information. Because copying is impossible, redundancy is built by **encoding**, not by copies: one logical state spread across several physical carriers, in an entangled way.

Two established benchmarks are the right comparison:
- **Repetition codes:** spread one logical qubit over several physical qubits so that one *type* of error can be outvoted.
- **The [[4,2,2]] code:** stores two logical qubits in four physical ones, and **detects** any single error on one of them. It cannot generally **correct** an error it can only detect. It *can* correct one if it knows **where** the error happened: an **erasure**.

[[DERIVED]] A related limit from PhaseKeep's earlier explorations (S29): any register of fewer than four qubits holding two logical qubits cannot detect every single error. That is a limit on universal detection, not on protection against specific noise.

That makes location information valuable. If a decayed atom could be flagged, for example because it lands in a state the register never uses, the error becomes an erasure at a known place. Neutral-atom research calls this **erasure conversion**. [[UNVERIFIED]] It is recalled from the literature, and the reference is still to be checked (Appendix 9).

## 21.7 The Buddy System, revisited

Edition 03 introduced the Buddy System: helper resources that prepare, assist and check data. The research since then sharpens what a Buddy can be:
- **Not a copy.** A Buddy can never hold a duplicate of unknown data.
- **A participant in encoded redundancy.** A Buddy can carry part of an encoding, or perform a check like the parity above.
- **Measured against the benchmarks.** A Buddy scheme earns its place only if it beats repetition codes or [[4,2,2]] on something specific: fewer resources, cheaper checks, better recovery, or a better fit with the register's natural operations.

**Alternating Stacked Verification (ASV)**, a working development term, proposes rotating which resource computes and which verifies. [[PROPOSED]] Whether that helps is untested.

One more proposal concerns shared failure. If the register and its verifier can fail through the **same** mechanism, for example one decay cascading into its neighbours, the check can fail at exactly the moment it is needed. A verifier built from a **different atomic species** might separate those failure mechanisms. [[PROPOSED]] Two cautions:
- different species do not guarantee independent errors
- the verifier still needs a gentle way to interact with the register

## 21.8 What is not yet shown

- **Not yet shown:**
  - no logical error *recovery* in this register, even in simulation
  - no Buddy scheme compared against the benchmarks yet
  - no verification that atom-decay flags would work as erasures
- **Shown:** what two simple checks catch and miss, and why the third level is needed.

## Summary

- **Integrity has three levels:** physical (carrier present), code (inside the allowed states), logical (right information).
- **Counting excitations catches loss** but not phase errors.
- **Parity catches escapes from the code** but not errors that act within it.
- **Drift can corrupt the logic invisibly,** which is why level 3 needs redundancy.
- **Redundancy comes from encoding, not copying.** [[4,2,2]] detects single errors and corrects known-location erasures.
- **The Buddy System is now framed as encoded redundancy,** to be judged against established codes.

## Try it

1. A register holds exactly one excitation at the end, but its fidelity is 25%. Which check passed, and why didn't it help? *Answer: excitation counting passed; the error was a phase error, which doesn't change the count.*
2. Why doesn't parity detect a phase flip on both compact qubits? *Answer: that operation is the code's logical NOT, so the register stays inside the code.*
3. What extra information turns [[4,2,2]] detection into correction? *Answer: knowing which carrier failed (an erasure).*
4. Why can't a Buddy simply keep a backup copy of the data? *Answer: unknown quantum states cannot be copied.*
