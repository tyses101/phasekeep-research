# Relationships Between Properties

::: plain
Most of Edition 03 was about the properties a single photon carries: its polarization and its twist. This volume is about something subtler: information that is not *in* any one property, but *between* them. Two parts of a quantum system can each look completely random, yet together hold a definite, useful pattern. Learning to see those relationships, and to tell real ones from fake ones, is the first step toward everything in Volumes 16 to 22.
:::

## 15.1 Two coins that always agree

Imagine two coins, sealed in boxes, sent to two people. Each person opens a box and sees heads or tails, half the time each. When they compare notes, they always got the *same* side. Each coin on its own looks random. The pattern is in the pair.

That much is ordinary. Someone could simply have packed two matching coins, heads-heads or tails-tails, chosen at random. This is a **classical correlation**: the result was fixed in advance, and the boxes just kept it hidden.

Quantum systems can do something that ordinary coins cannot: they can hold a pattern that **depends on how you look**. This is where relationships become genuinely quantum.

## 15.2 Phase: the hidden dial

Recall from Volume 2 that a quantum state is described by **amplitudes**, numbers whose squares give probabilities. Amplitudes also carry a **phase**: a direction, like the hand of a clock. A single overall phase changes nothing you can measure. The **relative phase** between two amplitudes does matter, because it decides whether they reinforce or cancel when combined.

Two states can therefore give *exactly the same probabilities* in one kind of measurement and *completely different results* in another. The difference sits in the relative phase. It is invisible until you measure in a basis that brings the amplitudes together.

::: key
Matching probabilities in one measurement do **not** mean two states are the same. Relative phase is real information, and you only see it by looking from more than one direction.
:::

## 15.3 Three states with identical parts

Here is the clearest example. Take two qubits (two two-level systems, such as two polarizations). Compare three situations:

- **Entangled A:** the pair is in the state (|00⟩ + |11⟩)/√2.
- **Entangled B:** the pair is in (|00⟩ − |11⟩)/√2. Same parts, opposite relative phase.
- **Coin mixture:** the pair was packed as 00 or as 11 at random, like the matched coins.

| Property | Entangled A | Entangled B | Coin mixture |
|---|---|---|---|
| Each qubit alone | 50/50 | 50/50 | 50/50 |
| Results agree in the standard basis (Z) | always | always | always |
| Correlation in the diagonal basis (X) | +1 (always agree) | −1 (always disagree) | 0 (no pattern) |
| Purity of the pair | 1 | 1 | 1/2 |

[[DERIVED]] All three look identical if you only check each qubit, or only check the standard basis. They separate only when you measure in a *second* basis.
- **Entangled A and B** have a definite relationship there, opposite to each other.
- **The coin mixture** has none.

That is the quantum difference: the relationship is real before anyone looks, and it exists in every direction of measurement, not just one.

::: watch
**A common mistake is to "verify" a quantum relationship by counting results in one basis.** All three rows of the table pass that test. Edition 03 made the same point about Buddy Checks (Volume 7): counts in the encoding basis cannot certify coherence or entanglement.
:::

## 15.4 Coherence, superposition, entanglement: what is different

These words are often used loosely. Here they mean distinct things:

| Word | Meaning | Needs more than one part? |
|---|---|---|
| **Superposition** | A state is a combination of basis states, relative to a chosen basis | No |
| **Coherence** | The relative phases in a superposition are well defined, so interference can happen | No |
| **Entanglement** | The joint state of two or more parts cannot be written as separate states for each part | Yes, and you must say which parts |
| **Correlation** | Measurement results on different parts are statistically linked | Yes; can be classical or quantum |

A single photon in a superposition of horizontal and vertical polarization is **coherent**, but nothing is entangled: there is only one part. Entanglement always needs a stated division into parts. Change the division and the answer can change.

## 15.5 Relationships inside one photon and between photons

A photon with two properties gives two possible "parts" even though it is one particle:

