# Controlled Transformations

*The optical parts that change a state, and what each one does to it*


## What you will learn

What a **Controlled Transformation (CT)** is, the short list of optical parts that perform one, and, for each part, the one question that matters: *does it keep the photon inside the four Tetragon addresses?*

## 5.1 What "CT" means here

A **Controlled Transformation** is a physical operation that we can set and repeat, and that changes the encoded information in a known way.

>
> **Common mistake**
> **"Controlled" means adjustable, not conditional.** In quantum computing, "controlled" often means "do this only if another qubit is 1". Here it simply means *we control the device*: we choose its setting. A CT is not automatically conditioned on another qubit. When we mean the conditional kind, we say "controlled on" something, and [Volume 6](06-two-photons.md) covers it. The older working terms PTEA and TV are retired; CT replaced both.


## 5.2 The parts, and what each does

The Tetragon has four addresses: H or V (polarization) times −1 or +1 (twist). Here is each part's job, written as what it does to an address.

| Part | What it does | Keeps the photon in the 4 addresses? |
|---|---|---|
| **Half-wave plate at 45°** | Swaps H and V. Up to a harmless overall factor it is the polarization "flip". | Yes. Polarization stays H/V; twist untouched. |
| **Quarter-wave plate** | Turns H/V into circular polarization and back. Two in a row equal one half-wave plate. | Yes as a pair; a single one leaves the H/V basis. |
| **Mirror** | Reflection flips the twist: ℓ becomes −ℓ. | Yes for twist −1/+1. It would leak if the twist set were {0, +1}. |
| **Image rotation** (for example a rotating Dove prism) | Adds a twist-dependent phase. For −1 and +1 the *relative* phase between them is exp(−2iφ), where φ is the rotation angle (sign depends on convention). | Yes. It changes phases, not populations. |
| **Beam splitter / polarizing beam splitter** | Routes light by path or polarization. A PBS maps polarization into a path label. | Yes, but it adds a path axis; treat as a sorter or a gate input, not as a free operation. |
| **q-plate** | Couples polarization to twist: the twist changes by ±2q depending on the circular polarization. | **No**, not on {−1, +1} as is. From −1 it sends light to +1 (for q = 1) but from +1 to +3, which is outside the register. Needs extra care. |

All of these closure facts were checked by writing the operators as matrices [DERIVED]. The q-plate description is the standard textbook one; the specific q-plate source in the project's reading list has not been checked [UNVERIFIED].

## 5.3 Phase is the quiet operation

Most of the useful single-photon operations are **phase** changes. They do not change how likely each address is, but they change how the addresses interfere. Because the two Tetragon axes are independent, a polarization operation and a twist operation can be applied separately and in either order. Such independent operations also **cannot create or remove** the tie between polarization and twist ([Volume 4](04-geometric-encoding.md), section 4.8); only a coupled device can.

>
> **Go deeper (optional math)**
> In matrix form, half-wave plate at 45 degrees acts on the polarization qubit as −iX (X is the H/V swap). A mirror acts on the twist qubit as X, up to a phase convention. A relative phase of exp(−2iφ) between twist +1 and −1 acts as a rotation about the Z axis of the twist qubit by angle 2φ. Because the two axes are independent, a joint operation is the tensor product of the two [DERIVED].


## 5.4 Shared or individually addressed

One waveplate acts on *every* part of the beam at once. If we want to change only one address, we first need to separate the addresses (a sorter), change one, and recombine. [Volume 4](04-geometric-encoding.md) described the A06 comparison, and [Volume 9](09-research-lab.md) gives the results. The lesson for design: a **shared** operation is the cheap one, and operations that require singling out an address pay for the sorter.

**Figure.** Shared operation (one plate acts on everything) versus sort, change individually, and recombine.

*Picture description:* Left: a bundle of parallel beams passes through a single waveplate. Right: the same bundle must first go through a sorter that separates the modes, then a separate waveplate on each beam, then an unsorter to recombine them. With eight modes the illustrative model counts 1 optical element on the left and 50 on the right.

## 5.5 Design rule: write down the closure

For every new part in the architecture, the Physical Architecture Specification records five things: what it does, what controls it, whether it keeps the photon inside the four addresses, its main risks, and its cost. A part that fails the closure test (like the bare q-plate) is not discarded, but its extra outputs have to be handled explicitly. The draft specification lists 12 components [PROPOSED].

>
> **Evidence status**
> **Evidence status.** Closure of waveplate, mirror and rotation: [DERIVED]. Non-closure of the bare q-plate on {−1, +1}: [DERIVED] from the standard description. Specific devices and their loss and crosstalk: [ASSUMED] in simulations, [MEASURED] none yet.


## Try it

1. State V, twist −1 goes through a half-wave plate at 45° and a mirror. What address results? (H with twist +1: address 01.)
2. A photon with twist +1 meets a q-plate that adds +2 for one circular polarization. What twist can it end with? (+3, which is outside the Tetragon.)
3. Why does a phase-only operation not change what a measurement of the addresses returns? (It leaves each address's probability alone. Only interference with other addresses changes.)

## Summary

>
> **Key idea**
> A CT is a controlled, repeatable optical change. Waveplates, mirrors and image rotation keep the photon in the four addresses; a bare q-plate does not. Shared operations are cheap; singling out an address costs a sorter.



---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
