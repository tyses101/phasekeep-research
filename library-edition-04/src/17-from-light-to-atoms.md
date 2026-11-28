# From Light to Atoms

::: plain
Photons are superb messengers and poor storage. This volume explains:
- why the PhaseKeep research looked beyond doing everything with photons
- what atoms offer
- what a real atomic experiment did, read carefully
- the new problem atoms bring: excited atoms do not stay excited for long
:::

## 17.1 Why look beyond photon-only execution

Edition 03 and the computational checkpoints kept meeting the same three costs.

- **Photons are hard to keep.** Light moves at the speed of light, so a photon is stored only by delaying it (in loops of fibre, for example) or by handing its information to matter.
- **Photons are easily lost.** Every component, fibre and detector loses some photons. The checkpoints found that unannounced loss can outweigh any cleverness in the checking (Volume 8).
- **Photons barely interact.** Two photons pass through each other. Making them influence each other needs extra resources, and often works only some of the time (Volume 6).

These are reasons to change the *job* photons do, not a defect of photons themselves. Photons remain the best way to **move** quantum information. The question became: what if information is **held and processed** in something else, with light used to carry it between places?

## 17.2 What atoms offer, and what they cost

Atoms bring what photons lack:

| Atoms can... | Because... |
|---|---|
| Stay in one place | They can be held in traps made of laser light, called optical tweezers |
| Hold information in their internal states | Electrons can sit in different energy levels; the nucleus has its own spin |
| Be controlled precisely | Microwaves, lasers and magnetic fields address chosen transitions |
| Interact strongly when asked | An atom excited to a very high level, a **Rydberg state**, becomes huge and interacts with neighbours micrometres away |

The cost: **an excited atom does not stay excited.** A Rydberg-excited atom falls back to lower states. [[REPORTED]] Lifetimes are typically tens to hundreds of microseconds at room temperature, and somewhat longer in cryogenic setups (Appendix 9). Low-lying ground states can hold information much longer, but they don't interact strongly. Much of the rest of this edition is about that trade.

## 17.3 A real experiment, read carefully

In 2025 a team stored a single photon in a cloud of cold atoms and turned it into a three-level quantum state inside the cloud. [[REPORTED]] What the paper reports (Jiao et al., Physical Review Research 7, 033267; sections I to IV read in full):

| Item | Value |
|---|---|
| Atoms | Up to about 1,000 rubidium-87 atoms in an optical tweezer |
| Storage | One photon stored as a shared excitation in the Rydberg level 60S |
| Control | Microwaves at 18.51 GHz (60S ↔ 59P) and 18.23 GHz (59P ↔ 59S): a chain, with no direct link from the first level to the third |
| Readout | The three levels are converted back to light one after another, as time bins |
| Total time | Under 1.8 microseconds |
| Single-excitation quality | g⁽²⁾(0) = 0.45 ± 0.05: mostly, but not purely, one excitation |
| Measured populations | 47.1%, 38.6%, 14.2% (ideal 50%, 50%, 0%) |

::: watch
**What the experiment did, and did not do.** It stored a single photon, then *created* the three-level superposition inside the atoms using microwaves. It did **not** store an incoming photon that already carried a three-level encoding, let alone a four-level Tetragon. The distinction is easy to blur and important to keep.
:::

The paper is valuable to PhaseKeep for three reasons:
- **The idea transfers.** Its "levels connected by microwave links" is exactly the kind of state map PhaseKeep draws.
- **Physics sets the shape.** The links form a chain because of physics: microwaves connect S-type levels to P-type levels.
- **Unwanted interactions are real.** Extra excitations shifted the measured phases.

## 17.4 Storage, or a register?

There is a difference between a **memory**, where information waits while computing happens elsewhere, and a **register**, where information stays put and the computing happens *to* it.

The research proposal that grew from here treats atoms as the register itself. Information rests in long-lived ground states. An operation briefly lifts it into interacting Rydberg states, acts, and returns it. [[PROPOSED]] That rest–activate–act–return cycle has established precedents in neutral-atom quantum computing. For PhaseKeep it is still a proposal.

