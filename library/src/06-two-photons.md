# Volume 6: Two Photons, and Making Light Interact

## What you will learn

Why photons do not normally affect each other, what a *controlled-SUM* operation is, how a published experiment forced two photons to interact (by throwing away most attempts), what this means for how many such operations we would need, and what two entangled Tetragons look like (the project's first target).

## 6.1 The problem: photons ignore each other

Two flashlight beams cross and pass through each other unchanged. Single photons are the same: they do not interact. That is wonderful for carrying information and terrible for computing, because computing needs one piece of information to *change another*.

## 6.2 Controlled-SUM: the two-register operation we want

Treat each photon as a four-level register with addresses 0, 1, 2, 3. **Controlled-SUM** takes two registers (a *control* j and a *target* k) and replaces the target by the sum modulo 4:

```
|j⟩|k⟩  becomes  |j⟩|(j + k) mod 4⟩
```

It is the four-level version of the familiar CNOT. Facts we verified numerically [[DERIVED]]:

- SUM can be built from a diagonal **controlled-phase** operation CP, which multiplies each |j,k⟩ by i^(jk), sandwiched between a Fourier transform and its inverse on the target: SUM = (I ⊗ F†)·CP·(I ⊗ F).
- The phase i^(jk) can itself be split into three two-bit phase gates: two controlled-Z and one controlled-S.
- **Kickback.** If the target is prepared in the right Fourier state |B_r⟩, then SUM leaves the target alone and applies a phase Z^(−r) to the control. This is a way to apply an operation to one photon using another as a tool.

## 6.3 How many "real" interaction gates would we need?

An **operator Schmidt rank** measures how far a two-register operation is from being a product of one operation on each register. Rank 1 means it is a product. A higher rank means more interaction is needed to build it, and the rank sets a floor on the number of interaction gates *in a stated gate model* (below). It is a mathematical count. It is not a measure of physical interaction strength, and it is not the same as the power to create entanglement (section 6.7).

| Operation | Operator Schmidt rank |
|---|---|
| CP on four-level registers | 4 |
| One controlled-phase-flip (CPF, flips the sign of the single state 3,3 only) | 2 |

A circuit of m CPF gates (with free single-photon operations in between) can reach rank at most 2^m. CP has rank 4, so at least **2** CPF gates are needed [[DERIVED]]. This is a *lower bound*. The true number needed is **undefined** until someone finds a circuit. [[BLOCKED]] on that search.

The bound belongs to a stated gate model. If every available interaction gate has operator Schmidt rank at most *r*, a target of rank *R* needs at least the smallest whole number *k* with *r*^k at least *R*. It is a floor, not a prediction, and it is often not tight. Example: a SWAP of two two-level systems has rank 4 and a CNOT has rank 2, so the floor is two CNOTs, yet the standard exact circuit uses three [[DERIVED]], checked by `two_tetragons.py`. It also says nothing directly about the number of optical components.

::: deeper
The rank of a diagonal two-register operator is the matrix rank of its 4 × 4 table of phases. For CP the table is the Fourier matrix, which has full rank 4. For CPF the table equals the all-ones matrix with one entry flipped, which has rank 2.
:::

## 6.4 Making photons talk: the published gate

Liu et al. (arXiv 2407.16356, a July 2024 preprint, not peer reviewed at the time we read it) report a **heralded four-dimensional controlled-phase-flip gate** using orbital angular momentum [[REPORTED]]. In plain terms:

- Two photons are the *computational* photons. Two more are *auxiliary* helpers.
- The conditional phase is produced optically, and the helpers are measured to announce success.
- The gate works only when specific detectors fire. The theoretical success rate is 1/4 × 1/2 = **1/8**.
- Success is judged by **post-selection**: they keep runs where exactly one photon appears at each output port, and a Bell-state measurement on the helpers' polarization is part of the herald. Only one outcome (Φ⁺) is described experimentally.
- Reported **process fidelity** is 0.64 to 0.82, measured using four-photon coincidences.
- It flips the sign of only |3,3⟩.

::: key
**Heralded** means: a detector click is supposed to announce success, so you know when to trust the output. **Post-selected** means: you keep the runs that look right and discard the rest. The gate works, but *only on the runs you kept*.
:::

## 6.5 Why bunching makes a gate

When two identical photons meet at a balanced beam splitter, they leave together: |1,1⟩ becomes (|2,0⟩ − |0,2⟩)/√2, with both photons in the same port [[DERIVED]] (sign convention dependent). That "stick together" behaviour is a two-photon effect that depends on whether the photons are in the same mode, so it can be used to attach a conditional phase.

## 6.6 Another route: a single atom in a cavity

Hacker, Welte, Rempe and Ritter (*Nature* 536; arXiv:1605.05261) demonstrated a photon-photon gate by letting the photons interact through a single atom in a high-finesse optical cavity, realizing the Duan-Kimble controlled-phase-flip protocol. What was checked:

| Item | Value | Checked against |
|---|---|---|
| Average gate fidelity | 76.2 ± 3.6 % | The paper's abstract [[REPORTED]] |
| Phase | π (a controlled phase flip) | The paper's abstract [[REPORTED]] |
| Two-photon transmission | (22 %)² = 4.8 % | Project notes only [[UNVERIFIED]] |
| Wavelength | 780 nm | Project notes only [[UNVERIFIED]] |
| Bandwidth | 0.7 MHz | Project notes only [[UNVERIFIED]] |

The abstract does not state the transmission, wavelength or bandwidth. If the 0.7 MHz figure is right, it is about 1,400 times narrower than a 1 GHz band, and the ORCA memory paper's abstract states a GHz-scale bandwidth, so the two would not obviously fit together [[DERIVED]] arithmetic on supplied values. The gate gives a π phase only, and our register needs more.

## 6.7 Two Tetragons: entanglement between registers

So far one photon carried one register. Now put a Tetragon on each of **two** photons, A and B. Each has four addresses, so together they have 4 × 4 = 16 joint states. This is **high-dimensional entanglement**: entanglement between systems with more than two levels each.

The simplest example is the equal blend of "both photons at 00", "both at 01", "both at 10" and "both at 11". Each photon alone looks completely random, yet the two always agree. This state has four equal Schmidt weights of 0.25, which is the most entanglement two four-level systems can hold: **2 ebits** (an *ebit* is the entanglement of one maximally entangled pair of two-level systems). The count for a pure state with *r* equal weights is log₂ *r* ebits [[DERIVED]]:

| Addresses taking part on each photon | Schmidt rank | Entanglement (ebits) |
|---|---|---|
| 1 | 1 | 0 |
| 2 (a line) | 2 | 1 |
| 3 (a group, not a triangle of edges) | 3 | 1.585 |
| 4 (the Tetragon) | 4 | 2 |
| 8 (a Cubion) | 8 | 3 |
| 16 (a Tesseron) | 16 | 4 |
| 4,096 (a Hyperion) | 4,096 | 12 |

Two registers need not use all their addresses in the entanglement. The joint space of two 12-axis registers has 4,096 × 4,096 = 16,777,216 dimensions. That is a large mathematical space, not millions of values we can read out (Volume 2).

### Five ways to line up the addresses

The pairing of A's addresses with B's can follow different patterns. Take address k = 2 × polarization + twist, so 0, 1, 2, 3 are 00, 01, 10, 11:

| Pattern | A addresses | B addresses | What turns "corresponding" into it, acting on B alone |
|---|---|---|---|
| Corresponding | 0, 1, 2, 3 | 0, 1, 2, 3 | Nothing |
| Horizontal reflection | 0, 1, 2, 3 | 1, 0, 3, 2 | Flip the twist (a mirror) |
| Vertical reflection | 0, 1, 2, 3 | 2, 3, 0, 1 | Flip the polarization (a half-wave plate) |
| Diagonal reflection | 0, 1, 2, 3 | 3, 2, 1, 0 | Both flips |
| Cyclic rotation | 0, 1, 2, 3 | 1, 3, 0, 2 | A **coupled** operation: the new polarization depends on the old twist |

All five have the same entanglement, 2 ebits, because an operation on one photon alone cannot change how entangled the pair is [[DERIVED]]. What differs is the *pattern*, and so what it takes to reach it:

- The first four are each a **polarization pair times a twist pair**: one pair entangled in polarization and one in twist, on the same two photons. Moving between them needs only a separate operation on each axis of photon B.
- The cyclic rotation is **not** such a product. Reaching it needs an operation inside photon B that couples its polarization and its twist [[DERIVED]]. In fact it is an exchange of the two axes (a SWAP: the polarization value becomes the twist value and the other way round) followed by a flip of one axis. Checked by `two_tetragons.py`.

This suggests sorting operations by what they need, not by how simple they look on the drawing:

| Kind | Meaning | Example |
|---|---|---|
| **Independent** | One separate operation per axis | The flips above |
| **Coupled** | Does not factor into one operation per axis (operator Schmidt rank above 1), yet may still never turn a product input into an entangled one | The axis SWAP, and so the cyclic rotation |
| **Entangling** | Can turn some product input into an entangled state | A controlled phase |

So "needs coupled control" does not mean "creates entanglement", and operator rank is a statement about whether the operation factors, not about physical interaction strength. Two operations that look equally simple as geometry can need very different equipment. Whether a device for the axis SWAP exists, and at what loss, is an open question for Volume 5 [[PROPOSED]]. A compiler could use this sorting to choose between plans for the *same* task, but nobody has shown that it saves anything. The five patterns are different target states, not different routes to one goal, so their costs cannot be compared with each other as if they were.

### What we can and cannot do to the entanglement

- **Relabel it.** Local operations on one photon move the pattern around without changing the amount (above).
- **Not raise it** with local operations. Increasing entanglement takes an interaction between the photons or an extra entangled resource. This is a standard result of quantum information theory.
- **Change a joint phase carefully.** A sign change that involves both photons can change entanglement while leaving every measurement probability the same, exactly as in Volume 4 section 4.8. "Changing a phase" is therefore not automatically harmless to the entanglement [[DERIVED]].

### What the literature already shows

These are established research areas and PhaseKeep did none of them. The status given is how much of each source we read:

- Photon pairs **hyperentangled in polarization and in orbital angular momentum with values ±1**, which is the Tetragon's pair of axes, were used by Barreiro, Wei and Kwiat for superdense coding (*Nature Physics* 4, 282, 2008). Read as the opening summary only [[REPORTED]]. Note that this pair is produced by a source. It was not made by a gate between the photons.
- A four-dimensional generalization of the Pauli X gate on the orbital angular momentum of single photons, together with a known Z gate as a complete high-dimensional set, was reported by Babazadeh et al. (*Phys. Rev. Lett.* 119, 180510; arXiv:1702.07299). Abstract only [[REPORTED]]. This is four dimensions in OAM alone, not the polarization-times-twist Tetragon, and the abstract gives no efficiency.
- Hyperentanglement in several degrees of freedom at once (Barreiro et al., *Phys. Rev. Lett.* 95, 260501, 2005; polarization, spatial mode and time-energy). Abstract only [[REPORTED]].

::: watch
**Not claimed.** The idea that organizing the entanglement by geometric patterns makes states easier to prepare or gates cheaper is a hypothesis [[PROPOSED]]. PhaseKeep has not prepared an entangled Tetragon pair, and the two-photon *gates* of this volume are the hard part. Counting ebits and patterns says what is possible in principle, not what it costs.
:::

## 6.8 What this means for PhaseKeep

- A true four-level controlled-SUM needs at least two CPF gates, and probably more.
- Each published gate is heralded: it succeeds only some fraction of the time.
- A classical controller can choose which operations to apply, but that **does not by itself establish any quantum advantage** [[PROPOSED]]. We do not claim one.
- Two Tetragons can in principle be entangled to 2 ebits in several geometric patterns. Making the *gates* that move between them is the hard part.
- The key question becomes: can we *tell* when the gate worked, without destroying the output? Volume 7 shows that this is harder than it sounds.

::: evidence
**Evidence status.** Controlled-SUM identities, kickback, Schmidt ranks, the bunching rule and the two-Tetragon counts and patterns: [[DERIVED]], checked by code. Liu et al. results: [[REPORTED]], read from the paper. Hacker et al.: fidelity and phase [[REPORTED]] from the abstract; the other figures [[UNVERIFIED]]. A PhaseKeep implementation of any of these: [[MEASURED]] none.
:::

## Try it

1. Controlled-SUM on |2⟩|3⟩ gives what? (|2⟩|(2+3) mod 4⟩ = |2⟩|1⟩.)
2. If a gate succeeds with probability 1/8 and you need two such gates in a row, both heralded, what is the success chance if they are independent? (1/64.)
3. Why can the lower bound "at least 2 CPF gates" be wrong as a count? (It is only a floor. Nobody has shown a two-gate circuit.)
4. Two photons each carry a Tetragon in the equal blend of "both at 00 ... both at 11". How many ebits? (2.) Does a half-wave plate on photon B change that? (No. It relabels the pattern; it cannot change the entanglement.)

## Summary

::: key
Photons do not interact on their own. Published gates force an interaction using helper photons and a lot of discarded runs. A four-level controlled-SUM needs at least two such gates, and nobody has shown that two is enough.
:::
