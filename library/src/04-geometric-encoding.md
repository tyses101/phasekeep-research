# Volume 4: Geometric Encoding (GEA)

## What you will learn

How to draw the possible states of a register as a **shape**, why the shape is a square, a cube, or a higher-dimensional cube, how to count its corners, edges and faces, and why "an edge on the drawing" is not always "a cheap step in the lab".

## 4.1 From labels to a shape

Take one binary EA. It has two values, so draw two dots and one line between them. Add a second binary EA: now two copies of that line, joined corner to corner, forming a **square**. Four dots, four edges. This square *is* the Tetragon of Volume 3.

Add a third binary EA and you get a **cube**. A fourth gives a four-dimensional cube (a tesseract), which we cannot draw but can count.

{{fig:cube|Squares and cubes. Each added binary axis doubles the number of corners.}}

**GEA** (Geometric Encoding Axies) is the project's name for reading the state space this way. A corner is an address. An **edge** joins two addresses that differ in exactly one axis, so an edge means "change just that one property". A **face** (a square) means "two axes together".

## 4.2 Counting the shape

For n binary axes, the shape has these counts [[DERIVED]]:

| What | Formula | n = 2 | n = 3 | n = 4 | n = 12 |
|---|---|---|---|---|---|
| Corners (addresses) | 2ⁿ | 4 | 8 | 16 | 4,096 |
| Edges | n · 2ⁿ⁻¹ | 4 | 12 | 32 | 24,576 |
| Square faces | C(n,2) · 2ⁿ⁻² | 1 | 6 | 24 | 67,584 |
| Cubes | C(n,3) · 2ⁿ⁻³ | 0 | 1 | 8 | 112,640 |
| Tesseracts (4-cubes) | C(n,4) · 2ⁿ⁻⁴ | 0 | 0 | 1 | 126,720 |

C(n,k) means "n choose k", the number of ways to pick k things from n. We checked these counts by running code against direct enumeration.

::: plain
A cube has 8 corners and 12 edges: from the table, n = 3 gives 8 and 3 × 4 = 12. A twelve-axis register would have 4,096 addresses and nearly 25 thousand edges.
:::

## 4.3 The family of register names

| Binary axes (n) | Name | Addresses |
|---|---|---|
| 1 | Qubit | 2 |
| 2 | Tetragon | 4 |
| 3 | Cubion | 8 |
| 4 | Tesseron | 16 |
| 5 | Penteron | 32 |
| 6 | Hexeron | 64 |
| 7 | Heptaron | 128 |
| 8 | Octeron | 256 |
| 9 | Ennearon | 512 |
| 10 | Decaron | 1,024 |
| 11 | Aetheron | 2,048 |
| 12 | Hyperion | 4,096 |

These are project names [[PROPOSED]]. Only the first two exist in the current design. Nothing above n = 2 has a hardware plan.

## 4.4 What an edge means, and what it costs

On the drawing, every edge looks the same. In a lab, they do not cost the same. Flipping polarization is one waveplate. Flipping twist might be a mirror, or a hologram, or a sorter. Moving to a state that differs in several axes needs several devices in a row.

::: watch
**The map is not the territory.** Geometry tells you which states are neighbours *in the description*. It does not tell you that stepping between them is cheap, accurate or lossless. That is what audit item A06 (Volume 9) set out to measure.
:::

## 4.5 What the shape does *not* give you

- **It does not give a speedup.** The cube lists addresses. It says nothing on its own about doing a calculation faster than a normal computer.
- **A pure state is not a point on the cube.** A state is a blend over all the corners with phases. The corners are the *basis*; the state lives in the space they span. For d corners it takes 2d − 2 real parameters [[DERIVED]].
- **More corners need more distinct, stable devices.** Each axis added is another property to prepare, change and read.

## 4.6 Shared or individual changes: the A06 question

Suppose we want to swap H and V on a photon that may be in any of several twist modes, leaving each mode in place. Do we do it **in one shared operation** (one half-wave plate acts on every mode at once), or do we **single out each mode**, change it separately, then recombine? The second route needs a sorter before and an inverse sorter after.

A computer model (A06) compared the two for N = 2 (the Tetragon pair), 4, 8, 16 and 32 modes. All error and loss numbers in it are assumptions [[ASSUMED]], so the result describes the model, not a lab [[SIMULATED]]. In plain terms:

| Modes N | Parts, state stays in place (shared vs individual) | Parts, full twist readout needed (shared vs individual) |
|---|---|---|
| 2 | 1 vs 8 | 6 vs 7 |
| 4 | 1 vs 22 | 14 vs 17 |
| 32 | 1 vs 218 | 126 vs 157 |

