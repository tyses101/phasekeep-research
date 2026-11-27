# Glossary

Every term in one place. Terms in **bold** are defined where they first matter; the volume number is given in brackets.

## Project terms

| Term | Meaning |
|---|---|
| **EA** (Encoding Axis, plural Axies) | A physical property of light chosen to carry a label, with distinguishable values. [3] |
| **CT** (Controlled Transformation) | A physical operation we can set and repeat that changes the encoded information. "Controlled" means adjustable, not "conditioned on another qubit"; conditional operations are one kind. [5] |
| **GEA** (Geometric Encoding Axies) | Reading the states of a register as the corners of a square, cube or hypercube. [4] |
| **Buddy System** | The proposed way to manage preparation, assistance, verification, preservation and continuation using helper (ancillary) photons. [7] |
| **Buddy Check** | A test that answers PASS, FAIL or UNKNOWN, based only on demonstrated evidence. [7] |
| **Tetragon** (PK-Q4) | The four-address register: H/V polarization × twist −1/+1. [3] |
| **PK-M** | The proposed four-mode atomic-vapor memory and its certification test. [8] |
| **PK-E** | The proposed prepared-instruction execution scheme. [10] |
| **Register** | An information-carrying system with a defined set of states. Binary, Structured and Adaptive forms are described. [10] |
| **Adaptive Register** | A register whose mapping or encoding could be chosen or reconfigured within supported capabilities. Proposed only. [10] |
| **Address** | One of the basis states of a register, for example 01 on the Tetragon. [3] |
| **Closure** | Whether an operation keeps the photon inside the chosen set of states. [5] |
| **Axis family names** | Qubit, Tetragon, Cubion, Tesseron, Penteron, Hexeron, Heptaron, Octeron, Ennearon, Decaron, Aetheron, Hyperion: registers of 1 to 12 binary axes. Labels only. [4] |
| **PQGS** (Photonic Quantum Geometric Superpositions) | A descriptive term for coherent photonic superpositions organized in a geometrically structured encoding space, especially non-separable ones spanning several EAs. Research terminology inside GEA, not a pillar. "Geometric" does not mean geometric phase. [4] |
| **State Space (SS) / State Space Environment (SSE)** | The mathematical space of all available quantum states; and the physical resources and control that make it accessible and useful. [10] |
| **Occupation / connectivity / correlation** | The three things an environment can change during a computation: which addresses carry amplitude, which can be coherently coupled, and how the encoded properties are related. [10] |
| **Available / active / operational geometry** | The addresses supported; the addresses taking part in the current state; the relationships that the available operations can manipulate. [10] |
| **Subspace** | The set of states that can be built from a chosen group of addresses; a line gives a two-dimensional subspace and a square a four-dimensional one. [4] |
| **Support** | The set of addresses that have non-zero amplitude. Not the same as the state, since phases and correlations are also needed. [10] |
| **Address geometry / state-space geometry / optical-mode geometry / execution geometry** | The four kinds of geometry: mathematical, mathematical, physical, physical. [4] |
| **Time** | The machine's clock. Not an EA in the current design. [3] |

## Light and quantum terms

| Term | Meaning |
|---|---|
| **Photon** | The smallest packet of light. [1] |
| **Polarization (H, V)** | The direction in which the light's electric field swings. [1] |
| **OAM (orbital angular momentum), twist ℓ** | A spiral structure of the wavefront; ℓ is a whole number. Phase factor exp(iℓφ). [1] |
| **Laguerre-Gaussian (LG) mode** | The common family of twisted beams. [1] |
| **Waveplate** | A crystal slice that changes polarization. [1] |
| **Q-plate** | A device that ties polarization to twist. Not closed on {−1, +1} as is. [5] |
| **Dove prism** | A prism that rotates an image; used for a twist-dependent phase. [5] |
| **Sorter** | A device that sends different twists to different places. [4] |
| **Beam splitter / PBS** | Splits light by amplitude, or by polarization. [5] |
| **Superposition** | A state that is a blend of several basis states. [2] |
| **Amplitude** | The complex number multiplying a basis state; its squared size is a probability. [2] |
| **Relative phase** | The angle between amplitudes; observable only through interference. [2] |
| **No-cloning theorem** | An unknown quantum state cannot be copied perfectly. [2] |
| **Fidelity** | A score from 0 to 1 for how close a state or process is to a target. Always say which definition. [2] |
| **Process fidelity** | Fidelity of an operation rather than of one state. [6] |
| **Coherent state** | The quantum state of ordinary laser light; n̄ is its mean photon number. [8] |
| **Thermal noise (v)** | Added unwanted light per mode in the memory model. [8] |
| **Efficiency (η)** | Overall fraction of light that comes back through the chain. [8] |
| **Isolation** | Selecting a subspace by filtering or projecting. Not reversible; the rest of the state is lost. [4] |
| **High-dimensional entanglement** | Entanglement between systems with more than two levels each. The project's adopted scientific foundation; the first target is two entangled Tetragons (16 joint states, up to 2 ebits). [6] |
| **Ebit** | Unit of entanglement: one maximally entangled pair of two-level systems. A pure state with r equal Schmidt weights holds log2 r ebits. [6] |
| **Hyperentanglement** | Entanglement in several properties of the same two photons at once, for example polarization and twist. [6] |
| **Independent, coupled, entangling operation** | Three kinds of operation on a register with two axes: one separate operation per axis; one that needs coordinated control of both axes but never entangles a product input (a SWAP of the axes); one that can turn a product input into an entangled state (a controlled phase). [6] |
| **Correlation pattern** | Which address of photon B goes with which address of photon A in an entangled pair, such as corresponding or cyclic. [6] |
| **Qudit** | A quantum system with d levels instead of 2. The Tetragon is a four-level qudit. [13] |
| **Fusion** | An entangling measurement used in fusion-based quantum computation. [13] |
| **Hilbert space** | The set of all possible states of a system. [2] |
| **Separable / non-separable** | A state is separable if it can be written as one polarization state times one twist state. Otherwise it is non-separable. [4] |
| **Schmidt weights, Schmidt rank** | The weights describing how strongly two parts of a state are tied together; rank is how many are non-zero. Separable states have rank 1. [4] |
| **Vector vortex beam** | A beam whose polarization varies around the beam axis. Non-separable polarization-twist states give such beams. [4] |
| **Geometric phase** | The Berry or Pancharatnam-Berry phase. A different idea from "geometric" in GEA. [4] |
| **Tomography** | Reconstructing a state or process from many measurements. [11] |

