# Which Machine Could Build It?

::: plain
Volumes 18–21 described the register in ideal simulations. This volume brings it back to the physical world. It covers:
- what a machine would need to provide
- how to compare candidate machines fairly
- what the numbers say about the biggest obstacle, **excited-atom decay**
- what could be tested on existing hardware right now

**No machine has built this register.** Every comparison here uses published values, read at the level stated in Appendix 9, combined with simple arithmetic. Several combinations mix numbers from different experiments; they are illustrations, not predictions.
:::

## 22.1 What the machine must provide

Think of the register as a **specification**, independent of what it is made from. A machine qualifies if it can provide all of the following, at the same time, in one device:

| Ingredient | Why it's needed | Volume |
|---|---|---|
| Sites with coherent hopping of one excitation | Full control needs it | 18 |
| Two internal levels per excitation, controllable | The second encoding axis | 18 |
| A fast, accurate phase on chosen sites | The staggered flip and its composite versions | 18, 20 |
| A level-selective interaction between registers | The controlled-Z gate | 19 |
| That interaction even across sites, or switchable | Unevenness is the main coupled error | 19, 20 |
| Hopping that stays steady during an operation | The echo depends on it | 20 |
| Different hopping rates in neighbouring registers | Frequency planning | 19 |
| Lifetimes much longer than an operation | Decay | this volume |
| Some way to check integrity and flag losses | IQA | 21 |

[[DERIVED]] Volume 20's rules turn several rows into numbers, inside the tested model:
- bond error × unevenness ≲ 0.015
- between-half hopping stability around 1 part in 10,000
- the interaction off or uniform during flips
- composite flips at an assumed control strength of a few times the hopping

## 22.2 How to compare machines fairly

Two simple figures of merit help.

**Operations per lifetime.** Multiply the hopping rate by the coherence time, and divide by the number of fragile parts exposed during an operation. A large number means many operations fit before something fails. [[PROPOSED]] This is a screening metric only.

**Survival per gate.** If an operation takes a time t, and each exposed part decays at a rate Γ (one over its lifetime), the chance that *nothing* decays during the operation is about e^(−t × ΣΓ). Written as a loss budget, 𝓑 = 1 / (t × ΣΓ), the survival per gate is e^(−1/𝓑). [[DERIVED]] So 𝓑 = 100 means about 99% of gates finish with nothing lost.

::: key
**Decay counts every fragile part, not only the information carrier.** In the S/P exchange model of Volume 18, all four atoms of each ring are Rydberg-excited during a two-ring operation: **eight fragile atoms**, not two. Any one of them decaying breaks the operation.
:::

## 22.3 The decay problem, in numbers

Take the gate of Volume 19, assuming its hopping corresponds to 1 MHz. [[ASSUMED]] Then the interaction pulse takes about 10 microseconds. [[DERIVED]] With eight Rydberg atoms exposed, the chance that none decays during one gate:

| Rydberg lifetime | Survival per gate |
|---|---|
| 50 µs (illustrative) | about 20% |
| about 123 µs (55P state, room temperature) | about 52% |
| 406 µs (55P state, at 4 K) | about 82% |

[[DERIVED]] from [[REPORTED]] lifetimes (Appendix 9) and the [[ASSUMED]] 1 MHz scale.

Everything else in Volumes 19 and 20 was tuned to errors of about 1 in 10,000. **Decay is hundreds to thousands of times larger.** Two routes help:

**Faster operations.** [[REPORTED]] Measured exchange constants suggest hopping of several MHz is possible a few micrometres apart; one published value gives about 7.5 MHz at 10 µm for a particular pair of states. At that speed, the same gate takes about 1.3 µs, and survival rises to roughly 92% at room temperature or 97% at 4 K. [[DERIVED]]

::: watch
**These two numbers combine a coupling constant from one experiment with a lifetime from another,** for different states and labs. They show the *size* of the effect, not what any real device would achieve. And faster hopping needs proportionally faster, stronger control pulses.
:::

**Longer lifetimes.** Lower temperatures help, by reducing decay driven by heat radiation. So do special long-lived states (section 22.4).

Even at 97% per gate, a sequence compounds quickly [[DERIVED]]:

| Gates in a row | Survival at 97% per gate | Survival at 99.99% per gate |
|---|---|---|
| 10 | 74% | 99.9% |
| 100 | 4.8% | 99.0% |

That's why storing information in long-lived ground states *between* operations (Volume 17's rest–activate–act–return cycle), flagging losses (Volume 21) and error correction all matter. Shelving between gates helps; it does nothing *during* a gate.

## 22.4 The candidates

PhaseKeep's working identifiers for the candidate platforms are **G0-A1 … G0-D**, kept unchanged.