- **Within one property:** a superposition of two polarizations.
- **Between properties of one photon:** a state such as (|horizontal, twist left⟩ + |vertical, twist right⟩)/√2, where polarization and twist cannot be described separately.
- **Between photons:** the familiar two-photon entanglement.
- **Across properties of different photons:** for example, one photon's polarization linked with another photon's twist.
- **Collective:** patterns that only appear when three or more parts are considered together.

::: deeper
The relationship *between properties of one photon* is mathematically a non-separable state on a tensor product of two degrees of freedom. Some authors call it single-particle or "classical" entanglement and debate the name, because it cannot be used to violate a Bell inequality between two distant parties. PhaseKeep uses it carefully: as a resource *inside* a register, never as a claim about distant correlations. [[REPORTED]] Published experiments have prepared such polarization–OAM states in single photons (see Appendix 9).
:::

## 15.6 Three more relationship words

**Indistinguishability.** Two photons interfere only if nothing, in any property, could tell them apart. If one carries a different twist, the interference can disappear. That is true even if the difference is in a property you weren't measuring.

**Contextuality.** The outcome of a measurement can depend on which other compatible measurements are made alongside it. That rules out any hidden "answer sheet" fixed in advance.
- **Needs at least three levels:** this needs a system with at least three distinguishable states, so a single two-level system cannot show it.
- **Enough for one Tetragon:** a Tetragon has four, which is enough. [[REPORTED]] Mermin's 1990 simplification of the relevant theorem uses a four-dimensional example (abstract-level reading; Appendix 9).

**Discord.** A measure of how "quantum" a correlation is, beyond entanglement. [[REPORTED]] It can be non-zero even for states that are not entangled (Ollivier and Zurek, abstract level). [[DERIVED]] The coin mixture in section 15.3 has zero discord, which makes it a useful control when testing for it.

## 15.7 PhaseKeep's names for this

Now the names. PhaseKeep calls the framework for describing a joint state, its divisions into parts, and all these relationships the **Quantum Dimensional Environment (QDE)**. The classification of relationship types above is grouped under **Convergent Quantum Relationships**.

::: watch
"Environment" here means the joint state space PhaseKeep is organizing, **not** the physical surroundings that disturb a quantum system (which physicists also call an environment). QDE is an organizing framework, not a newly discovered phenomenon. Both names are **working development terms** (Appendix 7), not part of the frozen Edition 03 vocabulary.
:::

## 15.8 Counting a two-Tetragon world

Two photons, each with two binary properties, make four two-level parts in total. Counting is straightforward [[DERIVED]]:

| Quantity | Value | Why |
|---|---|---|
| Joint dimension | 16 | 2 × 2 × 2 × 2 |
| Pairs of parts | 6 | ways to choose 2 of 4 |
| Triples of parts | 4 | ways to choose 3 of 4 |
| Real numbers to describe a general pure state | 30 | 16 complex amplitudes = 32 real numbers, minus normalization and overall phase |

::: watch
Six pairs do **not** mean six independent relationships you can set at will. All pairs come from one shared joint state and constrain each other. Counting possibilities is not the same as having independent controls, and certainly not the same as having readable classical bits (Volume 2).
:::

## Summary

- Information can live in **relationships**: relative phase, coherence, entanglement, correlation.
- **States that look identical part by part can differ completely as a whole.** Telling them apart needs more than one measurement basis.
- Entanglement always refers to a stated division into parts.
- Relationships can sit inside one photon, between photons, or across properties of different photons.
- PhaseKeep's working names: **QDE** and **Convergent Quantum Relationships**.

## Try it

1. Two qubits always agree in the standard basis and show correlation 0 in the diagonal basis. Which row of the table in 15.3 fits? *Answer: the coin mixture.*
2. Why can't a single two-level system show contextuality? *Answer: contextuality needs at least three distinguishable states; one two-level system has only two.*
3. A pair of qubits has purity 1/2. Can it be one of the entangled states in 15.3? *Answer: no, both have purity 1.*
4. How many pairs of parts are there in three Tetragons (six two-level parts)? *Answer: 15, the number of ways to choose 2 of 6.*