- When the state can stay where it is, the shared operation needs one plate against dozens or hundreds of parts.
- When the full twist must be read out at the end anyway, the saving shrinks to about 14 % at N = 2 and about 20 % at N = 32 (in parts counted).
- Under the default assumptions the shared plate's fidelity stays near 0.9996 for every N, while the individual design falls from 0.99959 (N = 2) to 0.99471 (N = 32), and its transmission from 0.979 to 0.937, because sorter error grows with the twist number.
- The shared plate would lose its advantage only if its retardance varied across the modes by roughly 13 to 20 times the amount assumed. Whether a real plate does that is unknown, and is the first thing a bench should measure.

::: deeper
The model's separating device was an illustrative tree of N−1 interferometers with three elements each, not a published sorter; real sorters are different devices, so the individual design here may even be optimistic. Its error per node grows with |ℓ| (Dove-prism sensitivity), and the aperture loss follows the Laguerre-Gaussian formula of Volume 1. Preparation, detection, radial modes, wavelength dependence and any two-photon operation were not simulated [[ASSUMED]].
:::

## 4.7 Four kinds of geometry

The word "geometry" is used for four different things in PhaseKeep, and only two of them are physical. Keeping them apart avoids a lot of confusion.

| Geometry | Mathematical or physical? | What it describes |
|---|---|---|
| **Address geometry** | Mathematical | How the basis addresses are related: the square, cube or hypercube of this volume |
| **State-space geometry** | Mathematical | The amplitudes, phases, superpositions and correlations of the quantum state itself |
| **Optical-mode geometry** | Physical | The actual intensity, phase and polarization pattern of the light across the beam |
| **Execution geometry** | Physical | The arrangement of components, light paths and interaction points on the bench |

The photon is not shaped like a square. The square describes how its possible encoded states relate to each other. But those states belong to real properties of light, so the mathematics can have physical consequences, which is what the next section shows.

A research question follows: *how well can these four geometries be made to complement one another?* If a mathematical relationship matches something light does naturally, the operation may be cheap. If it does not, we pay for sorters and extra parts. The A06 simulation above is one narrow example: swapping H and V does the same thing to every twist mode, so one shared plate does it. Whether this idea gives a general advantage is **not established** [[PROPOSED]].

## 4.8 Two kinds of blend: edge and diagonal

A state can be a blend of two addresses that share an edge of the square, or two that sit on opposite corners. These behave differently.

| | **Edge blend** | **Diagonal blend** |
|---|---|---|
| Example | (00 + 01)/√2 | (00 + 11)/√2 |
| In words | H with twist −1 plus H with twist +1 | H with twist −1 plus V with twist +1 |
| Occupied addresses | 2 | 2 |
| Can be written as polarization × twist? | **Yes**: H ⊗ (−1 + +1)/√2 | **No** |
| Schmidt rank | 1 | 2 |
| Schmidt weights | 1 and 0 | 0.5 and 0.5 |
| Polarization across the beam | Uniform, ideally | Varies around the beam, ideally |

{{fig:vortex|Polarization around the beam. The edge blend (left) has the same polarization everywhere; the diagonal blend (right) cycles through diagonal and circular polarizations, twice per turn.}}

A state that can be written as one polarization times one twist blend is called **separable**; one that cannot is **non-separable**. The diagonal blend is non-separable: its polarization and twist are correlated inside a single photon, with no second photon involved. For this state the light's polarization goes through both diagonal linear polarizations and both circular ones, repeating twice per turn around the beam axis. Beams like this are known as **vector vortex beams** [[DERIVED]] for the field pattern; the published literature on them has not been reviewed in this project [[UNVERIFIED]].

::: watch
**Non-separable is not the same as "structured".** A separable edge blend also produces a structured beam: its intensity has two lobes, with uniform polarization. Non-separability matters specifically for the *coupling* between polarization and twist, not for structured light in general.
:::

Two facts follow, both checked numerically [[DERIVED]]:

- Applying an independent unitary operation to each axis, such as a waveplate and a mirror, **cannot change the Schmidt weights**. A separable state stays separable and a non-separable one stays non-separable.
- Creating or undoing non-separability needs a *coupled* operation, such as a q-plate-type device or an interferometer. Filtering and measurement are separate cases that change the weights and are not covered by this rule.

## 4.9 What this means for registers

Separability is one more property a register description could record. A fuller register specification might list:

| Register property | Purpose |
|---|---|
| EA contents | Which physical encoding properties are available |
| Address geometry | The computational relationships |
| State dimension | The size of the state space |
| Separability | Whether the axes can be treated independently |
| Closure | Whether CT operations stay inside the encoding space |
| Symmetry | Chances for a shared operation |
| Coherence requirements | Which phase relationships must survive |
| Physical compatibility | Which components can do the operation |

A compiler could use a *known preparation record* to decide whether independent single-axis operations are enough or whether a coupled operation is needed. It cannot simply look at an unknown photon and read these properties off [[PROPOSED]].