| Branch | Platform | What's demonstrated (by others) | The catch |
|---|---|---|---|
| G0-A1 | Atoms in tweezers, ordinary Rydberg states | Coherent excitation hopping in chains of Rydberg atoms [[REPORTED]] | Decay; every ring atom is excited during operations |
| G0-A2 | **Circular** Rydberg states (electron in a ring-shaped orbit of maximal angular momentum) | Lifetimes of 2.55 ms and 3.7 ms measured [[REPORTED]] | Their exchange is *predicted* to be only a few to tens of kHz [[REPORTED]], theory. They win clearly only if a theoretical suppression of their decay (towards minutes) is realized |
| G0-B | Ground-state atoms "dressed" with a little Rydberg character | Interactions around 13 kHz measured [[REPORTED]] | Dressing slows interaction and decay together, so it doesn't improve their ratio [[DERIVED]], under a weak-dressing assumption. One decay can also disturb the whole array [[REPORTED]] |
| G0-C1 | Trapped ions | Hopping of single spin excitations along a chain [[REPORTED]] | Couplings reach beyond nearest neighbours. Hopping rates and coherence times for this use were not retrieved |
| G0-C2 | Mediated neutral-atom interactions | Not surveyed | — |
| G0-D | Superconducting circuits | **A three-site ring with synthetic flux and measured circulating currents**, and a 12-qubit hopping chain [[REPORTED]] | The closest demonstrated match. There is no natural second internal level, which needs mapping (a higher circuit level, a second ring, or an extra qubit per site). Numbers not retrieved |

::: watch
An earlier, mixed-source estimate ranked circular Rydberg states below ordinary ones. That ranking combined measured lifetimes with *predicted* couplings and is **not** an established comparison. No platform ranking in this volume is established; the missing numbers matter.
:::

## 22.5 What would change the picture

- **Faster, more even interactions:** stronger interaction with every site pair at similar distance, so operations shorten without unevenness growing.
- **Longer lifetimes:** cryogenic environments, or circular states if decay suppression works.
- **Resting in ground states between operations,** with fast, accurate transfer in and out.
- **Turning decay into flagged erasures,** so error correction knows where to look (Volume 21; reference unverified).
- **A different atomic species for checking,** to separate the register's and the verifier's failure mechanisms (Volume 21; proposed).

## 22.6 A test that could run now

The register's **logic** doesn't need any of this hardware (Volume 19):
- **Compact version:** the intended two-register gate is six qubits and one controlled-Z gate.
- **Physical-style version:** sixteen qubits, with excitation counting as a built-in loss check.

Both fit on existing cloud quantum computers. [[PROPOSED]]

What such a test **would** show: whether the code, the flips, the echo and the gate behave as the models predict on real, noisy hardware.

What it **would not** show: anything about Rydberg atoms, decay, hopping strengths or physical speed. Those need the target hardware.

So there are two paths, deliberately kept separate:
- **A reference implementation** on established hardware, to test the architecture's logic soon.
- **A target implementation** in atoms, to test the physical embedding, decay and speed.

## 22.7 Honest status

- **What exists:**
  - a written specification
  - simulated control results
  - tolerance rules
  - a first literature screening
- **What doesn't exist:** a demonstration of the register on any platform, or retrieved parameters for ions and superconducting circuits.
- **The central physical question:** can operations become short enough compared with the excited-state lifetime, with enough evenness and stability, to make the rest of the design matter?

## Summary

- **The register is a specification any platform can try to meet:** hopping sites, two levels, site phases, a level-selective and even (or switchable) interaction, steady hopping, frequency planning, long lifetimes, integrity checks.
- **Compare machines by operations per lifetime and survival per gate,** counting every fragile part.
- **Decay is the dominant error.** At 1 MHz hopping and eight exposed atoms, a gate survives about 20–82% of the time depending on lifetime. Faster hopping and colder setups help.
- **Candidates:** ordinary and circular Rydberg atoms, dressed atoms, ions, mediated atoms, superconducting circuits. None has built it, and key numbers are still missing.
- **The logic can be tested now** on six or sixteen qubits of existing hardware. The physics needs the target machine.

## Try it

1. A gate takes 2 µs with six fragile atoms of lifetime 300 µs. What is the survival per gate? *Answer: e^(−6 × 2/300) = e^(−0.04) ≈ 96%.*
2. What is the loss budget 𝓑 in question 1? *Answer: 300/(6 × 2) = 25.*
3. Why doesn't resting in ground states between operations solve decay during a gate? *Answer: the gate itself needs the Rydberg states, so the atoms are exposed throughout it.*
4. What would a six-qubit cloud test tell you about Rydberg decay? *Answer: nothing. It tests the logic, not the atomic physics.*
