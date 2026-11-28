# The Four-Atom Ring

*A register made of four atoms and one hopping excitation, and the honest surprise inside it*

*Edition 04 working draft, research snapshot as of 28 November 2026.*


>
> **In plain words**
> This volume builds a small quantum register out of four atoms arranged in a square, with one excitation hopping around them. It shows:
> - how to store a Tetragon's four states in that ring
> - why the hopping is essential
> - an honest surprise: written in the right way, the ring turns out to be a familiar structure, two ordinary qubits on the corners of a square
>
> That surprise is not a setback. It tells us exactly where anything new would have to come from.


## 18.1 An excitation that moves

Place four atoms on the corners of a small square, a few micrometres apart, each held in its own optical tweezer ([Volume 17](17-from-light-to-atoms.md)). Excite them to Rydberg states. Now give **one** of the atoms a slightly different excitation, a "marked" state, while the other three stay in the background state.

Rydberg atoms that sit close together can **swap** their states: the marked state jumps from one atom to its neighbour, back and forth, coherently. Physicists call this resonant dipole–dipole exchange. [REPORTED] It has been demonstrated in chains of Rydberg atoms held in tweezers ([Appendix 9](A9-sources-additions.md)).

>
> **Common mistake**
> **In the mechanism modelled here, every atom in the ring is in a Rydberg state, not only the marked one.** Resonant S/P exchange works between a background Rydberg state and a marked Rydberg state, for example an S-type state and a P-type state. A Rydberg excitation among *ground-state* atoms does not hop **by this mechanism**. Other transport mechanisms exist (for example, Rydberg dressing of ground-state atoms), but they are not the model used in this edition. This matters later: in this model, all four atoms can decay ([Volume 22](22-which-machine.md)).


The jumping is called **hopping**, and its strength, written J, sets how fast the marked state moves around the ring.

## 18.2 Four ring patterns

Because the excitation can hop, it doesn't have to sit on one atom. It can be spread over all four, with a definite phase on each. There are exactly four natural patterns, called **ring modes**, labelled ℓ = 0, 1, 2, 3:

| Mode ℓ | Phase on atoms 1, 2, 3, 4 | Energy with hopping J | What it looks like |
|---|---|---|---|
| 0 | 0°, 0°, 0°, 0° | +2J | Standing wave, all in step |
| 1 | 0°, 90°, 180°, 270° | 0 | Travels around the ring one way |
| 2 | 0°, 180°, 0°, 180° | −2J | Standing wave, alternating |
| 3 (same as −1) | 0°, 270°, 180°, 90° | 0 | Travels the other way |

[DERIVED] Modes 1 and 3 carry **opposite circulating currents**, even with no special setup, like the twists ±1 of light in [Volume 16](16-lights-many-handles.md). [SIMULATED] The models give currents of +0.5 and −0.5 for them, in the model's units. Modes 0 and 2 are standing waves: nothing circulates.

## 18.3 Storing a Tetragon in the ring

Choose the two **standing-wave** modes, 0 and 2, as one binary axis. Give the marked state two possible internal levels, R1 and R2, as the second axis. Then each ring holds four combinations: two patterns × two levels. That is a Tetragon, held in matter. [PROPOSED]

The standing waves are a good choice for two reasons.
- **They are separated in energy** (+2J and −2J), so the hopping itself keeps them apart from the travelling modes, which sit at 0.
- **They can be swapped exactly** by a simple control, shown next.

## 18.4 The flip

Shine a light shift on atoms 2 and 4 only, giving them an extra half-turn of phase (180°). Every pattern gets multiplied by the alternating sign +, −, +, −. Look at what that does:
- **Mode 0** (all in step) becomes mode 2 (alternating), and mode 2 becomes mode 0.
- **Modes 1 and 3** swap with each other.

[SIMULATED] So the **staggered flip** swaps the two standing waves exactly, with no leakage into the travelling modes. It is a clean "NOT" on the pattern axis, done with nothing more than a phase on two atoms.

>
> **Go deeper (optional math)**
> In the ring-mode basis, the staggered phase (−1)ʲ on an N-site ring (N even) shifts every mode by N/2: ℓ → ℓ + N/2 (mod N). On four sites that is a shift by two, which maps the pair {0, 2} onto itself, and {1, 3} onto itself. [DERIVED] Closure depends on ring size and on which modes form the code:
> - **Eight sites:** the alternating phase swaps ℓ with ℓ + 4, so a code built from modes {0, 4} stays closed, while one built from the travelling pair {1, 7} does not. [DERIVED]
> - **A different pattern:** one that winds twice around the ring (on four sites it coincides with the alternating one) shifts mode 1 to mode 3 on eight sites, outside a {1, 7} code. [SIMULATED]


## 18.5 Why the hopping is essential

