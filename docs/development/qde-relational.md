# QDE and relational computing research framework

[PROPOSED] **PROVISIONAL, 2026-11-27.** This is a documentation proposal under GEA, alongside IQA, not a new scientific result, implementation, simulation or release. [Dated checkpoint](checkpoints/qde-2026-11-27.md) records its scope. Existing terminology and identifiers, including Buddy System, remain intact.

[PROPOSED] New claims on this page use ESTABLISHED (standard theory or attributed literature), DERIVED (explicit arithmetic within a stated model), SIMULATED (computed evidence; none added here), PROPOSED or UNVERIFIED. These labels apply to this extension without relabelling historical records. Citation verification means the linked metadata and stated abstract scope were checked; it does not mean independent reproduction.

## QDE under GEA

[PROPOSED] **Quantum Dimensional Environment (QDE)** organizes the joint state space of participating systems: encoding dimensions, subsystem partitions, coherence, correlations, entanglement structure, available interactions and evolution. It is a framework under Geometric Encoding Axies (GEA), not a physical environmental bath or a newly discovered phenomenon. State Space (SS) remains the mathematical space; State Space Environment (SSE) remains its physical realization. The relationship to the earlier provisional Integrated Entangled Environment (IEE) needs reconciliation; QDE does not silently replace it.

[PROPOSED] The scope includes intra-axis state configurations, intra-photon, inter-photon, cross-axis and multipartite/collective relations, higher-order correlations and geometric configuration flexibility. Relational convergence, separation, migration and reconstruction are descriptive questions about explicit state maps, not additional forces or independent control knobs. Specify the input state, partition, reference basis, channel and output before using these descriptions.

[ESTABLISHED] Superposition within one axis is not entanglement without a specified tensor-product partition. Multipartite entanglement concerns several subsystems; hyperentanglement concerns simultaneous entanglement in multiple degrees of freedom; hybrid entanglement needs an explicit account of the different degrees of freedom or systems involved. These standard terms provide comparisons, not synonyms for every PhaseKeep label (see literature below).

## Convergent Quantum Relationships

[PROPOSED] **Convergent Quantum Relationships** is a provisional organizing classification, broader than the existing provisional **Convergent Entanglement** term for noncorresponding axes. It neither renames that term nor changes historical NEE entries. Distinguish subsystem properties from properties requiring a reference, multiple states, a partition or a measurement scenario; calling all of them intrinsic would obscure this distinction.

