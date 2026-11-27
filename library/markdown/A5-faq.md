# Questions and Misconceptions

*Straight answers to the questions people ask first*


Short answers to the questions people ask first. Each points to the volume with the full story.

## Big picture

**Is PhaseKeep a quantum computer?**
No. It is a research proposal. No PhaseKeep hardware has been built or measured. (Start Here)

**Is it faster than a normal computer?**
Not established, and not claimed. A classical controller choosing which operations to apply does not by itself give an advantage. (Volumes 6 and 10)

**What is actually new here?**
Mostly organization: EA (what carries information), GEA (how the states are arranged), CT (how they change), the Buddy System (how success is checked) and the evidence tags. Underlying physics is standard. Whether the organization helps is open. ([Volume 13](13-wider-field.md))

**Who has checked this?**
The numbers have been recomputed by scripts, and the herald result was rerun by a second party. None of it has had independent peer review. ([Volume 9](09-research-lab.md))

## Light and states

**Is the square physical?**
The four corners are mathematical (a map of addresses). The beam shape, polarization pattern and the bench layout are physical. Four kinds of geometry are in play. ([Volume 4](04-geometric-encoding.md), section 4.7)

**Does the photon have four bits?**
No. It has four possible addresses, which carry two bits when read out directly, and one reading returns one address. The *state* is richer than any one reading, but you cannot read all of it. (Volumes 2 and 3)

**Why can't you just copy a quantum state to protect it?**
The no-cloning theorem forbids copying an unknown state. Known recipes can be rebuilt; unknown results cannot. ([Volume 2](02-quantum-states.md))

**What is the difference between an edge blend and a diagonal blend?**
An edge blend can be written as one polarization times one twist blend; a diagonal blend cannot, and gives a beam whose polarization varies around the axis. ([Volume 4](04-geometric-encoding.md), section 4.8)

**Can a single four-level photon compute something a classical computer cannot?**
No. Four amplitudes and 4 × 4 operations are trivial to simulate. The Tetragon can test how cheaply operations are done, not computing power. Any advantage would have to come from scaling and multi-photon interaction. ([Volume 11](11-experiments.md), section 11.4)

**Why is high-dimensional entanglement the cornerstone?**
It is the quantum resource the other parts organize, change and protect, and the first target is two entangled Tetragons (up to 2 ebits). It is a project framing, not a result, and entanglement alone is not a computing advantage. (Start Here; [Volume 6](06-two-photons.md), section 6.7)

**What is the State Space Environment?**
The physical resources and control that make the mathematical state space usable, with their losses, costs and timing. It is a name for the whole stack, not a new pillar. ([Volume 10](10-intelligent-registers.md), section 10.5)

**Is a line on the square the path a state travels?**
No. A line marks a two-address subspace. Inside it the amplitudes and relative phase can change continuously. ([Volume 4](04-geometric-encoding.md), section 4.10)

**Can geometry make a computation more powerful?**
It cannot add capability. It can change the *cost* of an operation if useful relationships line up with operations that are easy to perform. That is a hypothesis, tested only in one narrow simulation. ([Volume 10](10-intelligent-registers.md), section 10.7)

**Is "twist" the same as polarization?**
No. They are separate properties of the same light, which is why they can be combined as two axes. ([Volume 1](01-light.md))

## Operations and gates

**Why does "controlled" not mean "conditional"?**
In PhaseKeep, a Controlled Transformation is one we can set and repeat. A conditional operation, one that depends on another qubit, is a kind of CT. ([Volume 5](05-controlled-transformations.md))

**Why do photons need helpers to interact?**
They ignore each other. Published gates use extra photons and keep only the attempts that look right. ([Volume 6](06-two-photons.md))

**What does 1/8 mean?**
The published gate's theoretical success rate: 1/4 × 1/2. The rest of the attempts are discarded. ([Volume 6](06-two-photons.md))

**What is a false herald?**
A success signal that fires when the output is not valid. In our reconstruction it happens 0.25 of the time, against 0.125 for valid outputs. ([Volume 7](07-buddy-checks.md))

## Checking and memory

**What does PASS / FAIL / UNKNOWN mean?**
PASS needs demonstrated evidence, FAIL needs demonstrated evidence the other way, and UNKNOWN is the honest default. A detector click is not evidence of success by itself. ([Volume 7](07-buddy-checks.md))

**Does the false-herald result mean the published experiment is wrong?**
No. It describes our reconstruction with ideal detectors. The published experiment relies on post-selection, and the mapping to its apparatus is still pending (A02). ([Volume 7](07-buddy-checks.md))

**What is "occupancy-valid"?**
Exactly one photon in each computational output register. It is not state fidelity. ([Volume 7](07-buddy-checks.md))

**Why is almost every number a loss number?**
Because photons are lost at every device, and loss multiplies along the chain. ([Volume 8](08-memory-and-loss.md))

**Why are there three different benchmark numbers (0.40, 0.25, 0.482253)?**
They belong to different tests: hidden random states, an entangled target, and a known set of coherent states. Do not mix them. ([Volume 8](08-memory-and-loss.md))

## Using this library

**How do I check a number?**
Look it up in the Ledger ([Appendix 2](A2-ledger.md)), then run the matching program in the `code` folder. ([Volume 14](14-workbook.md))

**What do the coloured tags mean?**
They say how much weight a claim bears: DERIVED, REPORTED, SIMULATED, ASSUMED, PROPOSED, MEASURED (none yet), UNVERIFIED, BLOCKED. (Start Here)

**How can I contribute a correction?**
Send the exact claim, its tag, the assumptions, the derivation or source and a reproducible procedure. Negative results are welcome. ([Volume 11](11-experiments.md))


---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*