You might hope to control the register using only things that act on one atom at a time: light shifts on individual atoms, microwaves on the internal levels, and laser pulses that change the internal level depending on the atom. Those are easy to aim. But there's a catch.

[DERIVED] **Controls that act atom by atom can never move the excitation from one atom to another.** The probability of finding it on each atom stays fixed. Some operations the register needs, such as changing the balance between the two travelling modes, *require* the excitation to move. So without hopping, full control is impossible.

[SIMULATED] Counting the independent directions of control makes this concrete. Full control of one ring (4 atoms × 2 levels = 8 states) needs 63 directions:

| Controls available | Directions reached (of 63) |
|---|---|
| Microwaves + level-changing laser pulses + staggered flip | 7 |
| + light shifts on any single atom | 9 |
| + hopping between neighbours | **63: full control** |

## 18.6 Twisting the ring: synthetic flux

Hopping can also carry a phase, as if a magnetic field threaded the ring. This is called **synthetic flux**. It has a subtlety worth knowing.

- **With flux π** (half a turn), the two travelling modes get different energies, ±1.41J. They still carry currents, ±0.35, and the ring remains fully controllable. [SIMULATED]
- **With flux 2π** (a full turn), the flux is physically the same as no flux at all. The modes are merely relabelled. A "splitting" that appears in the labels at 2π is not a physical effect, and those relabelled code states carry no current. [SIMULATED]

The standing-wave register needs **no** flux at all. Flux is only useful if you want the circulating modes themselves to carry information, which the research keeps as a separate option.

## 18.7 The honest surprise: it's two qubits on a square

Here is the finding that changes how to talk about this register.

Number the four atoms in an unusual order, called a **Gray code**: 00, 01, 11, 10. In that order, every hop between neighbours flips **exactly one** of two binary digits. So hopping acts like flipping one digit or the other, independently. [DERIVED] Written that way:
- **The ring's hopping** is just two independent qubit flips, J(X₁ + X₂).
- **The two standing waves** form the states where those two qubits agree in a particular way. That is a standard error-detecting code, called the X₁X₂ = +1 code.
- **The staggered flip** acts as the code's logical NOT.
- **The hopping** acts as the code's logical phase.

[REPORTED] An independent re-run checked this equivalence to about 10⁻¹⁵ ([Appendix 8](A8-ledger-additions.md)).

>
> **Key idea**
> **The four-atom ring is not a new kind of quantum bit.** Mathematically it is two qubits on the corners of a square, with a well-known code on top. Anything new in PhaseKeep's register must come from **how it is built and controlled**: the physical embedding, the protection the hopping provides, and the control tricks of [Volume 19](19-making-registers-talk.md). Saying so plainly is part of keeping ourselves honest.


The same picture explains why the ring should grow into **cubes and hypercubes**, not bigger rings.
- **Cubes and hypercubes:** one excitation hopping around a cube of 8 atoms is three independent qubit flips, and a four-dimensional hypercube gives four. [REPORTED] Checked up to 32 sites.
- **Bigger rings:** an 8-atom *ring* is not a cube, and the clean structure breaks.

Edition 03's register family is named after hypercube corners (Tetragon, Cubion, Tesseron), so this fits the existing naming well.

## 18.8 PhaseKeep's names

Now the names, all **working development terms** ([Appendix 7](A7-glossary-additions.md)):
- **Multispatial Register (MSR):** a register that persists between operations, described by its **axis signature**, the size of each encoding axis. The ring Tetragon is [2,2].
- **Single-axis registers:** a single three-level axis is [3] (provisionally a **Trigon**), and a five-level one is [5] (provisionally a **Pentagon**).

The frozen register family names are unchanged.

## Summary

- **An excitation hops around a ring of four Rydberg atoms.** All four atoms are Rydberg-excited.
- **Four ring modes:** two standing waves (energies ±2J) and two circulating ones (energy 0, opposite currents).
- **The ring Tetragon** uses the standing waves × two internal levels. A staggered phase on two atoms swaps the standing waves exactly.
- **Hopping is essential:** atom-by-atom controls reach only 7 or 9 of the 63 control directions, and hopping completes them.
- **Flux 2π is a relabelling.** The standing-wave register needs no flux.
- **The ring is two qubits on a square with a known code.** It grows naturally into hypercubes.

## Try it

1. What are the energies of the four ring modes when J = 1? *Answer: +2, 0, −2, 0.*
2. Which modes does the staggered flip swap? *Answer: 0 with 2, and 1 with 3.*
3. Why can't light shifts on single atoms move the excitation between atoms? *Answer: they only change the phase on each atom, never how likely the excitation is to be there.*
4. How many independent qubit flips describe hopping on a cube of 8 atoms? *Answer: three.*


---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Working draft.*