| Property | Context and distinction |
|---|---|
| Relative phase | [ESTABLISHED] A relation between amplitudes in a specified basis; global phase is not observable. |
| Coherence and superposition | [ESTABLISHED] Basis-dependent state descriptions, possible in a single subsystem; not sufficient evidence of entanglement. |
| Entanglement | [ESTABLISHED] Nonseparability across an explicitly specified partition of a joint state. |
| Orthogonality and nonorthogonality | [ESTABLISHED] Relations between states or subspaces, distinct from correlations within a state. |
| Indistinguishability | [ESTABLISHED] Requires specifying accessible modes and measurements; hidden distinguishing degrees of freedom affect interference. |
| Exchange symmetry | [ESTABLISHED] Identical-particle permutation symmetry, not the project's SEE corresponding-axis classification. Mode and subsystem labels must be stated. |
| Contextuality | [ESTABLISHED] Concerns statistics in a specified compatible-measurement scenario, not a synonym for entanglement. Kochen–Specker contextuality needs dimension at least 3, so a single binary axis cannot show it; a two-axis Tetragon (dimension 4) already admits a simplified Kochen–Specker argument ([Mermin](https://doi.org/10.1103/PhysRevLett.65.3373)). [PROPOSED] One Tetragon is a minimal contextuality test case. |
| Quantum discord | [ESTABLISHED] A partition- and measurement-side-dependent correlation measure; may be nonzero for separable states ([Ollivier and Zurek](https://doi.org/10.1103/PhysRevLett.88.017901)). [DERIVED] The classically correlated mixture ½(\|00⟩⟨00\| + \|11⟩⟨11\|) has zero discord, so it serves as a zero-discord control; a discord test needs a separable state that is not classical-classical. |
| Subsystem purity or occupation | [ESTABLISHED] Can be evaluated from a reduced state; occupation needs a basis, and the reduced state alone does not determine all joint correlations. |

[PROPOSED] Research question: can useful information be encoded and manipulated in relationships unavailable from individual reduced states, with an operational advantage under stated controls and costs? Standard quantum information already uses joint-state encodings. The question here is which specific encoding, task, measurement and resource comparison is useful, not whether correlations are a new information carrier. [UNVERIFIED] No PhaseKeep-specific advantage or novelty is established.

## QIJ roles and instruction encoding

[PROPOSED] **Quantum Interaction Junction (QIJ)** is a provisional role description for a specified interaction process, not proof that a device implements it. The role identifiers below extend the existing term-based development register; they do not renumber historical identifiers.

| Identifier | Proposed role |
|---|---|
| QIJ-I | [PROPOSED] Instruction selection or application. |
| QIJ-D | [PROPOSED] Data transformation. |
| QIJ-V | [PROPOSED] Verification with a specified information-disturbance budget. |
| QIJ-R | [PROPOSED] Resource preparation or recreation of a known state. |
| QIJ-T | [PROPOSED] Coherent transfer, including preservation of correlations with an external reference. |

[PROPOSED] Candidate mechanisms include interference with measurement/feed-forward, ancilla-assisted operations, nonlinear interactions and light-matter coupling. Specify a channel or instrument for each candidate. [ESTABLISHED] Photon trajectories crossing alone do not implement a logic gate; optical interference alone is not a guarantee of a deterministic entangling operation.

### Established optical constraints on QIJ candidates (added 2026-11-27)

| Constraint | Consequence for QIJ |
|---|---|
| [ESTABLISHED] Linear optics with single-photon sources and detectors supports efficient quantum computation only with detector feedback (feed-forward); without feedback only non-deterministic computation is possible ([Knill, Laflamme and Milburn](https://arxiv.org/abs/quant-ph/0006088)). | Inter-photon QIJ-I and QIJ-D candidates built from linear optics are probabilistic or need ancillas, measurement and feed-forward. This is the baseline any QIJ proposal must be compared against. |
| [ESTABLISHED] With linear optical elements and vacuum auxiliary modes, the four Bell states cannot be unambiguously discriminated with probability above 50% ([Calsamiglia and Lütkenhaus](https://arxiv.org/abs/quant-ph/0007058)). | A teleportation-based QIJ-T built this way has at most 50% success per attempt unless further resources are added. |
| [ESTABLISHED] Complete Bell-state analysis with linear optics is possible when the particles are entangled in more than one degree of freedom ([Kwiat and Weinfurter, Embedded Bell-state analysis](https://doi.org/10.1103/PhysRevA.58.R2623)). | This published case has one degree of freedom assisting an operation on another. It is the closest established precedent for cross-axis assistance and should anchor that question, not PhaseKeep novelty. |
| [ESTABLISHED] Spin angular momentum of light can be converted to orbital angular momentum in inhomogeneous anisotropic media ([Marrucci, Manzo and Paparo](https://doi.org/10.1103/PhysRevLett.96.163905)); spin-to-OAM information transfer has been demonstrated ([Nagali et al.](https://arxiv.org/abs/0810.2417)). | Operations between two axes of one photon need no photon-photon interaction. [PROPOSED] Internal instruction encoding (for example polarization selecting an OAM flip) is therefore the cheapest configuration to model first. Device efficiency and loss still apply. |
| [UNVERIFIED] Mirror reflection, including beam-splitter reflection, inverts the sign of OAM and adds polarization-dependent phases (standard reflection parity; primary citation pending). | Two-photon interference models in the Tetragon basis must track the reflected label (twist −1/+1 exchanged) explicitly, or distinguishability will be misassigned. |

[PROPOSED] Report interaction probability, heralding probability, output survival, target fidelity and coherent-continuation probability separately. State each denominator and joint event. A herald can be false or accompany a consumed output; multiplying separately quoted probabilities requires justified conditional dependencies.

[PROPOSED] Compare internal instruction encoding across axes in one photon, external encoding in separate resources, and hybrid classical-plus-quantum controls. Ask whether prepared geometry selects a specified transformation. Compare the complete process, including preparation, routing, feed-forward, measurement and disposal, against classical control, programmable quantum processors and measurement-based quantum computation (MBQC). No speed, resource or universality advantage is assumed. [ESTABLISHED] Exact deterministic universal programming with a finite-dimensional quantum program register is constrained by the no-programming result; restricted gate sets and probabilistic or approximate schemes require separate specifications ([Nielsen and Chuang](https://arxiv.org/abs/quant-ph/9703032)).

## IQA and ASV

[PROPOSED] **Alternating Stacked Verification (ASV)** is a provisional research pattern within **Integrated Quantum Assurance (IQA)**: rotate computation and verification roles, permit multiple ancillas and accumulate explicitly modelled evidence. There is no privileged permanent main photon in the proposed role assignment. This is not a claim that arbitrary physical resources are interchangeable or that repeated checks are nondestructive.

[PROPOSED] Retain the Buddy System name and existing functions. Investigate known-state resource recreation, coherent transfer or recovery of unknown logical information, and continuation after a demonstrably recoverable failure. State which subsystem holds the information at each step, the surviving reference entanglement, correlated faults, evidence dependence and false-accept/false-reject rates. Repeated evidence must not be treated as independent without justification.

[ESTABLISHED] Recreating a known preparation is not cloning an arbitrary unknown state or restoring an unknown state whose information has been irretrievably destroyed. Quantum error correction and coherent transfer require information to survive in a suitable encoding or other system; verification cannot evade no-cloning. [UNVERIFIED] No ASV circuit, fault tolerance threshold or practical continuation benefit has been established here.

## Initial two-Tetragon model

[PROPOSED] Restrict each photon to binary polarization and a selected binary OAM subspace, with distinguishable photon/register modes A and B. Fix tensor order (A-polarization, A-OAM, B-polarization, B-OAM) and the computational basis. Leakage, vacuum and other optical modes are outside this initial ideal model and must be added for physical benchmarking.

| Quantity | Within the specified model |
|---|---|
| Photons and encoded qubits | [DERIVED] 2 photons times 2 binary axes = 4 qubits. |
| Hilbert-space dimension | [DERIVED] 2^4 = 16. |
| Pair subsets | [DERIVED] C(4,2) = 6. |
| Triple subsets | [DERIVED] C(4,3) = 4. |
| Pure-state real parameters | [DERIVED] 16 complex amplitudes give 32 real coordinates, minus normalization and global phase = 30. |

[DERIVED] These counts enumerate subsystem subsets and pure-state degrees of freedom, not six independent pair entanglements plus four independent triple entanglements. Reduced states share one joint density operator and obey compatibility constraints. The count alone establishes no independently controllable relations, accessible classical bits or hardware resources.

[PROPOSED] Compare fully independent products, internally entangled photons, entanglement between corresponding axes on different photons, cross-axis entanglement and genuinely collective states. For each explicit transformation characterize which named relations it creates, preserves, redistributes or destroys, using the same basis, partitions and metrics before and after. Include GHZ-type controls so that pairwise tests cannot masquerade as complete state characterization.

[PROPOSED] Next mathematical step, not executed: apply explicitly ordered CNOT-type cross-axis gates (for example A-polarization controlling B-OAM) on the 16-dimensional state. Compute all six two-qubit reductions and their concurrence or negativity; for each of four three-qubit reductions compute named bipartition negativities and a separately justified genuine-tripartite witness. A pure-state three-tangle formula must not be applied directly to mixed reductions. Compare with identity, local basis changes, product states and GHZ controls, and record global/reference fidelity. No optical implementation is implied by the ideal matrix.

## Realism and benchmark plan

[PROPOSED] Add loss, phase drift, timing/frequency/spatial-mode mismatch, polarization drift, detector inefficiency, imperfect operations, environmental coupling, probabilistic failures and ancilla cost. Model the physical bath separately from QDE; include vacuum/leakage sectors and failed events instead of discarding them silently.

[PROPOSED] Report target fidelity, purity, basis-specified coherence, partition-specified entanglement, correlation structure, interference visibility, verification accuracy, resource use and continuation. Specify gate, photon, ancilla, detector, time and feed-forward costs; do not infer throughput without timing data. Report both conditioned-on-success and unconditional per-attempt outcomes, with acceptance probability and definitions for loss. Compare equivalent tasks against direct operations/classical control, standard ancilla verification, programmable processors and MBQC where applicable, under matched assumptions. An oracle or free preparation is an assumption to expose, not an implemented advantage.

## Architecture mapping

[PROPOSED] The environment-first question is whether computation can be organized as controlled evolution of the participating joint system, without presupposing a CPU/memory/OS split. Here environment means QDE, not the bath. This is a research viewpoint, not a replacement of the frozen architecture.

| Existing term | Proposed relationship, preserving its definition |
|---|---|
| GEA | [PROPOSED] Parent framework for QDE's encoding geometry. |
| HDOC | [PROPOSED] Orthogonal configuration families within a named QDE, with basis, partition and allowed transformations fixed. |
| CT | [PROPOSED] Candidate physical maps; controlled still means settable/repeatable, not necessarily a controlled-qubit gate. |
| IQA / Buddy System | [PROPOSED] Assurance objectives and verification/assistance functions; ASV is a candidate pattern, not a rename. |
| PK-M | [PROPOSED] Compare continuity needs with the existing proposed four-mode atomic-vapor memory and certification test, without assuming availability. |
| PK-E | [PROPOSED] Compare prepared-instruction execution with QIJ-I and internal/external/hybrid encoding. |
| AIS | [PROPOSED] Preserve AIS-1 classical scheduling, AIS-2 routing engineering and AIS-3 coherent selection as an undefined hypothesis; no promotion of AIS-3 to a working component. |
| DDQT | [PROPOSED] Investigate flow/inventory resource scheduling; no claim of eliminating data-touching probabilistic operations. |
| PKC | [PROPOSED] Preserve classical supervision of timing and resources. An external clock is not automatically a new Encoding Axis. |

[PROPOSED] A geometry-native ISA or OS remains provisional and should follow demonstrated operations, failure semantics and resources. Field boundaries are not physical boundaries, but connections need explicit models and evidence: **the architecture should follow the discoveries.** Curiosity, intellectual humility, scientific rigor and willingness to be proven wrong remain the guiding philosophy.

## Literature and verification boundary

[ESTABLISHED] The following sources exist at the linked primary-source pages. Metadata and the described topic were verified on 2026-11-27 from source pages or indexed primary-source abstracts. This is a targeted starting bibliography, not a systematic review, full-text technical audit or independent reproduction. Published experiments belong to their authors; none validates QDE, QIJ or ASV.

| Category | Source and verification | Scope |
|---|---|---|
| High-dimensional photonic information | [ESTABLISHED] Verified: [Erhard, Krenn and Zeilinger, Advances in High Dimensional Quantum Entanglement](https://arxiv.org/abs/1911.10006); [Flamini, Spagnolo and Sciarrino, Photonic quantum information processing: a review](https://arxiv.org/abs/1803.02790). | Reviews; context for encodings and photonic processing, not a PhaseKeep implementation. |
| Hyperentanglement | [ESTABLISHED] Verified: [Barreiro et al., Generation of Hyperentangled Photons Pairs](https://arxiv.org/abs/quant-ph/0507128). | Published experiment with multiple degrees of freedom; not all correlations are hyperentanglement. |
| Hybrid and intra-photon entanglement | [ESTABLISHED] Verified: [Spin-orbit hybrid entanglement of photons and quantum contextuality](https://arxiv.org/abs/1103.3962). | Reported single-photon and photon-pair spin-orbit states. [UNVERIFIED] Publisher lists an erratum; its implications require full-text checking before relying on detailed claims. |
| Transfer and swapping | [ESTABLISHED] Verified: [Pan et al., Experimental Entanglement Swapping](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.80.3891). | Published Bell-measurement-based experiment, not generic deterministic transfer. |
| Coupling between degrees of freedom | [ESTABLISHED] Verified: [Nagali et al., Quantum information transfer from spin to orbital angular momentum of photons](https://arxiv.org/abs/0810.2417). | Published q-plate spin/OAM transfer experiment; platform constraints still need review. |
| Multipartite correlations and graph states | [ESTABLISHED] Verified: [Hein, Eisert and Briegel, Multi-party entanglement in graph states](https://arxiv.org/abs/quant-ph/0307130). | Theoretical graph-state measures and transformations; graph edges are not a complete generic pairwise-entanglement description. |
| Programmable processors | [ESTABLISHED] Verified: [Nielsen and Chuang, Programmable quantum gate arrays](https://arxiv.org/abs/quant-ph/9703032). | Theory and programming constraints; no assumed prepared-geometry advantage. |
| Multiphoton interference | [ESTABLISHED] Verified: [Pan et al., Multiphoton entanglement and interferometry](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.84.777). | Review of theory and experiments. |
| MBQC | [ESTABLISHED] Verified: [Raussendorf and Briegel, A One-Way Quantum Computer](https://doi.org/10.1103/PhysRevLett.86.5188). | Theoretical comparison architecture, not a claim that QDE implements MBQC. |
| QEC and ancilla verification | [ESTABLISHED] Verified: [Knill and Laflamme, A Theory of Quantum Error-Correcting Codes](https://arxiv.org/abs/quant-ph/9604034). | Recovery conditions and encoded information. [UNVERIFIED] ASV-specific ancilla circuits, correlated-fault analysis and comparison with fault-tolerant verification protocols remain to check. |

[UNVERIFIED] Naming-conflict searches, the QDE/IEE boundary, concrete QIJ instruments, accessible gate sets, ASV correctness, platform costs and any advantage or novelty remain open. No additional simulation, scientific regression, release or DOI is asserted by this documentation checkpoint.