## Gates and heralding

| Term | Meaning |
|---|---|
| **SUM** | Controlled-SUM: the pair (j, k) becomes (j, (j+k) mod 4). [6] |
| **CP, CPF** | Controlled-phase operation, and the controlled-phase-flip that flips the sign of one state. [6] |
| **Kickback** | A target prepared in a special state passes a phase back to the control. [6] |
| **Operator Schmidt rank** | How many product terms an operation needs when written as a sum of one-operation-per-system terms. Rank 1 means it factors. A higher rank means it does not factor, which is a mathematical statement and not a measure of physical interaction strength or of entangling power. In Volume 6 it gives a floor on how many interaction gates are needed under a stated gate model; the floor is not always tight and does not predict optical component count. [6] |
| **Ancillary (auxiliary) photon** | A helper photon that is measured instead of kept. [7] |
| **Herald** | A detector signal meant to announce success. [7] |
| **Post-selection** | Keeping only the runs that look right. [6] |
| **Occupancy-valid** | Exactly one photon in each computational output register. Not state fidelity. [7] |
| **False herald** | The herald fires but the output is not occupancy-valid. [7] |
| **Herald probability / reliability** | How often it fires; how often it is right when it fires. [7] |
| **Output fidelity, availability, continuation yield** | The other three Buddy measures. [7] |
| **PNR detector** | Photon-number-resolving detector. [7] |
| **Monte Carlo** | Estimating by many random trials. [8] |

## Research terms

| Term | Meaning |
|---|---|
| **DERIVED, REPORTED, SIMULATED, ASSUMED, PROPOSED, MEASURED, UNVERIFIED, BLOCKED** | The evidence tags. See Start Here. |
| **A01 to A06** | The audit items. [9] |
| **BV-01 to BV-06** | Verification steps for the heralded gate. [9] |
| **B01 to B07** | The blocked register. [9] |
| **SIM-06** | The chain simulation. [7] |
| **R25, R29, R30** | Numbered revisions of the PhaseKeep research website. [9] |

## Earlier project terms

These come from earlier PhaseKeep material and review discussions, and were recovered for this edition. They are **not part of the adopted EA/CT vocabulary**, and the definitions below should be confirmed by the project owner [[PROPOSED]].

| Term | Meaning |
|---|---|
| **Quantum threading** | The project's earlier name for coordinating preparation, routing, storage and execution. |
| **DDQT** (Demand-Driven Quantum Threading) | Confirmed project term. One operating mode of quantum threading, with scheduling that can be classical. *Flow-based:* prepare, select successful resources, synchronize and execute without a persistent instruction bank. *Inventory-based:* prepare ahead of demand, store, request and retrieve. |
| **PKC** (PhaseKeep Conductor) | Confirmed project term. The classical supervisory system that handles scheduling, synchronization, resource management and optimization. It was proposed as a rename to avoid "PIC", which in photonics means photonic integrated circuit. |
| **PK-BS** (PhaseKeep Buddy System) | The project identifier for the Buddy System. [7] |
| **AIS** (Autonomous Instruction Streaming) | Confirmed project term. Three levels. **AIS-1:** classical scheduling of concurrent photon streams (implementable). **AIS-2:** tagged, state-dependent optical routing (requires engineering design). **AIS-3:** coherent quantum instruction selection (an undefined research hypothesis that must not appear as a working component). |

## Retired terms

::: watch
**PTEA** and **TV** were earlier working names. They have been replaced by **EA** and **CT**; do not use them.

Nothing in this library depends on the earlier project terms above.
:::