## 4.10 Geometry as a way to describe operations

So far we have used the shape to *organize addresses*. A sharper question is whether the shape can *describe operations* on the state space. Each geometric feature picks out a **subspace**: the set of states that can be built from the addresses it contains.

| Feature | Subspace it picks out | Dimension | Operations one could describe |
|---|---|---|---|
| **Vertex** | One address | 1 | Prepare it; apply a phase to just that address |
| **Line** (edge) | Two addresses that differ in one axis | 2 | Swap the two amplitudes; mix them (rotate within the pair); change their relative phase; prepare a blend of the pair; *isolate* the pair |
| **Parallel lines** | Several equivalent edges | 2 each | The same operation on each at once |
| **Diagonal** | Two addresses that differ in both axes | 2 | Selective mixing, which can create non-separability |
| **Face** (square) | Four addresses | 4 | Permuting labels, conditional operations, phase patterns, amplitude mixing, coupling or decoupling the axes |

For the 12-axis register of Section 4.2 the counts are: 4,096 vertices (dimension 1), 24,576 lines (2), 67,584 squares (4), 112,640 cubes (8) and 126,720 tesseracts (16) [[DERIVED]]. These subspaces **overlap**. They are different ways of addressing parts of one state space, not independent processors.

Four points keep this honest:

- **A line is not a path.** A drawn edge does not show the route a state takes. It marks a two-dimensional subspace inside which the amplitudes and relative phase can change continuously.
- **"Isolate" is not a reversible operation.** Selecting a two-address subspace by filtering or projecting throws the rest away and costs light. Swapping, mixing and phase changes within the subspace are reversible; isolating is not.
- **Parallel lines save parts, not steps.** If both OAM exchanges (00↔01 and 10↔11) are the same physical action, one mirror does both. That is what A06 exploited for the complementary case, a polarization exchange across many twist modes. The saving is in hardware; it is not a quantum speedup.
- **The geometry does not say which operations exist.** Volume 5 lists swap and phase operations for the twist axis. A general mixing of twist −1 with +1 is not on that list, and which device would do it is an open question [[PROPOSED]].

The diagonal case is worth testing with numbers. Rotating address 00 toward 11 by 45° gives (00 + 11)/√2, with Schmidt weights 0.5 and 0.5: non-separable. Flipping both axes together (X on each) just turns 00 into 11, which is still separable [[DERIVED]]. So *selectively* mixing a diagonal pair can create the tie between the axes, while a global double flip cannot. The program `tetragon.py` checks this.

## 4.11 PQGS: a name for what we study

**Photonic Quantum Geometric Superpositions (PQGS)** is a descriptive PhaseKeep term for coherent photonic superpositions organized within a geometrically structured encoding space, with particular interest in non-separable states that span more than one Encoding Axis.

- It is a **research term inside GEA**, not a new pillar and not a new physical phenomenon.
- "Geometric" means the organization of the addresses. It does **not** mean geometric phase (the Berry or Pancharatnam-Berry phase) or geometric quantum computation, which are different, established topics. For example, the abstract of Marrucci, Manzo and Paparo (*Phys. Rev. Lett.* 96, 163905) says that converting spin angular momentum to orbital angular momentum in such media is associated with Pancharatnam-Berry geometrical phases [[REPORTED]] (abstract only).
- The underlying superposition mathematics is standard. Any claim that this organization makes states easier to prepare, transform or preserve is [[PROPOSED]] and untested.

::: evidence
**Evidence status.** Counting formulas, Schmidt weights and the invariance under independent unitaries: [[DERIVED]], checked numerically. Names and the PQGS term: [[PROPOSED]]. Vector-vortex and spin-orbit literature: [[UNVERIFIED]], not reviewed here. A06 comparison: [[SIMULATED]] with [[ASSUMED]] inputs. No hardware cost has been [[MEASURED]].
:::

## Try it

1. How many corners and edges has a 4-axis register? (16 and 32.)
2. How many square faces does a cube have? (6.)
3. A state has equal blend over all four Tetragon addresses. Is it a corner? (No. A corner is a single address; a blend is a point in the space spanned by the corners.)
4. Is (01 + 10)/√2 separable? (No. It is a diagonal blend: V with twist −1 plus H with twist +1.)
5. A half-wave plate acts on the polarization of the diagonal blend (00 + 11)/√2. Is the result separable? (No. An independent operation on one axis cannot make it separable.)

## Summary

::: key
GEA is a way to *draw* the state space: one corner per address, one edge per single-property change. The counts are exact, but edges differ in real-world cost, and the shape alone gives no computational advantage. Four different geometries are in play, two mathematical and two physical. Edge blends are separable and diagonal blends are not, and only coupled operations can change that.
:::
