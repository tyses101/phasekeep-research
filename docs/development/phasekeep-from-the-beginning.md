# PhaseKeep from the beginning

**Status: educational overview, research snapshot as of 2026-11-28.** This page tells the whole PhaseKeep story, from the first question to today, in plain words. It adds no new results: every statement summarizes a page linked under "Read more", where the evidence labels and details live. **No PhaseKeep hardware has been built or measured, and no advantage has been shown.**

## Contents

1. [The question](#1-the-question)
2. [Light as an information carrier](#2-light-as-an-information-carrier)
3. [Checking without breaking](#3-checking-without-breaking)
4. [What the first computational checkpoints found](#4-what-the-first-computational-checkpoints-found)
5. [Relationships, not just properties](#5-relationships-not-just-properties)
6. [Why we looked beyond photon-only execution](#6-why-we-looked-beyond-photon-only-execution)
7. [The four-atom ring](#7-the-four-atom-ring)
8. [Making registers work together](#8-making-registers-work-together)
9. [What went wrong, and what it taught us](#9-what-went-wrong-and-what-it-taught-us)
10. [What machine could build it](#10-what-machine-could-build-it)
11. [What is and is not claimed](#11-what-is-and-is-not-claimed)
12. [What comes next, and how to check our work](#12-what-comes-next-and-how-to-check-our-work)

## 1. The question

A quantum computer stores information in fragile physical states. Those states must be prepared, changed on purpose, kept intact while waiting, and checked without destroying them.

PhaseKeep asks whether the **shape** of a quantum system (which properties it has, how they are arranged, and how they can interact) can be organized so that those jobs become cheaper, more reliable or easier to verify. The same question runs through every stage below. Only the physical system changes.

**Read more:** [central question](central-question.md), [research status](research-status.md).

## 2. Light as an information carrier

**The physics first.** A single particle of light, a photon, carries several independent properties at once:
- **Polarization:** which way its electric field oscillates, for example horizontal or vertical.
- **Orbital angular momentum (OAM):** how its wavefront twists, for example one turn to the left or to the right.

Because the two are independent, one photon can hold two choices at once: 2 × 2 = 4 combinations. In quantum mechanics it can also hold superpositions of those four, which is where both the power and the fragility come from.

**PhaseKeep's names.** The project calls each independent property an **Encoding Axis**. It calls the organized use of several axes **Geometric Encoding Axies (GEA)**. A photon holding four combinations is a **Tetragon**. Operations that change the encoded information on purpose are **Controlled Transformations (CT)**. These terms are frozen in the learning library.

**What we learned.** Most operations on a single photon are easy, because one optical element acts on one property. Making two photons influence each other is hard, because photons pass through each other without interacting. Getting them to interact needs extra resources, and it often only works some of the time.

**Read more:** the frozen [learning library](../../library/markdown/00-start-here.md) (Edition 03, Rev H), especially Volumes 1–6; [Tetragon](tetragon.md); [GEA](gea.md).

## 3. Checking without breaking

**The physics first.** Measuring a quantum state directly usually destroys the information it carries. An unknown quantum state also cannot be copied (the no-cloning theorem). So "make a backup and compare" is impossible. Instead, a helper system can test one *property* of the data without reading the data itself. A typical test asks "is the number of flips even?"; this is called a parity check.

**PhaseKeep's names.** The **Buddy System** is the proposal to use helper resources (Buddies) to prepare, assist and check data. A **Buddy Check** reports PASS, FAIL or UNKNOWN. **Integrated Quantum Assurance (IQA)** is the broader framework for keeping information intact during computation.

**The central lesson:** **detection is not verification.** A PASS confirms only the property that was checked. Some errors, such as a slightly wrong rotation angle, pass every check.

**Read more:** [Buddy](buddy.md), [IQA](iqa.md), library Volume 7.

## 4. What the first computational checkpoints found

Eleven checkpoints (V0 to V1.0), then a set of 31 explorations (S01–S31), tested these ideas in ideal models with simulated faults.

**The geometry line (V0 to V0.3).**
- Moving between ordinary and entangled encodings always costs an entangling operation.
- Switching encodings adaptively doesn't save operations for one logical qubit.
- Equivalent routes are not independent routes.

**The verification line (V0.4 to V1.0).**
- A parity check misses phase errors, and its own faults can make results less reliable.
- Silence from a detector is not a PASS once loss exists.
- Extra "flag" helpers push silent damage to a higher order, but don't remove it.
- Whether a failed two-photon interaction disturbs the data may decide whether checking helps at all.
- In some physical profiles, no verification configuration works.

**The explorations (S01–S31).**
- Flagging pays only below a critical ratio of idle errors to gate errors.
- Which design looks best depends on the metric chosen.
- Moving logical information to a separate, quieter register can help, but only if that register really is quieter and two-photon operations are nearly perfect.

**Read more:** [timeline](timeline.md), [negative results](negative-results.md), [physical feasibility](physical-feasibility.md), [explorations review](../../explorations/consolidated-review.md).

## 5. Relationships, not just properties

**The physics first.** Two quantum systems can share information that is not in either one alone. Picture two photons that each look completely random when measured on their own, yet whose results always agree, or always disagree, depending on how they are measured.

That information lives in the *relationship*:
- relative phase
- coherence
- entanglement
- correlations

Several different joint states can have identical statistics for each part, and differ only in how the parts relate.

**PhaseKeep's names.** The **Quantum Dimensional Environment (QDE)** is the provisional framework for describing the joint state space and these relationships. **Quantum Interaction Junction (QIJ)** describes the physical processes where carriers meet. **Alternating Stacked Verification (ASV)** is a provisional verification pattern within IQA.

**What we learned.** Some protection comes from symmetry. For example, combinations of polarization and twist whose angular momenta cancel are unchanged by a rotation of the whole beam. But that protection is specific to one disturbance: the same combination is not protected against other effects, such as birefringence.

**Read more:** [QDE framework](qde-relational.md), [QDE checkpoint](checkpoints/qde-2026-11-27.md).

## 6. Why we looked beyond photon-only execution

Photons are excellent for *moving* information: they travel far and fast with little disturbance. They are poor for *holding and processing* it:
- they are hard to store for long
- they are easily lost
- they barely interact with each other

The verification checkpoints kept running into exactly those costs: two-photon interactions that only sometimes work, and loss that silently removes helpers or data.

Matter offers what photons lack. Atoms can sit in one place, keep a state for a while, and interact strongly when excited to high-energy (Rydberg) states. So the research asked a different question: what if information is held and processed in atoms, with light used to move it? That makes the **light-matter interface** (PK-LMI) central.

It also brings a new limitation. **Excited atoms decay.** A Rydberg-excited atom returns to a lower state on a timescale of microseconds to milliseconds. That's a property of the atoms, not of the photons.

**What we learned from a published experiment.**
- **What it did:** a cold-atom experiment stored a single photon in a cloud of atoms, then used microwaves to prepare a three-level quantum state inside the cloud.
- **What it did not do:** store an arbitrary incoming encoded state.
- **Why it matters:** the distinction is important, and easy to blur.

**Read more:** [atomic-register physical development](atomic-register/02_the_full_story/03_physical_development.md), [physical feasibility](physical-feasibility.md).

## 7. The four-atom ring

**The physics first.** Imagine four atoms on the corners of a square, and one excitation that can hop from atom to atom. The excitation can spread around the ring in a few distinct patterns, called ring modes. Two of these patterns are "standing waves", like the vibrations of a guitar string. A simple control (flipping the phase of every second atom) swaps those two patterns exactly. Each excitation can also be in one of two internal energy levels.

So each ring holds four useful combinations: two patterns × two levels. That's the same count as the photonic Tetragon, now held in matter.

**What we found** (in ideal simulation):
- **Hopping is essential.** Controls that act on one atom at a time can't give full control. Letting the excitation hop between atoms makes full control possible.
- **An honest surprise.** Written in the right variables, the four-atom ring behaves *exactly* like two ordinary qubits on the corners of a square, and the two patterns form a standard error-detecting code. That means **the ring is not a new kind of quantum bit.** It is a known structure, built in a particular physical way.
- **How it grows.** The natural way to grow it is a cube or a hypercube, not a bigger ring.

**PhaseKeep's names.**
- **Multispatial Register (MSR):** a persistent register described by its axis signature (the Tetragon is [2,2]).
- **Random Access Multispatial Matrix (RAMM):** the layer that addresses and controls registers. It is not a memory.

Both are working development terms, not frozen vocabulary.

**Read more:** [register geometry](atomic-register/02_the_full_story/02_register_geometry.md), [architecture](atomic-register/02_the_full_story/01_architecture.md).

## 8. Making registers work together

**The physics first.** Two rings can be made to influence each other through an interaction that acts only when both excitations are in a particular energy level. Used carefully, that produces a standard two-qubit gate. But each ring's own hopping keeps running in the background, and real hopping strengths are never exactly what we intend.

A simple trick fixes much of that:
- **The echo:** halfway through, flip the phase pattern on every second atom. That reverses the direction of all hopping, so the second half undoes the first. For hopping that is wrong but *steady*, the cancellation is exact.
- **Different rates per ring:** giving neighbouring rings different hopping rates (a ratio near 1.5, avoiding 1 and 2) keeps them from exchanging their contents by accident.

**PhaseKeep's names.** Three proposed instructions:
- **HOLD:** stand still, with hopping cancelled.
- **ROTATE:** let hopping act on purpose.
- **COUPLE:** interact two registers while hopping cancels.

**Read more:** [RAMM instructions](atomic-register/02_the_full_story/05_ramm_instructions.md), [digital reference](atomic-register/02_the_full_story/04_digital_reference.md).

## 9. What went wrong, and what it taught us

Failures are kept on purpose. Each one moved the design forward.

| What we tried | What happened | What it taught us |
|---|---|---|
| A single parity Buddy Check | Missed phase errors; its own faults could hurt | Detection is not verification |
| Flag helpers | Removed only first-order silent damage | Protection has orders; each costs something |
| Microwave + Raman control of atom-cloud patterns | Incomplete, and it leaked | The ring needs hopping, not only local control |
| Energy "confinement" of unwanted patterns | Fixed leakage, but left phase errors and had no physical source | Change the geometry, not just the energies |
| Equal hopping in neighbouring rings | Complete leakage | Frequency planning: ratio near 1.5 |
| Combined imperfections | Much worse than separate ones (hopping error × unevenness ≲ 0.015) | Errors must be budgeted together |
| Hopping that drifts during an operation | Up to ~94% error, invisible to our checks | The echo needs balanced halves; stability matters |
| Real (finite) control pulses with the interaction on | Leakage and errors | Switch the uneven interaction off, or design both together |
| Smooth or notched interaction envelopes | Worse than simple segments | The interaction must be balanced across the echo's halves |

**Read more:** [negative results](negative-results.md), [all atomic-register failures](atomic-register/03_reference/evidence_and_failures.md), [errata](errata.md).

## 10. What machine could build it

The design is now written as a target set of interactions. Several kinds of hardware could, in principle, provide them:
- **Atoms in tweezers, excited to Rydberg states.** The original target. They provide strong exchange, but **excited-state decay is the biggest obstacle**. In the models, decay outweighs every carefully tuned error by a large margin.
- **Long-lived "circular" Rydberg states.** These help only if a theoretical suppression of their decay is realized; their exchange is much weaker.
- **Trapped ions.** They show the right kind of hopping. The relevant numbers still need retrieving.
- **Superconducting circuits.** They have already built a three-site ring with the right kind of control, so they are the closest demonstrated match. Their numbers still need retrieving.

**A cheaper first test.** The two-ring operation reduces to a single standard gate on six qubits, so the logic can be tested on existing cloud quantum computers before any new hardware exists. Nobody has run that test yet.

**Read more:** [platforms](atomic-register/02_the_full_story/12_platforms_G0.md).

## 11. What is and is not claimed

**Supported:** mathematical derivations, and simulated behaviour inside stated ideal models.

**Not established:**
- a new computational primitive
- any quantum advantage
- better resource efficiency
- fault tolerance
- a working quantum memory
- any hardware performance
- the originality of individual mechanisms

**Where a contribution might lie:** in the physical embedding, the integration of register, control and checking into one architecture, and testable tolerance rules. All of these still need a prior-art review.

**Read more:** [scientific framing](atomic-register/02_the_full_story/14_framing.md).

## 12. What comes next, and how to check our work

**Next:**
- verify and record the pending reproduction checks
- run the six-qubit gate in noisy simulation, then on hardware
- design pulses and interaction together
- model decay and loss realistically
- build logical error protection
- retrieve real platform numbers

**Check our work:**
- Every result has a script. See [reproducibility](reproducibility.md) and the [atomic-register reproduction guide](atomic-register/03_reference/reproduce.md).
- Corrections are welcome. See [contributing](contributing.md).

**Read more:** [open problems](open-problems.md), [atomic-register pending research](atomic-register/02_the_full_story/13_pending.md).