::: key
Edition 03 already uses the name **PK-M** for a specific proposal: a four-mode atomic-vapor memory. That frozen meaning is unchanged. The persistent register described here is a different idea, given its own working name in Volume 18.
:::

## 17.5 A "matter Tetragon"

Atoms can hold a Tetragon of their own. Take an atom whose outer electron and nucleus each have two spin states (spin ½ each, as in hydrogen). That gives four combinations, just like polarization × twist.

The two spins are linked by a small magnetic interaction between electron and nucleus, the hyperfine coupling. An external magnetic field competes with it, and that competition sets how the states behave [[DERIVED]]:

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

Two further consequences [[DERIVED]]:
- **The field chooses the natural two-spin operation.** At zero field the coupling naturally swaps the two spins. At strong field it naturally gives a conditional phase.
- **Clock states.** The two middle states make a pair whose energy difference does not change, to first order, when the field wobbles slightly near zero. Atomic clocks exploit exactly this.

That's the atomic version of Volume 16's principle. **The protected pair is again the one whose angular momenta cancel**: protected against field noise here, as the J = 0 light pair was protected against rotation.

## 17.6 Single atoms or a cloud?

Two quite different atomic registers are possible:

| | **Individual atoms** | **A cloud of atoms sharing one excitation** |
|---|---|---|
| Information lives in | Each atom's internal levels | One excitation spread over many atoms |
| Can hold a phase pattern spread across separate atoms (like light's twist) | No. A single atom does have electronic orbital angular momentum, but a pattern *spread over many atoms* needs many atoms | Yes: as a phase pattern across the cloud |
| Extra weakness | Fewer natural axes | The pattern scrambles as atoms move |

The research explored the cloud version first, storing twist as a phase pattern across the atoms, and hit a wall [[SIMULATED]]. With microwaves and two-photon laser pulses alone, the twist states cannot be fully controlled: the operations either ignore the twist or shift it out of the register. Volume 18 explains how a small **ring of individual atoms** gets around this.

## 17.7 Moving information between light and matter

Any design that uses both photons and atoms needs a way to hand information across without damaging it. PhaseKeep's name for that is the **light–matter interface (PK-LMI)**, a working term whose source definition is still being reconciled. The requirement, stated plainly [[PROPOSED]]:
- **What must survive the transfer:** amplitudes, relative phases, the relationships between axes (Volume 15), and any entanglement with outside systems.
- **Agree the mapping first:** a table saying which light state goes to which atomic state.
- **Report losses separately:** loss, leakage into unintended states, and loss of coherence.

## 17.8 Why decay will matter

A Rydberg-based operation must finish well within the excited lifetime of **every** atom that is excited during it. Volume 22 returns to this with numbers. The short version: in the models, excited-state decay outweighs every carefully tuned control error by a wide margin. Making operations faster, or finding longer-lived states, is the central physical question.

## Summary

- **Photons are best for moving information.** Storage, loss and weak interaction pushed the research toward matter for holding and processing it.
- **Atoms stay put, hold states and interact strongly** when Rydberg-excited. Excited atoms decay.
- **A real experiment** stored a photon and then *prepared* a three-level state with microwaves. It did not store an encoded one.
- **A two-spin atom is a "matter Tetragon"**, whose entanglement is tuned by a magnetic field. Its protected clock states echo Volume 16's principle.
- **Two register types:** individual atoms and atom clouds. The cloud route ran into a control limit.

## Try it

1. What is the concurrence of the middle states at b/A = 3? *Answer: 1/√10 ≈ 0.32.*
2. Why can't the microwave chain in the 2025 experiment link the first and third levels directly? *Answer: both are S-type levels; a single microwave photon connects S-type to P-type levels, so the path goes through the P level.*
3. Name one reason, other than decay, that photons are hard to use for computing. *Answer: they are hard to store, easily lost, or barely interact with each other.*
4. Is PK-M the persistent register described in 17.4? *Answer: no. PK-M is the frozen name for a four-mode atomic-vapor memory proposal.*
