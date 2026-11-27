# Start Here

*What PhaseKeep is, how to read this library, and how we keep ourselves honest*


## PhaseKeep in one paragraph

Light can carry information in more ways than "on" and "off". A single photon, the smallest piece of light, can be polarized in different directions and can have a twisting wavefront, and each of these properties can hold part of a message. PhaseKeep proposes using two such properties together so that one photon carries one of four addresses, then changing that information with ordinary optical parts, and finally checking that the result is still good before using it again. The proposal rests on two ideas, and everything else in the project is meant to serve them. Underneath both sits one scientific resource, high-dimensional entanglement, described just below.

>
> **Key idea**
> **The two pillars.**
>
> **GEA, Geometric Encoding Axies**: a way of organizing the possible states as the corners of a square, cube or higher-dimensional shape, so that "change this one property" becomes a clear step along one edge.
>
> **The Buddy System**: a way of preparing helper photons and, crucially, *checking* that an operation worked before continuing, because in optics the signal that says "success" is not always telling the truth.


## The cornerstone: high-dimensional entanglement

Under the two pillars sits one scientific foundation, adopted by the project owner: **high-dimensional entanglement**. Entanglement is a tie between two systems so strong that the pair has a state neither has alone. "High-dimensional" means each system has more than two levels. The first target is two entangled Tetragons, one on each photon: four addresses each, 16 joint states, and up to two ebits of entanglement (an ebit is the entanglement of one maximally entangled pair of two-level systems). [Volume 6](06-two-photons.md) explains it.

| Part | Role |
|---|---|
| High-dimensional entanglement | The fundamental quantum resource |
| GEA | Geometric organization of the information |
| State Space Environment | The configurable physical-plus-control setting that supports the relationships |
| Controlled Transformations and high-dimensional gates | Changing states and correlations, within and between registers |
| Intelligent register compilation | Choosing useful configurations and operations |
| Buddy System | Assistance, verification, preservation and continuation |

This table restates roles. It adds no new pillar, and it is a proposed framing [PROPOSED]. The physics of high-dimensional entanglement is established research that PhaseKeep did not invent. What PhaseKeep adds is an organized, checked way of using it, and that part is untested.

>
> **Common mistake**
> **Entanglement is a resource, not a result.** Highly entangled states can be easy for a classical computer to simulate, and one four-level photon is always easy. A computing advantage would have to be shown by measurement against the best classical method. None has been, and nothing at PhaseKeep has been measured yet. The hard parts are in Volumes 6 to 8: making two photons interact on demand, knowing that it worked, and keeping the result.


## Why anyone would try this

A quantum computer's difficulty is rarely the arithmetic. It is keeping fragile information alive through many steps. Light is attractive because photons travel without much disturbance and optical parts are mature technology. Light is difficult because photons almost never interact with each other, so making two photons do something together takes cleverness, and because photons get lost. PhaseKeep is a bet that careful bookkeeping of encoding (GEA) and checking (Buddy) can make an optical approach more manageable. It is a bet, not a result.

**Figure.** The PhaseKeep pipeline. Each volume in this library covers one or two boxes.

*Picture description:* Six boxes in a row joined by arrows: Source, Prepare, Encode (EA), Transform (CT), Buddy Check, Continue or measure. Source and Prepare are familiar laboratory technology, Encode and Transform are proposed but built from existing parts, and Buddy Check is unresolved. A dashed line beneath says time is a clock for the whole machine, not one of the carriers.

>
> **In plain words**
> **New to all of this?** Read [First Words](00b-first-words.md) next. It explains every background word, from "photon" to "fidelity", in plain language before any mechanics appear.


## What is established and what is not

| Question | Where we stand |
|---|---|
| Can we carry four addresses on one photon using polarization and a twist? | The mathematics is [DERIVED]. Preparing and reading both properties is standard lab technique, but PhaseKeep itself has not done it ([PROPOSED] for our build). |
| Can ordinary optics change those properties? | Yes for polarization (waveplates). For the twist, devices exist ([REPORTED]), but each has trade-offs we checked on paper. |
| Can two photons be made to interact on demand? | A published experiment did it with help from two extra photons and a lot of discarded attempts ([REPORTED]). Success was 1 in 8 in theory. |
| Can we tell the interaction worked, without destroying the photons? | **Unresolved.** In our computer model of the published design, the success signal was wrong two times out of three for some inputs. See [Volume 7](07-buddy-checks.md). |
| Can a memory store the photon's state? | Not shown for our encoding. [Volume 8](08-memory-and-loss.md) explains the thresholds. |
| Is any of this faster than a normal computer? | **Not established, and not claimed.** |

## The honesty system: evidence labels

Every claim and number in this library carries one of these labels, so you always know how much weight it can bear.

| Label | Meaning |
|---|---|
| [DERIVED] | Worked out mathematically from stated assumptions; where we say so, checked by running code. |
| [REPORTED] | A published source says so. We say how much of the source we read. |
| [SIMULATED] | The output of a computer model. Only as good as its inputs. |
| [ASSUMED] | An input we chose, not a measurement. |
| [PROPOSED] | A design or idea. Not shown to work. |
| [MEASURED] | Measured by PhaseKeep in a lab. **None yet.** |
| [UNVERIFIED] | Supplied to us or remembered, and not checked. |
| [BLOCKED] | Cannot move forward without something we lack. |

>
> **Common mistake**
> A computer simulation passing its own checks tests the *model*, not the laboratory. A published experiment is not the same as a working PhaseKeep capability. We keep these apart on purpose.


## How each volume is laid out

Every volume uses the same boxes.

>
> **In plain words**
> **In plain words** restates the idea with no jargon.


>
> **Key idea**
> **Key idea** is the one thing to remember.


>
> **Go deeper (optional math)**
> **Go deeper** holds optional math and detail. Skip freely.


>
> **Try it**
> **Try it** is a small exercise with the answer at the end of the box or the volume.


>
> **Common mistake**
> **Common mistake** flags a misunderstanding that is easy to make.


>
> **Evidence status**
> **Evidence status** lists the labels for what the volume claimed.


## A short vocabulary to carry with you

These four words are used throughout; each is explained again where it first matters. The background words are in [First Words](00b-first-words.md), and the project terms are in the [Glossary](A1-glossary.md).

| Word | Short meaning |
|---|---|
| **EA** (Encoding Axes) | The physical properties of light chosen to carry information, such as polarization and twist. |
| **CT** (Controlled Transformation) | A physical operation we can control that changes the encoded information. "Controlled" means adjustable, not "conditioned on another qubit". |
| **Herald** | A detector click that is supposed to announce that an operation succeeded. |
| **Buddy Check** | A test that decides whether it is safe to continue, with three possible answers: pass, fail, or unknown. |

Time is a clock for the machine. It is **not** one of the encoding properties in the current design.

## A note on names

You will meet playful names, such as the Tetragon for a four-state register. They are labels for mathematical structures, not new kinds of hardware. The same goes for PQGS (Photonic Quantum Geometric Superpositions), a descriptive term for the structured superpositions the project studies; it is explained in [Volume 4](04-geometric-encoding.md) and is not a third pillar. Earlier working vocabulary (PTEA and TV) has been replaced by EA and CT.

>
> **Evidence status**
> Established by this volume: nothing new physically. It sets the rules for reading the rest.



---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
