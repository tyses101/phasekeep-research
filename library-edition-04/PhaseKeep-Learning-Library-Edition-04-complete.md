# PhaseKeep Learning Library, Edition 04 (working draft, complete text)

*Research snapshot as of 28 november 2026.*

*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT (see NOTICE.txt). AI-assisted research, documentation and numerical analysis. Edition 03 Revision H remains the frozen baseline.*


Edition 04 continues the free, plain-language PhaseKeep book series from **Volume 15**. It is a **dated research snapshot as of 28 November 2026**: it describes what the research had found by that date, so the research can keep moving without the books needing constant rewrites. Later findings will go into a later edition, not into silent edits.

>
> **Key idea**
> **What stays the same.** Edition 03 Revision H (Start Here, First Words, Volumes 1–14 and Appendices 1–6) remains the **frozen baseline**, unchanged. Edition 04 builds on it. Every claim still carries an evidence label: [DERIVED] [REPORTED] [SIMULATED] [ASSUMED] [PROPOSED] [UNVERIFIED]. **No PhaseKeep hardware measurement exists yet.**


## How to read Edition 04

| If you are... | Read |
|---|---|
| New to PhaseKeep | Edition 03's Start Here and Volumes 1–4 first, or the one-page [PhaseKeep from the beginning](../development/phasekeep-from-the-beginning.html). Then Volumes 15, 16, 17 in order |
| Already familiar with Edition 03 | Volumes 15–17 (relationships, light's many handles, from light to atoms), then 18–20 (the four-atom ring, making registers talk, when things go wrong) |
| A reviewer | Appendix 10 (what this edition is), then Appendix 8 (every number and its source), then any volume |

## What is in this release

Volumes 15–20 and Appendices 7–10. Volumes 21 (checking without breaking, part 2) and 22 (which machine could build it), and a second workbook, are planned for the next release of this edition.

## A note on words

Each volume explains the physics **first**, in ordinary language, and only then gives the name PhaseKeep uses for its application. Names that came after Edition 03 are **working development terms**: they are not part of the frozen vocabulary, and Appendix 7 lists their status.


## Contents

- Volume 15: Relationships Between Properties
- Volume 16: Light's Many Handles
- Volume 17: From Light to Atoms
- Volume 18: The Four-Atom Ring
- Volume 19: Making Registers Talk
- Volume 20: When Things Go Wrong
- Glossary Additions
- Ledger Additions
- Sources Additions
- Edition 04 Notes

---

## Volume 15: Relationships Between Properties

*When the information lives between things, not inside them*


>
> **In plain words**
> Most of Edition 03 was about the properties a single photon carries: its polarization and its twist. This volume is about something subtler: information that is not *in* any one property, but *between* them. Two parts of a quantum system can each look completely random, yet together hold a definite, useful pattern. Learning to see those relationships, and to tell real ones from fake ones, is the first step toward everything in Volumes 16 to 22.


### 15.1 Two coins that always agree

Imagine two coins, sealed in boxes, sent to two people. Each person opens a box and sees heads or tails, half the time each. When they compare notes, they always got the *same* side. Each coin on its own looks random. The pattern is in the pair.

That much is ordinary. Someone could simply have packed two matching coins, heads-heads or tails-tails, chosen at random. This is a **classical correlation**: the result was fixed in advance, and the boxes just kept it hidden.

Quantum systems can do something that ordinary coins cannot: they can hold a pattern that **depends on how you look**. This is where relationships become genuinely quantum.

### 15.2 Phase: the hidden dial

Recall from [Volume 2](../library/02-quantum-states.html) that a quantum state is described by **amplitudes**, numbers whose squares give probabilities. Amplitudes also carry a **phase**: a direction, like the hand of a clock. A single overall phase changes nothing you can measure. The **relative phase** between two amplitudes does matter, because it decides whether they reinforce or cancel when combined.

Two states can therefore give *exactly the same probabilities* in one kind of measurement and *completely different results* in another. The difference sits in the relative phase. It is invisible until you measure in a basis that brings the amplitudes together.

>
> **Key idea**
> Matching probabilities in one measurement do **not** mean two states are the same. Relative phase is real information, and you only see it by looking from more than one direction.


### 15.3 Three states with identical parts

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

[DERIVED] All three look identical if you only check each qubit, or only check the standard basis. They separate only when you measure in a *second* basis.
- **Entangled A and B** have a definite relationship there, opposite to each other.
- **The coin mixture** has none.

That is the quantum difference: the relationship is real before anyone looks, and it exists in every direction of measurement, not just one.

>
> **Common mistake**
> **A common mistake is to "verify" a quantum relationship by counting results in one basis.** All three rows of the table pass that test. Edition 03 made the same point about Buddy Checks ([Volume 7](../library/07-buddy-checks.html)): counts in the encoding basis cannot certify coherence or entanglement.


### 15.4 Coherence, superposition, entanglement: what is different

These words are often used loosely. Here they mean distinct things:

| Word | Meaning | Needs more than one part? |
|---|---|---|
| **Superposition** | A state is a combination of basis states, relative to a chosen basis | No |
| **Coherence** | The relative phases in a superposition are well defined, so interference can happen | No |
| **Entanglement** | The joint state of two or more parts cannot be written as separate states for each part | Yes, and you must say which parts |
| **Correlation** | Measurement results on different parts are statistically linked | Yes; can be classical or quantum |

A single photon in a superposition of horizontal and vertical polarization is **coherent**, but nothing is entangled: there is only one part. Entanglement always needs a stated division into parts. Change the division and the answer can change.

### 15.5 Relationships inside one photon and between photons

A photon with two properties gives two possible "parts" even though it is one particle:

- **Within one property:** a superposition of two polarizations.
- **Between properties of one photon:** a state such as (|horizontal, twist left⟩ + |vertical, twist right⟩)/√2, where polarization and twist cannot be described separately.
- **Between photons:** the familiar two-photon entanglement.
- **Across properties of different photons:** for example, one photon's polarization linked with another photon's twist.
- **Collective:** patterns that only appear when three or more parts are considered together.

>
> **Go deeper (optional math)**
> The relationship *between properties of one photon* is mathematically a non-separable state on a tensor product of two degrees of freedom. Some authors call it single-particle or "classical" entanglement and debate the name, because it cannot be used to violate a Bell inequality between two distant parties. PhaseKeep uses it carefully: as a resource *inside* a register, never as a claim about distant correlations. [REPORTED] Published experiments have prepared such polarization–OAM states in single photons (see Appendix 9).


### 15.6 Three more relationship words

**Indistinguishability.** Two photons interfere only if nothing, in any property, could tell them apart. If one carries a different twist, the interference can disappear. That is true even if the difference is in a property you weren't measuring.

**Contextuality.** The outcome of a measurement can depend on which other compatible measurements are made alongside it. That rules out any hidden "answer sheet" fixed in advance.
- **Needs at least three levels:** this needs a system with at least three distinguishable states, so a single two-level system cannot show it.
- **Enough for one Tetragon:** a Tetragon has four, which is enough. [REPORTED] Mermin's 1990 simplification of the relevant theorem uses a four-dimensional example (abstract-level reading; Appendix 9).

**Discord.** A measure of how "quantum" a correlation is, beyond entanglement. [REPORTED] It can be non-zero even for states that are not entangled (Ollivier and Zurek, abstract level). [DERIVED] The coin mixture in section 15.3 has zero discord, which makes it a useful control when testing for it.

### 15.7 PhaseKeep's names for this

Now the names. PhaseKeep calls the framework for describing a joint state, its divisions into parts, and all these relationships the **Quantum Dimensional Environment (QDE)**. The classification of relationship types above is grouped under **Convergent Quantum Relationships**.

>
> **Common mistake**
> "Environment" here means the joint state space PhaseKeep is organizing, **not** the physical surroundings that disturb a quantum system (which physicists also call an environment). QDE is an organizing framework, not a newly discovered phenomenon. Both names are **working development terms** (Appendix 7), not part of the frozen Edition 03 vocabulary.


### 15.8 Counting a two-Tetragon world

Two photons, each with two binary properties, make four two-level parts in total. Counting is straightforward [DERIVED]:

| Quantity | Value | Why |
|---|---|---|
| Joint dimension | 16 | 2 × 2 × 2 × 2 |
| Pairs of parts | 6 | ways to choose 2 of 4 |
| Triples of parts | 4 | ways to choose 3 of 4 |
| Real numbers to describe a general pure state | 30 | 16 complex amplitudes = 32 real numbers, minus normalization and overall phase |

>
> **Common mistake**
> Six pairs do **not** mean six independent relationships you can set at will. All pairs come from one shared joint state and constrain each other. Counting possibilities is not the same as having independent controls, and certainly not the same as having readable classical bits ([Volume 2](../library/02-quantum-states.html)).


### Summary

- Information can live in **relationships**: relative phase, coherence, entanglement, correlation.
- **States that look identical part by part can differ completely as a whole.** Telling them apart needs more than one measurement basis.
- Entanglement always refers to a stated division into parts.
- Relationships can sit inside one photon, between photons, or across properties of different photons.
- PhaseKeep's working names: **QDE** and **Convergent Quantum Relationships**.

### Try it

1. Two qubits always agree in the standard basis and show correlation 0 in the diagonal basis. Which row of the table in 15.3 fits? *Answer: the coin mixture.*
2. Why can't a single two-level system show contextuality? *Answer: contextuality needs at least three distinguishable states; one two-level system has only two.*
3. A pair of qubits has purity 1/2. Can it be one of the entangled states in 15.3? *Answer: no, both have purity 1.*
4. How many pairs of parts are there in three Tetragons (six two-level parts)? *Answer: 15, the number of ways to choose 2 of 6.*


---

## Volume 16: Light's Many Handles

*Momentum, spin, twist, and why stability depends on the disturbance*


>
> **In plain words**
> A photon offers several properties that can carry information. This volume separates them clearly:
> - the momentum that carries it forward
> - the spin we see as polarization
> - the twist of its wavefront
>
> Then it asks a practical question: when the outside world disturbs the light, which combinations of properties survive? The answer is the most important idea in this volume. **Stability is not a property of a state on its own. It depends on which disturbance you are facing.**


### 16.1 One photon, three kinds of momentum

Light pushes. A photon carries momentum even though it has no mass. That momentum has three faces:

| Kind | What it describes | What you see |
|---|---|---|
| **Linear momentum** | Motion forward | Wavelength and direction of travel |
| **Spin angular momentum** | Rotation of the electric field | Circular polarization (left or right) |
| **Orbital angular momentum (OAM)** | Twist of the wavefront around the beam axis | A corkscrew wavefront and a doughnut-shaped beam |

Linear momentum depends only on wavelength: p = h/λ. [DERIVED] For visible light:

| Colour | Wavelength | Frequency | Photon energy | Momentum (kg·m/s) |
|---|---|---|---|---|
| Red | 650 nm | 461 THz | 1.91 eV | 1.02 × 10⁻²⁷ |
| Green | 532 nm | 564 THz | 2.33 eV | 1.25 × 10⁻²⁷ |
| Blue | 450 nm | 666 THz | 2.76 eV | 1.47 × 10⁻²⁷ |

Shorter wavelength means more momentum, but **not more speed**: in empty space light always travels at the same speed.

>
> **Common mistake**
> **The wave does not come from the twist.** An ordinary beam with no twist is just as much a wave. OAM is not a separate engine inside the photon. It describes how the forward flow of momentum *circulates* around the axis. On a twisted wavefront the momentum at each point is tilted slightly sideways, and that sideways part adds up to an angular momentum of ℓħ per photon, where ℓ is the twist number. **Polarization does not create the twist either.** Circularly polarized light can have a flat wavefront, and twisted light can be linearly polarized.


### 16.2 Families and axes

It is tempting to list every property as a separate "axis". But several of them are different descriptions of the same underlying freedom. Light really has three physical **families** [DERIVED]:

| Family | Different ways to describe it |
|---|---|
| **Polarization** | horizontal / vertical, circular left / right, any ellipse |
| **Spatial** | twist (OAM), ring structure (radial modes), path, position, sideways momentum |
| **Spectral–temporal** | frequency (colour), arrival time, pulse shape |

Choosing twist rather than path, for example, is often a choice of **basis** within the spatial family. That is the question Edition 03 called High-Dimensional Orthogonal Configurations (HDOC).

But a family can still hold **several independent encoding axes**. A photon could take one of two paths and, on each path, one of two twists: two binary axes from one family. The distinction to keep is:
- **physical family:** what nature provides
- **engineered encoding axis:** what we build from it, and must be able to control independently

### 16.3 Seeing a twist

A twisted beam has a dark centre: the phase spirals around a point where it is undefined, so the light must vanish there. Twists of **+1 and −1 produce the same doughnut of light**. A camera cannot tell them apart. Distinguishing them needs a phase-sensitive measurement: interference with a reference beam, a hologram or a mode sorter.

This matters for any register that stores information in the sign of the twist: reading it out is harder than looking.

### 16.4 Twins under focusing: the Gouy phase

When a beam is focused, it picks up an extra phase, called the **Gouy phase**, that depends on the beam's shape. For the standard family of twisted beams, the amount depends on 2p + |ℓ| + 1, where ℓ is the twist and p counts rings. [DERIVED] Because only the *size* of the twist enters, **+1 and −1 get exactly the same Gouy phase**, as long as their ring structure and beam parameters match. A superposition of +1 and −1 therefore does not drift during ideal focusing. A superposition of 0 and +1 would.

This is a real, but narrow, protection: it covers one mechanism, under matched conditions. It says nothing about turbulence, misalignment or other disturbances.

### 16.5 Rotations, and a combination that ignores them

Now rotate the whole beam about its axis by an angle θ. A twist of ℓ picks up a phase of ℓθ, so:

| Combination | Relative phase after rotation by θ |
|---|---|
| Twist +1 and −1 | 2θ |
| Twist +2 and −2 | 4θ |
| Twist 0 and +1 | θ |
| Circular polarization left and right | 2θ |

[DERIVED] Bigger twists are *more* sensitive to rotation. Polarization behaves like a twist of ±1, which makes sense: both are angular momentum.

Here is the elegant part. Spin and twist can be paired so that their angular momenta **cancel**: left-circular light with twist −1, and right-circular light with twist +1. Both carry *zero* total angular momentum along the beam. A rotation multiplies each by the same phase factor (one), so **any superposition of the two is unchanged by rotation of the whole beam**. That's whatever the angle. [DERIVED]

>
> **Common mistake**
> This protection is **specific to rotation**. The same pair is *not* protected against birefringence (a material that slows one polarization more than another). That disturbance acts on polarization alone, and it scrambles the pair. **"Protected" always needs a "against what".**


>
> **Go deeper (optional math)**
> The general rule: a set of states is protected against a disturbance exactly when the disturbance acts on all of them by the same phase. That means they sit in one eigenspace of the disturbance's generator. For rotation the generator is the total angular momentum J = S + L, and the pair above has J = 0. Such sets are called decoherence-free subspaces in the literature. [UNVERIFIED] Hybrid spin–orbit states of this kind have been used for alignment-free quantum communication (reference to be checked; Appendix 9).


### 16.6 A device that converts spin into twist

A **q-plate** is a patterned optical element that changes a photon's twist depending on its circular polarization. Left becomes right while gaining twist, and right becomes left while losing it. [REPORTED] Spin-to-orbital angular momentum conversion of this kind has been demonstrated (Marrucci, Manzo and Paparo, 2006; abstract level).

Two lessons [DERIVED]:
- **It generates the zero-angular-momentum pair.** Sending in horizontally polarized, untwisted light produces exactly the pair from 16.5. So a q-plate can *encode* a polarization qubit into the rotation-proof pair, and a second one can decode it.
- **It is not a closed gate on twists ±1.** Applied to a photon already twisted +1, it can give +2, which leaves a register built on ±1. Flipping a twist *within* ±1 needs a different element, such as an interferometer containing an image-rotating prism.

### 16.7 The principle: stability depends on the disturbance

Put together, these examples give one principle that runs through the rest of this edition:

| Configuration | Protected against | Not protected against |
|---|---|---|
| Twist ±1 pair | Gouy phase (matched beams) | Rotation (2θ), astigmatism |
| Spin–twist pair with J = 0 | Rotation of the whole beam | Birefringence |
| Horizontal / vertical polarization | Gouy phase | Rotation mixes them |

Rather than building checks that fight the physics, we can **choose configurations whose natural behaviour already preserves the information**, for the disturbances they will actually meet. Then we check for whatever is left. Volume 17 shows the same idea appearing in atoms.

### Summary

- **A photon has three kinds of momentum:** linear (forward), spin (polarization), orbital (twist). The wave exists without the twist.
- **Light has three physical families of properties.** Engineered encoding axes are built from them and must be independently controllable.
- **Twists ±1 look identical in brightness,** and share their focusing phase. Rotation still separates them.
- **Pairing spin and twist so their angular momenta cancel** gives a combination unchanged by rotation, but not by birefringence.
- **Stability always depends on the disturbance.**

### Try it

1. What relative phase do twists +3 and −3 pick up under a rotation by θ? *Answer: 6θ.*
2. Which pair, twist ±1 or twist 0 and +1, shares its Gouy phase under matched focusing? *Answer: twist ±1, because both have |ℓ| = 1.*
3. Which two spin–twist combinations have zero total angular momentum, taking left-circular as spin +1? *Answer: left-circular with twist −1, and right-circular with twist +1.*
4. Why can't a camera tell twist +1 from −1? *Answer: their intensity patterns are identical; only the phase differs.*


---

## Volume 17: From Light to Atoms

*Why the research looked beyond photon-only execution, and what atoms offer and cost*


>
> **In plain words**
> Photons are superb messengers and poor storage. This volume explains:
> - why the PhaseKeep research looked beyond doing everything with photons
> - what atoms offer
> - what a real atomic experiment did, read carefully
> - the new problem atoms bring: excited atoms do not stay excited for long


### 17.1 Why look beyond photon-only execution

Edition 03 and the computational checkpoints kept meeting the same three costs.

- **Photons are hard to keep.** Light moves at the speed of light, so a photon is stored only by delaying it (in loops of fibre, for example) or by handing its information to matter.
- **Photons are easily lost.** Every component, fibre and detector loses some photons. The checkpoints found that unannounced loss can outweigh any cleverness in the checking ([Volume 8](../library/08-memory-and-loss.html)).
- **Photons barely interact.** Two photons pass through each other. Making them influence each other needs extra resources, and often works only some of the time ([Volume 6](../library/06-two-photons.html)).

These are reasons to change the *job* photons do, not a defect of photons themselves. Photons remain the best way to **move** quantum information. The question became: what if information is **held and processed** in something else, with light used to carry it between places?

### 17.2 What atoms offer, and what they cost

Atoms bring what photons lack:

| Atoms can... | Because... |
|---|---|
| Stay in one place | They can be held in traps made of laser light, called optical tweezers |
| Hold information in their internal states | Electrons can sit in different energy levels; the nucleus has its own spin |
| Be controlled precisely | Microwaves, lasers and magnetic fields address chosen transitions |
| Interact strongly when asked | An atom excited to a very high level, a **Rydberg state**, becomes huge and interacts with neighbours micrometres away |

The cost: **an excited atom does not stay excited.** A Rydberg-excited atom falls back to lower states. [REPORTED] Lifetimes are typically tens to hundreds of microseconds at room temperature, and somewhat longer in cryogenic setups (Appendix 9). Low-lying ground states can hold information much longer, but they don't interact strongly. Much of the rest of this edition is about that trade.

### 17.3 A real experiment, read carefully

In 2025 a team stored a single photon in a cloud of cold atoms and turned it into a three-level quantum state inside the cloud. [REPORTED] What the paper reports (Jiao et al., Physical Review Research 7, 033267; sections I to IV read in full):

| Item | Value |
|---|---|
| Atoms | Up to about 1,000 rubidium-87 atoms in an optical tweezer |
| Storage | One photon stored as a shared excitation in the Rydberg level 60S |
| Control | Microwaves at 18.51 GHz (60S ↔ 59P) and 18.23 GHz (59P ↔ 59S): a chain, with no direct link from the first level to the third |
| Readout | The three levels are converted back to light one after another, as time bins |
| Total time | Under 1.8 microseconds |
| Single-excitation quality | g⁽²⁾(0) = 0.45 ± 0.05: mostly, but not purely, one excitation |
| Measured populations | 47.1%, 38.6%, 14.2% (ideal 50%, 50%, 0%) |

>
> **Common mistake**
> **What the experiment did, and did not do.** It stored a single photon, then *created* the three-level superposition inside the atoms using microwaves. It did **not** store an incoming photon that already carried a three-level encoding, let alone a four-level Tetragon. The distinction is easy to blur and important to keep.


The paper is valuable to PhaseKeep for three reasons:
- **The idea transfers.** Its "levels connected by microwave links" is exactly the kind of state map PhaseKeep draws.
- **Physics sets the shape.** The links form a chain because of physics: microwaves connect S-type levels to P-type levels.
- **Unwanted interactions are real.** Extra excitations shifted the measured phases.

### 17.4 Storage, or a register?

There is a difference between a **memory**, where information waits while computing happens elsewhere, and a **register**, where information stays put and the computing happens *to* it.

The research proposal that grew from here treats atoms as the register itself. Information rests in long-lived ground states. An operation briefly lifts it into interacting Rydberg states, acts, and returns it. [PROPOSED] That rest–activate–act–return cycle has established precedents in neutral-atom quantum computing. For PhaseKeep it is still a proposal.

>
> **Key idea**
> Edition 03 already uses the name **PK-M** for a specific proposal: a four-mode atomic-vapor memory. That frozen meaning is unchanged. The persistent register described here is a different idea, given its own working name in Volume 18.


### 17.5 A "matter Tetragon"

Atoms can hold a Tetragon of their own. Take an atom whose outer electron and nucleus each have two spin states (spin ½ each, as in hydrogen). That gives four combinations, just like polarization × twist.

The two spins are linked by a small magnetic interaction between electron and nucleus, the hyperfine coupling. An external magnetic field competes with it, and that competition sets how the states behave [DERIVED]:

| Ratio of field effect to hyperfine coupling (b/A) | How entangled the two middle energy states are (concurrence) |
|---|---|
| 0 | 1.00 (maximally entangled) |
| 0.25 | 0.97 |
| 0.5 | 0.89 |
| 1 | 0.71 |
| 2 | 0.45 |
| 10 | 0.10 |
| 100 | 0.01 (almost independent) |

The rule is concurrence = 1/√(1 + (b/A)²).
- **Weak field:** the natural states of the atom are entangled combinations of electron and nucleus.
- **Strong field:** they become independent.
- **The other two states,** both spins up or both down, are never entangled at any field.

Two further consequences [DERIVED]:
- **The field chooses the natural two-spin operation.** At zero field the coupling naturally swaps the two spins. At strong field it naturally gives a conditional phase.
- **Clock states.** The two middle states make a pair whose energy difference does not change, to first order, when the field wobbles slightly near zero. Atomic clocks exploit exactly this.

That's the atomic version of Volume 16's principle. **The protected pair is again the one whose angular momenta cancel**: protected against field noise here, as the J = 0 light pair was protected against rotation.

### 17.6 Single atoms or a cloud?

Two quite different atomic registers are possible:

| | **Individual atoms** | **A cloud of atoms sharing one excitation** |
|---|---|---|
| Information lives in | Each atom's internal levels | One excitation spread over many atoms |
| Can hold a phase pattern spread across separate atoms (like light's twist) | No. A single atom does have electronic orbital angular momentum, but a pattern *spread over many atoms* needs many atoms | Yes: as a phase pattern across the cloud |
| Extra weakness | Fewer natural axes | The pattern scrambles as atoms move |

The research explored the cloud version first, storing twist as a phase pattern across the atoms, and hit a wall [SIMULATED]. With microwaves and two-photon laser pulses alone, the twist states cannot be fully controlled: the operations either ignore the twist or shift it out of the register. Volume 18 explains how a small **ring of individual atoms** gets around this.

### 17.7 Moving information between light and matter

Any design that uses both photons and atoms needs a way to hand information across without damaging it. PhaseKeep's name for that is the **light–matter interface (PK-LMI)**, a working term whose source definition is still being reconciled. The requirement, stated plainly [PROPOSED]:
- **What must survive the transfer:** amplitudes, relative phases, the relationships between axes (Volume 15), and any entanglement with outside systems.
- **Agree the mapping first:** a table saying which light state goes to which atomic state.
- **Report losses separately:** loss, leakage into unintended states, and loss of coherence.

### 17.8 Why decay will matter

A Rydberg-based operation must finish well within the excited lifetime of **every** atom that is excited during it. Volume 22 returns to this with numbers. The short version: in the models, excited-state decay outweighs every carefully tuned control error by a wide margin. Making operations faster, or finding longer-lived states, is the central physical question.

### Summary

- **Photons are best for moving information.** Storage, loss and weak interaction pushed the research toward matter for holding and processing it.
- **Atoms stay put, hold states and interact strongly** when Rydberg-excited. Excited atoms decay.
- **A real experiment** stored a photon and then *prepared* a three-level state with microwaves. It did not store an encoded one.
- **A two-spin atom is a "matter Tetragon"**, whose entanglement is tuned by a magnetic field. Its protected clock states echo Volume 16's principle.
- **Two register types:** individual atoms and atom clouds. The cloud route ran into a control limit.

### Try it

1. What is the concurrence of the middle states at b/A = 3? *Answer: 1/√10 ≈ 0.32.*
2. Why can't the microwave chain in the 2025 experiment link the first and third levels directly? *Answer: both are S-type levels; a single microwave photon connects S-type to P-type levels, so the path goes through the P level.*
3. Name one reason, other than decay, that photons are hard to use for computing. *Answer: they are hard to store, easily lost, or barely interact with each other.*
4. Is PK-M the persistent register described in 17.4? *Answer: no. PK-M is the frozen name for a four-mode atomic-vapor memory proposal.*


---

## Volume 18: The Four-Atom Ring

*A register made of four atoms and one hopping excitation, and the honest surprise inside it*


>
> **In plain words**
> This volume builds a small quantum register out of four atoms arranged in a square, with one excitation hopping around them. It shows:
> - how to store a Tetragon's four states in that ring
> - why the hopping is essential
> - an honest surprise: written in the right way, the ring turns out to be a familiar structure, two ordinary qubits on the corners of a square
>
> That surprise is not a setback. It tells us exactly where anything new would have to come from.


### 18.1 An excitation that moves

Place four atoms on the corners of a small square, a few micrometres apart, each held in its own optical tweezer (Volume 17). Excite them to Rydberg states. Now give **one** of the atoms a slightly different excitation, a "marked" state, while the other three stay in the background state.

Rydberg atoms that sit close together can **swap** their states: the marked state jumps from one atom to its neighbour, back and forth, coherently. Physicists call this resonant dipole–dipole exchange. [REPORTED] It has been demonstrated in chains of Rydberg atoms held in tweezers (Appendix 9).

>
> **Common mistake**
> **Every atom in the ring is in a Rydberg state, not only the marked one.** The jump happens between a background Rydberg state and a marked Rydberg state, for example an S-type state and a P-type state. An excitation sitting among *ground-state* atoms does not hop. This matters later: all four atoms can decay (Volume 22).


The jumping is called **hopping**, and its strength, written J, sets how fast the marked state moves around the ring.

### 18.2 Four ring patterns

Because the excitation can hop, it doesn't have to sit on one atom. It can be spread over all four, with a definite phase on each. There are exactly four natural patterns, called **ring modes**, labelled ℓ = 0, 1, 2, 3:

| Mode ℓ | Phase on atoms 1, 2, 3, 4 | Energy with hopping J | What it looks like |
|---|---|---|---|
| 0 | 0°, 0°, 0°, 0° | +2J | Standing wave, all in step |
| 1 | 0°, 90°, 180°, 270° | 0 | Travels around the ring one way |
| 2 | 0°, 180°, 0°, 180° | −2J | Standing wave, alternating |
| 3 (same as −1) | 0°, 270°, 180°, 90° | 0 | Travels the other way |

[DERIVED] Modes 1 and 3 carry **opposite circulating currents**, even with no special setup, like the twists ±1 of light in Volume 16. [SIMULATED] The models give currents of +0.5 and −0.5 for them, in the model's units. Modes 0 and 2 are standing waves: nothing circulates.

### 18.3 Storing a Tetragon in the ring

Choose the two **standing-wave** modes, 0 and 2, as one binary axis. Give the marked state two possible internal levels, R1 and R2, as the second axis. Then each ring holds four combinations: two patterns × two levels. That is a Tetragon, held in matter. [PROPOSED]

The standing waves are a good choice for two reasons.
- **They are separated in energy** (+2J and −2J), so the hopping itself keeps them apart from the travelling modes, which sit at 0.
- **They can be swapped exactly** by a simple control, shown next.

### 18.4 The flip

Shine a light shift on atoms 2 and 4 only, giving them an extra half-turn of phase (180°). Every pattern gets multiplied by the alternating sign +, −, +, −. Look at what that does:
- **Mode 0** (all in step) becomes mode 2 (alternating), and mode 2 becomes mode 0.
- **Modes 1 and 3** swap with each other.

[SIMULATED] So the **staggered flip** swaps the two standing waves exactly, with no leakage into the travelling modes. It is a clean "NOT" on the pattern axis, done with nothing more than a phase on two atoms.

>
> **Go deeper (optional math)**
> In the ring-mode basis, the staggered phase (−1)ʲ shifts every mode by two: ℓ → ℓ + 2 (mod 4). Because 2 ≡ −2 (mod 4), it maps the pair {0, 2} onto itself, and {1, 3} onto itself. This only works for four sites. On an eight-site ring, the same pattern shifts mode 1 to mode 3, outside a {1, 7} code. [SIMULATED]


### 18.5 Why the hopping is essential

You might hope to control the register using only things that act on one atom at a time: light shifts on individual atoms, microwaves on the internal levels, and laser pulses that change the internal level depending on the atom. Those are easy to aim. But there's a catch.

[DERIVED] **Controls that act atom by atom can never move the excitation from one atom to another.** The probability of finding it on each atom stays fixed. Some operations the register needs, such as changing the balance between the two travelling modes, *require* the excitation to move. So without hopping, full control is impossible.

[SIMULATED] Counting the independent directions of control makes this concrete. Full control of one ring (4 atoms × 2 levels = 8 states) needs 63 directions:

| Controls available | Directions reached (of 63) |
|---|---|
| Microwaves + level-changing laser pulses + staggered flip | 7 |
| + light shifts on any single atom | 9 |
| + hopping between neighbours | **63: full control** |

### 18.6 Twisting the ring: synthetic flux

Hopping can also carry a phase, as if a magnetic field threaded the ring. This is called **synthetic flux**. It has a subtlety worth knowing.

- **With flux π** (half a turn), the two travelling modes get different energies, ±1.41J. They still carry currents, ±0.35, and the ring remains fully controllable. [SIMULATED]
- **With flux 2π** (a full turn), the flux is physically the same as no flux at all. The modes are merely relabelled. A "splitting" that appears in the labels at 2π is not a physical effect, and those relabelled code states carry no current. [SIMULATED]

The standing-wave register needs **no** flux at all. Flux is only useful if you want the circulating modes themselves to carry information, which the research keeps as a separate option.

### 18.7 The honest surprise: it's two qubits on a square

Here is the finding that changes how to talk about this register.

Number the four atoms in an unusual order, called a **Gray code**: 00, 01, 11, 10. In that order, every hop between neighbours flips **exactly one** of two binary digits. So hopping acts like flipping one digit or the other, independently. [DERIVED] Written that way:
- **The ring's hopping** is just two independent qubit flips, J(X₁ + X₂).
- **The two standing waves** form the states where those two qubits agree in a particular way. That is a standard error-detecting code, called the X₁X₂ = +1 code.
- **The staggered flip** acts as the code's logical NOT.
- **The hopping** acts as the code's logical phase.

[REPORTED] An independent re-run checked this equivalence to about 10⁻¹⁵ (Appendix 8).

>
> **Key idea**
> **The four-atom ring is not a new kind of quantum bit.** Mathematically it is two qubits on the corners of a square, with a well-known code on top. Anything new in PhaseKeep's register must come from **how it is built and controlled**: the physical embedding, the protection the hopping provides, and the control tricks of Volume 19. Saying so plainly is part of keeping ourselves honest.


The same picture explains why the ring should grow into **cubes and hypercubes**, not bigger rings.
- **Cubes and hypercubes:** one excitation hopping around a cube of 8 atoms is three independent qubit flips, and a four-dimensional hypercube gives four. [REPORTED] Checked up to 32 sites.
- **Bigger rings:** an 8-atom *ring* is not a cube, and the clean structure breaks.

Edition 03's register family is named after hypercube corners (Tetragon, Cubion, Tesseron), so this fits the existing naming well.

### 18.8 PhaseKeep's names

Now the names, all **working development terms** (Appendix 7):
- **Multispatial Register (MSR):** a register that persists between operations, described by its **axis signature**, the size of each encoding axis. The ring Tetragon is [2,2].
- **Single-axis registers:** a single three-level axis is [3] (provisionally a **Trigon**), and a five-level one is [5] (provisionally a **Pentagon**).

The frozen register family names are unchanged.

### Summary

- **An excitation hops around a ring of four Rydberg atoms.** All four atoms are Rydberg-excited.
- **Four ring modes:** two standing waves (energies ±2J) and two circulating ones (energy 0, opposite currents).
- **The ring Tetragon** uses the standing waves × two internal levels. A staggered phase on two atoms swaps the standing waves exactly.
- **Hopping is essential:** atom-by-atom controls reach only 7 or 9 of the 63 control directions, and hopping completes them.
- **Flux 2π is a relabelling.** The standing-wave register needs no flux.
- **The ring is two qubits on a square with a known code.** It grows naturally into hypercubes.

### Try it

1. What are the energies of the four ring modes when J = 1? *Answer: +2, 0, −2, 0.*
2. Which modes does the staggered flip swap? *Answer: 0 with 2, and 1 with 3.*
3. Why can't light shifts on single atoms move the excitation between atoms? *Answer: they only change the phase on each atom, never how likely the excitation is to be there.*
4. How many independent qubit flips describe hopping on a cube of 8 atoms? *Answer: three.*


---

## Volume 19: Making Registers Talk

*Coupling two rings, frequency planning, gentle pulses, the echo, and testing on today's computers*


>
> **In plain words**
> One ring on its own can only do so much. To compute, two rings must influence each other, and only in the way we intend. This volume shows:
> - how two rings are coupled
> - how to keep them from swapping contents by accident
> - why gentle pulses beat abrupt ones
> - a simple "echo" that cancels a whole class of hardware imperfections exactly
> - how the logic can be tested on today's quantum computers
>
> Everything here comes from ideal simulations: careful models, not hardware.


### 19.1 Two rings, one deliberate interaction

Put two four-atom rings near each other. Rydberg atoms in neighbouring rings push on each other, and the strength depends on which internal level each marked excitation is in. Arrange it so that the push acts **only when both excitations are in level R2**. Then, after the right amount of time, the pair picks up a phase of exactly π in that one case and nothing otherwise. That is a standard two-qubit gate, called a controlled-Z (CZ). [DERIVED]

But real atoms sit at different distances. The atoms of the two rings that face each other push harder than the far ones. Split the interaction into two parts:
- **The average part:** the same for every pair of atoms. This produces the intended gate.
- **The uneven part:** how much each pair differs from the average. This is an **error**: it can scramble the ring patterns.

Much of the design work is about keeping the uneven part from doing damage.

### 19.2 Frequency planning: keeping rings from trading contents

Each ring's standing waves sit at energies ±2J, and its travelling modes at 0. Now consider two rings together. With equal hopping in both, some combinations of a standing wave in one ring and the opposite standing wave in the other add up to **zero**. That is exactly the energy of states *outside* the register. The interaction can then push the register out of its code at no energy cost.

[DERIVED] Working through every combination, this happens whenever the ratio of the two rings' hopping strengths is **1, 2 or ½**. Away from those ratios the register's energies and the outside energies never coincide. The safest choice is a ratio of **1.5**, where the smallest gap equals the weaker ring's hopping.

[SIMULATED] The simulations confirm it. Settings: interaction strength one-twentieth of the weaker hopping, rings two ring-widths apart.

| Hopping ratio | Worst leakage out of the register |
|---|---|
| 1.0 | 100% |
| 1.425 | 3.9% |
| **1.5** | **3.0%** |
| 1.575 | 2.4% |
| 2.0 | 100% |

Giving neighbouring registers **different natural frequencies** so they don't interfere is called **frequency planning**. It's familiar from radio, and from superconducting quantum computers.

### 19.3 Gentle beats abrupt

How you switch the interaction on matters. Switch it on suddenly, and the register is jolted; part of it is knocked out of the code and stays out. Ramp it up and down smoothly, following a sin² curve, and the register adjusts as it goes and returns cleanly at the end.

[SIMULATED] For the same total gate time:

| Pulse | Final leakage |
|---|---|
| Abrupt on/off | 2.2 × 10⁻² |
| Smooth (sin²) | 2.3 × 10⁻⁶ |

That's about ten thousand times less leakage. The register still leaves the code *temporarily* during the pulse, but comes back.

### 19.4 The echo

While the rings interact, each ring's own hopping keeps running in the background, and real hopping strengths are never exactly what we intend. Here is a remarkably simple fix.

Recall the staggered flip from Volume 18: a half-turn of phase on every second atom. Every hop in a four-atom ring connects an "odd" atom to an "even" one. The flip therefore **reverses the sign of every hop**, whatever its strength.

So: run for a while, flip, run for the same time, flip back. The second half undoes the first half's hopping exactly. [DERIVED] In symbols, S·e^(−iHt)·S·e^(−iHt) = 1, where S is the flip and H is the hopping. That holds **even if the hopping strengths are wrong or uneven**, as long as they stay steady.

The average interaction, meanwhile, is unaffected by the flip and by the hopping. It keeps accumulating, so the intended gate survives the echo. [SIMULATED] Results:
- With the echo, the gate's average fidelity rose from 98.22% to **99.989%** in the standard model.
- With a 10% hopping error and a uniform interaction, the echo's cancellation was exact to about 10⁻¹⁴.
- That stays true even when the two internal levels hop at different rates.

>
> **Common mistake**
> The echo cancels hopping that is wrong but **steady**. Volume 20 shows what happens when hopping changes *during* the operation, and when the interaction is uneven. Both break the exact cancellation.


### 19.5 Three instructions

The echo gives the register three distinct modes of operation. PhaseKeep's working names for them (Appendix 7):

| Instruction | What it does | What it relies on |
|---|---|---|
| **HOLD** | Keeps the ring pattern still: hopping cancelled by the echo | Steady hopping |
| **ROTATE** | Lets hopping act on purpose, rotating the pattern's phase | Accurately known hopping and timing |
| **COUPLE** | Interacts two registers while each one's hopping cancels | Steady hopping and a uniform interaction |

The layer that chooses which registers receive which instruction is called **RAMM** (Random Access Multispatial Matrix), a working development term. RAMM is about **addressing and control**. It is not a memory, and not "quantum RAM" in the technical sense.

>
> **Common mistake**
> HOLD is not a quantum memory. It cancels hopping, nothing else. Decay and other disturbances carry on. And a register can't HOLD and ROTATE on the same axis at the same time, so a scheduler must keep them apart.


### 19.6 Testing the logic on today's quantum computers

The register doesn't need its own hardware to have its *logic* tested. Volume 18 showed that one ring is two qubits with a code on top. So the whole design can run on an existing quantum computer [DERIVED]:

| | Physical-style encoding (one qubit per atom-and-level) | Compact encoding (Gray code) |
|---|---|---|
| One ring | 8 qubits | 3 qubits |
| Two rings | 16 qubits | 6 qubits |
| One ring's hopping | Exact in a single step: 8 two-qubit gates | **No two-qubit gates**: single-qubit rotations only |
| Built-in check | Count the excitations (catches loss) | Parity check X₁X₂ (catches some errors) |

[DERIVED] The intended two-register gate, the clean controlled-Z from 19.1, is then **one CZ between the two internal qubits**. That's six qubits and one entangling gate, small enough for today's cloud quantum computers.

[REPORTED] By contrast, copying the *uneven* interaction faithfully into a circuit took 36 two-qubit gates per time slice after optimization (130 before), and 2,304 for a full 64-slice gate. That cost reproduces the hardware's imperfection, not the intended logic.

[PROPOSED] Nobody has run either version on real hardware yet.

### Summary

- **Two rings interact through a level-dependent push.** Its average makes a clean CZ gate; its unevenness is an error.
- **Hopping ratios of 1, 2 and ½ let rings trade contents** at no energy cost. A ratio of 1.5 is safest.
- **Smooth sin² pulses** leak about ten thousand times less than abrupt ones in the same time.
- **The staggered-flip echo cancels steady hopping exactly,** even uneven or miscalibrated hopping, while the intended gate survives.
- **Three working instructions:** HOLD, ROTATE, COUPLE, chosen by RAMM.
- **The logic fits on six qubits and one CZ.** It can be tested on existing quantum computers, and hasn't been yet.

### Try it

1. Why is a hopping ratio of exactly 1 dangerous? *Answer: some register states then have the same energy as states outside the register, so the interaction can push the register out at no cost.*
2. Does the echo cancel a hopping strength that is 10% too large but steady? *Answer: yes, exactly, because the flip reverses every hop regardless of strength.*
3. Which instruction depends most on knowing the hopping strength accurately? *Answer: ROTATE.*
4. How many qubits does the compact encoding need for three rings? *Answer: nine.*


---

## Volume 20: When Things Go Wrong

*A story of simulated failures, and the rules each one taught*


>
> **In plain words**
> Volume 19 described the register when everything behaves. This volume is the opposite: a story of experiments, all in simulation, that went looking for trouble and found it. Each failure is kept, because each one taught a rule the hardware would have to obey. The rules at the end of this volume are the most practical results in Edition 04.


### 20.1 Why failures are results

A design that only works when everything is perfect isn't a design yet. So the research deliberately added imperfections:
- uneven atoms
- wrong hopping strengths
- drifting settings
- slow control pulses

Then it measured what broke. Edition 03 did the same for verification (Volumes 7 and 9). The habit carries on here.

Two numbers appear throughout:
- **Infidelity:** how far the actual operation is from the intended one, averaged over inputs.
- **Leakage:** how much of the register escapes its four allowed states, in the worst case.

They measure different failures. A register can stay entirely inside its states while doing the wrong thing.

### 20.2 One imperfection at a time

Start with one ring and one flaw: an atom whose energy is slightly off, a bond whose hopping is slightly too strong, or a bond with a small stray phase.

[SIMULATED] For all three, leakage grows as roughly **0.1 × (size of the flaw)²**, and **does not keep growing over time**. The hopping gap keeps it bounded, which is the protection Volume 18 promised.

But one flaw behaves differently. A wrong **bond strength** changes the energy gap between the two standing waves. That makes the register's logical phase run at the wrong rate, and the error **accumulates**. [SIMULATED] A 1% bond error stays harmless over a short operation, but reaches an infidelity of about 2 × 10⁻³ over a longer one. The echo of Volume 19 fixes exactly this, as long as the error is steady.

### 20.3 Two imperfections together

Next, combine flaws in the two-ring gate:
- a bond error ε
- an atom detuning δ
- interaction unevenness α (0 = perfectly even, 1 = as uneven as the side-by-side geometry)

The research mapped 180 combinations. [SIMULATED]

**The surprise was how strongly single flaws are suppressed.** With the echo and smooth pulses, each flaw on its own causes error growing as its **sixth power**. Halving it cuts the error about 64-fold.

**Combined, the protection weakens sharply.** A wrong bond strength together with an uneven interaction causes error growing only as the **square** of their product. The fitted rule:

  error ≈ 0.43 × (ε × α)²  (plus smaller terms)

That gives a practical budget for the combined term:

| Error you can tolerate | Largest allowed ε × α |
|---|---|
| 1 in 100 | 0.15 |
| 1 in 1,000 | 0.05 |
| 1 in 10,000 | 0.015 |
| 1 in 100,000 | 0.005 |

Two honest notes [SIMULATED]:
- **Two simpler error models failed.** Both were proposed in advance, both failed badly on held-out data, and both are kept on record.
- **The sixth-power suppression is a property of this model and this pulse sequence,** not a law of the architecture. Nobody has yet derived why it happens.

### 20.4 When settings drift

The echo cancels hopping that is wrong but **steady**. What if the hopping strength drifts while the gate runs?

[SIMULATED] With a 5% drift during one gate:

| How the hopping changes | Infidelity | Leakage |
|---|---|---|
| Not at all (a steady 5% error) | ~0 (exact cancellation) | ~0 |
| Slow steady ramp | 39% | 0.03% |
| A jump halfway through | 81–88% | tiny |
| Half an oscillation per echo half | 94% | tiny |
| Whole oscillations within each echo half | about 10⁻⁹ to 10⁻⁸ | tiny |

**Why** [DERIVED]: the echo cancels hopping only when **both halves contain the same total amount of it**. During a long gate, each half accumulates about 90 radians of hopping phase. So even a 1% mismatch between the halves leaves almost a radian of error.

>
> **Common mistake**
> **These errors are nearly invisible.** The register stays inside its allowed states (tiny leakage) while doing almost entirely the wrong thing. The checks of Volume 21 look for escapes from the allowed states, so they would report everything fine. Stability of the hopping *during* operations is therefore a hard requirement, not a refinement.


>
> **Go deeper (optional math)**
> "Equal total hopping in each half" is exact only when the drifting part has the same form as the hopping itself (a uniform rescaling), so that the Hamiltonians at different times commute. In the tested case the drift sat on one bond, so the condition is first-order: whole-oscillation drift left residuals around 10⁻⁹ to 10⁻⁸ rather than zero. [SIMULATED]


### 20.5 Real pulses take time

The echo's flip was assumed instantaneous. Real flips take time, and the hopping keeps running during them. During a flip, each ring behaves exactly like a two-level system pushed slightly off its intended axis. That is a classic problem with classic answers. [DERIVED]

[SIMULATED] At a realistic control strength:

| Flip | Result inside the gate |
|---|---|
| Simple square pulse | Fails: about 53% infidelity |
| Smooth pulse | Fails: about 40% |
| **Composite pulse** (four timed pushes, two forward and two reverse) | **Exact**, if the interaction is uniform or switched off during the flip |
| Composite pulse with the **uneven** interaction left on | 0.7% infidelity, 6.9% leakage |

The lesson: a control pulse designed in isolation can fail once the rest of the system is running. **The uneven interaction must be off, or the pulse designed together with it.** Composite pulses are also tuned to the expected hopping strength, which brings back a small sensitivity to bond errors (about 5 × 10⁻⁵ at 5%).

### 20.6 Where to put the flips

Moving the flips changes which kinds of drift cancel. [SIMULATED]

| Flip timing | Cancels | Blind to |
|---|---|---|
| Halfway (the original echo) | Steady errors, oscillations of ½ cycle per gate | Slow ramps, jumps, 1 cycle per gate |
| At ¼ and ¾ (symmetric echo) | Steady errors, slow ramps, midpoint jumps, 1 cycle per gate | ½ cycle per gate |
| Four flips | A broader range | Leaks more with uneven interactions |

Every arrangement has a blind spot. This is well known from a technique called dynamical decoupling, which echoes generalize. Here the best tested compromise is the symmetric echo, with the interaction pulsed separately in each segment. It is about 10 times worse than the original when nothing drifts (1.4 × 10⁻⁵ against 1.7 × 10⁻⁶), but around a thousand times better against slow drift.

### 20.7 The balance rule

One more idea seemed promising: keep the interaction on continuously, and only dip it ("notch" it) around each flip.

[SIMULATED] It didn't work.
- **What was tried:** 90 notch shapes, widths and depths.
- **What they gave:** all of them landed between 1.2 × 10⁻³ and 2.8 × 10⁻³.
- **The segmented approach:** 1.4 × 10⁻⁵.
- **Depth barely mattered.**

The failure was informative. A careful check showed the error growing as the *fourth* power of the unevenness, not the sixth. That points to a specific cause [DERIVED]:
- **The shift:** the uneven interaction slightly shifts the register's energies.
- **Why it can cancel:** the shift reverses sign when the hopping reverses.
- **When it does cancel:** only if the interaction is, on average, **equally strong (squared) in both halves of the echo**.

| Interaction shape | Imbalance between halves | Infidelity |
|---|---|---|
| Separate smooth pulses per segment | 0 | 1.4 × 10⁻⁵ |
| Continuous, with notches | large (−0.95) | 1.8 × 10⁻³ |
| Flat-topped, with notches | smaller (−0.20) | 1.8 × 10⁻⁴ |
| Balanced, but with a steep notch | 0 | 4.2 × 10⁻⁴ (limited by leakage from the steep notch) |

Separate smooth pulses do everything at once: they are balanced, zero at every flip, and as gentle as possible.

### 20.8 What it all adds up to

Gathering the rules, each true **in these ideal models**:

1. **Budget errors together:** bond error × interaction unevenness ≲ 0.015 for errors of 1 in 10,000.
2. **Keep the hopping steady during operations:** the tested gate needs between-half stability of about 1 part in 10,000. This is the hardest requirement found, and the most hidden.
3. **Switch the uneven interaction off during flips,** make it uniform, or design the flips together with it.
4. **Use composite flips** at a control strength a few times the hopping.
5. **Balance the interaction across the echo's halves,** with zeros at the flips and gentle ramps.

None of these were known when the four-atom ring was first proposed. Every one came from something going wrong. They are what Volume 22 asks real hardware to meet.

### Summary

- **Single flaws are strongly suppressed** (sixth power). Combined flaws are much less so: the rule is ε × α ≲ 0.015.
- **Drifting hopping defeats the echo,** producing large, nearly invisible errors.
- **Composite flips work,** but only with the uneven interaction off or uniform.
- **Every echo timing has a blind spot.** Symmetric echoes handle slow drift best.
- **The interaction must be balanced across the echo's halves.** Separate smooth pulses do this naturally.

### Try it

1. Bond error 4%, unevenness 0.5. What error does the combined term predict? *Answer: 0.43 × (0.02)² ≈ 1.7 × 10⁻⁴.*
2. Why would a parity check miss the drift errors in 20.4? *Answer: the register stays inside its allowed states; the error is a wrong phase, not an escape.*
3. Which echo timing handles a slow ramp better, halfway or symmetric? *Answer: symmetric.*
4. Why did notches fail even at full depth? *Answer: the interaction was not balanced across the echo's halves, so the energy shift it causes didn't cancel.*


---

## Glossary Additions

*Terms used in Edition 04, with their status*


Terms used in Edition 04 that are not in Edition 03's frozen glossary ([Appendix 1](../library/A1-glossary.html)), or whose use here needs a note. **Working development terms** are provisional: they are not part of the frozen vocabulary. The development site's [register of terms](../development/register-of-terms.html) is the authoritative status list for every PhaseKeep term.

| Term | Meaning | Status | Volume |
|---|---|---|---|
| Classical correlation | Results linked because they were fixed in advance, like matched coins | Standard physics | 15 |
| Relative phase | The phase difference between two amplitudes; decides reinforcement or cancellation | Standard physics | 15 |
| Coherence | Well-defined relative phases, so interference can happen | Standard physics | 15 |
| Entanglement | A joint state that cannot be written as separate states of its parts, for a stated division into parts | Standard physics | 15 |
| Contextuality | Outcomes depend on which compatible measurements are made together; needs at least three levels | Standard physics | 15 |
| Discord | A measure of quantum correlation beyond entanglement | Standard physics | 15 |
| QDE (Quantum Dimensional Environment) | PhaseKeep's framework for a joint state space, its divisions into parts and its relationships; **not** the physical environment | Working development term | 15 |
| Convergent Quantum Relationships | PhaseKeep's classification of relationship types | Working development term | 15 |
| Spin angular momentum | Angular momentum of circular polarization | Standard physics | 16 |
| Orbital angular momentum (OAM) | Angular momentum of a twisted wavefront, ℓħ per photon | Standard physics (in Edition 03) | 16 |
| Physical family | Polarization, spatial or spectral–temporal: what light provides | Standard grouping | 16 |
| Gouy phase | Extra phase gained on focusing; depends on 2p + \|ℓ\| + 1 | Standard physics | 16 |
| Decoherence-free subspace | A set of states that a given disturbance changes only by a common phase | Standard physics | 16 |
| q-plate | Patterned optic that converts spin into twist | Standard device | 16 |
| Rydberg state | A very highly excited atomic state; strongly interacting, and decays | Standard physics | 17 |
| Optical tweezer | A focused laser beam that holds an atom | Standard technique | 17 |
| Hyperfine coupling | The magnetic link between an electron and its nucleus | Standard physics | 17 |
| Concurrence | A number from 0 to 1 measuring two-qubit entanglement | Standard measure | 17 |
| Clock states | A pair of atomic states whose splitting is insensitive, to first order, to small field changes | Standard physics | 17 |
| PK-LMI | Light–matter interface: transferring quantum information between photons and matter | Pending source reconciliation | 17 |
| PK-M | Unchanged frozen meaning: the proposed four-mode atomic-vapor memory | Frozen (Edition 03) | 17 |
| Resonant dipole–dipole exchange | Two nearby Rydberg atoms swapping their states; the source of hopping | Standard physics | 18 |
| Hopping (J) | The excitation moving between neighbouring atoms, and its strength | Standard physics | 18 |
| Ring mode | One of the four natural patterns of an excitation spread around a four-atom ring | Standard physics | 18 |
| Standing-wave code | The register built from ring modes 0 and 2 × two internal levels | Working development term | 18 |
| Staggered flip | A half-turn of phase on every second atom; swaps the standing waves | Working development term | 18 |
| Synthetic flux | A phase carried by hopping around a loop, as if a magnetic field threaded it | Standard physics | 18 |
| Gray code | An ordering in which neighbours differ in one binary digit | Standard mathematics | 18 |
| X₁X₂ = +1 code | A standard two-qubit error-detecting code; the ring's standing waves form it | Standard | 18 |
| MSR (Multispatial Register) | A persistent register described by its axis signature | Working development term | 18 |
| Axis signature | The size of each encoding axis, e.g. [2,2] for a Tetragon | Working development term | 18 |
| Trigon [3], Pentagon [5] | Single-axis three- and five-level registers | Working development terms | 18 |
| Controlled-Z (CZ) | A two-qubit gate adding phase π only when both qubits are 1 | Standard | 19 |
| Frequency planning | Giving neighbouring registers different natural frequencies so they don't interfere | Standard engineering practice | 19 |
| Echo (ring-mode echo) | Flipping halfway so the second half undoes the first half's hopping | Working development term for a standard idea | 19 |
| HOLD, ROTATE, COUPLE | Proposed register instructions | Working development terms | 19 |
| RAMM (Random Access Multispatial Matrix) | Register addressing and control; not a memory, not QRAM | Working development term | 19 |
| Infidelity | How far an operation is from the intended one (1 minus fidelity) | Standard measure | 20 |
| Leakage | Probability of escaping the register's allowed states | Standard measure | 20 |
| Composite pulse | A sequence of timed pushes designed to cancel a systematic error | Standard technique | 20 |
| Dynamical decoupling | Using repeated flips to cancel slow disturbances | Standard technique | 20 |


---

## Ledger Additions

*Every number in Edition 04, its evidence tag and where it came from*


Every number used in Volumes 15–17, with its evidence tag and where it came from. Numbering continues the idea of Edition 03's ledger ([Appendix 2](../library/A2-ledger.html)) with a new prefix, **E4-**, so no Edition 03 identifier is reused.

| ID | Number | Meaning | Tag | Source |
|---|---|---|---|---|
| E4-01 | 50/50, +1, +1/−1/0, 1/1/½ | Bell-state comparison table (15.3) | [DERIVED] | Standard two-qubit algebra |
| E4-02 | 16, 6, 4, 30 | Two-Tetragon dimension, pairs, triples, real parameters (15.8) | [DERIVED] | Counting; 2·16 − 2 = 30 |
| E4-03 | ≥ 3 levels | Minimum dimension for contextuality (15.6) | [REPORTED] | Kochen–Specker; Mermin 1990 (abstract) |
| E4-04 | 1.02, 1.25, 1.47 × 10⁻²⁷ kg·m/s | Photon momentum at 650, 532, 450 nm (16.1) | [DERIVED] | p = h/λ |
| E4-05 | 461, 564, 666 THz; 1.91, 2.33, 2.76 eV | Frequency and energy at the same wavelengths (16.1) | [DERIVED] | f = c/λ, E = hc/λ |
| E4-06 | 2p + \|ℓ\| + 1 | Gouy phase dependence (16.4) | [DERIVED] | Standard Laguerre–Gauss beam formula |
| E4-07 | 2θ, 4θ, θ, 2θ | Rotation phases for ±1, ±2, 0/+1 and circular polarization (16.5) | [DERIVED] | Phase ℓθ (and sθ for spin) |
| E4-08 | about 1,000 atoms; 60S, 59P, 59S | Experiment setup (17.3) | [REPORTED] | Jiao et al. 2025, full text §III |
| E4-09 | 18.51 GHz, 18.23 GHz | Microwave transition frequencies (17.3) | [REPORTED] | Jiao et al. 2025 |
| E4-10 | < 1.8 µs | Complete sequence time (17.3) | [REPORTED] | Jiao et al. 2025 |
| E4-11 | 0.45 ± 0.05 | g⁽²⁾(0) single-excitation measure (17.3) | [REPORTED] | Jiao et al. 2025 |
| E4-12 | 47.1%, 38.6%, 14.2% | Measured level populations (17.3) | [REPORTED] | Jiao et al. 2025 |
| E4-13 | 10–100 µs, ~123 µs, 406 µs | Rydberg lifetimes: typical alkali; 55P at room temperature; 55P at 4 K (17.2) | [REPORTED] | Jiao et al. 2025 (typical range); arXiv:2602.05959 (55P), summary level |
| E4-14 | 1/√(1 + x²) and the table values | Concurrence of the middle states versus field ratio x = b/A (17.5) | [DERIVED] | Two-spin hyperfine model |
| E4-15 | +2J, 0, −2J, 0 | Ring-mode energies (18.2) | [DERIVED] | 2J cos(πℓ/2) |
| E4-16 | ±0.5 | Currents of modes 1 and 3 at zero flux, model units (18.2) | [SIMULATED] | `code/atomic-register/ring_gauge.py` |
| E4-17 | 0 | Leakage of the staggered flip on the code (18.4) | [SIMULATED] | `lie_check.py`, `ring_chiral.py` |
| E4-18 | 7, 9, 63 of 63 | Control directions reached with/without hopping (18.5) | [SIMULATED] | `ring_lie.py` |
| E4-19 | ±1.41J, ±0.35 | Flux-π energies and currents (18.6) | [SIMULATED] | `ring_gauge.py` |
| E4-20 | ≲ 2.5 × 10⁻¹⁵ | Ring/hypercube ↔ independent-rotation equivalence residuals (18.7) | [REPORTED] | Independent re-run by a separate AI assistant; script not in the repository |
| E4-21 | 1, 2, ½; 1.5 | Forbidden and best hopping ratios (19.2) | [DERIVED] | Energy-coincidence analysis |
| E4-22 | 100%, 3.9%, 3.0%, 2.4%, 100% | Worst leakage at ratios 1, 1.425, 1.5, 1.575, 2 (v/J_B = 0.05, D = 2) (19.2) | [SIMULATED] | `two_ring.py` |
| E4-23 | 2.2 × 10⁻², 2.3 × 10⁻⁶ | Final leakage, abrupt vs sin² at equal time (19.3) | [SIMULATED] | `two_ring_shaped.py` |
| E4-24 | 98.22% → 99.989% | Gate fidelity without/with echo (19.4) | [SIMULATED] | `two_ring_echo.py` |
| E4-25 | ~10⁻¹⁴ | Echo cancellation with 10% bond error, uniform interaction, incl. state-dependent hopping (19.4) | [SIMULATED] | `echo_combined.py`, `echo_statedep.py` |
| E4-26 | 8 / 3 qubits; 16 / 6; 8 gates; 0 gates; 1 CZ | Encodings and costs (19.6) | [DERIVED] | Volume 18 mapping; `ref01_onehot.py` |
| E4-27 | 130 → 36 CNOT per slice; 2,304 total | Physical-interaction emulation cost (19.6) | [REPORTED] | Independent re-run; script not in the repository |
| E4-28 | 0.1 x²; 2 × 10⁻³ | Single-flaw leakage; 1% bond error over T = 10/J (20.2) | [SIMULATED] | `ref_tolerance.py` |
| E4-29 | sixth power; 0.43(εα)²; 0.15, 0.05, 0.015, 0.005 | Coupled-imperfection fit and budget (20.3) | [SIMULATED] | `p2cim.py`, `p2cim_analyze.py` |
| E4-30 | ~0, 39%, 81–88%, 94%, 10⁻⁹–10⁻⁸ | Drift results (20.4) | [SIMULATED] | `e5_drift.py` |
| E4-31 | ~90 rad | Hopping phase per echo half in the gate (20.4) | [DERIVED] | 2J·T_seg with T_seg ≈ 31/J |
| E4-32 | 53%, 40%, exact, 0.7% / 6.9%, 5 × 10⁻⁵ | Finite-flip results (20.5) | [SIMULATED] | `e6_flips.py` |
| E4-33 | 1.4 × 10⁻⁵ vs 1.7 × 10⁻⁶; ~1,000× | Symmetric vs original echo (20.6) | [SIMULATED] | `e7_timing.py` |
| E4-34 | 1.2–2.8 × 10⁻³; 4th power; table values | Notch results and balance comparison (20.7) | [SIMULATED] | `e7d_notch.py`, `e7d_followup.py` (follow-up confirmation pending at publication of the atomic-register checkpoint) |


---

## Sources Additions

*What was read for Edition 04, and how closely*


What was read for Volumes 15–17, and how closely. Edition 03's sources are in [Appendix 3](../library/A3-sources.html). **Reading levels:** *full text* (the paper body was read), *abstract or summary* (only the abstract or an indexed summary), *unverified* (cited from memory; must be checked before being relied on).

| Topic | Source | Reading level | Used in |
|---|---|---|---|
| Single photonic qutrit in a Rydberg polariton | Jiao, Hughes, Festenstein, Bai, Zhao, Li, Weatherill, Adams, *Phys. Rev. Research* **7**, 033267 (2025), doi:10.1103/3xnw-cpj2 | Full text, sections I–IV | 17.2, 17.3 |
| Kochen–Specker simplification | Mermin, *Phys. Rev. Lett.* **65**, 3373 (1990) | Abstract | 15.6 |
| Quantum discord | Ollivier and Zurek, *Phys. Rev. Lett.* **88**, 017901 (2001) | Abstract | 15.6 |
| Spin-to-orbital angular momentum conversion | Marrucci, Manzo and Paparo, *Phys. Rev. Lett.* **96**, 163905 (2006) | Abstract | 16.6 |
| Spin–orbit hybrid states in photons | arXiv:1103.3962 (listed in the development site's QDE literature) | Abstract | 15.5 |
| Cryogenic Rydberg lifetimes | arXiv:2602.05959 (55P₃/₂, 406 µs at 4 K) | Summary | 17.2 |
| Alignment-free communication with spin–orbit states | D'Ambrosio et al. (2012), as recalled | **Unverified** | 16.5 |
| Single-photon CNOT between polarization and OAM | quant-ph/0402208 (listed in the development site's literature page) | Abstract | 16.6 |
| Excitation hopping in a chain of Rydberg atoms | Barredo et al., *Phys. Rev. Lett.* **114**, 113002 (2015), arXiv:1408.1055 | Summary | 18.1 |
| Strength and local control of dipolar exchange | de Léséleuc et al. (2017), arXiv:1705.03293 | Summary | 18.1 |
| Superconducting ring with synthetic flux | Roushan et al., *Nat. Phys.* **13**, 146 (2017), arXiv:1606.00077 | Summary | 18.6 (context) |
| Simulation scripts for Volumes 18–20 | `code/atomic-register/` in this repository | Run and reproduced, except the two E7-D follow-up runs still pending independent confirmation | 18–20 |

The development site's [literature page](../development/literature.html) is the single entry point to every source list in the project.


---

## Edition 04 Notes

*What this edition is, how it relates to the frozen Edition 03, and what comes next*


### What this edition is

Edition 04 continues the PhaseKeep learning library from Volume 15. It is a **working draft** and a **dated research snapshot as of 28 November 2026**. It describes the research up to that date; later findings go into a later edition or revision, recorded in a revision log like the one below, never as silent edits.

### How it relates to Edition 03

| | Edition 03, Revision H | Edition 04 |
|---|---|---|
| Status | **Frozen** baseline, including its vocabulary | Working draft |
| Contents | Start Here, First Words, Volumes 1–14, Appendices 1–6 | Volumes 15 onward, Appendices 7 onward |
| Files | `library/` (never edited) | `library-edition-04/` |

Edition 04 links back to Edition 03 rather than repeating it. Edition 03's numbering is not reused: ledger rows use the prefix **E4-**, and appendices continue from 7.

### Vocabulary

Edition 03 froze its core vocabulary and set a rule: a new term needs a literature check and a demonstrated purpose before it is added ([Appendix 6](../library/A6-edition-notes.html)). Edition 04 follows that rule:
- **Physics first:** each volume explains the physics before naming it.
- **New names stay provisional:** terms introduced after Edition 03 (for example QDE) are **working development terms**, marked as such in Appendix 7.
- **Frozen meanings are untouched:** PK-M remains the four-mode atomic-vapor memory proposal, and PK-E the prepared-instruction execution scheme.

### Revision log

- **Release 1** (28 November 2026): Volumes 15–17 and Appendices 7–10. Volumes 18–22 are planned:
  - **18:** the four-atom ring
  - **19:** making registers talk
  - **20:** when things go wrong
  - **21:** checking without breaking, part 2
  - **22:** which machine could build it

  A second workbook will add exercises and the runnable models.
- **Release 2** (28 November 2026): Volumes 18–20 added: the four-atom ring; making registers talk; when things go wrong.
  - **Glossary, ledger and sources:** Appendices 7–9 extended (ledger rows E4-15 to E4-34).
  - **Correction to Volume 17:** individual atoms do have electronic orbital angular momentum. What they cannot hold is a phase pattern spread across separate atoms.
  - **Still planned:** Volumes 21–22 and the second workbook.

### How this edition was checked

- **Numbers:** every number appears in Appendix 8 with its tag and source. Derived numbers were recomputed when written; reported numbers cite the reading level in Appendix 9.
- **Corrections carried over** from the development site:
  - circulating currents do not require synthetic flux; flux splits their energies
  - photons themselves do not undergo atomic decay; excited atoms do
  - the 2025 Rydberg experiment did not store an encoded multi-level photon
- **Further review:** independent review by Codex is part of publishing this edition.

### Authorship and licence

By Tyler O'Bryan, PhaseKeep Research. AI-assisted research, documentation and numerical analysis. Text CC BY 4.0; code MIT; see `NOTICE.txt`. Cited works remain the work of their authors and are summarized in our own words.
